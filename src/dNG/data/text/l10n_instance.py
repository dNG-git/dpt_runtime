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
from .l10n_template import L10nTemplate

class L10nInstance(dict):
    """
L10n (localization) methods on top of an dict.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    def __init__(self, lang):
        """
Constructor __init__(L10n)

:param lang: Language code

:since: v1.0.0
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
:since:  v1.0.0
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

    def _apply_translate_rule(self, rule_list, number, kwargs):
        """
Applies the given translation rule definition list to the arguments if applicable.

:param rule_list: Translation rule definition list
:param number: Number as int or float
:param kwargs: Keyword arguments relevant for the rule definition list

:return: (str) L10n value
:since:  v1.0.0
        """

        _return = ''

        for rule_definition in rule_list:
            if (number is not None
                and type(rule_definition) is list
                and len(rule_definition) == 3
                and (rule_definition[0] is None or rule_definition[0] <= number)
                and (rule_definition[1] is None or rule_definition[1] >= number)
               ):
                _return = rule_definition[2]
                break
            elif (type(rule_definition) is dict
                  and 'conditions' in rule_definition
                  and type(rule_definition['conditions']) is dict
                  and 'value' in rule_definition
                 ):
                is_matched = True

                for condition_key in rule_definition['conditions']:
                    if (condition_key not in kwargs
                        or kwargs[condition_key] != rule_definition['conditions'][condition_key]
                       ):
                        is_matched = False
                        break
                    #
                #

                if (is_matched):
                    _return = (self._apply_translate_rule(rule_definition['value'], number, kwargs)
                               if (type(rule_definition['value']) is list) else
                               rule_definition['value']
                              )

                    break
                #
            #
        #

        return _return
    #

    def format_number(self, number, fractional_digits = -1):
        """
Returns a formatted number.

:param number: Number as int or float
:param fractional_digits: Fractional digits to return
:param lang: Language code

:return: (str) Formatted value
:since:  v1.0.0
        """

        return NumberFormatter.format(number, self['lang_number_format'], fractional_digits)
    #

    def read_file(self, file_path_name, required = False):
        """
Read all translations from the given file.

:param file_path_name: File path and name
:param required: True if missing files should throw an exception

:since: v1.0.0
        """

        if (file_path_name not in self.files or JsonFileContent.is_changed(file_path_name)):
            json_data = JsonFileContent.read(file_path_name, required)
            if (type(json_data) is dict): self.update(json_data)
        #
    #

    def translate(self, key, *args, **kwargs):
        """
Return a translation for the given key and arguments.

:param key: L10n key

:return: (str) L10n value
:since:  v1.0.0
        """

        l10n_value = self[key]
        number = None

        if (len(args) == 1 and isinstance(args[0], int) and 'n' not in kwargs):
            kwargs['n'] = args[0]
            number = args[0]
        #

        if (type(l10n_value) is list):
            l10n_value = self._apply_translate_rule(l10n_value, number, kwargs)
        #

        _return = l10n_value

        if ('%' in l10n_value):
            template = L10nTemplate(l10n_value)
            _return = template.safe_substitute(kwargs)
        #

        return _return
    #

    def write_file(self, file_path_name, template_path_name):
        """
Write all translations to the given file using the given template.

:param file_path_name: File path and name of the translation file
:param template_path_name: File path and name of the translation template
       file

:return: (bool) True on success
:since:  v1.0.0
        """

        return False
    #
#
