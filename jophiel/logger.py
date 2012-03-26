'''
Created on 2012-3-21

@author: lzz
'''
import logging
import sys

class NullHandler(logging.Handler):

    def emit(self, record):
        pass

def get_logger(logger):
    if isinstance(logger, basestring):
        logger = logging.getLogger(logger)
        
    if not logger.handlers:
        hdlr = logging.FileHandler("logger.txt")
        formatter = logging.Formatter('[%(asctime)s]%(levelname)-8s"%(message)s"', '%Y-%m-%d %a %H:%M:%S') 
        
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)
        logger.setLevel(logging.NOTSET)
        logger.addHandler(NullHandler())
    return logger

