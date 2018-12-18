#!/usr/bin/env python
import re
from os import path as op
from setuptools import setup, find_packages

PATTERNS = {
    'version': re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]'),
    'doc': re.compile(r'__doc__ = [\'"]([^\'"]*)[\'"]')
}
packages = find_packages(exclude=['tests'])


def extract(pattern, fname):
    result = ''
    reg = re.compile(PATTERNS[pattern])
    with open(fname, 'r') as fp:
        for line in fp:
            m = reg.match(line)
            if m:
                result = m.group(1)
                break
    if not result:
        raise RuntimeError('Cannot find matched information for pattern {}'.format(pattern))
    return result


def get_readme(fname):
    result = ''
    if op.exists(fname):
        with open(fname, encoding='utf-8') as f:
            result = f.read()
    return result


setup(
    name=packages[0],
    version=extract('version', "{}/__init__.py".format(packages[0])),
    description=extract('doc', "{}/__init__.py".format(packages[0])),
    long_description=get_readme('README.md'),
    packages=packages,
    install_requires=open('requirements.txt').read() if op.exists('requirements.txt') else ''
)
