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

SIMPLE_TYPES = ['string','password','choices','integer','hostname','boolean']

class jsonConfigParser(dict):
	def __init__(self,*args):
		dict.__init__(self,*args)
		self.update(definitions)
		jsonschema.Draft4Validator.check_schema(self)
		self.defPattern = 'def'
	
	def __deepcopy__(self,memo):
		newone = type(self)(dict(self))
		return newone
	
	def validate(self,json):
		jsonschema.validate(json,self)
		
	def cliCreate(self,required=False):
		#try:
			# Object
			########
			if self.getType() == 'object':
				result = {}
				properties = sorted(self['properties'].iteritems(),key=lambda k:k[1]['order'] if 'order' in k[1].keys() else 0)
				for item in properties:
					status = ''
					if 'conditions' in self.keys():
						conditions = [cond for cond in self['conditions'] if cond['then_prop'] == item[0]]
						for cond in conditions:
							if cond['if_prop'] in result.keys() and result[cond['if_prop']] in cond['if_val']:
								status = cond['then_status']
								break
					if status != 'disabled':
						item_required = (item[0] in self['required']) if 'required' in self.keys() else False
						result[item[0]] = jsonConfigParser(item[1]).cliCreate(required=item_required)
				return result
				
			# Array
			#######
			elif self.getType() == 'array':
				result = []
				while True:
					reponse = jsonConfigParser(self['items']).cliCreate()
					if not all(val is None for val in reponse.values()):
						result.append(reponse)
						if not Prompt.promptYN('Another {0}?'.format(self['title']),default='n'):
							return result
					else:
						return result
			
			# Field
			#######
			elif self.getType() in SIMPLE_TYPES:
				default = self['default'] if 'default' in self.keys() else None
				if self.getType() == 'choices':
					matchObj = re.match(r'^#/choices/(\w+)$',self['$def'],re.M)
					choices = self['choices'][matchObj.group(1)]
				else:
					choices = []
					
				warning = ''
				while True:
					if self.getType() == 'boolean':
						result = Prompt.promptYN(self['title'],default=default)
					else:
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
		
