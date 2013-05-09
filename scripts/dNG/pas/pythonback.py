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

try:
#
	_PY_BYTES = unicode.encode
	PY_BYTES_TYPE = str
	_PY_STR = unicode.encode
	_PY_UNICODE = str.decode
	PY_UNICODE_TYPE = unicode
#
except:
#
	_PY_BYTES = str.encode
	PY_BYTES_TYPE = bytes
	_PY_STR = bytes.decode
	_PY_UNICODE = bytes.decode
	PY_UNICODE_TYPE = str
#

def direct_bytes(data):
#
	"""
Returns the bytes representing the (maybe encoded) input data

:param data: Input string

:return: (bytes) Byte representation
:since:  v0.1.00
	"""

	global _PY_BYTES, PY_BYTES_TYPE
	if (type(data) != PY_BYTES_TYPE): data = _PY_BYTES(data, "utf-8")
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

	global _PY_STR, PY_BYTES_TYPE, PY_UNICODE_TYPE

	var_type = type(data)
	if (var_type != str and (var_type == PY_BYTES_TYPE or var_type == PY_UNICODE_TYPE)): data = _PY_STR(data, "utf-8")

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

	global _PY_UNICODE, PY_UNICODE_TYPE
	if (type(data) != PY_UNICODE_TYPE): data = _PY_UNICODE(data, "utf-8")
	return data
#

##j## EOF