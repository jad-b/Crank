
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import io
import codecs
import os
import sys

import crank

here = os.path.abspath(os.path.dirname(__file__))

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.md')

setup(
    name='crank',
    version=crank.__version__,
    url='http://github.com/jad-b/crank/',
    license='Apache Software License',
    author='Jeremy Dobbins-Bucklad',
    tests_require=['nose'],
    install_requires=[],
    # cmdclass={'test': PyTest},
    author_email='j.american.db@gmail.com',
    description='Automate your workout',
    long_description=long_description,
    packages=['crank'],
    include_package_data=True,
    platforms='any',
    test_suite='crank.test.test_crank',
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        ],
    extras_require={
        'testing': ['nose', 'coverage'],
    }
)

