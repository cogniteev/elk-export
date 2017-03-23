#!/usr/bin/env python
"""
title:           A CLI tool for exporting data from Logstash into a file.
usage:           elk-export -o /tmp/elk-export.log
                 elk-export --date-range "[2017-01-17 TO 2017-01-18}" -o /tmp/elk-export.log
                 elk-export --date-range "[2017-01-17 TO 2017-01-18}" --tags nginx -o /tmp/elk-export.log
                 elk-export --date-range "[2017-01-17 TO 2017-01-18}" --tags nginx -z -o /tmp/elk-export.log.gz
"""
import gzip
import sys
import argparse
from functools import partial

import elasticsearch

FLUSH_BUFFER = 1000  # Chunk of docs to flush in temp file
CONNECTION_TIMEOUT = 120
TIMES_TO_TRY = 3
RETRY_DELAY = 60
EXPORT_FIELD = 'message'
SCROLL_TIME = '10m'
SCROLL_SIZE = 150


class EsScanner:
    def __init__(self, es_host):
        self.es_client = elasticsearch.Elasticsearch(es_host, timeout=CONNECTION_TIMEOUT)

    def start_scan(self, es_search_args):
        es_args = dict(search_type='scan', scroll=SCROLL_TIME, size=SCROLL_SIZE)
        es_args.update(es_search_args)
        scroll_init = self.es_client.search(**es_args)

        scroll_id = scroll_init.get('_scroll_id', None)

        if scroll_id is None:
            raise Exception('unable to retrieve data')

        def scan(scroll_id):
            have_hits = True

            while have_hits:
                scroll_response = self.es_client.scroll(
                    scroll_id=scroll_id,
                    scroll=SCROLL_TIME
                )

                hits = scroll_response['hits']['hits']

                have_hits = len(hits) > 0

                for h in hits:
                    yield h

                scroll_id = scroll_response['_scroll_id']

        return scroll_init['hits']['total'], partial(scan, scroll_id)


class SingleFieldWriter:
    def __init__(self, output_file, export_field, gzip_file=False):
        if gzip_file:
            self.output_file = gzip.open(output_file, 'wb')
        else:
            self.output_file = open(output_file, 'w')
        self.export_field = export_field

    def write(self, hit):
        self.output_file.write(hit['_source'].get(self.export_field))
        self.output_file.write('\n')

    def close(self):
        self.output_file.close()


class LogstashExport:

    def __init__(self, es_host):
        self.es_scanner = EsScanner(es_host=es_host)

    def export(self, es_index, date_range, output_file, es_query_tags=None, gzip_file=False):

        es_query_args = dict(index=es_index)
        es_q_filters = []
        if date_range:
            es_q_filters.append('@timestamp:{}'.format(date_range))
        if es_query_tags is not None:
            es_q_filters.append(u'tags:"{}"'.format(es_query_tags))
        if es_q_filters:
            es_query_args['q'] = u' AND '.join(es_q_filters)

        writer = SingleFieldWriter(output_file, EXPORT_FIELD, gzip_file=gzip_file)

        nb_hits, scanner = self.es_scanner.start_scan(es_query_args)

        print u'Starting export of {} hits...'.format(nb_hits)
        count = 0
        for hit in scanner():
            writer.write(hit)
            count += 1

        writer.close()

        print u'Successfully exported {} hits'.format(count)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--date-range', type=str, help='Date range to export in query string format. Example: [2012-01-01 TO 2012-12-31]')
    p.add_argument('--es-host', default='http://localhost:9200', type=str, help='Elasticsearch host URL. Default is %(default)s.')
    p.add_argument('--index-prefixes', dest='index_prefixes', default=['logstash-*'], type=str, nargs='+', metavar='INDEX', help='Index name prefix(es). Default is %(default)s.')
    p.add_argument('--tags', dest='tags', type=str, nargs='+', help='Query tags.')
    p.add_argument('-z', '--gzip', action='store_true', help='Compress output file with gzip')
    p.add_argument('-o', '--output_file', dest='output_file', type=str, required=True, metavar='FILE', help='CSV file location.')

    if len(sys.argv) == 1:
        p.print_help()
        exit()

    opts = p.parse_args()
    es = LogstashExport(opts.es_host)

    es.export(es_index=opts.index_prefixes,
              date_range=opts.date_range,
              output_file=opts.output_file,
              es_query_tags=opts.tags,
              gzip_file=opts.gzip)

if __name__ == '__main__':
    main()
