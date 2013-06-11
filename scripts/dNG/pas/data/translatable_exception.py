# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.translatable_exception
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

from .binary import direct_binary
from .exception import direct_exception
from .text.l10n import direct_l10n

class direct_translatable_exception(direct_exception):
#
	"""
"direct_translatable_exception" gets a l10n message ID to translate the
exception message to the selected language.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self, l10n_id, value = None, py_exception = None):
	#
		"""
Constructor __init__(direct_translatable_exception)

:param l10n_id: L10n translatable key (prefixed with "errors_")
:param value: Exception message value
:param py_exception: Inner exception

:since: v0.1.00
		"""

		self.l10n_message = direct_l10n.get("errors_{0}".format(l10n_id), l10n_id)
		"""
Translated message
		"""

		if (value == None): value = self.l10n_message

		direct_exception.__init__(self, value, py_exception)
	#

	def __format__(self, format_spec):
	#
		"""
python.org: Convert a value to a "formatted" representation, as controlled by
format_spec.

:param format_spec: String format specification

:since: v0.1.00
		"""

		if (format_spec == "l10n_message"): return direct_binary.str(self.l10n_message)
		else: direct_exception.__format__(self, format_spec)
	#
#

##j## EOF