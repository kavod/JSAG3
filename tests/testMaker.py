#!/usr/bin/env python
#encoding:utf-8
from __future__ import unicode_literals

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import mock
import JSAG.JSAGcli

pattern = '''
	@mock.patch("JSAG.JSAGcli.raw_input",create=True,side_effect={0})
	@mock.patch("JSAG.JSAGcli.print",create=True)
	def test_{1}(self,myMockPrint,mock_input):
		expected = load_expected('{1}')
		reponse = {2}
		self.assertEqual(reponse,{3})
		for key,line in enumerate(expected):
			self.assertEqual(myMockPrint.mock_calls[key],line)
		self.assertEqual(len(expected),len(myMockPrint.mock_calls))'''

@mock.patch("JSAG.JSAGcli.raw_input",create=True)
@mock.patch("JSAG.JSAGcli.print",create=True)
def create(title,cmd,side_effect,myMockPrint,mock_input):
	mock_input.side_effect = side_effect
	reponse = eval(cmd)
	if isinstance(reponse,unicode):
		reponse = "'{0}'".format(reponse.replace("'","\\'"))
	text_file = open(makeFilename(title),'w')
	for line in myMockPrint.mock_calls:
		text_file.write(line[1][0] + '\n')
	text_file.close()
	print pattern.format(unicode(side_effect),title,cmd,reponse)
	
@mock.patch("JSAG.JSAGcli.raw_input",create=True)
@mock.patch("JSAG.JSAGcli.print",create=True)
def dry_test(title,cmd,side_effect,myMockPrint,mock_input):
	mock_input.side_effect = side_effect
	reponse = eval(cmd)
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
	print 'Title of test'
	title = raw_input()
	print 'Command'
	cmd = raw_input()
	side_effect = []
	print 'user inputs'
	try:
		while True:
			side_effect.append(raw_input())
	except EOFError:
		print side_effect
	reponse = dry_test(title,cmd,side_effect)
	print "Returned value: {0} ({1})".format(unicode(reponse),type(reponse))
	print "OK ?"
	reponse = raw_input('')
	if reponse == 'OK':
		create(title,cmd,side_effect)
	#create('niouf1',"JSAG.JSAGcli.prompt('Optinal question',default='')",['','1','2'])
