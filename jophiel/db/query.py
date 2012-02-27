'''
Created on 2012-2-13

@author: liu
'''
import app
from .models import to_db

class QuerySet(object):
    def __init__(self, model, order_by=None, filter_by=None):
        assert not (order_by and filter_by)
        self.model = model
        self.index = order_by or self.model._meta.ordering
        self.filter = filter_by
    
    def __repr__(self):
        return u'<%s: %s>' % (self.__class__.__name__, list(self))

    def __getitem__(self, key):
        is_slice = isinstance(key, slice)
        if is_slice:
            assert key.step == 1 or key.step is None
            start = key.start or 0
            stop = key.stop
        else:
            start = key
            stop = key + 1

        if stop == -1:
            num = stop
        else:
            num = stop - start
        
        if self.index.startswith('-'):
            desc = True
            index = self.index[1:]
        else:
            desc = False
            index = self.index

        results = self._get_results(start, num, index, desc)
        
        if is_slice:
            return results
        return results[0]

    def __len__(self):
        if self.index.startswith('-'):
            index = self.index[1:]
        else:
            index = self.index
        
        return app.db.count(self.model, index)

    def __iter__(self):
        for r in self[0:-1]:
            yield r

    def _get_results(self, start, num, index, desc=False):
        datas = []
        if self.filter:
            datas = [(pk, app.db.get_data(self.model, pk)) for pk in app.db.list_by_cindex(self.model, **to_db(self.model, self.filter))]
        else:
            datas = app.db.list(self.model, index, start, num, desc)

        return [self.model(pk, **data) for pk, data in datas]

    def order_by(self, index):
        assert not self.filter
        self.index = index
        return self
