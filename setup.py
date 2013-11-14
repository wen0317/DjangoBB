#!/usr/bin/env python
from setuptools import setup, find_packages
from setuptools.command.install_lib import install_lib as _install_lib
from distutils.command.build import build as _build
from distutils.cmd import Command
from djangobb_forum import get_version


class compile_translations(Command):
    description = 'compile message catalogs to MO files via django compilemessages'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import os
        import sys
        from django.core.management.commands.compilemessages import \
            compile_messages
        curdir = os.getcwd()
        os.chdir(os.path.realpath('djangobb_forum'))
        compile_messages(stderr=sys.stderr)
        os.chdir(curdir)


class build(_build):
    sub_commands = [('compile_translations', None)] + _build.sub_commands


class install_lib(_install_lib):
    def run(self):
        self.run_command('compile_translations')
        _install_lib.run(self)

setup(name='djangobb_forum',
    version=get_version(),
    description='DjangoBB is a quick and simple forum which uses the Django Framework.',
    license='BSD',
    url='http://djangobb.org/',
    author='Alexey Afinogenov, Maranchuk Sergey',
    author_email='Maranchuk Sergey <slav0nic0@gmail.com>',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
            'django>=1.5.1',
            'pil>=1.1.7',
            'django-haystack==2.0',
            'django-pagination',
            'south',
            'postmarkup',
            'setuptools'
            ],
    keywords='django forum bb',
    test_suite='runtests.runtests',
    cmdclass={'build': build, 'install_lib': install_lib,
        'compile_translations': compile_translations}
)
