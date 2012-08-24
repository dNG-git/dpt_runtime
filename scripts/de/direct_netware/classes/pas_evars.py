# -*- coding: utf-8 -*-
##j## BOF

"""
de.direct_netware.classes.pas_evars

@internal  We are using epydoc (JavaDoc style) to automate the
           documentation process for creating the Developer's Manual.
           Use the following line to ensure 76 character sizes:
----------------------------------------------------------------------------
@author    direct Netware Group
@copyright (C) direct Netware Group - All rights reserved
@package   pas_core
@since     v0.1.00
@license   http://www.direct-netware.de/redirect.php?licenses;w3c
           W3C (R) Software License
"""
"""n// NOTE
----------------------------------------------------------------------------
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
http://www.direct-netware.de/redirect.php?pas

This work is distributed under the W3C (R) Software License, but without any
warranty; without even the implied warranty of merchantability or fitness
for a particular purpose.
----------------------------------------------------------------------------
http://www.direct-netware.de/redirect.php?licenses;w3c
----------------------------------------------------------------------------
#echo(pasCoreVersion)#
pas/#echo(__FILEPATH__)#
----------------------------------------------------------------------------
NOTE_END //n"""

import base64,re

from .pas_globals import direct_globals
from .pas_xml import direct_xml
from .pas_xml_bridge import direct_xml_bridge

class direct_evars (object):
#
	"""
evars (Extended variables) are our answer for dynamic data in (for example)
SQL log tables.

@author    direct Netware Group
@copyright (C) direct Netware Group - All rights reserved
@package   pas_core
@since     v0.1.00
@license   http://www.direct-netware.de/redirect.php?licenses;w3c
           W3C (R) Software License
	"""

	def get (data):
	#
		"""
To receive all data (key-value pairs) from evars, use "get ()". This
function needs for its recursive job a helper function.

@param  data Internally evars are XML strings containing base64-encoded
        data if chosen (for binary content).
@return (dict) Key-value pair dictionary
@since  v0.1.00
		"""

		f_debug = direct_globals['debug']
		if (f_debug != None): f_debug.append ("#echo(__FILEPATH__)# -direct_evars.get (+data)- (#echo(__LINE__)#)")

		f_return = { }

		data = data.strip ()
		f_result_object = re.compile("<evars>(.+?)</evars>",(re.S | re.I)).search (data)
		f_xml_object = direct_xml_bridge.py_get ()

		if ((f_result_object != None) and (f_xml_object != None)):
		#
			f_result_dict = f_xml_object.xml2array (f_result_object.group (0),True,False)

			if ((type (f_result_dict) == dict) and ("evars" in f_result_dict)):
			#
				f_result_dict = direct_evars.get_walker (f_result_dict['evars'])
				if (len (f_result_dict) > 0): f_return = f_result_dict
			#
		#

		return f_return
	#
	get = staticmethod (get)

	def get_walker (xml_dict):
	#
		"""
This is a helper function for "direct_evars.get ()" to convert an XML
dictionary recursively.

@param  xml_dict XML nodes in a specific level.
@return (dict) Key-value pair dictionary
@since  v0.1.00
		"""

		f_return = { }

		if (type (xml_dict) == dict):
		#
			if ("xml.item" in xml_dict): del (xml_dict['xml.item'])

			if ("xml.mtree" in xml_dict):
			#
				f_mtree = True
				f_return = [ ]
				del (xml_dict['xml.mtree'])
			#
			else: f_mtree= False

			if (len (xml_dict) > 0):
			#
				for f_key in xml_dict:
				#
					try:
					#
						f_xml_node_dict = xml_dict[f_key]

						if (("xml.item" in f_xml_node_dict) or ("xml.mtree" in f_xml_node_dict)):
						#
							if (f_mtree): f_return.append (direct_evars.get_walker (f_xml_node_dict))
							else: f_return[f_key] = direct_evars.get_walker (f_xml_node_dict)
						#
						elif (len (f_xml_node_dict['tag']) > 0):
						#
							if (f_mtree):
							#
								if (("attributes" in f_xml_node_dict) and ("base64" in f_xml_node_dict['attributes'])): f_return.append (base64.b64decode (f_xml_node_dict['value']))
								else: f_return.append (f_xml_node_dict['value'])
							#
							else:
							#
								if (("attributes" in f_xml_node_dict) and ("base64" in f_xml_node_dict['attributes'])): f_return[f_xml_node_dict['tag']] = base64.b64decode (f_xml_node_dict['value'])
								else: f_return[f_xml_node_dict['tag']] = f_xml_node_dict['value']
							#
						#
					#
					except: pass
				#
			#
		#

		return f_return
	#
	get_walker = staticmethod (get_walker)

	def write (data_dict,binary_safe = False):
	#
		"""
To save all data from f_data as an evars-string, call "write ()". The
helper function will encode relevant data with b64encode if applicable.

@param  data_dict Input dictionary
@param  binary_safe True to encode values with base64.
@return (str) XML string
@since  v0.1.00
		"""

		f_debug = direct_globals['debug']
		if (f_debug != None): f_debug.append ("#echo(__FILEPATH__)# -direct_evars.write (+data_dict,+binary_safe)- (#echo(__LINE__)#)")

		f_return = ""
		f_xml_object = direct_xml.py_get ()

		if ((type (data_dict) == dict) and (len (data_dict) > 0) and (f_xml_object != None)):
		#
			f_data = { "evars": data_dict }
			f_xml_object.array_import (f_data,True)

			if (binary_safe):
			#
				f_data = direct_evars.write_base64_walker (f_xml_object.get ())
				f_return = f_xml_object.array2xml (f_data,False)
			#
			else: f_return = f_xml_object.cache_export (True)
		#

		return f_return
	#
	write = staticmethod (write)

	def write_base64_walker (data):
	#
		"""
This recursive function is used to protect binary data in a system optimized
for strings.

@param  data Input data
@return (mixed) The return value is based on the input type (and will contain
        base64-encoded values if required)
@since  v0.1.00
		"""

		f_list_check = False

		if (type (data) == list):
		#
			f_list_check = True
			f_return = [ ]
		#
		elif (type (data) == dict): f_return = { }
		else: data = [ ]

		if (len (data) > 0):
		#
			f_re_whitespace = re.compile ("\\W")

			for f_entry in data:
			#
				if (f_list_check): f_node_dict = f_entry
				else: f_node_dict = data[f_entry]

				if (type (f_node_dict) == dict):
				#
					if ("xml.item" in f_node_dict):
					#
						if (f_list_check): f_return.append (direct_evars.write_base64_walker (f_node_dict))
						else: f_return[f_entry] = direct_evars.write_base64_walker (f_node_dict)
					#
					elif (len (f_node_dict['tag']) > 0):
					#
						if (f_re_whitespace.search (f_node_dict['value']) != None):
						#
							f_node_dict['attributes'] = { "base64": 1 }
							f_node_dict['value'] = base64.b64encode (f_node_dict['value'])
						#

						f_return[f_entry] = f_node_dict
					#
				#
			#
		#

		return f_return
	#
	write_base64_walker = staticmethod (write_base64_walker)
#

##j## EOF