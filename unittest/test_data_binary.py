# -*- coding: utf-8 -*-
##j## BOF

"""
UnitTest for dNG.pas.data.Binary
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

from os import path
import sys
import unittest

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

from dNG.pas.data.binary import Binary

class TestDataBinary(unittest.TestCase):
#
	def test_formats(self):
	#
		# global: _PY_BYTES, _PY_BYTES_TYPE, _PY_STR, _PY_UNICODE, _PY_UNICODE_TYPE

		self.assertEqual(_PY_BYTES_TYPE, type(Binary.bytes("data")))
		self.assertEqual(str, type(Binary.raw_str("data")))
		self.assertEqual(str, type(Binary.str("data")))
		self.assertEqual(_PY_UNICODE_TYPE, type(Binary.utf8("data")))
		self.assertEqual(_PY_BYTES_TYPE, type(Binary.utf8_bytes("data")))
	#
#

if (__name__ == "__main__"):
#
	sys.path.append(path.normpath("../src"))
	unittest.main()
#

##j## EOF