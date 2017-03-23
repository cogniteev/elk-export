#!/usr/bin/python

from distutils.core import setup

from setuptools import find_packages

module_name = 'elk_export'
description = "A CLI tool for exporting data from Logstash"
root_url = 'https://github.com/cogniteev/' + module_name
__version__ = '0.0.1'

with open('requirements.txt') as file_requirements:
    requirements = file_requirements.read().splitlines()

setup(
    name='elk-export',
    version=__version__,
    py_modules=['elk_export'],
    url=root_url,
    license='Apache license version 2.0',
    keywords='elk logstash oncrawl',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
    ],
    author='Cogniteev',
    author_email='tech@cogniteev.com',
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'elk-export=elk_export:main'
        ]
    },
)
