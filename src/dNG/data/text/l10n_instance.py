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

from dNG.data.binary import Binary
from dNG.data.cache.json_file_content import JsonFileContent

from .number_formatter import NumberFormatter

class L10nInstance(dict):
    """
L10n (localization) methods on top of an dict.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    def __init__(self, lang):
        """
Constructor __init__(L10n)

:param lang: Language code

:since: v0.2.00
        """

        dict.__init__(self)

        self.files = [ ]
        """
L10n files initialized
        """

        self['lang_code'] = lang
    #

    def __getitem__(self, key):
        """
python.org: Called to implement evaluation of self[key].

:param key: L10n key

:return: (str) L10n value
:since:  v0.2.00
        """

        return Binary.str(dict.__getitem__(self, key))
    #

    @property
    def lang(self):
        """
Returns the language code of this instance.

:return: (str) Language code
:since:  v1.0.0
        """

        return self['lang_code']
    #

    def format_number(self, number, fractional_digits = -1):
        """
Returns a formatted number.

:param number: Number as int or float
:param fractional_digits: Fractional digits to return
:param lang: Language code

:return: (str) Formatted value
:since:  v0.2.00
        """

        return NumberFormatter.format(number, self['lang_number_format'], fractional_digits)
    #

    def read_file(self, file_path_name, required = False):
        """
Read all translations from the given file.

:param file_path_name: File path and name
:param required: True if missing files should throw an exception

:since: v0.2.00
        """

        if (file_path_name not in self.files or JsonFileContent.is_changed(file_path_name)):
            json_data = JsonFileContent.read(file_path_name, required)
            if (type(json_data) is dict): self.update(json_data)
        #
    #

    def write_file(self, file_path_name, template_path_name):
        """
Write all translations to the given file using the given template.

:param file_path_name: File path and name of the translation file
:param template_path_name: File path and name of the translation template
       file

:return: (bool) True on success
:since:  v0.2.00
        """

        return False
    #
#
