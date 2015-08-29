#!/usr/bin/env python
#encoding:utf-8
from __future__ import unicode_literals

import os
import unittest
import JSAG
import json


class Test_JSAGparser(unittest.TestCase):
	def setUp(self):
		directory = os.path.dirname(os.path.abspath(__file__))
		self.schemaFilename = directory + '/../example.jschem'
		self.dataFilename = directory + '/../example.json'
		
	def test_creation(self):
		with open(self.schemaFilename) as data_file:    
			data = json.load(data_file)
		self.assertIsInstance(JSAG.JSAGparser(data),JSAG.JSAGparser)
		
	def test_loadFile(self):
		parser = JSAG.loadParserFromFile(self.schemaFilename)
		self.assertIsInstance(parser,JSAG.JSAGparser)
		self.assertIsInstance(parser['items'],JSAG.JSAGparser)
		
	def test_loadFile_with_path(self):
		parser = JSAG.loadParserFromFile(self.schemaFilename,path=['items'])
		self.assertIsInstance(parser,JSAG.JSAGparser)
		self.assertIsInstance(parser['properties']['sex'],JSAG.JSAGparser)

	def test_validate(self):
		parser = JSAG.loadParserFromFile(self.schemaFilename)
		with open(self.dataFilename) as data_file:    
			data = json.load(data_file)
		parser.validate(data)
			
	def test_display(self):
		parser = JSAG.loadParserFromFile(self.schemaFilename)
		with open(self.dataFilename) as data_file:    
			data = json.load(data_file)
		parser.display(data)

	def test_display(self):
		parser = JSAG.loadParserFromFile(self.schemaFilename)
		with open(self.dataFilename) as data_file:    
			data = json.load(data_file)
		self.assertEqual(parser.getType(),u'array')
		self.assertEqual(parser['items'].getType(),u'object')
		self.assertEqual(parser['items']['properties']['sex'].getType(),u'choices')
		self.assertEqual(parser['items']['properties']['firstName'].getType(),u'string')
		self.assertEqual(parser['items']['properties']['age'].getType(),u'integer')
		self.assertEqual(parser['items']['properties']['email'].getType(),u'email')
		self.assertEqual(parser['items']['properties']['married'].getType(),u'boolean')

	def test_convert(self):
		parser = JSAG.JSAGparser({'title':'number','type':'integer'})
		with open(self.dataFilename) as data_file:    
			data = json.load(data_file)
		self.assertIsNone(parser._convert(''))
		self.assertIsNone(parser._convert(None))
		parser = JSAG.JSAGparser({'title':'number','type':'integer','default':42})
		with open(self.dataFilename) as data_file:    
			data = json.load(data_file)
		self.assertEqual(parser._convert(''),42)
