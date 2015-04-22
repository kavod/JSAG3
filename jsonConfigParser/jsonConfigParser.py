#!/usr/bin/env python
#encoding:utf-8

import sys
import json
import jsonschema
from jsonschema import Draft4Validator

definitions =  {
				"password": {
					"type":"string"
				}
			}

class jsonConfigParser(dict):
	def __init__(self,*args):
		dict.__init__(self,*args)
		self.update({'definitions':definitions})
		Draft4Validator.check_schema(self)
	
	def validate(self,json):
		jsonschema.validate(json,self)
