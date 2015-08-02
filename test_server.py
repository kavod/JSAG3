#!/usr/bin/env python
#encoding:utf-8

import os
import sys
import cherrypy
import json
import jsonConfigParser

class Root(object):
	exposed = True
	
	@cherrypy.tools.accept(media='text/plain')
	def GET(self):
		with open ("jcp.html", "r") as myfile:
			return myfile.read()

	@cherrypy.tools.accept(media='application/json')
	def POST(self,*args,**kwargs):
		cl = cherrypy.request.headers['Content-Length']
		rawbody = cherrypy.request.body.read(int(cl))
		value = json.loads(rawbody)
		schema_key = value.keys()[0]
		schema = jsonConfigParser.loadParserFromFile('config.jschem')
		values = value['conf']
		try:
			cp = jsonConfigParser.jsonConfigParser(schema)
		except:
			return str(schema)
		value = jsonConfigParser.jsonConfigValue(cp,values,'config.json')
		value.save()
		cherrypy.response.headers['Content-Type'] = "application/json"
		return json.dumps(value.getValue())

local_dir = os.path.abspath(os.getcwd())

if __name__ == '__main__':
	root = Root()
	
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
                	'tools.staticfile.root': local_dir,
					'tools.staticfile.on': True,
					'tools.staticfile.filename': './config.json'
				},
				# Link to the json schema file
				'/config.jschem': {
                	'tools.staticfile.root': local_dir,
					'tools.staticfile.on': True,
					'tools.staticfile.filename': './config.jschem'
				},
				# JS directory (containing JS script & "Jquery Serialize Object" library (required by JS script)
				'/js': {
                	'tools.staticdir.root': local_dir,
					'tools.staticdir.on': True,
					'tools.staticdir.dir': './js'
				}
		}
	cherrypy.quickstart(root, '/', conf)

