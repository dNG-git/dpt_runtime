# -*- coding: utf-8 -*-
##j## BOF

"""
UnitTest for dNG.pas.data.text.Tmd5
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

from dNG.pas.data.text.tmd5 import Tmd5

class TestTmd5(unittest.TestCase):
#
	def test_values(self):
	#
		self.assertEqual("8f98a27ba7566c4ddca2a67902b4ba9cfa4cb410c65df90385bad89355ea1338f0f6430e187e05326ff0b32f9811a3d6", Tmd5.hash("Hello world"))
		self.assertEqual("2cef7df359d3944e4d8ab2900773ec9b12313a3d28f802e3a22b07d2e01c6dcf05f21388389da3241f2e3663398397c4", Tmd5.hash("Hello world", "some_random_binary_value_should_be_used_here"))
	#
#

if (__name__ == "__main__"):
#
	sys.path.append(path.normpath("../src"))
	unittest.main()
#

##j## EOF