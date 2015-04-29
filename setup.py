import subprocess
from setuptools import setup
import io
import os

here = os.path.abspath(os.path.dirname(__file__))


def read_version(filename='VERSION'):
    subprocess.check_output(['git', 'describe', '--abbrev=0', '--tags'])


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

setup(
    author='Jeremy Dobbins-Bucklad',
    author_email='j.american.db@gmail.com',
    classifiers=[
        # 'License :: OSI Approved :: MIT',
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    description='Automate your workout',
    entry_points={
        'console_scripts': [
            'fto=crank.fto.cli:process_input'
        ]
    },
    extras_require={
        'testing': ['nose', 'coverage'],
    },
    include_package_data=True,
    install_requires=[],
    keywords='workout automation',
    license='MIT',
    long_description=read('README.rst'),
    name='crank',
    packages=['crank'],
    platforms='any',
    test_suite='crank.test.test_crank',
    tests_require=['nose'],
    url='http://github.com/jad-b/crank',
    version=read_version()
)
