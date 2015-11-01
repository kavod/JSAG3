#!/usr/bin/env python
#encoding:utf-8
from __future__ import unicode_literals
from __future__ import print_function

import os
import unittest
import __builtin__
import mock
import copy
import json
import tempfile
import datetime
import tzlocal
from random import randint
import JSAG

directory = os.path.dirname(os.path.realpath(__file__))
def load_expected(filename):
	with open (directory + "/expected_" + filename + ".txt", "r") as myfile:
		data=myfile.readlines()
	return [mock.call(line.replace('\n','')) for line in data]

class Test_JSAGdata(unittest.TestCase):
	def setUp(self):
		directory = os.path.dirname(os.path.abspath(__file__))
		self.schemaFilename = directory + '/../example.jschem'
		self.dataFilename = directory + '/../example.json'
		self.parser = JSAG.loadParserFromFile(self.schemaFilename)
		self.value0 = [{u"firstName": u"Dana", u"lastName": u"Scully", u"sex": u"f",u"age":randint(0,150)}]
		self.value1 = copy.deepcopy(self.value0)
		self.value2 = copy.deepcopy(self.value0)
		self.value2[0].update({"spouse":None,"married":None,"children":None,"password":None})
		self.value3 = [{u"firstName": u"Amélie", u"lastName": u"Poulain", u'married': False, u"sex": u"f",u"age":randint(0,150)}]
		
		# Insert data in file
		self.dataContent = [{"password": "donuts", "firstName": "Homer", "lastName": "Simpson", "age": 44, "married": True, "sex": "m", "spouse": {"firstName": "Marge", "weddate": "1978-05-16T12:14:05+00:00"}, "children": ["Bart", "Lisa", "The baby"]}]
		with open(self.dataFilename, 'w') as outfile:
			json.dump(self.dataContent, outfile,encoding='utf8')
	
	def validate(self):
		self.data.parser.validate(self.data.getValue())
		self.assertTrue(len(self.data.getValue())>0)
		self.assertTrue(u'sex' in self.data.getValue()[0])
		self.assertTrue(u'firstName' in self.data.getValue()[0])
		if u'married' in self.data.getValue()[0] and self.data.getValue()[0]['married']:
			self.assertGreater(len(self.data.getValue()[0]['spouse']['firstName']),0)
		else:
			self.assertFalse(u'spouse' in self.data.getValue()[0])
			self.assertFalse(u'spouse' in self.data.getValue()[0])

	def tearDown(self):
		# self.value1 must never be touched
		self.assertEqual(self.value0,self.value1)
		
	def test_creation(self):
		self.data = JSAG.JSAGdata(configParser=self.parser,value=self.value1)
		self.assertIsInstance(self.data,JSAG.JSAGdata)
		self.validate()

	def test_load(self):
		self.data = JSAG.JSAGdata(configParser=self.parser,value=[])
		self.data.load(filename=self.dataFilename)
		self.validate()

	def test_load_unexisted_file(self):
		tmpfile = unicode(tempfile.mkstemp()[1])
		os.remove(tmpfile)
		self.data = JSAG.JSAGdata(configParser=self.parser,value=[])
		with self.assertRaises(IOError):
			self.data.load(filename=tmpfile)

	def test_save(self):
		with open(self.dataFilename) as data_file:    
			data1 = json.load(data_file)
		self.test_load()
		self.data.save()
		with open(self.dataFilename) as data_file:
			data2 = json.load(data_file)
		self.assertEqual(data1,data2)
		
	def test_save_new_file(self):
		with open(self.dataFilename) as data_file:    
			data1 = json.load(data_file)
		f = tempfile.NamedTemporaryFile()
		self.test_load()
		self.data.save(f.name)
		with open(f.name) as data_file:
			data2 = json.load(data_file)
		self.assertEqual(data1,data2)
		f.close

	def test_save_with_path_list(self):
		tmpfile = unicode(tempfile.mkstemp()[1])
		with open(self.dataFilename) as f:
			with open(tmpfile,'w') as f1:
				for line in f:
					f1.write(line)
		with open(self.dataFilename) as data_file:    
			data1 = json.load(data_file)
		data1[0]['children'] = ['Bart','Lisa','Maggie']
		
		self.data = JSAG.JSAGdata(configParser=self.parser['items']['properties']['children'],value=[])
		self.data.setFilename(filename=tmpfile,path=[0,'children'])
		self.data.setValue(['Bart','Lisa','Maggie'])
		self.data.save()
		
	def test_save_with_path_dict(self):
		tmpfile = unicode(tempfile.mkstemp()[1])
		with open(self.dataFilename) as f:
			with open(tmpfile,'w') as f1:
				for line in f:
					f1.write(line)
		with open(self.dataFilename) as data_file:    
			data1 = json.load(data_file)
		new_wedday = datetime.datetime.now(tzlocal.get_localzone())-datetime.timedelta(hours=-12) #"last night, after Moe"
		data1[0]['spouse'] = {"firstName": "Karl", "weddate": new_wedday.isoformat()} 
		
		self.data = JSAG.JSAGdata(configParser=self.parser['items']['properties']['spouse'],value={},commit=False)
		self.data.setFilename(filename=tmpfile,path=[0,'spouse'])
		self.data.setValue({"firstName": "Karl", "weddate": new_wedday.isoformat()})
		self.data.save()
		
	def test_save_newfile_with_path_list(self):
		tmpfile = unicode(tempfile.mkstemp()[1])
		
		self.data = JSAG.JSAGdata(configParser=self.parser['items'],value={},commit=False)
		self.data.setFilename(filename=tmpfile,path=[0])
		self.data.setValue(self.value3[0])
		self.data.save()
		
		with open(tmpfile) as data_file:
			data2 = json.load(data_file)
		self.assertEqual(self.value3,data2)
		os.remove(tmpfile)
		
	def test_save_newfile_with_path_dict(self):
		tmpfile = unicode(tempfile.mkstemp()[1])
		
		self.data = JSAG.JSAGdata(configParser=self.parser['items'],value={},commit=False)
		self.data.setFilename(filename=tmpfile,path=['choosenOne'])
		self.data.setValue(self.value3[0])
		self.data.save()
		
		with open(tmpfile) as data_file:
			data2 = json.load(data_file)
		self.assertEqual({'choosenOne':self.value3[0]},data2)
		os.remove(tmpfile)

	# load array element
	def test_load_with_path(self):
		self.parser = JSAG.loadParserFromFile(self.schemaFilename,path=['items'])
		self.data = JSAG.JSAGdata(configParser=self.parser,value={},commit=False)
		self.data.setFilename(filename=self.dataFilename,path=[0])
		self.data.load()
		self.assertIsInstance(self.data.getValue(),dict)

	# load simple element
	def test_load_with_path1(self):
		self.parser = JSAG.loadParserFromFile(self.schemaFilename,path=['items','properties','sex'])
		self.data = JSAG.JSAGdata(configParser=self.parser,value=[])
		self.data.setFilename(filename=self.dataFilename,path=[0,u'sex'])
		self.data.load()
		self.assertIsInstance(self.data.getValue(),unicode)
	
	def test_save_with_path(self):
		# load array element
		with open(self.dataFilename) as data_file:    
			data1 = json.load(data_file)
		self.test_load_with_path()
		self.data.save()
		with open(self.dataFilename) as data_file:    
			data2 = json.load(data_file)
		self.assertEqual(data1,data2)
		
		# load simple element
		with open(self.dataFilename) as data_file:    
			data1 = json.load(data_file)
		self.test_load_with_path1()
		self.data.save()
		with open(self.dataFilename) as data_file:    
			data2 = json.load(data_file)
		self.assertEqual(data1,data2)
			
	def test_getValue(self):
		self.test_creation()
		value = copy.deepcopy(self.value1)
		value[0].update({'married':False})
		self.assertEqual(self.data.getValue(hidePasswords=False),value)
		self.assertEqual(self.data[0].getValue(hidePasswords=False),value[0])
		self.assertEqual(self.data[0]['sex'].getValue(hidePasswords=False),value[0][u'sex'])
			
	def test_getValue_unicode(self):
		self.data = JSAG.JSAGdata(configParser=self.parser,value=self.value3)
		self.assertIsInstance(self.data,JSAG.JSAGdata)
		self.validate()
		value = copy.deepcopy(self.value3)
		self.assertEqual(self.data.getValue(hidePasswords=False),value)
		self.assertEqual(self.data[0].getValue(hidePasswords=False),value[0])
		self.assertEqual(self.data[0]['firstName'].getValue(hidePasswords=False),value[0][u'firstName'])

	def test_setValue(self):
		self.test_load()
		self.data.setValue(self.value1)
		self.validate()
		
	def test_setValue_with_empty_array(self):
		self.test_load()
		self.data.setValue([])
		self.data.parser.validate(self.data.getValue())
		
	def test_setValue_with_none_values(self):
		self.test_load()
		self.data.setValue(self.value1)
		data1 = self.data.getValue()
		self.data.setValue(self.value2)
		self.validate()
		data2 = self.data.getValue()
		self.assertEqual(data1,data2)
		
	def test_setValue_unicode(self):
		self.test_load()
		self.data.setValue(self.value3)
		self.validate()
		
	def test_setValue_simple_with_none(self):
		data = copy.deepcopy(self.dataContent)
		data[0].pop('children',None)
		self.test_load()
		del(self.data[0]['children'])
		self.validate()
		self.assertEqual(data,self.data.getValue(hidePasswords=False))
		
	def test_setValue_simple_with_none_on_required(self):
		self.test_load()
		with self.assertRaises(Exception):
			del(self.data[0]['firstName'])
		self.data.rollback()
		self.validate()
		self.assertEqual(self.dataContent,self.data.getValue(hidePasswords=False))
		
	def test_setValue_simple_with_path(self):
		data = copy.deepcopy(self.dataContent)
		data[0]['firstName'] = 'Doooh'
		self.test_load()
		self.data[0]['firstName'].setValue(data[0]['firstName'])
		self.validate()
		self.assertEqual(data,self.data.getValue(hidePasswords=False))
		
	def test_setValue_object_with_path(self):
		data = copy.deepcopy(self.dataContent)
		data1 = copy.deepcopy(self.dataContent)
		new_wedday = datetime.datetime.now(tzlocal.get_localzone()) #just married!
		data[0]['spouse'] = {"firstName": "Edna", "weddate": new_wedday}
		data1[0]['spouse'] = {"firstName": "Edna", "weddate": new_wedday.isoformat()}
		self.test_load()
		self.data[0]['spouse'].setValue(data[0]['spouse'])
		self.validate()
		self.assertEqual(data1,self.data.getValue(hidePasswords=False))
		
	def test_setValue_array_with_path(self):
		data = copy.deepcopy(self.dataContent)
		data[0]['children'] = ['Bart','Lisa','Maggy']
		self.test_load()
		self.data[0]['children'].setValue(data[0]['children'])
		self.validate()
		self.assertEqual(data,self.data.getValue(hidePasswords=False))
		
	def test_insert(self):
		self.test_load()
		data = self.data[0].getValue(hidePasswords=False)
		self.data.insert(0,self.value3[0])
		self.validate()
		self.assertEqual(self.data.getValue(hidePasswords=False),[self.value3[0],data])
		
	def test_insert_empty(self):
		self.data = JSAG.JSAGdata(configParser=self.parser,value=[])
		self.data.insert(0,self.value3[0])
		self.validate()
		self.assertEqual(self.data.getValue(hidePasswords=False),[self.value3[0]])
		
	def test_append(self):
		self.test_load()
		data = self.data[0].getValue(hidePasswords=False)
		self.data.append(self.value3[0])
		self.validate()
		self.assertEqual(self.data.getValue(hidePasswords=False),[data,self.value3[0]])
		
	def test_display(self):
		self.test_load()
		self.data.display()
		
	def test_len(self):
		self.test_load()
		self.assertEqual(len(self.data),1)
		
	def test_len_0(self):
		self.data = JSAG.JSAGdata(configParser=self.parser,value={})
		self.assertEqual(len(self.data),0)
		self.data = JSAG.JSAGdata(configParser=self.parser,value=[])
		self.assertEqual(len(self.data),0)
	
	def test_getitem(self):
		self.data = JSAG.JSAGdata(configParser=self.parser,value=self.value1)
		self.assertIsInstance(self.data[0],JSAG.JSAGdata)
		self.assertIsInstance(self.data[0]['firstName'],JSAG.JSAGdata)
		
	def test_setitem_dict(self):
		self.data = JSAG.JSAGdata(configParser=self.parser,value=self.value1)
		self.assertEqual(len(self.data),1)
		self.data.append(self.value3[0])
		self.assertIsInstance(self.data,JSAG.JSAGdata)
		self.assertEqual(len(self.data),2)
		self.assertIsInstance(self.data[1],JSAG.JSAGdata)
		self.validate()

	def test_setitem_JSAGdata(self):
		self.data = JSAG.JSAGdata(configParser=self.parser,value=self.value1)
		self.data1 = JSAG.JSAGdata(configParser=self.parser['items'],value=self.value3[0])
		self.assertEqual(len(self.data),1)
		self.data.append(self.data[0])
		self.assertIsInstance(self.data,JSAG.JSAGdata)
		self.assertEqual(self.data[1]['lastName'].getValue(),'Scully')
		self.assertEqual(len(self.data),2)
		self.data[1] = self.data1
		self.assertIsInstance(self.data[0],JSAG.JSAGdata)
		self.assertIsInstance(self.data[1],JSAG.JSAGdata)
		self.assertEqual(self.data[1]['lastName'].getValue(),'Poulain')
		self.validate()
		
	@mock.patch("__builtin__.raw_input",create=True,side_effect=[])
	@mock.patch("__builtin__.print",create=True)
	def test_display2(self,myMockPrint,mock_input):
		expected = load_expected('display2')
		parser = JSAG.loadParserFromFile(os.path.dirname(os.path.abspath(__file__))+ '/../example.jschem')
		data = JSAG.JSAGdata(configParser=parser,value=[{u"firstName": u"Dana",u"lastName": u"Scully", u"sex": u"f",u"age":40}])
		data.load(os.path.dirname(os.path.abspath(__file__))+'/../example.json')
		reponse = data.display2()
		self.assertEqual(reponse,None)
		for key,line in enumerate(expected):
			self.assertEqual(myMockPrint.mock_calls[key],line)
		self.assertEqual(len(expected),len(myMockPrint.mock_calls))
		
	# Interactive methods
	"""def test_cliCreate(self):
		self.test_load()
		self.data.cliCreate()
		self.validate()
		
	def test_cliChange(self):
		self.test_load()
		self.data.cliCreate()
		self.validate()
		
	def test_proposeSave(self):
		with open(self.dataFilename) as data_file:    
			data1 = json.load(data_file)
		self.test_load()
		self.data.proposeSave()
		with open(self.dataFilename) as data_file:
			data2 = json.load(data_file)
		self.assertEqual(data1,data2)"""
