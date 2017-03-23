# elk-export

A CLI tool for exporting data from Logstash into a file.

## Getting started

From source:
```sh
 pip install git+https://github.com/cogniteev/elk-export.git
```

If your elasticsearch is running on `localhost:9200` then simply type this command to export all events:
```sh
elk_export -o /tmp/elk_export.log
```

A more complex example:
```sh
elk_export --date-range "[2017-01-17 TO 2017-01-18}" --tags nginx -z -o /tmp/elk_export.log.gz
```

## Getting Started with docker

`elk-export` can be used from docker directly. Since it will run in a container, we have to specify how to get our elasticsearch and mount a volume to have access to the exported file.

```sh
docker run --rm -v /tmp:/tmp cogniteev/elk-export -o /tmp/logstash.log --es-host http://$(hostname -f):9200
```

## Usage

```
usage: elk-export [-h] [--date-range DATE_RANGE] [--es-host ES_HOST]
                  [--index-prefixes INDEX [INDEX ...]]
                  [--tags TAGS [TAGS ...]] [-z] -o FILE

title:           A CLI tool for exporting data from Logstash into a file.
usage:           elk_export -o /tmp/elk_export.log
                 elk_export --date-range "[2017-01-17 TO 2017-01-18}" -o /tmp/elk_export.log
                 elk_export --date-range "[2017-01-17 TO 2017-01-18}" --tags nginx -o /tmp/elk_export.log
                 elk_export --date-range "[2017-01-17 TO 2017-01-18}" --tags nginx -z -o /tmp/elk_export.log.gz

optional arguments:
  -h, --help            show this help message and exit
  --date-range DATE_RANGE
                        Date range to export in query string format. Example:
                        [2012-01-01 TO 2012-12-31]
  --es-host ES_HOST     Elasticsearch host URL. Default is
                        http://localhost:9200.
  --index-prefixes INDEX [INDEX ...]
                        Index name prefix(es). Default is ['logstash-*'].
  --tags TAGS [TAGS ...]
                        Query tags.
  -z, --gzip            Compress output file with gzip
  -o FILE, --output_file FILE
                        output file location.
```

## Related

In case you are using ELK to store web server logs, you could also be interested in [oncrawl-elk](https://github.com/cogniteev/oncrawl-elk).