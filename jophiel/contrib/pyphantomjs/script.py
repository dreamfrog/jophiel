#!/usr/bin/env python
'''
Created on 2012-4-16

@author: lzz
'''

from runpy import run_module

# automatically convert Qt types by using api 2
import sip 
for item in ('QDate', 'QDateTime', 'QString', 'QTextStream', 'QTime'
             'QUrl', 'QVariant'):
    sip.setapi(item, 2)

if __name__ == '__main__':
    run_module('pyphantomjs.pyphantomjs', run_name='__main__')