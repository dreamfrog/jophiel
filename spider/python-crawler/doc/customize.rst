.. _getting_started:


***************
Getting started
***************

.. _installing:

Installing python-crawler
=========================

.. _package-requirement:

Package Requirement
-------------------

Two dependent python packages are::

  python-lxml
  python-bsddb3

.. _windows-install:

Installation in Windows
-----------------------


.. _ubuntu-install:

Installation in Ubuntu
----------------------

.. _simple-crawler:

Runing Simple Cralwer
=====================

Example::

  from crawler.crawler import Crawler
  mycrawler = Crawler()
  seeds = ['http://www.example.com/'] # list of url
  mycrawler.add_seeds(seeds)
  url_patterns = ['^(.+example\.com)(.+)$'] # list of regular expression for urls that crawler will work on.
  mycrawler.start(url_patterns) # start crawling
