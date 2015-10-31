#!/usr/bin/env python
#encoding:utf-8
from __future__ import unicode_literals
from __future__ import print_function

import os
import mock
import unittest
import JSAG.JSAGcli

directory = os.path.dirname(os.path.realpath(__file__))
def load_expected(filename):
	with open (directory + "/expected_" + filename + ".txt", "r") as myfile:
		data=myfile.readlines()
	return [mock.call(line.replace('\n','')) for line in data]

class Test_cli(unittest.TestCase):
	@mock.patch("JSAG.JSAGcli.raw_input",create=True,side_effect=['', '1', '2'])
	@mock.patch("JSAG.JSAGcli.print",create=True)
	def test_prompt_optional(self,myMockPrint,mock_input):
		expected = load_expected('prompt_optional')
		reponse = JSAG.JSAGcli.prompt('Optinal question',default='')
		self.assertEqual(reponse,'')
		for key,line in enumerate(expected):
			self.assertEqual(myMockPrint.mock_calls[key],line)
		self.assertEqual(len(expected),len(myMockPrint.mock_calls))
		
	@mock.patch("JSAG.JSAGcli.raw_input",create=True,side_effect=['', '1', '2'])
	@mock.patch("JSAG.JSAGcli.print",create=True)
	def test_optional_default(self,myMockPrint,mock_input):
		expected = load_expected('optional_default')
		reponse = JSAG.prompt('Optinal question',default='niouf')
		self.assertEqual(reponse,'niouf')
		for key,line in enumerate(expected):
			self.assertEqual(myMockPrint.mock_calls[key],line)
		self.assertEqual(len(expected),len(myMockPrint.mock_calls))
		
	@mock.patch("JSAG.JSAGcli.raw_input",create=True,side_effect=['', '1', '2'])
	@mock.patch("JSAG.JSAGcli.print",create=True)
	def test_prompt_mandatory(self,myMockPrint,mock_input):
		expected = load_expected('prompt_mandatory')
		reponse = JSAG.prompt('Mandatory question',default=None)
		self.assertEqual(reponse,'1')
		for key,line in enumerate(expected):
			self.assertEqual(myMockPrint.mock_calls[key],line)
		self.assertEqual(len(expected),len(myMockPrint.mock_calls))
		
	@mock.patch("JSAG.JSAGcli.raw_input",create=True,side_effect=['', '1', 'y', 'n'])
	@mock.patch("JSAG.JSAGcli.print",create=True)
	def test_prompt_yn(self,myMockPrint,mock_input):
		expected = load_expected('prompt_yn')
		reponse = JSAG.promptYN('Yes or No?')
		self.assertEqual(reponse,True)
		for key,line in enumerate(expected):
			self.assertEqual(myMockPrint.mock_calls[key],line)
		self.assertEqual(len(expected),len(myMockPrint.mock_calls))
		
	@mock.patch("JSAG.JSAGcli.raw_input",create=True,side_effect=['', '1', 'n'])
	@mock.patch("JSAG.JSAGcli.print",create=True)
	def test_prompt_yn_default(self,myMockPrint,mock_input):
		expected = load_expected('prompt_yn_default')
		reponse = JSAG.promptYN('Yes or No?',True)
		self.assertEqual(reponse,True)
		for key,line in enumerate(expected):
			self.assertEqual(myMockPrint.mock_calls[key],line)
		self.assertEqual(len(expected),len(myMockPrint.mock_calls))
		
	@mock.patch("JSAG.JSAGcli.raw_input",create=True,side_effect=['', 'y', '1', 'n'])
	@mock.patch("JSAG.JSAGcli.print",create=True)
	def test_prompt_int_mandatory(self,myMockPrint,mock_input):
		expected = load_expected('prompt_int_mandatory')
		reponse = JSAG.promptInt('How old are you?',default=None)
		self.assertEqual(reponse,1)
		for key,line in enumerate(expected):
			self.assertEqual(myMockPrint.mock_calls[key],line)
		self.assertEqual(len(expected),len(myMockPrint.mock_calls))
		
	@mock.patch("JSAG.JSAGcli.raw_input",create=True,side_effect=['', '1', 'y', 'n'])
	@mock.patch("JSAG.JSAGcli.print",create=True)
	def test_prompt_int_default_0(self,myMockPrint,mock_input):
		expected = load_expected('prompt_int_default_0')
		reponse = JSAG.promptInt('How old are you?')
		self.assertEqual(reponse,0)
		for key,line in enumerate(expected):
			self.assertEqual(myMockPrint.mock_calls[key],line)
		self.assertEqual(len(expected),len(myMockPrint.mock_calls))
		
	@mock.patch("JSAG.JSAGcli.raw_input",create=True,side_effect=['', '1', 'y', 'n'])
	@mock.patch("JSAG.JSAGcli.print",create=True)
	def test_prompt_int_default_42(self,myMockPrint,mock_input):
		expected = load_expected('prompt_int_default_42')
		reponse = JSAG.promptInt('How old are you?',default=42)
		self.assertEqual(reponse,42)
		for key,line in enumerate(expected):
			self.assertEqual(myMockPrint.mock_calls[key],line)
		self.assertEqual(len(expected),len(myMockPrint.mock_calls))
		
	@mock.patch("JSAG.JSAGcli.raw_input",create=True,side_effect=['', '-1', '0', '4', '3', '1'])
	@mock.patch("JSAG.JSAGcli.print",create=True)
	def test_prompt_choices_mandatory(self,myMockPrint,mock_input):
		expected = load_expected('prompt_choices_mandatory')
		reponse = JSAG.promptChoices("Gender",['m','f','I don\'t know'])
		self.assertEqual(reponse,2)
		for key,line in enumerate(expected):
			self.assertEqual(myMockPrint.mock_calls[key],line)
		self.assertEqual(len(expected),len(myMockPrint.mock_calls))
		
	@mock.patch("JSAG.JSAGcli.raw_input",create=True,side_effect=['', '-1', '0', '4', '3', '1'])
	@mock.patch("JSAG.JSAGcli.print",create=True)
	def test_prompt_choices_default_1(self,myMockPrint,mock_input):
		expected = load_expected('prompt_choices_default_1')
		reponse = JSAG.promptChoices("Gender",['m','f','I don\'t know'],default=1)
		self.assertEqual(reponse,1)
		for key,line in enumerate(expected):
			self.assertEqual(myMockPrint.mock_calls[key],line)
		self.assertEqual(len(expected),len(myMockPrint.mock_calls))
