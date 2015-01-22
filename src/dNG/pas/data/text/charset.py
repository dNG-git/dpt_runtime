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

from dNG.pas.data.binary import Binary

try:
#
	_PY_BYTES_TYPE = str
	_PY_STR = unicode.encode
	_PY_UNICODE = str.decode
	_PY_UNICODE_TYPE = unicode
#
except NameError:
#
	_PY_BYTES_TYPE = bytes
	_PY_STR = bytes.decode
	_PY_UNICODE = bytes.decode
	_PY_UNICODE_TYPE = str
#

class Charset(object):
#
	"""
Helper methods to convert charsets to (UTF-8) strings. Both data types are
used throughout the Python Application Services but always with the UTF-8
charset.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	@staticmethod
	def convert_to_str(data, charset):
	#
		"""
Convert data from the input charset to their UTF-8 string representation.

:param data: Input string
:param charset: Original data charset

:return: (bytes) Byte representation
:since:  v0.1.00
	"""

		return Binary.str(Charset.convert_to_utf8(data, charset))
	#

	@staticmethod
	def convert_to_utf8(data, charset):
	#
		"""
Returns the unicode data representing the (maybe encoded) input data.

:param data: Input string
:param charset: Original data charset

:return: (bytes) Unicode representation
:since:  v0.1.00
		"""

		# global: _PY_BYTES, _PY_BYTES_TYPE, _PY_UNICODE, _PY_UNICODE_TYPE

		if (str is not _PY_UNICODE_TYPE and isinstance(data, str)): data = _PY_UNICODE(data, charset)
		elif (str is _PY_UNICODE_TYPE and isinstance(data, _PY_BYTES_TYPE)): data = _PY_STR(data, charset)

		return data
	#
#

##j## EOF