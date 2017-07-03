#!/usr/bin/env python

from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='cmediasort',
    version='0.7.0',
    author='Chris Oboe',
    author_email='chrisoboe@eml.cc',
    description='A tool for automaticly sorting movies and episodes',
    license='GPLv3+',
    url='https://github.com/ChrisOboe/cmediasort',
    download_url='https://github.com/ChrisOboe/cmediasort/archive/v0.7.0.tar.gz',
    packages=['cmediasort'],
    install_requires=[
        'mediasort'
        'appdirs'
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)"
    ],
    entry_points={
        'console_scripts': [
            'cmediasort = cmediasort.__main__:main'
        ]
    }
)
