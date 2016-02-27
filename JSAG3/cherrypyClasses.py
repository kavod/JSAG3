#!/usr/bin/env python
#encoding:utf-8
from __future__ import unicode_literals

import os
import json
import cherrypy
from functions import updateData, hidePasswords

class staticData(object):
	def __init__(self,jsag3):
		self.jsag3 = jsag3
	
	"""def __init__(self,dataFile,schema):
		if isinstance(schema,basestring):
			schemaFile = schema
			with open(schemaFile) as data_file:    
				self.schema = json.load(data_file)
		elif isinstance(schema,dict):
			self.schema = schema
		else:
			raise TypeError("staticData accept basestring (for filename) or dict. {0} received".format(type(schema)))
		self.dataFile = dataFile
		self.update()
			
	def update(self):
		if not hasattr(self,"lastModified") or os.path.getmtime(self.dataFile) != self.lastModified:
			with open(self.dataFile) as data_file:    
				self.data = hidePasswords(json.load(data_file),self.schema)"""
			
	@cherrypy.expose
	@cherrypy.tools.json_out()
	def index(self):
		#self.update()
		cherrypy.response.headers['Cache-Control'] = 'no-cache, must-revalidate'
		cherrypy.response.headers['Pragma'] = 'no-cache'
		cherrypy.lib.caching.expires(secs=0)
		#return self.data
		return self.jsag3.getValue(hidePassword=True)

class staticJsonFile(object):
	def __init__(self,filename):
		self.filename = filename
		self.update()
			
	def update(self):
		if not hasattr(self,"lastModified") or os.path.getmtime(self.filename) != self.lastModified:
			with open(self.filename) as data_file:    
				self.data = json.load(data_file)
			self.lastModified = os.path.getmtime(self.filename)
			
	@cherrypy.expose
	@cherrypy.tools.json_out()
	def index(self):
		self.update()
		cherrypy.response.headers['Cache-Control'] = 'no-cache, must-revalidate'
		cherrypy.response.headers['Pragma'] = 'no-cache'
		cherrypy.lib.caching.expires(secs=0)
		return self.data
		
class staticJsonString(object):
	def __init__(self,data):
		self.data = data
		
	@cherrypy.expose
	@cherrypy.tools.json_out()
	def index(self):
		cherrypy.response.headers['Cache-Control'] = 'no-cache, must-revalidate'
		cherrypy.response.headers['Pragma'] = 'no-cache'
		cherrypy.lib.caching.expires(secs=0)
		return self.data
		
class Root(object):
	pass
