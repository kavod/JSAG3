#!/usr/bin/env python
#encoding:utf-8

from jsonConfigParser import *

class jsonConfigValue(dict):
	def __init__(self,configParser=None,value=None,filename=None):
		if isinstance(configParser,jsonConfigParser):
			self.configParser = configParser
		elif isinstance(configParser,dict):
			self.configParser = jsonConfigParser(configParser)
		else:
			raise TypeError("configParser argument is mandatory and must be a jsonConfigParser instance")

		self.setFilename(filename)

		if value is None:
			dict.__init__(self,{})
		else:
			self.setValue(value)
			
	def cliCreate(self):
		newConf = self.configParser.cliCreate()
		self.setValue(newConf)
		
	def cliChange(self):
		newConf = self.configParser.cliChange(self)
		self.setValue(newConf)
			
	def save(self,filename=None):
		if filename is not None:
			self.setFilename(filename)
		if self.filename is None:
			raise Exception("No file specified")
		try:
			with open(self.filename, 'w') as outfile:
				json.dump(self, outfile)
		except:
			raise Exception("Unable to write file {0}".format(str(self.filename)))

	def load(self,filename=None):
		if filename is not None:
			self.setFilename(filename)
		if self.filename is None:
			raise Exception("No file specified")
		try:
			with open(self.filename) as data_file:    
				data = json.load(data_file)
		except:
			raise Exception("Unable to read file {0}".format(str(self.filename)))
		self.setValue(data)
			
	def setFilename(self,filename=None):
		if filename is None:
			self.filename = None
			return
		if not isinstance(filename,str):
			raise TypeError("Filename must be a string. {0} entered".format(str(filename)))
		self.filename = filename
		
	def setValue(self,value):
		result = self.merge({},value)
		self.configParser.validate(result)
		dict.__init__(self,result)		
		
	def update(self,value):
		result = self.merge(copy.deepcopy(self),value)
		self.configParser.validate(result)
		for key in result.keys():
			self[key] = result[key]
			
	def merge(self,initial,value):
		for item in value.iteritems():
			if self.configParser['properties'][item[0]].getType() == 'object':
				if item[0] not in initial.keys():
					initial[str(item[0])] = {}
				initial[str(item[0])].update(jsonConfigValue(configParser=self.configParser['properties'][item[0]],value=item[1]))
			elif self.configParser['properties'][item[0]].getType() == 'array':
				subitems = []
				for element in item[1]:
					if self.configParser['properties'][item[0]]['items'].getType() in SIMPLE_TYPES:
						subitems = item[1]
					else:
						subitems.append(jsonConfigValue(configParser=self.configParser['properties'][item[0]]['items'],value=element))
				initial[str(item[0])] = subitems
			else:
				initial[str(item[0])] = item[1]
		return initial
