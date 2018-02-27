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

from .binary import Binary
from .text.l10n import L10n
from .traced_exception import TracedException

class TranslatableException(TracedException):
    """
"TranslatableException" gets a l10n message ID to translate the exception
message to the selected language.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    def __init__(self, l10n_id, value = None, _exception = None):
        """
Constructor __init__(TranslatableException)

:param l10n_id: L10n translatable key (prefixed with "errors_")
:param value: Exception message value
:param _exception: Inner exception

:since: v1.0.0
        """

        self.l10n_message = L10n.get("errors_{0}".format(l10n_id), l10n_id)
        """
Translated message
        """

        if (value is None): value = self.l10n_message

        TracedException.__init__(self, value, _exception)
    #

    def __format__(self, format_spec):
        """
python.org: Convert a value to a "formatted" representation, as controlled by
format_spec.

:param format_spec: String format specification

:since: v1.0.0
        """

        if (format_spec == "l10n_message"): return Binary.str(self.l10n_message)
        else: TracedException.__format__(self, format_spec)
    #
#
