#!/usr/bin/env python
#encoding:utf-8
from __future__ import unicode_literals
from __future__ import print_function

import mock
import unittest

class char(object):
	CURSOR_UP_ONE = '\x1b[1A'
	CURSOR_DOWN_ONE = '\x1b[1B'
	
	ERASE_LINE = '\x1b[2K'
	PURPLE = '\033[95m'
	WHITE = '\033[97m'
	CYAN = '\033[96m'
	DARKCYAN = '\033[36m'
	BLUE = '\033[94m'
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	END = '\033[0m'
	
CHAR_TITLE = '#'
CHAR_PROMPT = '> '
NB_LINES = 0
	
def prompt(question,mandatory=False,validate=None,possibles=''):
	reponse = None
	warning = ''
	while reponse is None or (reponse == '' and mandatory):
		print_header(question,possibles=possibles,warning=warning)
		reponse = myInput()
		if reponse == '' and mandatory:
			rollback()
			warning = 'Mandatory answer!'
		elif validate is not None:
			isValid = validate(reponse)
			if isValid is not True:
				rollback()
				reponse = None
				warning = isValid
	commit()
	return reponse
	
def validate_YN(reponse):
	if reponse.lower() not in ['y','n']:
		return 'Incorrect answer'
	return True
		
def print_header(title,possibles='',warning=''):
	max_length = max(len(title)+len(possibles)+1,len(warning))
	print_line(CHAR_TITLE*(max_length+4))
	print_header_line(title,max_length,bold=True,possibles=possibles)
	print_header_line(warning,max_length)
	print_line(CHAR_TITLE*(max_length+4))
	
def print_header_line(text,length = 0,possibles='',bold=False):
	if possibles!='':
		str_pos = ' '+possibles
	else:
		str_pos = possibles
	pattern = CHAR_TITLE + ' {1}{0}' + char.END + '{2}{3} ' + CHAR_TITLE
	trim = ' '*(length-(len(text)+len(str_pos)))
	if bold:
		style = char.BOLD
	else:
		style = ''
	print_line(pattern.format(text,style,str_pos,trim))
	
def commit():
	global NB_LINES
	NB_LINES = 0
	
def print_line(text):
	global NB_LINES
	print(text)
	NB_LINES += 1
	
def myInput():
	return raw_input(CHAR_PROMPT)
	
def rollback():
	global NB_LINES
	print((char.CURSOR_UP_ONE + char.ERASE_LINE)*(NB_LINES+1), end='')
	commit()
	
class Test_cli(unittest.TestCase):
	def myMock(self,inputs):
		myMockInput = mock.Mock(side_effect=inputs)
		mockPrint = mock.Mock()
		self.original_raw_input = __builtins__['raw_input']
		__builtins__['raw_input'] = myMockInput
		self.original_print = __builtins__['print']
		__builtins__['print'] = mockPrint
		return mockPrint
		
	def unMock(self):
		__builtins__['print'] = self.original_print
		__builtins__['raw_input'] = self.original_raw_input
		
	def test_prompt_optional(self):
		myMockPrint = self.myMock(['','1','2'])
		expected = [mock.call('#####################'),
					mock.call('# \x1b[1mOptinal question\x1b[0m  #'),
					mock.call('# \x1b[0m                  #'),
					mock.call('#####################')]
		reponse = prompt('Optinal question',mandatory=False)
		self.assertEqual(reponse,'')
		self.unMock()
		for key,line in enumerate(expected):
			self.assertEqual(myMockPrint.mock_calls[key],line)
		
	def test_prompt_mandatory(self):
		myMockPrint = self.myMock(['','1','2'])
		expected = [mock.call('#######################'),
					mock.call('# \x1b[1mMandatory question\x1b[0m  #'),
					mock.call('# \x1b[0m                    #'),
					mock.call('#######################')]
		reponse = prompt('Mandatory question',mandatory=True)
		self.assertEqual(reponse,'1')
		self.unMock()
		for key,line in enumerate(expected):
			self.assertEqual(myMockPrint.mock_calls[key],line)
	
if __name__ == '__main__':
	print_header('Niouf Niouf !',possibles='[Y/n]',warning='niorf')
	prompt('Optinal question',mandatory=False)
	prompt('Mandatory question',mandatory=True)
	prompt('Yes or No?',possibles='[y/n]',validate=validate_YN,mandatory=True)
