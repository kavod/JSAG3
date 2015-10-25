#!/usr/bin/env python
#encoding:utf-8
from __future__ import unicode_literals

import datetime
from codecs import open
from JSAGparser import *

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
					item['value'] = item['value'].encode('utf8')
				print ('{0:' + unicode(max(width,0)+15) + '}{1}').format(label,unicode(item['value']))
			except:
				print "ERROR"
				print myList
				sys.exit()
				
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
				raise IndexError("key not found")
			return self.data[key]
		elif self.parser.getType() == 'array':
			if key >= len(self.data):
				raise IndexError("array is not long enough")
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
		if isinstance(value,JSAGdata):
			value = value.getValue()
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

	def display(self,maxLevel=-1,cleanScreen=True):
		lines = self.displayConf(maxLevel=maxLevel)
		width = getWidth(lines)
		if cleanScreen:
			print(chr(27) + "[2J")
		printList(lines,ident='',width=width)
		
	def displayConf(self,maxLevel=-1,key=''):
		lines = []
		value = self.getValue()
		if self.parser.getType() == 'object':
			if value is None:
				val = "Not managed"
			else:
				if maxLevel != 0:
					val = ''
				else:
					val = "Managed"
			lines.append({'pattern':pattern.DICT,"label":self.parser['title']+key,"value":val})
			if maxLevel !=0 and value is not None:
				lines.append([])
				for item in sorted(self.parser['properties'].iteritems(),key=lambda k:k[1]['order'] if 'order' in k[1].keys() else 0):
					if item[0] in self.keys():
						lines[1] +=self[item[0]].displayConf(maxLevel=maxLevel-1)
		# array
		elif self.parser.getType() == 'array':
			if value is None or len(value)<1:
				val = "0 managed"
			else:
				if maxLevel != 0:
					val = ''
				else:
					val = unicode(len(value)) + " managed"
			label = "List of " + self.parser['title']
			lines.append({'pattern':pattern.LIST,"label":label,"value":val})
			if value is not None and maxLevel != 0:
				lines.append(self.displayList(maxLevel=maxLevel-1))
				

		# Simple
		else:
			val = value if value is not None else "None"
			lines.append({'pattern':pattern.SIMPLE,"label":self.parser['title'],"value":val})
		return lines
			
	def displayList(self,maxLevel=-1):
		lines = []
		value = self.getValue()
		for key,item in enumerate(value):
			if self.parser['items'].getType() == 'object':
				lines+=self[key].displayConf(maxLevel=maxLevel,key=' '+unicode(key+1))
			elif self.parser['items'].getType() == 'array':
				lines.append({'pattern':pattern.LIST,"label":self.parser['title']+' '+unicode(key+1),"value":''})
			else:
				value = unicode(item)
				lines.append({'pattern':pattern.SIMPLE,"label":self.parser['title']+' '+unicode(key+1),"value":value})
		return lines
			
	def cliCreate(self):
		newConf = self.parser.cliCreate()
		self.setValue(newConf)
		
	def cliChange(self):
		newConf = self.parser.cliChange(self.getValue(path=[],hidePasswords=True))
		self.setValue(newConf)
		
	def proposeSave(self,display=True,filename=None,path=[]):
		if filename is not None:
			self.setFilename(filename,path)
		if display:
			self.display()
		if self.filename is not None:
			if Prompt.promptYN("Save in file {0}?".format(self.filename),default='N',cleanScreen=False):
				self.save(path=path)
				print "Saved!"
				return True
			else:
				print "Not saved!"
				return False
		else:
			raise Exception("No filename specified")
