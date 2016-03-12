#!/usr/bin/env python
#encoding:utf-8
from __future__ import unicode_literals

import os
import json
import unittest
import logging
import tempfile
import JSAG3

DEBUG=False

class TestJSAG3(unittest.TestCase):
	def setUp(self):
		self.absdir = os.path.abspath(os.path.dirname(__file__))
	
		# Complete test case
		self.id1="conf1"
		self.schemaFile1=self.absdir+"/JSAG3.jschem"
		self.optionsFile1=self.absdir+"/JSAG3.jopt"
		self.dataFile1=self.absdir+"/JSAG3.json"
		
		# Options file not exists
		self.id2=self.id1
		self.schemaFile2=self.schemaFile1
		self.optionsFile2=None
		self.dataFile2=self.dataFile1
		
		# Data file not exists
		self.id3=self.id1
		self.schemaFile3=self.schemaFile1
		self.optionsFile3=self.optionsFile1
		self.dataFile3=None
		
	def test_creation(self):
		conf = self.creation(id=self.id1,schemaFile=self.schemaFile1,optionsFile=self.optionsFile1,dataFile=self.dataFile1)
		isinstance(conf,JSAG3.JSAG3)
		
	def test_creation_without_options(self):
		conf = self.creation(id=self.id2,schemaFile=self.schemaFile2,optionsFile=self.optionsFile2,dataFile=self.dataFile2)
		isinstance(conf,JSAG3.JSAG3)
		
	def test_creation_without_datafile(self):
		tmpfile = unicode(tempfile.mkstemp('.json')[1])
		os.remove(tmpfile)
		self.assertFalse(os.path.isfile(tmpfile))
		conf = self.creation(id=self.id3,schemaFile=self.schemaFile3,optionsFile=self.optionsFile3,dataFile=tmpfile)
		isinstance(conf,JSAG3.JSAG3)
		self.assertTrue(os.path.isfile(tmpfile))
		with open(tmpfile) as data_file:
			data = json.load(data_file)
		self.assertEqual(data,{self.id3:[]})
		os.remove(tmpfile)
		
	def test_addSchema_file(self):
		with open(self.schemaFile2) as data_file:
			schema = json.load(data_file)
		jsag3 = self.creation(id=self.id2)
		jsag3.addSchema(self.schemaFile2)
		jsag3.addData(self.dataFile2)
		self.assertEquals(getattr(jsag3.getRoot().schema,self.id2).index(),schema)
		
	def test_addSchema_dict(self):
		with open(self.schemaFile2) as data_file:
			schema = json.load(data_file)
		jsag3 = self.creation(id=self.id2)
		jsag3.addSchema(schema)
		jsag3.addData(self.dataFile2)
		self.assertEquals(getattr(jsag3.getRoot().schema,self.id2).index(),schema)
		
	def test_incomplete(self):
		conf = self.creation(id=self.id2)
		isinstance(conf,JSAG3.JSAG3)
		with self.assertRaises(Exception):
			conf.checkCompleted()
		conf.addSchema(self.schemaFile2)
		with self.assertRaises(Exception):
			conf.checkCompleted()
		conf.addData(self.dataFile2)
		try:
			conf.checkCompleted()
		except:
			self.fail("conf2 should be completed")
			
	def test_getConf(self):
		initial_conf = {'/'.encode('utf8'):{}}
		conf = {'/data'.encode('utf8'): {'tools.caching.on': False}}
		conf.update(initial_conf)
		jsag3 = self.creation(id=self.id1,schemaFile=self.schemaFile1,optionsFile=self.optionsFile1,dataFile=self.dataFile1)
		self.assertEquals(conf,jsag3.getConf(initial_conf))
		
	def test_getRoot(self):
		jsag3 = self.creation(id=self.id1,schemaFile=self.schemaFile1,optionsFile=self.optionsFile1,dataFile=self.dataFile1)
		self.assertTrue(hasattr(jsag3.getRoot(),"schema"))
		self.assertTrue(hasattr(jsag3.getRoot(),"options"))
		self.assertTrue(hasattr(jsag3.getRoot(),"data"))
		
	def test_updateData(self):
		with open(self.dataFile1) as data_file:
			data = json.load(data_file)[self.id1]
			
		tmpfile = unicode(tempfile.mkstemp('.json')[1])
		os.remove(tmpfile)
		self.assertFalse(os.path.isfile(tmpfile))
		conf = self.creation(id=self.id3,schemaFile=self.schemaFile3,optionsFile=self.optionsFile3,dataFile=tmpfile)
		isinstance(conf,JSAG3.JSAG3)
		self.assertTrue(os.path.isfile(tmpfile))
		conf.updateData(data)
		with open(tmpfile) as data_file:
			newData = json.load(data_file)
		self.assertEqual(newData,{self.id1:data})
		os.remove(tmpfile)
		
	def test_save(self):
		value = [{"keywords": [], "provider_type": "kat"}]
		tmpfile = unicode(tempfile.mkstemp('.json')[1])
		os.remove(tmpfile)
		conf = self.creation(id="conf",schemaFile=self.schemaFile3,optionsFile=self.optionsFile3,dataFile=tmpfile)
		conf.setValue(value)
		conf.save()
		with open(tmpfile) as data_file:
			data = json.load(data_file)
		self.assertEqual(data,{"conf":value})
		os.remove(tmpfile)	
		
	def test_save_with_filename(self):
		value = [{"keywords": [], "provider_type": "kat"}]
		tmpfile = unicode(tempfile.mkstemp('.json')[1])
		os.remove(tmpfile)
		conf = self.creation(id="conf",schemaFile=self.schemaFile3,optionsFile=self.optionsFile3,dataFile=None)
		conf.setValue(value)
		conf.save(filename=tmpfile)
		with open(tmpfile) as data_file:
			data = json.load(data_file)
		self.assertEqual(data,{"conf":value})
		os.remove(tmpfile)	
		
	def test_share_data_file(self):
		value = [{"keywords": [], "provider_type": "kat"}]
	
		tmpfile = unicode(tempfile.mkstemp('.json')[1])
		os.remove(tmpfile)
		conf1 = self.creation(id="conf1",schemaFile=self.schemaFile3,optionsFile=self.optionsFile3,dataFile=tmpfile)
		conf2 = self.creation(id="conf2",schemaFile=self.schemaFile3,optionsFile=self.optionsFile3,dataFile=tmpfile)
		conf1.setValue(value)
		conf2.setValue(value)
		conf1.save()
		conf2.save()
		with open(tmpfile) as data_file:
			data = json.load(data_file)
		self.assertEqual(data,{"conf1":value,"conf2":value})
		os.remove(tmpfile)
		
	def test_append(self):
		value = {"keywords": [], "provider_type": "kat"}
		conf = self.creation(id="conf",schemaFile=self.schemaFile3,optionsFile=self.optionsFile3,dataFile=None)
		conf.append(value)
		conf.append(value)
		self.assertEqual(conf.getValue(),[value,value])
		
	def creation(self,id,schemaFile=None,optionsFile=None,dataFile=None):
		return JSAG3.JSAG3(id,schemaFile,optionsFile,dataFile,verbosity=DEBUG)
