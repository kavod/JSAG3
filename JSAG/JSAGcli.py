#!/usr/bin/env python
#encoding:utf-8
from __future__ import unicode_literals
from __future__ import print_function

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
	
# For mandatory:default = None
def prompt(question,validate=None,instructions='',default='',choices=[]):
	reponse = None
	warning = ''
	if instructions == '' and default is not None and default != '':
		instructions = '(default: {0})'.format(default)
	while reponse is None or (reponse == '' and default is None):
		print_header(question,instructions=instructions,warning=warning,choices=choices)
		reponse = myInput()
		if reponse == '' and default is None:
			rollback()
			warning = 'Mandatory answer!'
		elif reponse == '' and default is not None:
			reponse = default
		elif validate is not None:
			isValid = validate(reponse)
			if isValid is not True:
				rollback()
				reponse = None
				warning = isValid
	commit()
	return reponse
	
def promptYN(question,default=None):
	if default is not None and isinstance(default,bool):
		instructions = '[Y/n]' if default else '[y/N]'
		default_reponse = 'y' if default else 'n'
	else:
		instructions = '[y/n]'
		default_reponse = None
	reponse = prompt(question,default=default_reponse,validate=validate_YN,instructions=instructions)
	return reponse.lower() == 'y'
	
def validate_YN(reponse):
	if reponse.lower() not in ['y','n']:
		return 'Incorrect answer'
	return True
	
def promptInt(question,default=0):
	if not isinstance(default,int):
		default = None
		default_reponse = None
	else:
		default_reponse = unicode(default)
	reponse = prompt(question,default=default_reponse,validate=validate_digit)
	return int(reponse)
	
def validate_digit(reponse):
	if reponse.isdigit():
		return True
	else:
		return "Integer expected"
		
def promptChoices(question,choices,default=None):
	valid = validate_choices(1,len(choices))
	if isinstance(default,int) and default < len(choices):
		default_reponse = default+1
	else:
		default_reponse = None
	reponse = int(prompt(question,validate=valid.validate,instructions='',default=default_reponse,choices=choices)) 
	return reponse-1
	
class validate_choices(object):
	def __init__(self,min,max):
		self.min = min
		self.max = max
	def validate(self,reponse):
		digit = validate_digit(reponse)
		if digit is True:
			return True if int(reponse) >= self.min and int(reponse) <= self.max else "Invalid answer"
		else:
			return digit
		
def print_header(title,instructions='',warning='',choices=[]):
	max_length = max(len(title)+len(instructions)+1,len(warning))
	print_line(CHAR_TITLE*(max_length+4))
	print_header_line(title,max_length,bold=True,instructions=instructions)
	print_header_line(warning,max_length)
	print_line(CHAR_TITLE*(max_length+4))
	for id,choice in enumerate(choices):
		print_line(CHAR_TITLE + " {0}: {1}".format(unicode(id+1),choice))
	
def print_header_line(text,length = 0,instructions='',bold=False):
	if instructions!='':
		str_pos = ' '+instructions
	else:
		str_pos = instructions
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
	global NB_LINES
	NB_LINES += 1
	return raw_input(CHAR_PROMPT)
	
def rollback():
	global NB_LINES
	print(((char.CURSOR_UP_ONE + char.ERASE_LINE)*(NB_LINES)),end='')
	commit()
	
