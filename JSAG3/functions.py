#!/usr/bin/env python
#encoding:utf-8
from __future__ import unicode_literals

import logging
import datetime
import dateutil.parser
import tzlocal

PASSWORDMASK='********'

def updateData(dataSrc,dataDst,schema):
	logging.debug("[JSAG3.updateData] Update data from\n{0}\n --to--\n{1}.".format(dataSrc,dataDst))
	if 'type' in schema.keys() and schema['type'] == 'object' and 'properties' in schema.keys():
		result = {}
		for key in schema['properties'].keys():
			if key in dataDst.keys():
				src = dataSrc[key] if (isinstance(dataSrc,dict) and key in dataSrc.keys()) else None
				result.update({key:updateData(src,dataDst[key],schema['properties'][key])})
		return result
	elif 'type' in schema.keys() and schema['type'] == 'array' and 'items' in schema.keys():
		result = []
		i = 0
		for item in dataDst:
			if dataSrc is not None and len(dataSrc) > i:
				src = dataSrc[i]
			else:
				src = None
			result.append(updateData(src,item,schema['items']))
			i=i+1
		return result
	elif 'format' in schema.keys() and schema['format'] == 'password':
		return dataSrc if dataDst == PASSWORDMASK else dataDst
	else:
		return dataDst

def hidePasswords(data,schema):
	logging.debug("[JSAG3.hidePasswords] Hidepassword of {0}".format(unicode(data)))
	if 'type' in schema.keys() and schema['type'] == 'object' and 'properties' in schema.keys():
		result = {}
		if data is not None:
			for key in schema['properties'].keys():
				if key in data.keys():
					result.update({key:hidePasswords(data[key],schema['properties'][key])})
		return result
	elif 'type' in schema.keys() and schema['type'] == 'array' and 'items' in schema.keys():
		result = []
		if data is not None:
			for item in data:
				result.append(hidePasswords(item,schema['items']))
		return result
	elif 'format' in schema.keys() and schema['format'] == 'password':
		return PASSWORDMASK
	else:
		return data
		
def string2datetime(data,schema):
	logging.debug("[JSAG3.string2datetime] string2datetime of {0}".format(unicode(data)))
	if 'type' in schema.keys() and schema['type'] == 'object' and 'properties' in schema.keys():
		result = {}
		if data is not None:
			for key in schema['properties'].keys():
				if key in data.keys():
					result.update({key:string2datetime(data[key],schema['properties'][key])})
		return result
	elif 'type' in schema.keys() and schema['type'] == 'array' and 'items' in schema.keys():
		result = []
		if data is not None:
			for item in data:
				result.append(string2datetime(item,schema['items']))
		return result
	elif 'format' in schema.keys() and schema['format'] == 'datetime' and isinstance(data,basestring):
		date = dateutil.parser.parse(data)
		if date.tzinfo is not None and date.tzinfo.utcoffset(date) is not None:
			return date
		else:
			tzlocal.get_localzone().localize(dateutil.parser.parse(data))
	else:
		return data
				
def datetime2string(data,schema):
	logging.debug("[JSAG3.datetime2string] datetime2string of {0}".format(unicode(data)))
	if 'type' in schema.keys() and schema['type'] == 'object' and 'properties' in schema.keys():
		result = {}
		if data is not None:
			for key in schema['properties'].keys():
				if key in data.keys():
					result.update({key:datetime2string(data[key],schema['properties'][key])})
		return result
	elif 'type' in schema.keys() and schema['type'] == 'array' and 'items' in schema.keys():
		result = []
		if data is not None:
			for item in data:
				result.append(datetime2string(item,schema['items']))
		return result
	elif 'format' in schema.keys() and schema['format'] == 'datetime' and isinstance(data,datetime.datetime):
		return data.isoformat()
	else:
		return data
