#!/usr/bin/env python
#encoding:utf-8
from __future__ import unicode_literals

import os
import unittest
import jsonConfigParser
import json


class TestJsonConfigParser(unittest.TestCase):
	def setUp(self):
		directory = os.path.dirname(os.path.abspath(__file__))
		self.schemaFilename = directory + '/../example.jschem'
		self.dataFilename = directory + '/../example.json'
		
	def test_creation(self):
		with open(self.schemaFilename) as data_file:    
			data = json.load(data_file)
		self.assertIsInstance(jsonConfigParser.jsonConfigParser(data),jsonConfigParser.jsonConfigParser)
		
	def test_loadFile(self):
		jcp = jsonConfigParser.loadParserFromFile(self.schemaFilename)
		self.assertIsInstance(jcp,jsonConfigParser.jsonConfigParser)
		self.assertIsInstance(jcp['items'],jsonConfigParser.jsonConfigParser)
		
	def test_loadFile_with_path(self):
		jcp = jsonConfigParser.loadParserFromFile(self.schemaFilename,path=['items'])
		self.assertIsInstance(jcp,jsonConfigParser.jsonConfigParser)
		self.assertIsInstance(jcp['properties']['sex'],jsonConfigParser.jsonConfigParser)

	def test_validate(self):
		jcp = jsonConfigParser.loadParserFromFile(self.schemaFilename)
		with open(self.dataFilename) as data_file:    
			data = json.load(data_file)
		jcp.validate(data)
			
	def test_display(self):
		jcp = jsonConfigParser.loadParserFromFile(self.schemaFilename)
		with open(self.dataFilename) as data_file:    
			data = json.load(data_file)
		jcp.display(data)

	def test_display(self):
		jcp = jsonConfigParser.loadParserFromFile(self.schemaFilename)
		with open(self.dataFilename) as data_file:    
			data = json.load(data_file)
		self.assertEqual(jcp.getType(),u'array')
		self.assertEqual(jcp['items'].getType(),u'object')
		self.assertEqual(jcp['items']['properties']['sex'].getType(),u'choices')
		self.assertEqual(jcp['items']['properties']['firstName'].getType(),u'string')
		self.assertEqual(jcp['items']['properties']['age'].getType(),u'integer')
		self.assertEqual(jcp['items']['properties']['email'].getType(),u'email')
		self.assertEqual(jcp['items']['properties']['married'].getType(),u'boolean')

	def test_convert(self):
		jcp = jsonConfigParser.jsonConfigParser({'title':'number','type':'integer'})
		with open(self.dataFilename) as data_file:    
			data = json.load(data_file)
		self.assertIsNone(jcp._convert(''))
		self.assertIsNone(jcp._convert(None))
		jcp = jsonConfigParser.jsonConfigParser({'title':'number','type':'integer','default':42})
		with open(self.dataFilename) as data_file:    
			data = json.load(data_file)
		self.assertEqual(jcp._convert(''),42)
