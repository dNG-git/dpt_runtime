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

from dNG.data.text.l10n import L10n
from dNG.module.named_loader import NamedLoader

class TestDataTextL10n(unittest.TestCase):
    """
UnitTest for dNG.data.text.L10n

:since: v0.1.01
    """

    def setUp(self):
        cache_instance = NamedLoader.get_singleton("dNG.data.cache.Content", False)
        if (cache_instance is not None): cache_instance.disable()

        self.de_dict = L10n.get_dict("de")
        L10n.init("core", "de")
        L10n.init("core", "en")
    #

    def test_format_number(self):
        """
One key tests everything :)
        """

        self.assertEqual("1234.568", L10n.format_number(1234567.895, 0))
        self.assertEqual("1234.567,90", L10n.format_number(1234567.895, 2))
        self.assertEqual("1234.567,123456", L10n.format_number(1234567.123456))
        self.assertEqual("1234,568", L10n.format_number(1234567.895, 0, lang = "en"))
        self.assertEqual("1234,567.90", L10n.format_number(1234567.895, 2, lang = "en"))
        self.assertEqual("1,235", L10n.format_number(1.234567895, 3))
    #

    def test_value(self):
        """
One key tests everything :)
        """

        self.assertEqual("de-DE", self.de_dict.get("lang_rfc_region"))
        self.assertEqual("en-US", L10n.get("lang_rfc_region", lang = "en"))
    #
#

if (__name__ == "__main__"):
    unittest.main()
#
