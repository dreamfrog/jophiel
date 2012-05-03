'''
Created on 2012-3-28

@author: lzz
'''
import os
import pystache
import jophiel

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'templates/mustache')

class ResWeb(pystache.View):
    
    template_path = TEMPLATE_PATH
    
    def __init__(self):
        super(ResWeb, self).__init__()

    def media_folder(self):
        return '/media/'

    def close(self):pass

    def address(self):
        return '%s:%s' % (self.resq.host, self.resq.port)

    def version(self):
        return str(jophiel.__version__)

    def pages(self, start, size, link_function, width=20):
        pages = []

        num_pages = size / width
        if size % width > 0:
            num_pages += 1

        if size < width:
            return pages

        for i in range(num_pages):
            current = True
            if start == i * width:
                current = False
            link = link_function(i * width)
            link_name = str(i + 1)
            pages.append(dict(link=link, link_name=link_name, current=current))
        return pages
