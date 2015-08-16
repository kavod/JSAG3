# JSAP (jsonSchemaAppGenerator)

*formely "jsonConfigParser"*

Simplify you json files management in your python or webapp applications

## How JSAP helps me?

If you manage your application with json files in order to store configurations or user datas, you certainly noticed you spend a lot of time into changing your file structure.
Of course, you have to take into account all modification in your core algorithm. This script has not the claim to avoid this part of the development work.
BUT in this case, you also need to take this change into account in classical functionnalities like:
* data load from file
* data save in file
* user interface for maintain the data
* user input controls for data modifications
* ...
I don't know for you, but in my opinion, I hate spend times into code modification for these valueless functions.

This library will allow you to manipulate your data structure (adding/deleting/modifing fields/types/structure/hierarchy...) 

### Example - the "old" way
You write this python script:

**myScript.py**
```python
#!/usr/bin/env python
#encoding:utf-8

class helloMe(object):
	def __init__(self):
		pass
		
	def run(self):
		print u'Hello Kavod'

if __name__ == '__main__':
	myFriend = helloMe()
	myFriend.run()
```
You do not have the chance to be called Kavod? No problem, let's put the name into a configuration file:

**myData.json**
```json
{"myName":"Kavod"}
```
and let's adapt script:

**myScript.py**
```python
#!/usr/bin/env python
#encoding:utf-8

import json
from codecs import open

class helloMe(object):
	def __init__(self):
		with open(u'myData.json',encoding=u'utf8') as data_file:
			data = json.load(data_file)
		self.myName = data['myName']
		
	def run(self):
		print u'Hello {0}'.format(self.myName)

if __name__ == '__main__':
	myFriend = helloMe()
	myFriend.run()
```
Good good... But you have to let user have a look on the configuration and modify this name directly within the script if required

**myScript.py**
```python
#!/usr/bin/env python
#encoding:utf-8

import json
from codecs import open

class helloMe(object):
	def __init__(self):
		with open(u'myData.json',encoding=u'utf8') as data_file:
			data = json.load(data_file)
		self.myName = data['myName']
		
	def run(self):
		print u"Current configuration:"
		print u"Name: {0}\n".format(self.myName)
		print u"do you want to change?"
		
		answer = raw_input("Type Y or N > ")
		if answer.lower() == 'y':
			self.config()
		print u'Hello {0}'.format(self.myName)
				
	def config(self):
		print u"Please enter your name"
		self.myName = raw_input("> ")
		data = {"myName":self.myName}
		with open(u'myData.json', 'w') as outfile:
			json.dump(data, outfile,encoding='utf8')

if __name__ == '__main__':
	myFriend = helloMe()
	myFriend.run()
```
This is really a lot of codelines for a really dirty code (no input controls etc.)
But the worth is when you want to modify the structure. Let's add a new data: title (Mr/Ms/Mrs)

**myData.json**
```json
{"myName":"Kavod","title":"Mr"}
```
**myScript.py**
```python
#!/usr/bin/env python
#encoding:utf-8

import json
from codecs import open

class helloMe(object):
	def __init__(self):
		with open(u'myData.json',encoding=u'utf8') as data_file:
			data = json.load(data_file)
		self.myName = data['myName']
		self.title = data['title']
		
	def run(self):
		print u"Current configuration:"
		print u"Title: {0}".format(self.title)
		print u"Name: {0}\n".format(self.myName)
		print u"do you want to change?"
		answer = raw_input("Type Y or N > ")
		if answer.lower() == 'y':
			self.config()
		print u'Hello {0} {1}'.format(self.title,self.myName)
				
	def config(self):
		#title
		print "Mr, Ms or Mrs?"
		possible_answer = ['Mr','Ms','Mrs']
		while True:
			self.title = raw_input('> ')
			if self.title in possible_answer:
				break
		#name		
		print u"Please enter your name"
		self.myName = raw_input("> ")
		
		#save
		data = {"myName":self.myName,"title":self.title}
		with open(u'myData.json', 'w') as outfile:
			json.dump(data, outfile,encoding='utf8')

if __name__ == '__main__':
	myFriend = helloMe()
	myFriend.run()
```
Yeah!!!! 43 codelines for... that?
If we want to deal with input control, required data etc. we need to add extra boring linecodes.
But the worst: if I need to add another field, I will need to change both of the 3 methods:
* \_\_init\_\_ to save into attribute the new data
* run to display the new attribute (normal, it is core functionnality) but also to modify the configuration display
* config to 

Let's try with JSAG now!

### Example - the JSAG way!!!
First, I will create a JSON schema in order to describe my file structure
If you don't know JSON schema, please have a look [on this website](http://json-schema.org/)

**myData.jschem**
```json
{
	"type":"object",
	"title":"Configuration",
	"properties": {
		"myName":{"title":"Your name","type":"string"},
		"title":{
			"title":"Mr/Ms/Mrs",
			"$def":"#/choices/title",
			"choices": {"title": {"Mr": "Mr", "Ms": "Ms", "Mrs": "Mrs"}}
		}
	},
	"required": ["myName","title"]
}
```
Here, we defined a 2 attributes object.
* myName is a string
* title is a field which can only take Mr, Ms or Mrs as value
Both of the fields are required.
This is only a very simple example. But, I suggest again to view documentation of [JSON Schema website](http://json-schema.org/) in order to have a look of the possibilities (required data, pattern controls, min/max number controls, number/hostname/emails formats, hierarchied data, lists...)
OK, now here the new script:

**myScript.py**
```python
#!/usr/bin/env python
#encoding:utf-8

import json
from codecs import open
import JSAG

class helloMe(object):
	def __init__(self):
		self.schema = JSAG.loadParserFromFile(filename='myData.jschem')
		self.data = JSAG.JSAGdata(configParser=self.schema)
		self.data.load(filename='myData.json')
		
	def run(self):
		self.data.display()
		print u"Do you want modify configuration file before run?"
		answer = raw_input("Type Y or N > ")
		if answer.lower() == 'y':
			self.config()
		print u'Hello {0} {1}'.format(self.data.getValue(['title']),self.data.getValue(['myName']))
				
	def config(self):
		self.data.cliChange() #title and name
		self.data.save() #save

if __name__ == '__main__':
	myFriend = helloMe()
	myFriend.run()
```
And, here the result:
```
Configuration: 
 Your name:    Kavod
 Mr/Ms/Mrs:    Mr
Do you want modify configuration file before run?
Type Y or N > Y
* Configuration
***************
1 : Your name - Kavod 
2 : Mr/Ms/Mrs - Mr
> 1
* Your name 
************
> Joe Doe
* Your name changed!
********************
Hello Mr Joe Doe
```
It is smaller... a more beautifull (unfortunatly, you cannot see color here).
But the better: if we have to add another field (or fieldset, or list etc.), you just need touch "run" method for the core functionnaly. Configuration display/modification/load/save is already managed.

Use ``unittest`` scripts of the repository to have a larger view of functionnalities

## And about Javascript?
Well... I'm a bit tried now. But I promise to write a example soon.
But you can also have a look on example in the repository. Just launch ``python example_server.py`` and go to ``http://localhost:8080``.
