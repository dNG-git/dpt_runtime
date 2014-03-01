# -*- coding: utf-8 -*-
##j## BOF

"""
UnitTest for dNG.pas.data.text.L10n
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

from dNG.pas.data.text.l10n import L10n

class TestDataTextL10n(unittest.TestCase):
#
	def setUp(self):
	#
		self.de = L10n.get_instance("de")
		self.de.init("core")
	#

	def test_value(self):
	#
		"""
One key tests everything :)
		"""

		self.assertEqual("de-DE", self.de.get("lang_rfc_region"))
	#
#

if (__name__ == "__main__"):
#
	sys.path.append(path.normpath("../src"))
	unittest.main()
#

##j## EOF