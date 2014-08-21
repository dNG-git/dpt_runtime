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

from os import path
import sys
import unittest

from dNG.pas.data.text.tmd5 import Tmd5

class TestDataTextTmd5(unittest.TestCase):
#
	"""
UnitTest for dNG.pas.data.text.Tmd5

:since: v0.1.01
	"""

	def test_values(self):
	#
		self.assertEqual("8f98a27ba7566c4ddca2a67902b4ba9cfa4cb410c65df90385bad89355ea1338f0f6430e187e05326ff0b32f9811a3d6", Tmd5.hash("Hello world"))
		self.assertEqual("d3cc8d008571a9d367ba954bef5ebab1e115bd839d6aee498354a214310792d40338a7e1bc545a0ba06dc0d0c37139bd", Tmd5.hash("Hello world", "some_random_binary_value_should_be_used_here"))
		self.assertEqual("e212d1deb155ec764023171f700178f24fdd3c00473b61d0c9c81e784613474cdf1c6e99c2e97bd276110870405c24bc", Tmd5.password_hash("Hello world", "some_random_binary_value_should_be_used_here", "additional pepper :)"))
	#
#

if (__name__ == "__main__"):
#
	sys.path.append(path.normpath("../src"))
	unittest.main()
#

##j## EOF