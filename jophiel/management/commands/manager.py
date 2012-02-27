'''
Created on 2012-2-25

@author: lzz
'''
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
import sys 
import logging

from jophiel.horde import Khan
from jophiel.utils import setup_pidfile

class Command(BaseCommand):
    option_list = BaseCommand.option_list + ( 
                                             
        make_option("--host", dest="host", default="localhost"),
        make_option("--port", dest="port", type="int", default=6379),
        make_option("-i", '--interval', dest='interval', default=None, help='the default time interval to sleep between runs'),
        make_option('-l', '--log-level', dest='log_level', default='info', 
                    help='log level.  Valid values are "debug", "info", "warning", "error", "critical",' +
                    'in decreasing order of verbosity. Defaults to "info" if parameter not specified.'),
        
        make_option("--pool", type="int", dest="pool_size", default=1, 
                    help="Number of minions to spawn under the manager."),
        make_option('-f', dest='logfile', 
                    help='If present, a logfile will be used.  "stderr", "stdout", and "syslog" are all special values.'),
        make_option('-p', dest='pidfile', 
                    help='If present, a pidfile will be used.')
    )   
    help = 'Runs the test suite for the specified applications, or the entire site if no apps are specified.'
    args = '[appname ...]'



    def handle(self, *args, **options):
        log_level = getattr(logging, options["log_level"].upper(), 'INFO')
    
        setup_pidfile(options.get("pidfile",None))
    
        interval = options.get("interval",None)
        if interval is not None:
            interval = float(interval)
    
        queues = args[0].split(',')
        
        print "----",queues,args
        server = '%s:%s' % (options["host"], options["port"])
                                    
        Khan.run(pool_size=options["pool_size"], queues=queues, server=server, logging_level=log_level, log_file=options["logfile"])
