# -*- coding: utf-8 -*-

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

import unittest

try:
    _PY_BYTES = unicode.encode
    _PY_BYTES_TYPE = str
    _PY_STR = unicode.encode
    _PY_UNICODE = str.decode
    _PY_UNICODE_TYPE = unicode
except NameError:
    _PY_BYTES = str.encode
    _PY_BYTES_TYPE = bytes
    _PY_STR = bytes.decode
    _PY_UNICODE = bytes.decode
    _PY_UNICODE_TYPE = str
#

from dNG.data.binary import Binary

class TestDataBinary(unittest.TestCase):
    """
UnitTest for dNG.data.Binary

:since: v0.1.01
    """

    def test_formats(self):
        # global: _PY_BYTES, _PY_BYTES_TYPE, _PY_STR, _PY_UNICODE, _PY_UNICODE_TYPE

        self.assertEqual(_PY_BYTES_TYPE, type(Binary.bytes("data")))
        self.assertEqual(str, type(Binary.raw_str("data")))
        self.assertEqual(str, type(Binary.str("data")))
        self.assertEqual(_PY_UNICODE_TYPE, type(Binary.utf8("data")))
        self.assertEqual(_PY_BYTES_TYPE, type(Binary.utf8_bytes("data")))
    #
#

if (__name__ == "__main__"):
    unittest.main()
#
