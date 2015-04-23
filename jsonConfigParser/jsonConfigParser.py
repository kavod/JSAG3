#!/usr/bin/env python
#encoding:utf-8

import sys
import json
import jsonschema
import getpass

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
		jsonschema.Draft4Validator.check_schema(self)
	
	def __deepcopy__(self,memo):
		newone = type(self)(dict(self))
		return newone
	
	def validate(self,json):
		jsonschema.validate(json,self)
		
	def cliCreate(self):
		#try:
			if 'type' in self.keys() and self['type'] == 'object':
				result = {}
				properties = sorted(self['properties'].iteritems(),key=lambda k:k['order'])
				for item in properties:
					result[item] = jsonConfigParser(properties[item]).cliCreate()
				return result
			elif 'type' in self.keys() and  self['type'] == 'array':
				result = []
				while True:
					result.append(jsonConfigParser(self['items']).cliCreate())
					print "Another?"
					reponse = raw_input()
					if reponse == 'N':
						return result
			elif 'type' in self.keys() and  self['type'] == 'string':
				print self['title']
				result = raw_input()
				if result == '':
					return None
				return result
			elif '$def' in self.keys() and  self['$def'] == '#/def/password':
				print self['title']
				return getpass.getpass()
			else:
				raise Exception
			"""except:
				print "Unknown"
				print self
				sys.exit()"""
			
		
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
