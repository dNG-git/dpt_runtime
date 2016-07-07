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

from dNG.data.settings import Settings

class TestDataSettings(unittest.TestCase):
#
	"""
UnitTest for dNG.data.Settings

:since: v0.1.01
	"""

	def setUp(self): self.settings = Settings.get_instance()

	def test_paths(self):
	#
		path_base = path.abspath("..")

		self.assertEqual(path_base, self.settings.get("path_base"))
		self.assertEqual("{0}/data".format(path_base), self.settings.get("path_data"))
		self.assertEqual("{0}/lang".format(path_base), self.settings.get("path_lang"))
		self.assertEqual("{0}/src".format(path_base), self.settings.get("path_system"))
	#

	def test_import_json(self):
	#
		"""
Valid JSON
		"""

		json = """
{
"hello": "world",
"more_complex": [ "this", "that", true, 1 ]
}
		"""

		self.assertTrue(Settings._import_file_json(json))
		self.assertEqual("world", self.settings.get("hello"))
		self.assertEqual("that", self.settings.get("more_complex")[1])
		self.assertEqual(1, self.settings.get("more_complex")[2])

		"""
Invalid JSON
		"""

		json = "{ 'hello': 'world' }"
		self.assertFalse(Settings._import_file_json(json))
	#

	def test_read_file(self):
	#
		Settings.read_file("{0}/settings/core.json".format(self.settings.get("pas_data")))
		self.assertEqual("en", self.settings.get("core_lang"))
	#

	def test_value(self):
	#
		self.assertIsNone(self.settings.get("test_value"))
		self.assertEqual("", self.settings.get("test_value", ""))

		self.settings.set("test_value", "set works")
		self.assertEqual("set works", self.settings.get("test_value"))
	#
#

if (__name__ == "__main__"):
#
	sys.path.append(path.normpath("../src"))
	unittest.main()
#

##j## EOF