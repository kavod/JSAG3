#!/usr/bin/env python
#encoding:utf-8
from __future__ import unicode_literals

import os
import json
import logging
import cherrypy
import jsonschema
from functions import updateData, hidePasswords
from cherrypyClasses import staticData, staticJsonFile, staticJsonString, Root

class JSAG3(object):
	def __init__(self,id,schemaFile=None,optionsFile=None,dataFile=None,verbosity=False):
		logger = logging.getLogger()
		if verbosity:
			logger.setLevel(logging.DEBUG)
		logging.debug("[JSAG3] Verbosity is set to {0}".format(unicode(verbosity)))
			
		logging.debug("[JSAG3] Creation of JSAG3 with id '{0}'".format(unicode(id)))
		if not isinstance(id, basestring):
			raise Exception("id must be str or unicode. {0} received".format(type(id)))
		
		self.local_dir = os.path.abspath(os.getcwd())
		self.conf = {
			"/data".encode('utf8'): {
				'tools.caching.on': False
			}
		}
		self.root = Root()
		self.root.schema = Root()
		self.root.options = Root()
		self.root.data = Root()
		
		self.id = id
		self.schemaFile = None
		self.schema = None
		self.optionsFile = None
		self.options = {}
		self.dataFile = None
		self.data = None
		
		setattr(self.root.options,self.id.encode('utf8'),staticJsonString({}))
		self.addFile(schemaFile=schemaFile,optionsFile=optionsFile,dataFile=dataFile)
			
	def addFile(self,schemaFile=None,optionsFile=None,dataFile=None):
		if schemaFile is not None:
			self.addSchema(schemaFile)
		if optionsFile is not None:
			self.addOptions(optionsFile)
		if dataFile is not None:
			self.addData(dataFile)
			
	def addSchema(self,schemaFile):
		logging.debug("[JSAG3] Add schema {0}".format(unicode(schemaFile)))
		self.schemaFile = schemaFile
		with open(self.schemaFile) as data_file:
			content = data_file.read()   
			logging.debug("[JSAG3] Schema content: \n{0}".format(unicode(content)))
			self.schema = json.loads(content)
		setattr(self.root.schema,self.id.encode('utf8'),staticJsonFile(schemaFile))
		
	def addOptions(self,optionsFile):
		if self.schema is None:
			raise Exception("Schema has not been provided")
		self.optionsFile = optionsFile
		with open(self.optionsFile) as data_file:    
			self.options = json.load(data_file)
		setattr(self.root.options,self.id.encode('utf8'),staticJsonFile(optionsFile))
		
	def addData(self,dataFile):
		if self.schema is None:
			raise Exception("Schema has not been provided")
		self.dataFile = dataFile
		if os.path.isfile(self.dataFile):
			with open(self.dataFile) as data_file:    
				self.data = json.load(data_file)
		else:
			self.createEmpty()
		setattr(self.root.data,self.id.encode('utf8'),staticData(self.dataFile,self.schemaFile))
		
	def checkCompleted(self):
		if self.schema is None:
			raise Exception("Schema has not been provided")
		if self.dataFile is None:
			raise Exception("Datafile has not been provided")
			
	def createEmpty(self):
		self.checkCompleted()
		if 'type' in self.schema.keys() and self.schema['type'] == 'object':
			self.data = {}
		elif 'type' in self.schema.keys() and self.schema['type'] == 'array':
			self.data = []
		else:
			self.data = None
		with open(self.dataFile, 'w') as outfile:
			json.dump(self.data, outfile)
		
	def getConf(self,conf={}):
		self.checkCompleted()
		x = conf.copy()
		x.update(self.conf)
		return x
		
	def getRoot(self,root=None):
		self.checkCompleted()
		if root is None:
			root = self.root
		else:
			if not hasattr(root, 'schema'):
				root.schema = Root()
			if not hasattr(root, 'options'):
				root.options = Root()
			if not hasattr(root, 'data'):
				root.data = Root()
			setattr(root.schema,self.id.encode('utf8'),getattr(self.root.schema,self.id.encode('utf8')))
			setattr(root.options,self.id.encode('utf8'),getattr(self.root.options,self.id.encode('utf8')))
			setattr(root.data,self.id.encode('utf8'),getattr(self.root.data,self.id.encode('utf8')))		
		return root
		
	def updateData(self,newData):
		self.checkCompleted()
		newData = updateData(self.data,newData,self.schema)
		self.isValid(newData)
		self.data = newData
		self.save()
		
	def save(self):
		self.checkCompleted()
		self.isValid()
		with open(self.dataFile, 'w') as outfile:
			json.dump(self.data, outfile)
		
	def __repr__(self):
		return "JSAG3(schema={0},options={1},dataFile=None,data=None)".encode('utf8').format(self.schema,self.options,self.dataFile,self.data)
		
	def __str__(self):
		return unicode(self.data).encode('utf8')
		
	def __getitem__(self,key):
		self.checkCompleted()
		if self.data is None:
			raise IndexError
		if 'type' in self.schema.keys() and self.schema['type'] == 'object':
			if key not in self.data.keys():
				raise IndexError("key not found")
			return self.data[key]
		elif 'type' in self.schema.keys() and self.schema['type'] == 'array':
			if isinstance(key,int):
				if key >= len(self.data):
					raise IndexError("array is not long enough")
				return self.data[key]
			else:
				raise IndexError("key must be integer")
		else:
			raise TypeError("value is not object nor list")
	
	def _checkitem(self,key):
		self.checkCompleted()
		if self.data is None:
			raise IndexError
		if 'type' in self.schema.keys() and self.schema['type'] == 'object':
			if key not in self.data.keys():
				raise IndexError
		elif 'type' in self.schema.keys() and self.schema['type'] == 'array':
			if isinstance(key,int):
				if key >= len(self.data):
					raise IndexError
			else:
				raise IndexError("key must be integer")
		else:
			raise TypeError("value is not object nor list")
			
	def __setitem__(self,key,value):
		self._checkitem(key)
		self.data[key] = value
		
	def __delitem__(self,key):
		self._checkitem(key)
		del(self.data[key])
		
	def __len__(self):
		self.checkCompleted()
		if 'type' in self.schema.keys() and self.schema['type'] == 'array':
			if self.data is None:
				return 0
			return len(self.data)
		elif 'type' in self.schema.keys() and self.schema['type'] == 'object':
			if self.data is None:
				return 0
			return len(self.keys())
		else:
			raise TypeError("JSAG3 with type {0} has no len()".format(self.configParser.getType()))

	def keys(self):
		self.checkCompleted()
		if self.data is None:
			return []
		elif 'type' in self.schema.keys() and self.schema['type'] == 'array':
			return range(0,len(self.data))
		return self.data.keys()
		
	def getType(self):
		self.checkCompleted()
		if 'type' in self.schema.keys():
			return self.schema['type']
		else:
			return ''
			
	def insert(self,i,x):
		if self.getType() != 'array':
			raise Exception("Insert can only be used on array data")
		y = copy.deepcopy(x)
		self.data.insert(i,y)
		
	def append(self,x):
		self.insert(len(self),x)
		
	def setValue(self,value):
		self.data = value
		
	def isValid(self,data=None):
		self.checkCompleted()
		if data is None:
			data = self.data
		jsonschema.validate(data,self.schema,format_checker=jsonschema.FormatChecker())
		return True
