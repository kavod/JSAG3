#!/usr/bin/env python
#encoding:utf-8
from __future__ import unicode_literals

import os
import sys
import json
import datetime
import dateutil.parser
import jsonschema
import getpass
import re
import copy
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
		"hidden": {
			"type":"string"
		},
	},
}

SIMPLE_TYPES = ['string','password','choices','integer','hostname','boolean','file','email','hidden','date-time']

def loadParserFromFile(filename,path=[]):
	if not isinstance(filename,str) and not isinstance(filename,unicode):
		raise TypeError("Filename must be a string. {0} entered".format(unicode(filename)))
	try:
		with open(filename) as data_file:    
			confschema = json.load(data_file)
	except:
		raise Exception("Cannot parse {0}".format(unicode(filename)))
	while len(path)>0:
		confschema = confschema[path.pop(0)]
	return JSAGparser(confschema)
	
class JSAGparser(dict):
	def __init__(self,*args):
		self.defPattern = 'def'
		dict.__init__(self,*args)
		if self.getType() == 'object' and 'properties' in self.keys():
			for item in self['properties'].iteritems():
				newitem = dict(item[1])
				newitem.update(definitions)
				self['properties'][item[0]] = JSAGparser(newitem)
		elif self.getType() == 'array' and 'items' in self.keys():
			newitem = dict(self['items'])
			newitem.update(definitions)
			self['items'] = JSAGparser(newitem)
				
		self.update(definitions)
		jsonschema.Draft4Validator.check_schema(self)
	
	def __deepcopy__(self,memo):
		newone = type(self)(dict(self))
		return newone
	
	def validate(self,json):
		jsonschema.validate(json,self,format_checker=jsonschema.FormatChecker())
		
	def cliCreate(self,required=False,inList=False):
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
						if ( ( cond['if_prop'] in result.keys() and result[cond['if_prop']] in cond['if_val']) or
								( cond['if_prop'] not in result.keys() and None in cond['if_val'] ) ):
							status = cond['then_status']
							break
				if status != 'disabled':
					item_required = (item[0] in self['required']) if 'required' in self.keys() else False
					pre_result = item[1].cliCreate(required=item_required)
					if pre_result is not None:
						result[item[0]] = pre_result
			return result
			
		# Array
		#######
		elif self.getType() == 'array':
			result = []
			while True:
				reponse = self['items'].cliCreate(inList=True)
				if self['items'].getType() in SIMPLE_TYPES:
					if reponse is not None:
						result.append(reponse)
					else:
						return result
				elif self['items'].getType() == 'object':
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
				default = [item[0] for item in enumerate(self['choices']) if items[1] == default] if default is not None else None
			else:
				choices = {}
				
			warning = ''
			while True:
				description = self['placeholder'] if 'placeholder' in self.keys() else self['description'] if 'description' in self.keys() else self['title']
				if inList:
					description += ' [keep blank to finish]'
				if self.getType() == 'boolean':
					result = Prompt.promptYN(self['title'],default=default)
				else:
					result = Prompt.promptSingle(
								description,
								choix=choices.values(),
								password=(self.getType() == 'password'),
								mandatory=required,
								default=default,
								warning=warning
								)
				if result == "" or result is None:
					return default
				if self.getType() == 'choices':
					result = choices.keys()[result]
				try:
					result = self._convert(result)
					if result is None:
						if required:
							raise Exception
					else:
						self.validate(result)
					return result
				except:
					warning='Incorrect answer, {0} expected'.format(self.getType())
		elif self.getType() == 'hidden':
			return self['default']
		else:
			raise Exception
				
	def cliChange(self,json):
		self.validate(json)
		# Object
		########
		if self.getType() == 'object':
			choices = []
			width = len(max([i['title'] for i in self['properties'].values()], key=len))
			properties = sorted(self['properties'].iteritems(),key=lambda k:k[1]['order'] if 'order' in k[1].keys() else 0)
			for key,item in properties:
				if item.getType() in SIMPLE_TYPES:
					line = item.display(json[key],width=width,ident='')
				elif item.getType() == 'array':
					item_count = unicode(len(json[key])) if key in json.keys() else "0"
					value = '{0} managed'.format(item_count)
					line = ("{0:" + unicode(width)+"} - {1}").format(item['title'],value)
				elif item.getType() == 'hidden':
					continue
				else:
					value = 'Managed'
					line = ("{0:" + unicode(width)+"} - {1}").format(item['title'],value)
				choices.append(line)
			reponse = Prompt.promptChoice(unicode(self['title']),choices,warning='',selected=[],default = None,mandatory=True,multi=False)
		
			changed_item = properties[reponse][1]
			result = changed_item.cliChange(json[properties[reponse][0]])
			json.update({properties[reponse][0]:result})
			return json

		# array
		########
		elif self.getType() == 'array':
			lines = self.display(json)
			warning = '\n'.join(lines)
			choices = ['Add','Delete','Reset all']
			reponse = Prompt.promptChoice('** Managed {0}'.format(self['title']),choices,warning=warning,selected=[],default = None,mandatory=True,multi=False)
			if reponse == 0: # Add
				element = self['items'].cliCreate()
				if element is not None:
					json.append(element)
				return json
			elif reponse == 1: # Delete
				result = Prompt.promptSingle(
						'Which {0} must be deleted?'.format(self['items']['title']),
						choix=[self['items'].display(item) for item in json],
						password=False,
						mandatory=True,
						default=None,
						warning=''
						)
				del json[result]
				return json
			elif reponse == 2: # Reset all
				del json
				return []
		# Field
		########
		elif self.getType() in SIMPLE_TYPES:
			result = self.cliCreate()
			Prompt.print_question(self['title'] + ' changed!')
			return result
		
		# Hidden
		#########
		elif self.getType() == 'hidden':
			return self['default']
				
	def display(self,json,width=None,ident=' '):
		# object
		########
		if self.getType() == 'object':
			lines = []
			lines.append(unicode(ident)+'| \033[1m{0}\033[0m'.format(self['title']))
			lines.append(unicode(ident)+('-'*(len(self['title'])+2)))
			if width is None:
				width = len(max([item['title'] for item in self['properties'].values()],key=len))
			for key,item in sorted(self['properties'].items(),key=lambda k:k[1]['order']):
				if key in json.keys():
					lines.append(unicode(ident)+' '+item.display(json[key],width=width,ident=unicode(ident)+' '))
			lines = '\n'.join(lines)
			return lines
		# array
		########
		if self.getType() == 'array':
			lines = []
			for key,item in enumerate(json):
				lines.append(unicode(ident)+'| \033[1m{0} {1}\033[0m'.format(self['items']['title'],unicode(key+1)))
				lines.append(unicode(ident)+'-'*(len(self['title'])+4))
				if width is None:
					width = len(max([prop['title'] for prop in self['items']['properties'].values()],key=len))
				for prop in sorted(self['items']['properties'].items(),key=lambda k:k[1]['order']):
					if prop[1].getType() in SIMPLE_TYPES:
						val = item[prop[0]] if prop[0] in item else None
						lines.append(prop[1].display(val,width=width,ident=unicode(ident)+unicode(' ')))
					elif prop[1].getType() == 'array':
						value = '{0} managed'.format(unicode(len(item[prop[0]])))
						line = ("{0} {1:" + unicode(width)+"} - {2}").format(unicode(ident),prop[1]['title'],value)
						lines.append(line)
					elif prop[1].getType() == 'hidden':
						continue
					else:
						if prop[0] in item.keys():
							lines.append(prop[1].display(item[prop[0]],width=width,ident=unicode(ident)+unicode(' ')))
				lines.append('')
			return lines
		# Field
		########
		elif self.getType() in SIMPLE_TYPES:
			value = json if self.getType() != 'password' else '****'
			return ("{0}{1:" + unicode(width)+"} - {2}").format(unicode(ident),self['title'],value)
			
		# Hidden
		#########
		elif self.getType() == 'hidden':
			return ''
			
		else:
			raise Exception(self.getType())
			
				
	def getType(self,path=[]):
		configParser = self
		if len(path) > 0:
			for level in path:
				if isinstance(level,int):
					configParser = configParser['items']
				else:
					configParser = configParser['properties'][level]
		if '$def' in configParser.keys():
			matchObj = re.match(r'^#/{0}/(\w+)$'.format(self.defPattern),configParser['$def'],re.M)
			if matchObj:
				return matchObj.group(1)
			matchObj = re.match(r'^#/choices/(\w+)$',configParser['$def'],re.M)
			if matchObj:
				return 'choices'
		elif 'format' in configParser.keys():
			return self['format']
		elif 'type' in configParser.keys():
			return self['type']
		return ''
		
	def _convert(self,value):
		if (value is None or value == "") and 'default' in self.keys():
			return self['default']
			
		if value is None: # or value == "":
			return None
		elif self.getType() == "integer":
			"""if value is None: or value == "":
				return None"""
			return int(value)
		elif self.getType() == 'date-time':
			"""if value is None or value == "":
				return None"""
			if isinstance(value,datetime.datetime):
				return unicode(value.isoformat())
			else:
				try:
					strdate = dateutil.parser.parse(value).isoformat()
				except:
					raise ValueError("unknown string format: {0}".format(value))
				return unicode(strdate)
				
		elif self.getType() == "object":
			if not isinstance(value,dict):
				raise TypeError("Dict instance expected, {0} received instead".format(type(value)))
			result = {}
			for prop in self['properties'].keys():
				if prop not in value.keys():
					value[prop] = None
			for prop in value.keys():
				if prop in self['properties'].keys():
					element = self['properties'][prop]._convert(value[prop])
					if element is not None:
						result[prop] = element
				else:
					raise("Unknown key: " + unicode(prop))
			"""if result == {}:
				return None"""
			return result
		elif self.getType() == "array":
			result = []
			for prop in value:
				element = self['items']._convert(prop)
				if element is not None:
					result.append(element)
			"""if len(result)==0:
				return None"""
			return result
		return value
