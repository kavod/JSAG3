#!/usr/bin/env python
#encoding:utf-8
from __future__ import unicode_literals

import datetime
from codecs import open
from JSAGparser import *

def fusion(initial,path,data):
	if len(path)==0:
		initial = data
	else:
		if len(path)>0:
			level = path.pop(0)
			#dict
			if isinstance(initial,dict) and level in initial.keys():
				initial[level] = fusion(initial[level],path,data)
			elif isinstance(initial,dict):
				initial[level] = fusion({},path,data)
			#list
			elif isinstance(initial,list) and not isinstance(level,int):
				raise Exception("invalid key: {0}. Int expected")
			elif isinstance(initial,list) and len(initial)>level:
				initial[level] = fusion(initial[level],path,data)
			elif isinstance(initial,list) and len(initial) == level:
				initial.append(fusion({},path,data))
			#other????
			else:
				raise Exception("unexpected case")
	return initial

class JSAGdata(object):
	def __init__(self,configParser=None,value=None,commit=True):
		
		self.parser = None
		self.data = None
		self.commited = False
		self.filename = None
		self.path = []
		self.commitedData = None
	
		if isinstance(configParser,JSAGparser):
			self.parser = configParser
		elif isinstance(configParser,dict):
			self.parser = JSAGparser(configParser)
		else:
			raise TypeError("configParser argument is mandatory and must be a JSAGparser instance")

		if value is None or unicode(value) == '':
			if 'default' in self.parser.keys():
				value = self.parser['default']
			else:
				value = None
		
		self.setValue(value,commit=commit)
		
	def __getitem__(self,key):
		if self.data is None:
			raise IndexError
		if self.parser.getType() == 'object':
			if key not in self.data.keys():
				raise IndexError
			return self.data[key]
		elif self.parser.getType() == 'array':
			if key >= len(self.data):
				raise IndexError
			return self.data[key]
		else:
			raise TypeError("value is not object nor list")
			
	def __setitem__(self,key,value):
		if self.data is None:
			raise IndexError
		if self.parser.getType() == 'object':
			if key not in self.data.keys():
				raise IndexError
		elif self.parser.getType() == 'array':
			if key >= len(self.data):
				raise IndexError
		else:
			raise TypeError("value is not object nor list")
			
		self.data[key].setValue(value,commit=True)
		
	def __delitem__(self,key):
		if self.data is None:
			raise IndexError
		if self.parser.getType() == 'object':
			if key not in self.data.keys():
				raise IndexError
		elif self.parser.getType() == 'array':
			if key >= len(self.data):
				raise IndexError
		else:
			raise TypeError("value is not object nor list")
		del(self.data[key])
		self.commit()		
		
	def __len__(self):
		if self.parser.getType() == 'array':
			if self.data is None:
				return 0
			return len(self.data)
		elif self.parser.getType() == 'object':
			if self.data is None:
				return 0
			return len(self.keys())
		else:
			raise TypeError("JSAGdata with type {0} has no len()".format(self.configParser.getType()))
		
	def keys(self):
		if self.data is None:
			return []
		elif self.parser.getType() == 'array':
			return range(0,len(self.data))
		return self.data.keys()
		
	def insert(self,i,x):
		if self.parser.getType() != 'array':
			raise Exception("Insert can only be used on array data")
		y = copy.deepcopy(x)
		if not isinstance(y,JSAGdata):
			y = JSAGdata(configParser=self.parser['items'],value=y)
		self.data.insert(i,y)
		self.commit()
		
	def append(self,x):
		self.insert(len(self),x)
	
	def setValue(self,src_value,commit=True):
		value = copy.deepcopy(src_value)
		value = self.parser._convert(value)
		
		if self.parser.getType() in SIMPLE_TYPES:
			self.data = value
		elif self.parser.getType() == 'object':
			if value is None:
				self.data = None
			else:
				self.data = {}
				for key in value.keys():
					if key in self.parser['properties']:
						self.data[key] = JSAGdata(configParser=self.parser['properties'][key],value=value[key])
					else:
						raise Exception("{0} is not a properties of {1}".format(self.parser['title']))
		elif self.parser.getType() == 'array':
			if value is None:
				self.data = None
			else:
				self.data = []
				for item in value:
					self.data.append(JSAGdata(configParser=self.parser['items'],value=item))
		self.commited = False
		if commit:
			self.commit()
			
	def getValue(self,hidePasswords=True):
		if self.parser.getType() == 'password' and hidePasswords:
			if self.data is None:
				return None
			return '****'
		if self.parser.getType() in SIMPLE_TYPES:
			return self.data
		elif self.parser.getType() == 'object':
			result = {}
			if self.data is None:
				return None
			for key in self.data.keys():
				result[key] = self.data[key].getValue(hidePasswords=hidePasswords)
			return result
		elif self.parser.getType() == 'array':
			if self.data is None:
				return None
			return [item.getValue(hidePasswords=hidePasswords) for item in self.data]
			
	def commit(self):
		self.parser.validate(self.getValue())
		del(self.commitedData)
		self.commitedData = copy.deepcopy(self.data)
		self.commited = True
		
	def rollback(self):
		del(self.data)
		self.data = copy.deepcopy(self.commitedData)
			
	def setFilename(self,filename=None,path=[]):
		if filename is None:
			self.filename = None
			return
		if not isinstance(filename,str) and not isinstance(filename,unicode):
			raise TypeError("Filename must be a string. {0} entered".format(unicode(filename)))
		if not isinstance(path,list):
			raise TypeError("path parameter must be a list")
		self.filename = filename
		self.path = path
		
	def load(self,filename=None,path=[]):
		if filename is not None:
			self.setFilename(filename,path)
		if self.filename is None:
			raise Exception("No file specified")
		if not os.path.isfile(self.filename):
			raise IOError("File {0} does not exists".format(self.filename))
		try:
			with open(self.filename,encoding='utf8') as data_file:
				data = json.load(data_file)
		except:
			raise Exception("Unable to read file {0}".format(unicode(self.filename)))
		try:
			path = list(self.path)
			while len(path)>0:
				data = data[path.pop(0)]
		except:
			raise Exception("path cannot be reached: " + unicode(path))
		self.setValue(data,commit=True)
	
	def save(self,filename=None,path=[]):
		if not self.commited:
			raise Exception("Data not commited")
		if filename is not None:
			self.setFilename(filename,path)
		if self.filename is None:
			raise Exception("No file specified")
		path = list(self.path)
		try:
			with open(self.filename,encoding='utf8') as data_file:
				existingData = json.load(data_file)
		except:
			# File not exists yet
			if len(path)>0:
				if isinstance(path[0],int):
					existingData = []
				else:
					existingData = {}
			else:
				existingData = {}
		
		existingData = fusion(existingData,path,self.getValue(hidePasswords=False))
		try:
			with open(self.filename, 'w') as outfile:
				json.dump(existingData, outfile,encoding='utf8') #self.value
		except:
			raise Exception("Unable to write file {0}".format(unicode(self.filename)))
