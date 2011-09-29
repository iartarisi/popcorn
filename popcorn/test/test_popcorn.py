import unittest

import redis

from popcorn import configs
configs.rdb = rdb = redis.Redis('localhost', db='13')
from popcorn import server


class TestPopcorn(unittest.TestCase):
    def test_submit_success(self):
        submission = ("POPCORN 0.1 x86_64 TEST_HW_UUID\n"
                      "v python 2.5 1.1 None x86_64 openSUSE-11.4\n"
                      "o python-lint 1.1 1 None noarch openSUSE-11.4\n")
        server.parse_popcorn(submission)
        self.assertEqual(rdb.get('global:nextSubmissionId'), '1')
        self.assertEqual(rdb.get('global:nextSystemId'), '1')
        self.assertEqual(rdb.get('global:nextPackageId'), '2')
        self.assertEqual(rdb.get(
            'vendor:openSUSE-11.4:package:python-2.5-1.1.x86_64'), '1')
        self.assertEqual(rdb.get(
            'vendor:openSUSE-11.4:package:python-lint-1.1-1.noarch'), '2')
        self.assertEqual(rdb.hget('package:1:status', 'voted'), '1')
        self.assertEqual(rdb.hget('package:2:status', 'old'), '1')

        self.assertEqual(rdb.smembers('vendors'), set(['openSUSE-11.4']))
        self.assertEqual(rdb.smembers('vendor:openSUSE-11.4:packages'),
                         set(['1', '2']))
        self.assertEqual(rdb.smembers('systems'), set(['TEST_HW_UUID']))
        self.assertEqual(rdb.smembers('system:1:submissions'), set(['1']))

    def tearDown(self):
        rdb.flushdb()
