import sys, os

def safe_evaluate(s):
    #backup import, os and sys
    backup = {}
    backup['import'] =  globals()['__builtins__'].__import__
    backup['os'] = globals()['os']
    backup['sys'] = globals()['sys']
    
    #delete them from global namespace
    del (globals()['__builtins__'].__import__)
    del(globals()['os'])
    del(globals()['sys'])
    
    #evaluate your string
    print eval(s) 
    
    #restore global namespace
    globals()['__builtins__'].__import__ = backup['import']
    globals()['os'] = backup['os']
    globals()['sys'] = backup['sys']

s1 = "len('Hello world')"
s2 = "__import__('os').getcwd()"

safe_evaluate(s1)
safe_evaluate(s2)