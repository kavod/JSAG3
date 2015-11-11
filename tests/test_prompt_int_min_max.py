#!/usr/bin/env python
#encoding:utf-8
from __future__ import unicode_literals
from __future__ import print_function

from mock import *
import unittest
import __builtin__

class Test_prompt_int_min_max(unittest.TestCase):
	@patch("__builtin__.print",create=True)
	def test_prompt_int_min_max(self,myMockPrint):
		with patch("__builtin__.raw_input",create=True,side_effect=[])as mock_input:
			import JSAG
			self.assertEqual(myMockPrint.mock_calls,[])
			myMockPrint.reset_mock()
		with patch("__builtin__.raw_input",create=True,side_effect=['y', '0', '80', '50'])as mock_input:
			reponse = JSAG.promptInt("How old are you?",min=7,max=77)
			self.assertEqual(myMockPrint.mock_calls,[call(u'################################################'),
 call(u'# \x1b[1mHow old are you?\x1b[0m (min: 7 max: 77 default: 0) #'),
 call(u'# \x1b[0m                                             #'),
 call(u'################################################'),
 call(u'\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A'),
 call(u'################################################'),
 call(u'# \x1b[1mHow old are you?\x1b[0m (min: 7 max: 77 default: 0) #'),
 call(u'# Integer min: 7 max: 77 expected\x1b[0m              #'),
 call(u'################################################'),
 call(u'\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A'),
 call(u'################################################'),
 call(u'# \x1b[1mHow old are you?\x1b[0m (min: 7 max: 77 default: 0) #'),
 call(u'# Integer min: 7 max: 77 expected\x1b[0m              #'),
 call(u'################################################'),
 call(u'\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A'),
 call(u'################################################'),
 call(u'# \x1b[1mHow old are you?\x1b[0m (min: 7 max: 77 default: 0) #'),
 call(u'# Integer min: 7 max: 77 expected\x1b[0m              #'),
 call(u'################################################')])
			myMockPrint.reset_mock()
		with patch("__builtin__.raw_input",create=True,side_effect=[])as mock_input:
			self.assertTrue(reponse == 50)
			self.assertEqual(myMockPrint.mock_calls,[])
			myMockPrint.reset_mock()

