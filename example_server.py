#!/usr/bin/env python
#encoding:utf-8

import os
import sys
import cherrypy
import json
import jsonConfigParser

class Root(object):
	exposed = True
	
	# If GET method is called, just return the html file
	@cherrypy.tools.accept(media='text/plain')
	def GET(self):
		with open ("jcp.html", "r") as myfile:
			return myfile.read()

	# If POST method is called, process the submitted form
	@cherrypy.tools.accept(media='application/json')
	def POST(self,*args,**kwargs):
		cl = cherrypy.request.headers['Content-Length']
		rawbody = cherrypy.request.body.read(int(cl))
		value = json.loads(rawbody)
		# Load schema
		schema = jsonConfigParser.loadParserFromFile('example.jschem')
		values = value['conf']
		try:
			# Create a jsonConfigParser object
			cp = jsonConfigParser.jsonConfigParser(schema)
		except:
			return str(schema)
		# Load JSON values with the jsonConfigParser object
		# This JSON will be validated
		value = jsonConfigParser.jsonConfigValue(cp,values,'example.json')
		# If validated, save in the file indicated in constructor (here: example.json)
		value.save()
		cherrypy.response.headers['Content-Type'] = "application/json"
		# Return computed values
		return json.dumps(value.getValue())

class Data(object):
	exposed = True
	
	@cherrypy.tools.accept(media='application/json')
	def GET(self):
		cherrypy.response.headers['Content-Type'] = "application/json"
		try:
			with open ("example.json", "r") as myfile:
				return myfile.read()
		except:
			# If file is missing, you MUST return nothing
			return "{}"
			
local_dir = os.path.abspath(os.getcwd())

if __name__ == '__main__':
	root = Root()
	root.data = Data()
	
	conf = {
				# root:
				#	GET method will retrieve html page
				#	POST method will submit the form modification (and update data file)
				'/' : {
					'tools.caching.on': False,
					'request.dispatch': cherrypy.dispatch.MethodDispatcher(), 
				},
				# Link to the data file
				'/data': {
                	'tools.caching.on': False,
					'request.dispatch': cherrypy.dispatch.MethodDispatcher(), 
				},
				# Link to the json schema file
				'/config.jschem': {
                	'tools.staticfile.root': local_dir,
					'tools.staticfile.on': True,
					'tools.staticfile.filename': './example.jschem'
				},
				# JS directory (containing JS script & "Jquery Serialize Object" library (required by JS script)
				'/js': {
                	'tools.staticdir.root': local_dir,
					'tools.staticdir.on': True,
					'tools.staticdir.dir': './js'
				}
		}
	cherrypy.quickstart(root, '/', conf)

