#!/usr/bin/env python
#encoding:utf-8
from __future__ import unicode_literals
from __future__ import print_function

import mock
import unittest
import JSAG.JSAGcli

class Test_cli(unittest.TestCase):	
	@mock.patch("JSAG.JSAGcli.raw_input",create=True,side_effect=['','1','2'])
	@mock.patch("JSAG.JSAGcli.print",create=True)
	def test_prompt_optional(self,myMockPrint,mock_input):
		expected = [mock.call('#####################'),
					mock.call('# \x1b[1mOptinal question\x1b[0m  #'),
					mock.call('# \x1b[0m                  #'),
					mock.call('#####################')]
		reponse = JSAG.JSAGcli.prompt('Optinal question',default='')
		self.assertEqual(reponse,'')
		for key,line in enumerate(expected):
			self.assertEqual(myMockPrint.mock_calls[key],line)
		self.assertEqual(len(expected),len(myMockPrint.mock_calls))
		
	@mock.patch("JSAG.JSAGcli.raw_input",create=True,side_effect=['','1','2'])
	@mock.patch("JSAG.JSAGcli.print",create=True)
	def test_prompt_optional_default(self,myMockPrint,mock_input):
		expected = [mock.call('#####################################'),
					mock.call('# \x1b[1mOptinal question\x1b[0m (default: niouf) #'),
					mock.call('# \x1b[0m                                  #'),
					mock.call('#####################################')]
		reponse = JSAG.prompt('Optinal question',default='niouf')
		self.assertEqual(reponse,'niouf')
		for key,line in enumerate(expected):
			self.assertEqual(myMockPrint.mock_calls[key],line)
		self.assertEqual(len(expected),len(myMockPrint.mock_calls))
		
	@mock.patch("JSAG.JSAGcli.raw_input",create=True,side_effect=['','1','2'])
	@mock.patch("JSAG.JSAGcli.print",create=True)
	def test_prompt_mandatory(self,myMockPrint,mock_input):
		expected = [mock.call('#######################'),
					mock.call('# \x1b[1mMandatory question\x1b[0m  #'),
					mock.call('# \x1b[0m                    #'),
					mock.call('#######################'),
					mock.call('\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K', end=u''),
					mock.call('#######################'),
					mock.call('# \x1b[1mMandatory question\x1b[0m  #'),
					mock.call('# Mandatory answer!\x1b[0m   #'),
					mock.call('#######################')]
		reponse = JSAG.prompt('Mandatory question',default=None)
		self.assertEqual(reponse,'1')
		for key,line in enumerate(expected):
			self.assertEqual(myMockPrint.mock_calls[key],line)
		self.assertEqual(len(expected),len(myMockPrint.mock_calls))
		
	@mock.patch("JSAG.JSAGcli.raw_input",create=True,side_effect=['','1','y','n'])
	@mock.patch("JSAG.JSAGcli.print",create=True)
	def test_prompt_yn(self,myMockPrint,mock_input):
		expected = [mock.call('####################'),
					mock.call('# \x1b[1mYes or No?\x1b[0m [y/n] #'),
					mock.call('# \x1b[0m                 #'),
					mock.call('####################'),
					mock.call('\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K', end=u''),
					mock.call('#####################'),
					mock.call('# \x1b[1mYes or No?\x1b[0m [y/n]  #'),
					mock.call('# Mandatory answer!\x1b[0m #'),
					mock.call('#####################'),
					mock.call('\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K', end=u''),
					mock.call('####################'),
					mock.call('# \x1b[1mYes or No?\x1b[0m [y/n] #'),
					mock.call('# Incorrect answer\x1b[0m #'),
					mock.call('####################'),]
		reponse = JSAG.promptYN('Yes or No?')
		self.assertEqual(reponse,True)
		for key,line in enumerate(expected):
			self.assertEqual(myMockPrint.mock_calls[key],line)
		self.assertEqual(len(expected),len(myMockPrint.mock_calls))
		
	@mock.patch("JSAG.JSAGcli.raw_input",create=True,side_effect=['','1','y','n'])
	@mock.patch("JSAG.JSAGcli.print",create=True)
	def test_prompt_yn_default(self,myMockPrint,mock_input):
		expected = [mock.call('####################'),
					mock.call('# \x1b[1mYes or No?\x1b[0m [Y/n] #'),
					mock.call('# \x1b[0m                 #'),
					mock.call('####################')]
		reponse = JSAG.promptYN('Yes or No?',True)
		self.assertEqual(reponse,True)
		for key,line in enumerate(expected):
			self.assertEqual(myMockPrint.mock_calls[key],line)
		self.assertEqual(len(expected),len(myMockPrint.mock_calls))
		
	@mock.patch("JSAG.JSAGcli.raw_input",create=True,side_effect=['','y','1','n'])
	@mock.patch("JSAG.JSAGcli.print",create=True)
	def test_prompt_int_mandatory(self,myMockPrint,mock_input):
		expected = [mock.call('#####################'),
					mock.call('# \x1b[1mHow old are you?\x1b[0m  #'),
					mock.call('# \x1b[0m                  #'),
					mock.call('#####################'),
					mock.call('\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K', end=u''),
					mock.call('#####################'),
					mock.call('# \x1b[1mHow old are you?\x1b[0m  #'),
					mock.call('# Mandatory answer!\x1b[0m #'),
					mock.call('#####################'),
					mock.call('\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K', end=u''),
					mock.call('#####################'),
					mock.call('# \x1b[1mHow old are you?\x1b[0m  #'),
					mock.call('# Integer expected\x1b[0m  #'),
					mock.call('#####################')]
		reponse = JSAG.promptInt('How old are you?',default=None)
		self.assertEqual(reponse,1)
		for key,line in enumerate(expected):
			self.assertEqual(myMockPrint.mock_calls[key],line)
		self.assertEqual(len(expected),len(myMockPrint.mock_calls))
		
	@mock.patch("JSAG.JSAGcli.raw_input",create=True,side_effect=['','1','y','n'])
	@mock.patch("JSAG.JSAGcli.print",create=True)
	def test_prompt_int_default_0(self,myMockPrint,mock_input):
		expected = [mock.call('#################################'),
					mock.call('# \x1b[1mHow old are you?\x1b[0m (default: 0) #'),
					mock.call('# \x1b[0m                              #'),
					mock.call('#################################')]
		reponse = JSAG.promptInt('How old are you?')
		self.assertEqual(reponse,0)
		for key,line in enumerate(expected):
			self.assertEqual(myMockPrint.mock_calls[key],line)
		self.assertEqual(len(expected),len(myMockPrint.mock_calls))
		
	@mock.patch("JSAG.JSAGcli.raw_input",create=True,side_effect=['','1','y','n'])
	@mock.patch("JSAG.JSAGcli.print",create=True)
	def test_prompt_int_default_42(self,myMockPrint,mock_input):
		expected = [mock.call('##################################'),
					mock.call('# \x1b[1mHow old are you?\x1b[0m (default: 42) #'),
					mock.call('# \x1b[0m                               #'),
					mock.call('##################################')]
		reponse = JSAG.promptInt('How old are you?',default=42)
		self.assertEqual(reponse,42)
		for key,line in enumerate(expected):
			self.assertEqual(myMockPrint.mock_calls[key],line)
		self.assertEqual(len(expected),len(myMockPrint.mock_calls))
		
	@mock.patch("JSAG.JSAGcli.raw_input",create=True,side_effect=['','-1','0','4','3','1'])
	@mock.patch("JSAG.JSAGcli.print",create=True)
	def test_prompt_choices_mandatory(self,myMockPrint,mock_input):
		expected = [mock.call('###########'),
					mock.call('# \x1b[1mGender\x1b[0m  #'),
					mock.call('# \x1b[0m        #'),
					mock.call('###########'),
					mock.call(u'# 1: m'),
					mock.call(u'# 2: f'),
					mock.call(u"# 3: I don't know"),
					mock.call(u'\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K', end=u''),
					mock.call('#####################'),
					mock.call('# \x1b[1mGender\x1b[0m            #'),
					mock.call('# Mandatory answer!\x1b[0m #'),
					mock.call('#####################'),
					mock.call(u'# 1: m'),
					mock.call(u'# 2: f'),
					mock.call(u"# 3: I don't know"),
					mock.call(u'\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K', end=u''),
					mock.call('####################'),
					mock.call('# \x1b[1mGender\x1b[0m           #'),
					mock.call('# Integer expected\x1b[0m #'),
					mock.call('####################'),
					mock.call(u'# 1: m'),
					mock.call(u'# 2: f'),
					mock.call(u"# 3: I don't know"),
					mock.call(u'\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K', end=u''),
					mock.call('##################'),
					mock.call('# \x1b[1mGender\x1b[0m         #'),
					mock.call('# Invalid answer\x1b[0m #'),
					mock.call('##################'),
					mock.call(u'# 1: m'),
					mock.call(u'# 2: f'),
					mock.call(u"# 3: I don't know"),
					mock.call(u'\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2K', end=u''),
					mock.call('##################'),
					mock.call('# \x1b[1mGender\x1b[0m         #'),
					mock.call('# Invalid answer\x1b[0m #'),
					mock.call('##################'),
					mock.call(u'# 1: m'),
					mock.call(u'# 2: f'),
					mock.call(u"# 3: I don't know")]
		reponse = JSAG.promptChoices("Gender",['m','f','I don\'t know'])
		self.assertEqual(reponse,2)
		for key,line in enumerate(expected):
			self.assertEqual(myMockPrint.mock_calls[key],line)
		self.assertEqual(len(expected),len(myMockPrint.mock_calls))
		
	@mock.patch("JSAG.JSAGcli.raw_input",create=True,side_effect=['','-1','0','4','3','1'])
	@mock.patch("JSAG.JSAGcli.print",create=True)
	def test_prompt_choices_default_1(self,myMockPrint,mock_input):
		expected = [mock.call('#######################'),
					mock.call('# \x1b[1mGender\x1b[0m (default: 2) #'),
					mock.call('# \x1b[0m                    #'),
					mock.call('#######################'),
					mock.call(u'# 1: m'),
					mock.call(u'# 2: f'),
					mock.call(u"# 3: I don't know")]
		reponse = JSAG.promptChoices("Gender",['m','f','I don\'t know'],default=1)
		self.assertEqual(reponse,1)
		for key,line in enumerate(expected):
			self.assertEqual(myMockPrint.mock_calls[key],line)
		self.assertEqual(len(expected),len(myMockPrint.mock_calls))
