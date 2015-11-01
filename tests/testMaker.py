#!/usr/bin/env python
#encoding:utf-8
from __future__ import unicode_literals

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import mock

pattern = '''
	@mock.patch("__builtin__.raw_input",create=True,side_effect={0})
	@mock.patch("__builtin__.print",create=True)
	def test_{1}(self,myMockPrint,mock_input):
		expected = load_expected('{1}')
		{5}
		reponse = {2}
		self.assertEqual(reponse,{3})
		for key,line in enumerate(expected):
			self.assertEqual(myMockPrint.mock_calls[key],line)
		self.assertEqual(len(expected),len(myMockPrint.mock_calls))'''
module = ''

def create(title,cmd1,cmd2,side_effect):
	with mock.patch("__builtin__.raw_input",create=True)as mock_input:
		with mock.patch("__builtin__.print",create=True) as myMockPrint:
			mock_input.side_effect = side_effect
			exec('\n'.join(cmd1))
			reponse = eval(cmd2)
			if isinstance(reponse,unicode):
				reponse = "'{0}'".format(reponse.replace("'","\\'"))
			text_file = open(makeFilename(title),'w')
			for line in myMockPrint.mock_calls:
				text_file.write(line[1][0] + '\n')
			text_file.close()
			print pattern.format(unicode(side_effect),title,cmd2,reponse,module,'\n\t\t'.join(cmd1))
	
def dry_test(title,cmd1,cmd2,side_effect):
	with mock.patch("__builtin__.raw_input",create=True) as mock_input:
		with mock.patch("__builtin__.print",create=True) as myMockPrint:
			mock_input.side_effect = side_effect
			if len(cmd1)>0:
				print('\n'.join(cmd1))
				exec('\n'.join(cmd1))
			print(cmd2)
			reponse = eval(cmd2)
			mock_input.side_effect = side_effect
			if isinstance(reponse,unicode):
				reponse = "'{0}'".format(reponse.replace("'","\\'"))
			print("File: "+makeFilename(title))
			for line in myMockPrint.mock_calls:
				print(line[1][0])
			return reponse
	
def makeFilename(title):
	return currentdir + '/expected_' + title + '.txt'
	
if __name__ == '__main__':
	print 'Module?'
	module = raw_input()
	mod = __import__(module)
	print 'Title of test'
	title = raw_input()
	print 'Command'
	try:
		cmd1=[]
		while True:
			cmd1.append(raw_input())
	except EOFError:
		cmd2=cmd1.pop()
	side_effect = []
	print 'user inputs'
	try:
		while True:
			side_effect.append(raw_input())
	except EOFError:
		print side_effect
	reponse = dry_test(title,cmd1,cmd2,side_effect)
	print "Returned value: {0} ({1})".format(unicode(reponse),type(reponse))
	print "OK ?"
	reponse = raw_input('')
	if reponse == 'OK':
		create(title,cmd1,cmd2,side_effect)
