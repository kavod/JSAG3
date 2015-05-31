#!/usr/bin/env python
#encoding:utf-8

import os
import sys
import cherrypy
import json
from jsonConfigParser import *
		
class Schema(object):
	@cherrypy.expose
	@cherrypy.tools.accept(media='application/json')
	def submit(self,*args,**kwargs):
		cl = cherrypy.request.headers['Content-Length']
		rawbody = cherrypy.request.body.read(int(cl))
		value = json.loads(rawbody)
		schema_key = value.keys()[0]
		schema = schemas[schema_key]['schema']
		values = value[schema_key]
		try:
			cp = jsonConfigParser(schema)
		except:
			return str(schema)
		value = jsonConfigValue(cp,values,schemas[schema_key]['values_file'])
		value.save()
		schemas[schema_key]['values'] = value.getValue()
		cherrypy.response.headers['Content-Type'] = "application/json"
		return value.getValue()

	@cherrypy.expose
	def default(self,*args,**kwargs):
		return json.dumps(schemas[args[1]][args[0]])

local_dir = os.path.abspath(os.getcwd())
schemas = {}
jcp_path = 'jcp/'
jcp_conf = {
				'/' + jcp_path + 'jcp.js': {
                	'tools.staticfile.root': local_dir,
					'tools.staticfile.on': True,
					'tools.staticfile.filename': './web/jcp.js'
				},
				'/' + jcp_path + 'jquery.serialize-object.min.js': {
                	'tools.staticfile.root': local_dir,
					'tools.staticfile.on': True,
					'tools.staticfile.filename': './web/jquery.serialize-object.min.js'
				}
			}

def addSchema(id,jcp_path,schema_file,values_file):
	schema = loadParserFromFile(schema_file)
	value = jsonConfigValue(schema,value=None,filename=values_file)
	value.load()
	schemas[id] = {
					'schema':schema,
					'values':value.getValue(),
					'values_file':values_file,
					}

class Root(object):
	pass

if __name__ == '__main__':
	root = Root()
	root.jcp = Root()
	root.jcp = Schema()
	
	conf = {
				'/' : {
					'tools.caching.on': False
				},
				'/index.html': {
                	'tools.staticfile.root': local_dir,
					'tools.staticfile.on': True,
					'tools.staticfile.filename': './jcp.html'
				}
		}
	conf.update(jcp_conf)
	addSchema('conf',jcp_path,'config.jschem','config.json')
	cherrypy.quickstart(root, '/', conf)

