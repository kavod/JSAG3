#!/usr/bin/env python
#encoding:utf-8
from __future__ import unicode_literals
from __future__ import print_function

from mock import *
import unittest
import __builtin__

class Test_display2(unittest.TestCase):
	@patch("__builtin__.print",create=True)
	def test_display2(self,myMockPrint):
		with patch("__builtin__.raw_input",create=True,side_effect=[])as mock_input:
			import JSAG
			self.assertEqual(myMockPrint.mock_calls,[])
			myMockPrint.reset_mock()
		with patch("__builtin__.raw_input",create=True,side_effect=[])as mock_input:
			parser = JSAG.loadParserFromFile('example.jschem')
			self.assertEqual(myMockPrint.mock_calls,[])
			myMockPrint.reset_mock()
		with patch("__builtin__.raw_input",create=True,side_effect=[])as mock_input:
			dataContent = [{"password": "donuts", "firstName": "Homer", "lastName": "Simpson", "age": 44, "married": True, "sex": "m", "spouse": {"firstName": "Marge", "weddate": "1978-05-16T12:14:05+00:00"}, "children": ["Bart", "Lisa", "The baby"]}]
			self.assertEqual(myMockPrint.mock_calls,[])
			myMockPrint.reset_mock()
		with patch("__builtin__.raw_input",create=True,side_effect=[])as mock_input:
			data = JSAG.JSAGdata(configParser=parser,value=dataContent)
			self.assertEqual(myMockPrint.mock_calls,[])
			myMockPrint.reset_mock()
		with patch("__builtin__.raw_input",create=True,side_effect=['1', '1', '2'])as mock_input:
			data.cliChange2()
			self.assertEqual(myMockPrint.mock_calls,[call(u'##########################'),
 call(u'# \x1b[1mChoose item to change\x1b[0m  #'),
 call(u'# \x1b[0m                       #'),
 call(u'##########################'),
 call(u'# 1: \x1b[1m\x1b[91mContact 1:\x1b[0m Managed'),
 call(0),
 call(u'##########################'),
 call(u'# \x1b[1mChoose item to change\x1b[0m  #'),
 call(u'# \x1b[0m                       #'),
 call(u'##########################'),
 call(u'# 1: \x1b[1mSex :\x1b[0m m'),
 call(u'# 2: \x1b[1mFirst Name :\x1b[0m Homer'),
 call(u'# 3: \x1b[1mLast Name :\x1b[0m Simpson'),
 call(u'# 4: \x1b[1mAge :\x1b[0m 44'),
 call(u'# 5: \x1b[1mPassword :\x1b[0m ****'),
 call(u'# 6: \x1b[1mMarried? :\x1b[0m True'),
 call(u'# 7: \x1b[1m\x1b[91mSpouse :\x1b[0m Managed'),
 call(u'# 8: \x1b[1m\x1b[92mChildren :\x1b[0m List of 3 items'),
 call(0),
 call(u'########'),
 call(u'# \x1b[1mSex\x1b[0m  #'),
 call(u'# \x1b[0m     #'),
 call(u'########'),
 call(u'# 1: Mr'),
 call(u'# 2: Ms')])
			myMockPrint.reset_mock()
		with patch("__builtin__.raw_input",create=True,side_effect=['1', '2', 'Marge'])as mock_input:
			data.cliChange2()
			self.assertEqual(myMockPrint.mock_calls,[call(u'##########################'),
 call(u'# \x1b[1mChoose item to change\x1b[0m  #'),
 call(u'# \x1b[0m                       #'),
 call(u'##########################'),
 call(u'# 1: \x1b[1m\x1b[91mContact 1:\x1b[0m Managed'),
 call(0),
 call(u'##########################'),
 call(u'# \x1b[1mChoose item to change\x1b[0m  #'),
 call(u'# \x1b[0m                       #'),
 call(u'##########################'),
 call(u'# 1: \x1b[1mSex :\x1b[0m f'),
 call(u'# 2: \x1b[1mFirst Name :\x1b[0m Homer'),
 call(u'# 3: \x1b[1mLast Name :\x1b[0m Simpson'),
 call(u'# 4: \x1b[1mAge :\x1b[0m 44'),
 call(u'# 5: \x1b[1mPassword :\x1b[0m ****'),
 call(u'# 6: \x1b[1mMarried? :\x1b[0m True'),
 call(u'# 7: \x1b[1m\x1b[91mSpouse :\x1b[0m Managed'),
 call(u'# 8: \x1b[1m\x1b[92mChildren :\x1b[0m List of 3 items'),
 call(1),
 call(u'###############################'),
 call(u'# \x1b[1mFirst Name\x1b[0m (default: Homer) #'),
 call(u'# \x1b[0m                            #'),
 call(u'###############################')])
			myMockPrint.reset_mock()
		with patch("__builtin__.raw_input",create=True,side_effect=['1', '4', 'sd', '39'])as mock_input:
			data.cliChange2()
			self.assertEqual(myMockPrint.mock_calls,[call(u'##########################'),
 call(u'# \x1b[1mChoose item to change\x1b[0m  #'),
 call(u'# \x1b[0m                       #'),
 call(u'##########################'),
 call(u'# 1: \x1b[1m\x1b[91mContact 1:\x1b[0m Managed'),
 call(0),
 call(u'##########################'),
 call(u'# \x1b[1mChoose item to change\x1b[0m  #'),
 call(u'# \x1b[0m                       #'),
 call(u'##########################'),
 call(u'# 1: \x1b[1mSex :\x1b[0m f'),
 call(u'# 2: \x1b[1mFirst Name :\x1b[0m Marge'),
 call(u'# 3: \x1b[1mLast Name :\x1b[0m Simpson'),
 call(u'# 4: \x1b[1mAge :\x1b[0m 44'),
 call(u'# 5: \x1b[1mPassword :\x1b[0m ****'),
 call(u'# 6: \x1b[1mMarried? :\x1b[0m True'),
 call(u'# 7: \x1b[1m\x1b[91mSpouse :\x1b[0m Managed'),
 call(u'# 8: \x1b[1m\x1b[92mChildren :\x1b[0m List of 3 items'),
 call(3),
 call(u'#####################'),
 call(u'# \x1b[1mAge\x1b[0m (default: 44) #'),
 call(u'# \x1b[0m                  #'),
 call(u'#####################'),
 call(u'\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A'),
 call(u'#####################'),
 call(u'# \x1b[1mAge\x1b[0m (default: 44) #'),
 call(u'# Integer expected\x1b[0m  #'),
 call(u'#####################')])
			myMockPrint.reset_mock()
		with patch("__builtin__.raw_input",create=True,side_effect=['5', '1', '5', 'niouf'])as mock_input:
			data.cliChange2()
			self.assertEqual(myMockPrint.mock_calls,[call(u'##########################'),
 call(u'# \x1b[1mChoose item to change\x1b[0m  #'),
 call(u'# \x1b[0m                       #'),
 call(u'##########################'),
 call(u'# 1: \x1b[1m\x1b[91mContact 1:\x1b[0m Managed'),
 call(u'\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A'),
 call(u'##########################'),
 call(u'# \x1b[1mChoose item to change\x1b[0m  #'),
 call(u'# Invalid answer\x1b[0m         #'),
 call(u'##########################'),
 call(u'# 1: \x1b[1m\x1b[91mContact 1:\x1b[0m Managed'),
 call(0),
 call(u'##########################'),
 call(u'# \x1b[1mChoose item to change\x1b[0m  #'),
 call(u'# \x1b[0m                       #'),
 call(u'##########################'),
 call(u'# 1: \x1b[1mSex :\x1b[0m f'),
 call(u'# 2: \x1b[1mFirst Name :\x1b[0m Marge'),
 call(u'# 3: \x1b[1mLast Name :\x1b[0m Simpson'),
 call(u'# 4: \x1b[1mAge :\x1b[0m 39'),
 call(u'# 5: \x1b[1mPassword :\x1b[0m ****'),
 call(u'# 6: \x1b[1mMarried? :\x1b[0m True'),
 call(u'# 7: \x1b[1m\x1b[91mSpouse :\x1b[0m Managed'),
 call(u'# 8: \x1b[1m\x1b[92mChildren :\x1b[0m List of 3 items'),
 call(4),
 call(u'############################'),
 call(u'# \x1b[1mPassword\x1b[0m (default: ****) #'),
 call(u'# \x1b[0m                         #'),
 call(u'############################')])
			myMockPrint.reset_mock()
		with patch("__builtin__.raw_input",create=True,side_effect=['1', '6', 'n'])as mock_input:
			data.cliChange2()
			self.assertEqual(myMockPrint.mock_calls,[call(u'##########################'),
 call(u'# \x1b[1mChoose item to change\x1b[0m  #'),
 call(u'# \x1b[0m                       #'),
 call(u'##########################'),
 call(u'# 1: \x1b[1m\x1b[91mContact 1:\x1b[0m Managed'),
 call(0),
 call(u'##########################'),
 call(u'# \x1b[1mChoose item to change\x1b[0m  #'),
 call(u'# \x1b[0m                       #'),
 call(u'##########################'),
 call(u'# 1: \x1b[1mSex :\x1b[0m f'),
 call(u'# 2: \x1b[1mFirst Name :\x1b[0m Marge'),
 call(u'# 3: \x1b[1mLast Name :\x1b[0m Simpson'),
 call(u'# 4: \x1b[1mAge :\x1b[0m 39'),
 call(u'# 5: \x1b[1mPassword :\x1b[0m ****'),
 call(u'# 6: \x1b[1mMarried? :\x1b[0m True'),
 call(u'# 7: \x1b[1m\x1b[91mSpouse :\x1b[0m Managed'),
 call(u'# 8: \x1b[1m\x1b[92mChildren :\x1b[0m List of 3 items'),
 call(5),
 call(u'##################'),
 call(u'# \x1b[1mMarried?\x1b[0m [Y/n] #'),
 call(u'# \x1b[0m               #'),
 call(u'##################')])
			myMockPrint.reset_mock()
		with patch("__builtin__.raw_input",create=True,side_effect=[])as mock_input:
			7
			self.assertEqual(myMockPrint.mock_calls,[])
			myMockPrint.reset_mock()
		with patch("__builtin__.raw_input",create=True,side_effect=['7', '1', '7', '1', 'Homer'])as mock_input:
			data.cliChange2()
			self.assertEqual(myMockPrint.mock_calls,[call(u'##########################'),
 call(u'# \x1b[1mChoose item to change\x1b[0m  #'),
 call(u'# \x1b[0m                       #'),
 call(u'##########################'),
 call(u'# 1: \x1b[1m\x1b[91mContact 1:\x1b[0m Managed'),
 call(u'\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A'),
 call(u'##########################'),
 call(u'# \x1b[1mChoose item to change\x1b[0m  #'),
 call(u'# Invalid answer\x1b[0m         #'),
 call(u'##########################'),
 call(u'# 1: \x1b[1m\x1b[91mContact 1:\x1b[0m Managed'),
 call(0),
 call(u'##########################'),
 call(u'# \x1b[1mChoose item to change\x1b[0m  #'),
 call(u'# \x1b[0m                       #'),
 call(u'##########################'),
 call(u'# 1: \x1b[1mSex :\x1b[0m f'),
 call(u'# 2: \x1b[1mFirst Name :\x1b[0m Marge'),
 call(u'# 3: \x1b[1mLast Name :\x1b[0m Simpson'),
 call(u'# 4: \x1b[1mAge :\x1b[0m 39'),
 call(u'# 5: \x1b[1mPassword :\x1b[0m ****'),
 call(u'# 6: \x1b[1mMarried? :\x1b[0m False'),
 call(u'# 7: \x1b[1m\x1b[91mSpouse :\x1b[0m Managed'),
 call(u'# 8: \x1b[1m\x1b[92mChildren :\x1b[0m List of 3 items'),
 call(6),
 call(u'##########################'),
 call(u'# \x1b[1mChoose item to change\x1b[0m  #'),
 call(u'# \x1b[0m                       #'),
 call(u'##########################'),
 call(u'# 1: \x1b[1mFirstname :\x1b[0m Marge'),
 call(u'# 2: \x1b[1mWedding date :\x1b[0m 1978-05-16T12:14:05+00:00'),
 call(0),
 call(u'##############################'),
 call(u'# \x1b[1mFirstname\x1b[0m (default: Marge) #'),
 call(u'# \x1b[0m                           #'),
 call(u'##############################')])
			myMockPrint.reset_mock()
		with patch("__builtin__.raw_input",create=True,side_effect=['8', '1', '8', '3', 'Maggie'])as mock_input:
			data.cliChange2()
			self.assertEqual(myMockPrint.mock_calls,[call(u'##########################'),
 call(u'# \x1b[1mChoose item to change\x1b[0m  #'),
 call(u'# \x1b[0m                       #'),
 call(u'##########################'),
 call(u'# 1: \x1b[1m\x1b[91mContact 1:\x1b[0m Managed'),
 call(u'\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A'),
 call(u'##########################'),
 call(u'# \x1b[1mChoose item to change\x1b[0m  #'),
 call(u'# Invalid answer\x1b[0m         #'),
 call(u'##########################'),
 call(u'# 1: \x1b[1m\x1b[91mContact 1:\x1b[0m Managed'),
 call(0),
 call(u'##########################'),
 call(u'# \x1b[1mChoose item to change\x1b[0m  #'),
 call(u'# \x1b[0m                       #'),
 call(u'##########################'),
 call(u'# 1: \x1b[1mSex :\x1b[0m f'),
 call(u'# 2: \x1b[1mFirst Name :\x1b[0m Marge'),
 call(u'# 3: \x1b[1mLast Name :\x1b[0m Simpson'),
 call(u'# 4: \x1b[1mAge :\x1b[0m 39'),
 call(u'# 5: \x1b[1mPassword :\x1b[0m ****'),
 call(u'# 6: \x1b[1mMarried? :\x1b[0m False'),
 call(u'# 7: \x1b[1m\x1b[91mSpouse :\x1b[0m Managed'),
 call(u'# 8: \x1b[1m\x1b[92mChildren :\x1b[0m List of 3 items'),
 call(7),
 call(u'##########################'),
 call(u'# \x1b[1mChoose item to change\x1b[0m  #'),
 call(u'# \x1b[0m                       #'),
 call(u'##########################'),
 call(u'# 1: \x1b[1mChild 1:\x1b[0m Bart'),
 call(u'# 2: \x1b[1mChild 2:\x1b[0m Lisa'),
 call(u'# 3: \x1b[1mChild 3:\x1b[0m The baby'),
 call(2),
 call(u'#############################'),
 call(u'# \x1b[1mChild\x1b[0m (default: The baby) #'),
 call(u'# \x1b[0m                          #'),
 call(u'#############################')])
			myMockPrint.reset_mock()

