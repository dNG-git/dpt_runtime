# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.logging.AbstractLogHandler
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

import logging
import re
import sys
import traceback

from dNG.pas.data.binary import Binary
from dNG.pas.data.traced_exception import TracedException

class AbstractLogHandler(object):
#
	"""
The abstract log handler provides common variables and methods.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self):
	#
		"""
Constructor __init__(AbstractLogHandler)

:since: v0.1.00
		"""

		self.ident = "pas"
		"""
Log identifier
		"""
		self.level = None
		"""
Log level
		"""
		self.levels = { }
		"""
Mapped log levels
		"""
		self.log_handler = None
		"""
The configured log handler
		"""
		self.version = "#echo(pasCoreVersion)#"
		"""
Version identifier
		"""
	#

	def add_logger(self, name):
	#
		"""
Add the logger name given to the active log handler.

:return: (object) Log handler
:since:  v0.1.00
		"""

		logging.getLogger(name).addHandler(self.log_handler)
	#

	def get_level(self):
	#
		"""
Get the log level.

:return: (str) Log level
:since:  v0.1.00
		"""

		return self.levels.index(self.level)
	#

	def _get_line(self, data):
	#
		"""
Get the formatted log message.

:param data: Log data

:return: (str) Formatted log line
:since:  v0.1.00
		"""

		if (isinstance(data, TracedException)): data = data.get_printable_trace()
		elif (isinstance(data, BaseException)):
		#
			try:
			# Try to extract exception - might result in the wrong one
				( exc_type, exc_value, exc_traceback ) = sys.exc_info()
				data = "{0} {1}".format(repr(data), "".join(traceback.format_exception(exc_type, exc_value, exc_traceback)))
			#
			except Exception: data = repr(data)
		#
		else:
		#
			data = Binary.str(data)
			if (type(data) != str): data = repr(data)
		#

		if ("\n" in data or "\r" in data): data = "\"" + re.sub("[\n\r]", "\"; \"", data) + "\""
		_return = "{0} {1} {2}".format(self.ident, data, self.version)

		return _return
	#

	def set_level(self, level):
	#
		"""
Sets the log level.

:param level: Log level

:since: v0.1.00
		"""

		if (level in self.levels): self.level = self.levels[level]
	#
#

##j## EOF