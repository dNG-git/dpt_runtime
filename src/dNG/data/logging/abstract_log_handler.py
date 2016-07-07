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

from threading import current_thread
import logging
import re
import sys
import traceback

from dNG.data.binary import Binary
from dNG.data.traced_exception import TracedException
from dNG.runtime.not_implemented_exception import NotImplementedException
from dNG.runtime.value_exception import ValueException

class AbstractLogHandler(object):
#
	"""
The abstract log handler provides common variables and methods.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self):
	#
		"""
Constructor __init__(AbstractLogHandler)

:since: v0.2.00
		"""

		self.ident = "pas"
		"""
Log identifier
		"""
		self.level = { }
		"""
Log level
		"""
		self.level_map = { }
		"""
Mapped log levels
		"""
		self.log_handler = None
		"""
The configured log handler
		"""
		self.log_thread_id = False
		"""
True to add the thread ID to each log line as well
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
:since:  v0.2.00
		"""

		logging.getLogger(name).addHandler(self.log_handler)
	#

	def debug(self, data, *args, **kwargs):
	#
		"""
Debug message method

:param data: Debug data
:param context: Logging context

:since: v0.2.00
		"""

		# pylint: disable=star-args

		raise NotImplementedException()
	#

	def error(self, data, *args, **kwargs):
	#
		"""
Error message method

:param data: Error data
:param context: Logging context

:since: v0.2.00
		"""

		# pylint: disable=star-args

		raise NotImplementedException()
	#

	def _get_implementation_level(self, context = "global"):
	#
		"""
Returns the log implementation specific level value.

:param context: Logging context

:return: (mixed) Log implementation specific level value
:since:  v0.2.00
		"""

		if (context not in self.level): self._load_context_level(context)
		return self.level[context]
	#

	def get_level(self, context = "global"):
	#
		"""
Get the log level.

:param context: Logging context

:return: (mixed) Log level
:since:  v0.2.00
		"""

		if (context not in self.level): self._load_context_level(context)

		level_matches = [ k for k, v in self.level_map.items() if self.level[context] == v ]

		if (len(level_matches) > 0): _return = level_matches[0]
		elif (context != "global" and len(level_matches) < 0): _return = self.get_level("global")
		else: raise ValueException("Log level can not be identified")

		return _return
	#

	def _get_line(self, data, *args):
	#
		"""
Get the formatted log message.

:param data: Log data

:return: (str) Formatted log line
:since:  v0.2.00
		"""

		# pylint: disable=broad-except,star-args

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

			if (type(data) is not str): data = repr(data)
			elif (len(args) > 0): data = data.format(*args)
		#

		if ("\n" in data or "\r" in data): data = "\"" + re.sub("[\n\r]", "\"; \"", data) + "\""

		ident = self.ident
		if (self.log_thread_id): ident += " [Thread {0}]".format(current_thread().ident)

		_return = "{0} {1} {2}".format(ident, data, self.version)

		return _return
	#

	def info(self, data, *args, **kwargs):
	#
		"""
Info message method

:param data: Info data
:param context: Logging context

:since: v0.2.00
		"""

		# pylint: disable=star-args

		raise NotImplementedException()
	#

	def _load_context_level(self, context):
	#
		"""
Determines the context specific log level.

:param context: Logging context

:since: v0.2.00
		"""

		if (context != "global"): self.level[context] = self.level['global']
	#

	def set_level(self, level, context = "global"):
	#
		"""
Sets the log level.

:param level: Log level identifier
:param context: Logging context

:since: v0.2.00
		"""

		if (level in self.level_map): self.level[context] = self.level_map[level]
	#

	def warning(self, data, *args, **kwargs):
	#
		"""
Warning message method

:param data: Warning data
:param context: Logging context

:since: v0.2.00
		"""

		# pylint: disable=star-args

		raise NotImplementedException()
	#

	@staticmethod
	def get_instance():
	#
		"""
Get the LogHandler singleton.

:return: (LogHandler) Object on success
:since:  v0.2.00
		"""

		raise NotImplementedException()
	#
#

##j## EOF