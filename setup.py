#!/usr/bin/env python
import os
import re
from subprocess import call
from setuptools import setup, find_packages, Command
from setuptools.command.install import install
from os import path as op
from glob import glob

__version__ = "1.2"

PACKAGES = find_packages(exclude=['tests'])
NAME = PACKAGES[0]
SCRIPTS = ['manage.py']
DATA_FILES = [('', ['Makefile', '.gunicorn.py'])]

patterns = {
    'version': re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]'),
    'doc': re.compile(r'__doc__ = [\'"]([^\'"]*)[\'"]')
}


def extract(pattern, fname):
    result = ''
    reg = re.compile(patterns[pattern])
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


def pip(*args):
    rc = call(f"pip {' '.join(args)}", shell=True)
    if rc:
        return exit(rc)
    return rc


class Dependencies(Command):
    description = 'install required dependencies'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        return pip('install -U pip')


class Requirements(Command):
    description = 'install required packages'
    user_options = [
        ('enviornment=', 'e', 'setup enviorment'),
        ('req=', 'r', 'file with requirements')
    ]

    def initialize_options(self):
        self.enviornment = None
        self.req = None

    def finalize_options(self):
        if self.enviornment is None:
            self.enviornment = os.environ.get('ENVIORNMENT', 'production')
        if self.req is None:
            self.req = 'requirements.txt'
        if not op.exists(self.req):
            raise Exception("Can't find requirements file: {}".format(self.req))

    def run(self):
        self.requirements_production()
        if self.enviornment == 'testing':
            self.requirements_test()
        elif self.enviornment == 'develop':
            self.requirements_test()
            self.requirements_develop()

    def requirements_production(self):
        return pip('install -r', self.req)

    def requirements_test(self):
        return pip('install pytest pyhamcrest pytest-cov flake8')

    def requirements_develop(self):
        return pip('install ipython ptvsd==3.0.0')


class Submodules(Command):
    description = 'install submodules'
    user_options = [
        ('folder=', 'f', 'submodule folder location'),
        ('upgrade', 'u', 'submodule folder location')
    ]
    boolean_options = ['upgrade']

    def initialize_options(self):
        self.folder = None
        self.upgrade = None

    def finalize_options(self):
        if self.folder is None:
            self.folder = '__submodules__'
        self.upgrade = self.upgrade is not None

    def run(self):
        if not op.isdir(self.folder):
            return

        return pip('install',
                   '-U' if self.upgrade else '',
                   *[f for f in glob(op.join(self.folder, '*')) if op.isdir(f)])


class Install(install):
    def run(self):
        self.run_command('dependencies')
        self.run_command('requirements')
        self.run_command('submodules')
        install.run(self)


setup(
    version=extract('version', "{}/__init__.py".format(NAME)),
    description=extract('doc', "{}/__init__.py".format(NAME)),
    long_description=get_readme('README.md'),
    install_requires=open('requirements.txt').read(),
    cmdclass={
        'install': Install,
        'dependencies': Dependencies,
        'requirements': Requirements,
        'submodules': Submodules,
    },
    packages=PACKAGES,
    scripts=SCRIPTS,
    data_files=DATA_FILES,
    include_package_data=True
)
