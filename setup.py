# coding=utf-8
"""

"""
# -*- coding: utf-8 -*-

import sys
import types

from io import StringIO
from os import path as op
from os.path import join
from setuptools import (
    setup,
    find_packages,
)
from setuptools.command.test import test as TestCommand
from textwrap import dedent

import pick_three


def _read(filename):
    try:
        fp = open(join(op.dirname(__file__), filename))
        try:
            return fp.read()
        finally:
            fp.close()
    except (IOError, OSError):  # IOError/2.7, OSError/3.5
        return str()


def _read_requirements(filename):
    is_valid = lambda _: _ and not any(_.startswith(ch) for ch in ['#', '-'])

    data = getattr(types, 'UnicodeType', str)(_read(filename))
    return list((_.strip() for _ in StringIO(data) if is_valid(_.strip())))


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to pytest")]

    def initialize_options(self):
        super().initialize_options()
        self.pytest_args = []

    def run_tests(self):
        # Import here, cause outside the eggs aren't loaded.
        import pytest

        errno = pytest.main(self.pytest_args.split())
        sys.exit(errno)


setup_params = dict(
    name="Pick Three",
    version=pick_three.__version__,
    description="Wrapper code for executing bash commands from python",
    long_description=dedent("""
        Solves problem of needing to write 5-15 lines of code to execute a bash command.
        """).strip(),
    author="Matthew Martin",
    author_email='matthewdeanmartin@gmail.com',
    url='https://wakayos.com',

    classifiers=dedent("""
        Natural Language :: English
        Development Status :: 1 - Planning
        Operating System :: POSIX :: Linux
        Programming Language :: Python
        Programming Language :: Python :: 3.6
        """),
    license='Copyright(2018)',
    keywords=[],

    packages=find_packages(),
    # package_dir={'': 'src'},  # tell distutils packages are under `src`
    include_package_data=True,
    # package_data={
    #     # If any package contains *.txt files, include them:
    #     '': ['*.txt'],
    #     # And include any *.dat files found in the `data` subdirectory
    #     # of the `mypkg` package, also:
    #     'mypkg': ['data/*.dat'],
    # },
    # # ...but exclude README.txt from all packages
    # exclude_package_data={'': ['README.txt']},
    # data_files=[
    #     ('bitmaps', ['bm/b1.gif', 'bm/b2.gif']),
    #     ('config', ['cfg/data.cfg']),
    #     ('/etc/init.d', ['init-script']),
    # ],
    zip_safe=False,

    # entry_points={
    #     'console_scripts': [
    #         'foo = bash_helpers.some_module:main_func',
    #         'bar = other_module:some_func',
    #     ],
    #     'gui_scripts': [
    #         'baz = my_package_gui:start_func',
    #     ]
    # },

    install_requires=_read_requirements('requirements.txt'),
    # extras_require={
    #     'PDF':  ['ReportLab>=1.2', "RXP'],
    #     'reST': ['docutils>=0.3'],
    # },
    setup_requires=[
        'wheel',
        'sphinx',
        'sphinx-pypi-upload3',
    ],
    tests_require=_read_requirements('requirements_dev.txt'),

    cmdclass={'test': PyTest},
)


def main():
    setup(**setup_params)


if __name__ == '__main__':
    main()
