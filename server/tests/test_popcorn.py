import unittest

import redis

import popcorn

popcorn.rdb = rdb = redis.Redis(host='localhost', port=6379, db=13)
class TestPopcorn(unittest.TestCase):

    def test_get_system_id_new(self):
        self.assertEqual(
            popcorn.get_system_id('first-system-id'),
            '1')

    def test_get_system_id_old(self):
        self.assertEqual(
            popcorn.get_system_id('first-system-id'),
            '1')
    def test_get_system_id_second(self):
        self.assertEqual(
            popcorn.get_system_id('second-system-id'),
            '2')

    @classmethod
    def tearDownAll(self):
        rdb.flushdb()
    
