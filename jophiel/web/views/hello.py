#coding=utf-8
'''
Created on 2012-2-24

@author: lzz
'''

from django.shortcuts import render_to_response

import pystache

class Hello(pystache.View):
    
    def __init__(self):
        super(Hello, self).__init__()
        
    def set_names(self, names):
        self.__names = names
    
    def names(self):
        return self.__names
    
def hello(request):
    from jophiel.views import templates
    index_template = Hello()
    index_template.set_names([{
        'id': '1',
        'name': 'Joe',
        }])
        
    return render_to_response('hello.html', {"helloView": index_template })
   
    
