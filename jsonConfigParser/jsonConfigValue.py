#!/usr/bin/env python
#encoding:utf-8

from jsonConfigParser import *

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

class pattern:
	DICT = '{0}' + color.BOLD + color.RED + '{1}{2}' + color.END
	LIST = '{0}' + color.BOLD + color.GREEN + '{1}{2}' + color.END
	SIMPLE = '{0}' + color.BOLD + '{1}{2}:' + color.END + ' {3}'

class jsonConfigValue(object):
	def __init__(self,configParser=None,value=None,filename=None):
		if isinstance(configParser,jsonConfigParser):
			self.configParser = configParser
		elif isinstance(configParser,dict):
			self.configParser = jsonConfigParser(configParser)
		else:
			raise TypeError("configParser argument is mandatory and must be a jsonConfigParser instance")

		self.setFilename(filename)

		if value is None:
			self.value = None
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
				json.dump(self.value, outfile)
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
		if self.configParser.getType() == 'object':
			result = self.merge({},value)
		elif self.configParser.getType() == 'array':
			result = [jsonConfigValue(self.configParser['items'],val) for val in value]
		elif self.configParser.getType() in SIMPLE_TYPES:
			result = value
		self.configParser.validate(result)
		self.value = result		
		
	def update(self,value):
		if self.configParser.getType() == 'object':
			result = self.merge(copy.deepcopy(self.value),value)
			self.configParser.validate(result)
			for key in result.keys():
				self.value[key] = result[key]
		else:
			self.setValue(value)
			
	def merge(self,initial,value):
		for item in value.iteritems():
			if self.configParser['properties'][item[0]].getType() == 'object':
				if item[0] not in initial.keys():
					initial[str(item[0])] = {}
				initial[str(item[0])] = jsonConfigValue(configParser=self.configParser['properties'][item[0]],value=item[1])
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
		
	def displayConf(self,ident='',key=''):
		for item in self.configParser['properties'].iteritems():
			if item[1].getType() == 'object':
				line = pattern.DICT.format(ident,item[1]['title'],key)
				print line
				if item[0] in self.keys():
					self[item[0]].displayConf(' '+ident)
				else:
					print ident + 'Not managed'
			elif item[1].getType() == 'array':
				line = pattern.LIST.format(ident,"List of " + item[0],key)
				print line
				if item[0] in self.keys():
					self[item[0]].displayList(item[1],ident)
				else:
					print ident + 'Not managed'
			else:
				line = pattern.SIMPLE.format(ident,item[0],item[1],key)
				print line
				
	def displayList(self,ident):
		for key,item in enumerate(self):
			item.displayConf(ident,key=' '+str(key+1))
