#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  2023 ozkary.com.
#
#  MTA turnstile data engineering and analysis
#

import unittest
from datetime import timedelta, date
from etl_web_to_gcs import get_file_date, valid_task

class test_valid_request(unittest.TestCase):
    def test_valid_request(self):        
        self.assertEqual(valid_task(2023,3,28), True)
        self.assertEqual(valid_task(2023,0,0), False)        

class test_file_date(unittest.TestCase):
    def test_file_date(self):
        self.assertEqual(get_file_date(date(2023,3,28)), '230325')                 

if __name__ == '__main__':
    unittest.main()
