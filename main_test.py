import unittest
import main
import datetime
from dateutil.tz import tzutc


class TestConvertTime(unittest.TestCase):
    def test_happy_path(self):
        d = datetime.datetime(2020, 7, 12, 23, 11, 22,  tzinfo=tzutc())
        result = main.convertTime("2020-07-12T23:11:22Z")
        self.assertEqual(result, d)


class TestGetFilePath(unittest.TestCase):
    def test_happy_path(self):
        d = datetime.datetime(2017, 9, 14, 23, 11, 22,  tzinfo=tzutc())
        result = main.getFilePath("nybp", "b", d)
        self.assertEqual(result, "/cors/rinex/2017/257/nybp/nybp257b.17o.gz")
