#!/usr/bin/env python
#encoding:utf-8

import sys
import json
import jsonschema
import getpass
import re
import Prompt

definitions =  {
	"$schema": "http://json-schema.org/draft-04/schema#",
    "additionalProperties": False,
	"def":{
		"password": {
			"type":"string"
		},
		"file": {
			"type":"string"
		},
	}
}

class jsonConfigParser(dict):
	def __init__(self,*args):
		dict.__init__(self,*args)
		self.update(definitions)
		if 'choices' not in self.keys():
			self.update({'choices':{}})
		jsonschema.Draft4Validator.check_schema(self)
		self.defPattern = 'def'
	
	def __deepcopy__(self,memo):
		newone = type(self)(dict(self))
		return newone
	
	def validate(self,json):
		jsonschema.validate(json,self)
		
	def cliCreate(self,required=False):
		#try:
			if self.getType() == 'object':
				result = {}
				properties = sorted(self['properties'].iteritems(),key=lambda k:k[1]['order'] if 'order' in k[1].keys() else 0)
				for item in properties:
					item_required = (item[0] in self['required']) if 'required' in self.keys() else False
					item[1].update({"choices":self['choices']})
					result[item[0]] = jsonConfigParser(item[1]).cliCreate(required=item_required)
				return result
			elif self.getType() == 'array':
				result = []
				while True:
					self['items'].update({"choices":self['choices']})
					reponse = jsonConfigParser(self['items']).cliCreate()
					if reponse != '':
						result.append(reponse)
						if not Prompt.promptYN('Another {0}?'.format(self['title']),default='n'):
							return result
					else:
						return result
			elif self.getType() == 'string' or self.getType() == 'password' or self.getType() == 'choices' 	or self.getType() == 'integer' or self.getType() == 'hostname':
				default = self['default'] if 'default' in self.keys() else None
				if self.getType() == 'choices':
					matchObj = re.match(r'^#/choices/(\w+)$',self['$def'],re.M)
					choices = self['choices'][matchObj.group(1)]
				else:
					choices = []
					
				warning = ''
				while True:
					result = Prompt.promptSingle(
								self['title'],
								choix=choices,
								password=(self.getType() == 'password'),
								mandatory=required,
								default=default,
								warning=warning
								)
					if result == "" or result is None:
						return default
					try:
						result = self.convert(result)
						self.validate(result)
						return result
					except:
						warning='Incorrect answer'
			else:
				raise Exception
			"""except:
				print "Unknown"
				print self
				sys.exit()"""
				
	def getType(self):
		if 'type' in self.keys():
			return self['type']
		elif '$def' in self.keys():
			matchObj = re.match(r'^#/{0}/(\w+)$'.format(self.defPattern),self['$def'],re.M)
			if matchObj:
				return matchObj.group(1)
			matchObj = re.match(r'^#/choices/(\w+)$',self['$def'],re.M)
			if matchObj:
				return 'choices'
		return ''
		
	def convert(self,value):
		if self.getType() == "integer":
			return int(value)
		return value
			
		
class jsonConfigValue(dict):
	def __init__(self,configParser,value=None):
		if isinstance(configParser,jsonConfigParser):
			self.configParser = configParser
		elif isinstance(configParser,dict):
			self.configParser = jsonConfigParser(configParser)
		else:
			raise TypeError("First argument must be a jsonConfigParser instance")

		if value is None:
			self = {}
		else:
			self.configParser.validate(value)
			self = value
		
