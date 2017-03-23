#!/usr/bin/python

from distutils.core import setup

from setuptools import find_packages
import pip.req as pipreq

module_name = 'elk-export'
description = "A CLI tool for exporting data from Logstash"
root_url = 'https://github.com/cogniteev/' + module_name
__version__ = '0.0.1'

setup(
    name='elk-export',
    version=__version__,
    packages=find_packages(exclude=['*.tests']),
    url=root_url,
    license='Apache license version 2.0',
    keywords='elk logstash oncrawl',
    author='Philippe David',
    author_email='philippe@cogniteev.com',
    install_reqs=pipreq.parse_requirements('requirements.txt', session='hack'),
    entry_points={
        'console_scripts': [
            'elk-export = elk-export:main'
        ]
    },
)
