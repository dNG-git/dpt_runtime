# -*- coding: utf-8 -*-
##j## BOF

"""
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?pas;core

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;mpl2
----------------------------------------------------------------------------
#echo(pasCoreVersion)#
#echo(__FILEPATH__)#
"""

# pylint: disable=invalid-name,no-member,undefined-variable

try:
#
	_PY_BYTES = unicode.encode
	_PY_BYTES_TYPE = str
	_PY_STR = unicode.encode
	_PY_UNICODE = str.decode
	_PY_UNICODE_TYPE = unicode
#
except NameError:
#
	_PY_BYTES = str.encode
	_PY_BYTES_TYPE = bytes
	_PY_STR = bytes.decode
	_PY_UNICODE = bytes.decode
	_PY_UNICODE_TYPE = str
#

class Binary(object):
#
	"""
Python 2.x and Python 3.x handle UTF-8 strings differently. This class
abstracts this behaviour.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	BYTES_TYPE = _PY_BYTES_TYPE
	"""
Bytes data type
	"""
	UNICODE_TYPE = _PY_UNICODE_TYPE
	"""
Unicode string data type
	"""

	@staticmethod
	def bytes(data):
	#
		"""
Returns the bytes representing the (maybe encoded) input data.

:param data: Input string

:return: (bytes) Byte representation
:since:  v0.1.00
	"""

		# global: _PY_BYTES, _PY_BYTES_TYPE

		if (str != _PY_BYTES_TYPE and isinstance(data, str)): data = _PY_BYTES(data, "raw_unicode_escape")
		return data
	#

	@staticmethod
	def raw_str(data):
	#
		"""
Returns the string representing the (maybe encoded) input data.

:param data: Input string

:return: (str) String representation
:since:  v0.1.00
		"""

		# global: _PY_STR, _PY_BYTES_TYPE, _PY_UNICODE_TYPE

		if ((not isinstance(data, str))
		    and (isinstance(data, _PY_BYTES_TYPE) or isinstance(data, _PY_UNICODE_TYPE))
		   ): data = _PY_STR(data, "raw_unicode_escape")

		return data
	#

	@staticmethod
	def str(data):
	#
		"""
Returns the string representing the (maybe UTF-8 encoded) input data.

:param data: Input string

:return: (str) String representation
:since:  v0.1.00
		"""

		# global: _PY_STR, _PY_BYTES_TYPE, _PY_UNICODE_TYPE

		if ((not isinstance(data, str))
		    and (isinstance(data, _PY_BYTES_TYPE) or isinstance(data, _PY_UNICODE_TYPE))
		   ): data = _PY_STR(data, "utf-8")

		return data
	#

	@staticmethod
	def utf8(data):
	#
		"""
Returns the unicode data representing the (maybe encoded) input data.

:param data: Input string

:return: (bytes) Unicode representation
:since:  v0.1.00
		"""

		# global: _PY_BYTES_TYPE, _PY_UNICODE, _PY_UNICODE_TYPE

		if (str != _PY_UNICODE_TYPE and isinstance(data, str)): data = _PY_UNICODE(data, "utf-8")
		elif (str == _PY_UNICODE_TYPE and isinstance(data, _PY_BYTES_TYPE)): data = _PY_STR(data, "utf-8")

		return data
	#

	@staticmethod
	def utf8_bytes(data):
	#
		"""
Returns the bytes representing the (maybe UTF-8 encoded) input data.

:param data: Input string

:return: (bytes) Byte representation
:since:  v0.1.00
	"""

		# global: _PY_BYTES, _PY_BYTES_TYPE

		if (str != _PY_BYTES_TYPE and isinstance(data, str)): data = _PY_BYTES(data, "utf-8")
		return data
	#
#

##j## EOF