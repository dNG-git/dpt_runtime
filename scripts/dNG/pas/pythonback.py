# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.pythonback
"""
"""n// NOTE
----------------------------------------------------------------------------
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
http://www.direct-netware.de/redirect.py?pas;core

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
http://www.direct-netware.de/redirect.py?licenses;mpl2
----------------------------------------------------------------------------
#echo(pasCoreVersion)#
#echo(__FILEPATH__)#
----------------------------------------------------------------------------
NOTE_END //n"""

try: direct_settings = { "bytes": unicode.encode, "bytes_type": str, "str": unicode.encode, "unicode": str.decode, "unicode_type": unicode }
except: direct_settings = { "bytes": str.encode, "bytes_type": bytes, "str": bytes.decode, "unicode": bytes.decode, "unicode_type": str }

def direct_bytes(data):
#
	"""
Returns the bytes representing the (maybe encoded) input data

:param data: Input string

:return: (bytes) Byte representation
:since:  v0.1.00
	"""

	global direct_settings
	if (type(data) != direct_settings['bytes_type']): data = direct_settings['bytes'](data, "utf-8")
	return data
#

def direct_str(data):
#
	"""
Returns the string representing the (maybe encoded) input data

:param data: Input string

:return: (str) String representation
:since:  v0.1.00
	"""

	global direct_settings

	var_type = type(data)
	if (var_type != str and (var_type == direct_settings['bytes_type'] or var_type == direct_settings['unicode_type'])): data = direct_settings['str'](data, "utf-8")

	return data
#

def direct_unicode(data):
#
	"""
Returns the unicode data representing the (maybe encoded) input data

:param data: Input string

:return: (bytes) Unicode representation
:since:  v0.1.00
	"""

	global direct_settings
	if (type(data) != direct_settings['unicode_type']): data = direct_settings['unicode'](data, "utf-8")
	return data
#

##j## EOF