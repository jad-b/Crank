import subprocess
from setuptools import setup, find_packages
import io
import os

here = os.path.abspath(os.path.dirname(__file__))


def git_version():
    try:
        subprocess.check_output(['git', 'describe', '--tags'])
    except:
        return '0.0.1'


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


install_requires = [
    'python-dateutil'
]
tests_require = [
    'pytest',
    'pytest-cov'
] + install_requires

setup(
    name='crank',
    description='Automate your workout',
    long_description=read('README.md'),
    version=git_version(),
    author='Jeremy Dobbins-Bucklad',
    author_email='j.american.db@gmail.com',
    url='http://github.com/jad-b/crank',
    license='GPLv3',
    include_package_data=True,
    install_requires=install_requires,
    setup_requires=[
        'pytest-runner'
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'fto=crank.program.fto.cli:process_input'
        ]
    },
    tests_require=tests_require,
    keywords='workout automation',
    platforms='any',
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
)
