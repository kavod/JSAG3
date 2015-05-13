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
	DICT = '{0}' + color.BOLD + color.RED + '{1}:' + color.END + ' {2}'
	LIST = '{0}' + color.BOLD + color.GREEN + '{1}:' + color.END + ' {2}'
	SIMPLE = '{0}' + color.BOLD + '{1}:' + color.END + ' {2}'


def deepupdate(dict1,dict2,appendArray=False):
	for key in dict2.keys():
		if type(key) == 'unicode':
			key = str(key)
		if key in dict1.keys():
			if isinstance(dict1[key],dict) and isinstance(dict2[key],dict):
				deepupdate(dict1[key],dict2[key])
			elif appendArray and isinstance(dict1[key],list) and isinstance(dict2[key],list):
				dict1[key] += dict2[key]
			else:
				dict1[key] = copy.deepcopy(dict2[key])
		else:
			dict1[key] = copy.deepcopy(dict2[key])

def printList(myList,ident=""):
	for item in myList:
		if isinstance(item,list):
			printList(item,ident=" " + ident)
		else:
			print item['pattern'].format(ident,item['label'],item['value'])

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

	def keys(self):
		return self.value.keys()

	def __getitem__(self,key):
		if self.configParser.getType() in ['object','array']:
			return self.value[key]
		else:
			TypeError("value is not object nor list")
		
	def setValue(self,value):
		if self.configParser.getType() == 'object':
			result = dict(value)
		elif self.configParser.getType() == 'array':
			result = list(value)
		elif self.configParser.getType() in SIMPLE_TYPES:
			result = copy.copy(value)
		self.configParser.validate(result)
		self.value = result

	def getValue(self,path=[]):
		value = self.value
		if len(path) > 0:
			for level in path:
				value = value[level]
		return value

	def getConfigParser(self,path=[]):
		configParser = self.configParser
		if len(path) > 0:
			for level in path:
				if isinstance(level,int):
					configParser = configParser['items']
				else:
					configParser = configParser['properties'][level]
		return configParser

	def update(self,value,appendArray=False):
		deepupdate(self.value,value,appendArray)

	def choose(self):
		lines = self.displayConf(maxLevel=0)
		for key,line in enumerate(lines):
			print color.BOLD + '[' + str(key+1)+'] '+color.END+pattern.SIMPLE.format('',line['label'],line['value'])

	def display(self,maxLevel=-1):
		lines = self.displayConf(maxLevel=maxLevel)
		printList(lines,ident='')
		
	def displayConf(self,path=[],maxLevel=-1):
		lines = []
		value = self.getValue(path)
		configParser = self.getConfigParser(path)
		for item in sorted(configParser['properties'].iteritems(),key=lambda k:k[1]['order'] if 'order' in k[1].keys() else 0):
			if item[1].getType() == 'object':
				if item[0] in value.keys():
					if maxLevel != 0:
						lines.append({'pattern':pattern.DICT,"label":item[1]['title'],"value":''})
						lines.append(self.displayConf(path=path+[item[0]],maxLevel=maxLevel-1))
					else:
						lines.append({'pattern':pattern.DICT,"label":item[1]['title'],"value":'Managed'})
				else:
					lines.append({'pattern':pattern.DICT,"label":item[1]['title'],"value":'Not managed'})
			elif item[1].getType() == 'array':
				label = "List of " + item[1]['description']
				if item[0] in value.keys():
					if maxLevel != 0:
						lines.append({'pattern':pattern.LIST,"label":label,"value":''})
						lines.append(self.displayList(path=path+[item[0]],maxLevel=maxLevel))
					else:
						lines.append({'pattern':pattern.LIST,"label":label,"value":str(len(value[item[0]]))+' managed'})
				else:
					lines.append({'pattern':pattern.LIST,"label":label,"value":'0 managed'})
			else:
				val = value[item[0]] if item[0] in value else "None"
				if item[1].getType() == 'password':
					val = '****'
				lines.append({'pattern':pattern.SIMPLE,"label":item[1]['description'],"value":val})
		return lines
				
	def displayList(self,path=[],maxLevel=-1):
		lines = []
		value = self.getValue(path)
		configParser = self.getConfigParser(path)
		for key,item in enumerate(value):
			if configParser['items'].getType() == 'object':
				lines.append({'pattern':pattern.DICT,"label":configParser['description']+' '+str(key+1),"value":''})
				lines.append(self.displayConf(path=path+[key],maxLevel=maxLevel))
			elif configParser['items'].getType() == 'array':
				lines.append({'pattern':pattern.LIST,"label":configParser['description']+' '+str(key+1),"value":''})
			else:
				value = str(item)
				lines.append({'pattern':pattern.SIMPLE,"label":configParser['description']+' '+str(key+1),"value":value})
		return lines
