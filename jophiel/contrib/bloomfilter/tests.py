import os
import doctest
import unittest
import random
import tempfile
from .pybloom import BloomFilter, ScalableBloomFilter
from unittest import TestSuite



import random
import redis
import sys
import unittest

from datetime import datetime,timedelta

from .bloomfilter import BloomFilter, TimeSeriesBloomFilter

class SimpleTestCase(unittest.TestCase):
    def setUp(self):
        self.connection = redis.Redis()
        
        self.single = BloomFilter(connection=self.connection, 
                        bitvector_key='test_bloomfilter',
                        n=1024,
                        k=4)
        
        self.timeseries = TimeSeriesBloomFilter(connection=self.connection,
                            bitvector_key='test_timed_bloomfilter', 
                            n=1024*8, 
                            k=4, 
                            time_resolution=timedelta(microseconds=1000), 
                            time_limit=timedelta(microseconds=10000))
    
    def tearDown(self):
        # remove the key in redis
        self.connection.delete('test_bloomfilter')

class SimpleTest(SimpleTestCase):
    def test_add(self):
        f = self.single
        
        f.add('three')
        f.add('four')
        f.add('five')
        f.add('six')
        f.add('seven')
        f.add('eight')
        f.add('nine')
        f.add("ten")        
        
        # test membership operations
        assert 'ten' in f 
        assert 'five' in f
        assert 'two' not in f
        assert 'eleven' not in f         
    
    def test_delete(self):
        f = self.single
        
        f.add('ten')
        assert 'ten' in f
        
        f.delete('ten')
        assert 'ten' not in f
        
    
    def test_timeseries_add(self):
        f = self.timeseries
        
        assert 'test_value' not in f
        f.add('test_value')
        assert 'test_value' in f
    
    def test_timeseries_delay(self):
        f = self.timeseries
        
        f.add('test_value')
        start = datetime.now()
        # allow for 3ms delay in storing/timer resolution
        delay = timedelta(microseconds=3000)
        
        # make sure that the filter doesn't say that test_value is in the filter for too long
        while 'test_value' in f:
            assert datetime.now() < (start+timedelta(microseconds=10000)+delay)
        assert 'test_value' not in f


def additional_tests():
    proj_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    readme_fn = os.path.join(proj_dir, 'README.txt')
    suite = TestSuite([doctest.DocTestSuite('pybloom.pybloom')])
    if os.path.exists(readme_fn):
        suite.addTest(doctest.DocFileSuite(readme_fn, module_relative=False))
    return suite

class TestUnionIntersection(unittest.TestCase):
    def test_union(self):
        bloom_one = BloomFilter(100, 0.001)
        bloom_two = BloomFilter(100, 0.001)
        chars = [chr(i) for i in range(97, 123)]
        for char in chars[len(chars)/2:]:
            bloom_one.add(char)
        for char in chars[:len(chars)/2]:
            bloom_two.add(char)
        new_bloom = bloom_one.union(bloom_two)
        for char in chars:
            self.assert_(char in new_bloom)

    def test_intersection(self):
        bloom_one = BloomFilter(100, 0.001)
        bloom_two = BloomFilter(100, 0.001)
        chars = [chr(i) for i in range(97, 123)]
        for char in chars:
            bloom_one.add(char)
        for char in chars[:len(chars)/2]:
            bloom_two.add(char)
        new_bloom = bloom_one.intersection(bloom_two)
        for char in chars[:len(chars)/2]:
            self.assert_(char in new_bloom)
        for char in chars[len(chars)/2:]:
            self.assert_(char not in new_bloom)

    def test_intersection_capacity_fail(self):
        bloom_one = BloomFilter(1000, 0.001)
        bloom_two = BloomFilter(100, 0.001)
        def _run():
            new_bloom = bloom_one.intersection(bloom_two)
        self.assertRaises(ValueError, _run)

    def test_union_capacity_fail(self):
        bloom_one = BloomFilter(1000, 0.001)
        bloom_two = BloomFilter(100, 0.001)
        def _run():
            new_bloom = bloom_one.union(bloom_two)
        self.assertRaises(ValueError, _run)

    def test_intersection_k_fail(self):
        bloom_one = BloomFilter(100, 0.001)
        bloom_two = BloomFilter(100, 0.01)
        def _run():
            new_bloom = bloom_one.intersection(bloom_two)
        self.assertRaises(ValueError, _run)

    def test_union_k_fail(self):
        bloom_one = BloomFilter(100, 0.01)
        bloom_two = BloomFilter(100, 0.001)
        def _run():
            new_bloom = bloom_one.union(bloom_two)
        self.assertRaises(ValueError, _run)

class Serialization(unittest.TestCase):
    SIZE = 12345
    EXPECTED = set([random.randint(0, 10000100) for _ in xrange(SIZE)])

    def test_serialization(self):
        for klass, args in [(BloomFilter, (self.SIZE,)),
                            (ScalableBloomFilter, ())]:
            filter = klass(*args)
            for item in self.EXPECTED:
                filter.add(item)

            # It seems bitarray is finicky about the object being an
            # actual file, so we can't just use StringIO. Grr.
            f = tempfile.TemporaryFile()
            filter.tofile(f)
            del filter

            f.seek(0)
            filter = klass.fromfile(f)

            for item in self.EXPECTED:
                self.assert_(item in filter)

if __name__ == '__main__':
    unittest.main()
