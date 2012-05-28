
from types import *
def  task(func):
    def new_func(values):
        try:
            print "inside new_func"
            print type(func(values)) is GeneratorType
            print isinstance(func(values),GeneratorType)
            for value in func(values):
                yield value
        finally:
            print "finish"
    return new_func
@task
def ite(values=[]):
    for value in values:
        yield value
values = [1,2,3,4,5]

for value in ite(values):
    print value
