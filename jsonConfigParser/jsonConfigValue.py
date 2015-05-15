#!/usr/bin/env python
#encoding:utf-8

from jsonConfigParser import *
import Prompt
from codecs import open

class color:
   PURPLE = '\033[95m'
   WHITE = '\033[97m'
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
	DICT = '{0}' + color.BOLD + color.RED + '{1}:' + color.END
	LIST = '{0}' + color.BOLD + color.GREEN + '{1}:' + color.END
	SIMPLE = '{0}' + color.BOLD + color.WHITE + '{1}:' + color.END


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

def getWidth(myList,maxLevel=-1,ident=0):
	width = 0
	for item in myList:
		if isinstance(item,list):
			width = max(width,getWidth(item,maxLevel=maxLevel-1,ident=ident+1))
		else:
			width = max(width,len(item['label'])+ident)
	return width

def printList(myList,ident="",width=0):
	for item in myList:
		if isinstance(item,list):
			printList(item,ident=" " + ident,width=width)
		else:
			try:
				label = item['pattern'].format(ident,item['label'],item['value'])
				if isinstance(item['value'],unicode):
					item['value'] =  item['value'].encode('utf8')
				print ('{0:' + str(max(width,0)+15) + '}{1}').format(label,str(item['value']))
			except:
				print "ERROR"
				print myList
				sys.exit()

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
		newConf = self.configParser.cliChange(self.value)
		self.setValue(newConf)
			
	def save(self,filename=None):
		if filename is not None:
			self.setFilename(filename)
		if self.filename is None:
			raise Exception("No file specified")
		try:
			with open(self.filename, 'w') as outfile:
				json.dump(self.value, outfile,encoding='utf8')
		except:
			raise Exception("Unable to write file {0}".format(str(self.filename)))

	def load(self,filename=None):
		if filename is not None:
			self.setFilename(filename)
		if self.filename is None:
			raise Exception("No file specified")
		try:
			with open(self.filename,encoding='utf8') as data_file:    
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
		
	def setValue(self,value,path=[]):
		configParser = self.getConfigParser(path)
		if configParser.getType() == 'object':
			result = dict(value)
		elif configParser.getType() == 'array':
			result = list(value)
		elif configParser.getType() in SIMPLE_TYPES:
			result = copy.copy(value)
		configParser.validate(result)
		self.value = result

	def getValue(self,path=[],hidePasswords=True):
		value = self.value
		configParser = self.getConfigParser(path=path)
		if len(path) > 0:
			for level in path:
				if (isinstance(value,dict) and level in value.keys()) or (isinstance(value,list) and len(value) > level):
					value = value[level]
				else:
					return None
		if configParser.getType() == "object":
			result={}
			for key in value.keys():
				result[key] = self.getValue(path=path+[key],hidePasswords=hidePasswords)
			return result
		elif configParser.getType() == 'array':
			return [self.getValue(path=path+[item[0]],hidePasswords=hidePasswords) for item in enumerate(value)]
		elif configParser.getType() == 'password' and hidePasswords:
			return '****'
		else: 
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

	def choose(self,path=[]):
		value = self.getValue(path)
		configParser = self.getConfigParser(path)
		if (configParser.getType() in SIMPLE_TYPES) or (configParser.getType() == 'array' and configParser['items'].getType() in SIMPLE_TYPES) or value is None:
			parent = self.getValue(path[:-1])
			parent[path[-1]] = configParser.cliCreate()
		else:
			lines = self.displayConf(path=path,maxLevel=1)
			question = lines[0]['pattern'].format('',lines[0]['label'],lines[0]['value'])
			choices = []
			width = getWidth(lines,maxLevel=1)
			target_path = []
			for key,line in enumerate(lines[1]):
				label = pattern.SIMPLE.format('',line['label'])
				line['value'] =  line['value'].encode('utf8')
				choices.append(('{0:' + str(max(width,0)+15) + '}{1}').format(label,line['value']))
				target_path.append(line['path'])
			reponse = Prompt.promptChoice(question,choices,warning='',selected=[],default = None,mandatory=True,multi=False)
			self.choose(target_path[reponse])

	def display(self,path=[],maxLevel=-1):
		lines = self.displayConf(path=path,maxLevel=maxLevel)
		width = getWidth(lines)
		printList(lines,ident='',width=width)
		
	def displayConf(self,path=[],maxLevel=-1,key=''):
		lines = []
		value = self.getValue(path)
		configParser = self.getConfigParser(path)
		if configParser.getType() == 'object':
			if value is None:
				val = "Not managed"
			else:
				if maxLevel != 0:
					val = ''
				else:
					val = "Managed"
			lines.append({'pattern':pattern.DICT,"label":configParser['title']+key,"value":val,"path":path})
			if maxLevel !=0 and value is not None:
				lines.append([])
				for item in sorted(configParser['properties'].iteritems(),key=lambda k:k[1]['order'] if 'order' in k[1].keys() else 0):
					lines[1] +=self.displayConf(path=path+[item[0]],maxLevel=maxLevel-1)
		# array
		elif configParser.getType() == 'array':
			if value is None or len(value)<1:
				val = "0 managed"
			else:
				if maxLevel != 0:
					val = ''
				else:
					val = str(len(value)) + " managed"
			label = "List of " + configParser['title']
			lines.append({'pattern':pattern.LIST,"label":label,"value":val,"path":path})
			if value is not None and maxLevel != 0:
				lines.append(self.displayList(path=path,maxLevel=maxLevel-1))
				

		# Simple
		else:
			val = value if value is not None else "None"
			lines.append({'pattern':pattern.SIMPLE,"label":configParser['title'],"value":val,"path":path})
		return lines
			
	def displayList(self,path=[],maxLevel=-1):
		lines = []
		value = self.getValue(path)
		configParser = self.getConfigParser(path)
		for key,item in enumerate(value):
			if configParser['items'].getType() == 'object':
				lines+=self.displayConf(path=path+[key],maxLevel=maxLevel,key=' '+str(key+1))
			elif configParser['items'].getType() == 'array':
				lines.append({'pattern':pattern.LIST,"label":configParser['title']+' '+str(key+1),"value":'',"path":path})
			else:
				value = str(item)
				lines.append({'pattern':pattern.SIMPLE,"label":configParser['title']+' '+str(key+1),"value":value,"path":path})
		return lines
