# -*- coding: utf-8 -*-
##j## BOF

"""
de.direct_netware.classes.pas_pythonback

@internal  We are using epydoc (JavaDoc style) to automate the documentation
           process for creating the Developer's Manual.
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

try: _direct_core_unicode_object = { "type": unicode,"str": unicode.encode,"unicode": str.decode }
except: _direct_core_unicode_object = { "type": bytes,"str": bytes.decode,"unicode": str.encode }

def direct_str (data):
#
	"""
Returns the string representing the (maybe encoded) input data

@param  data Input string
@return (str) String representation
@since  v0.1.00
	"""

	global _direct_core_unicode_object
	if (type (data) == _direct_core_unicode_object['type']): data = _direct_core_unicode_object['str'] (data,"utf-8")
	return data
#

def direct_bytes (data):
#
	"""
Returns the bytes representing the (maybe encoded) input data

@param  data Input string
@return (bytes) Byte representation
@since  v0.1.00
	"""

	global _direct_core_unicode_object

	try:
	#
		if (bytes == _direct_core_unicode_object['type']): data = direct_unicode (data)
		else: data = direct_str (data)
	#
	except: data = direct_str (data)

	return data
#

def direct_unicode (data):
#
	"""
Returns the unicode data representing the (maybe encoded) input data

@param  data Input string
@return (bytes) Unicode representation
@since  v0.1.00
	"""

	global _direct_core_unicode_object
	if (type (data) == str): data = _direct_core_unicode_object['unicode'] (data,"utf-8")
	return data
#

##j## EOF