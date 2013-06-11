# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.logging.abstract_log_handler
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

import logging, re, sys, traceback

from dNG.pas.data.binary import direct_binary
from dNG.pas.data.exception import direct_exception

class direct_abstract_log_handler(object):
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
Constructor __init__(direct_abstract_log_handler)

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

	def get_line(self, data):
	#
		"""
Get the formatted log message.

:param data: Log data

:access: protected
:return: (str) Formatted log line
:since:  v0.1.00
		"""

		if (isinstance(data, direct_exception)): data = str(data)
		elif (isinstance(data, Exception)):
		#
			try:
			# Try to extract exception - might result in the wrong one
				( exc_type, exc_value, exc_traceback ) = sys.exc_info()
				data = "{0} {1}".format(repr(data), "".join(traceback.format_exception(exc_type, exc_value, exc_traceback)))
			#
			except: data = repr(data)
		#
		else:
		#
			data = direct_binary.str(data)
			if (type(data) != str): data = repr(data)
		#

		if ("\n" in data or "\r" in data): data = "\"" + re.sub("[\n\r]", "\"; \"", data) + "\""
		var_return = "{0} {1} {2}".format(self.ident, data, self.version)

		return var_return
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