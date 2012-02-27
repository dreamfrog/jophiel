#!/usr/bin/env python

# Copyright 2011 Yifei Jiang
#
# This is free software, licensed under the Lesser Affero General 
# Public License, available in the accompanying LICENSE.txt file.


"""
Distutils setup script for python-crawler module.
"""
#      provides=['crawler'],
#      py_modules=['crawler','crawler_database', 'download_manager','webpage','example'],
from distutils.core import setup


__version__ = '0.1.2'

setup(name='crawler',
      version=__version__,
      author='Yifei Jiang',
      author_email='jiangyifei@gmail.com',
      url='http://code.google.com/p/python-crawler/',
      download_url='http://code.google.com/p/python-crawler/downloads/list',
      description='python crawler.',
      long_description="python crawler.",
      packages= ['crawler'],
      requires=['lxml', 'bsddb3',],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP",
        ],
    keywords='python crawler spider',
    license='Apache License 2.0',
     )
