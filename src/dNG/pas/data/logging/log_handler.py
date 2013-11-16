# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.logging.LogHandler
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
from time import strftime
from weakref import ref
import os

from dNG.pas.data.settings import Settings
from dNG.pas.runtime.instance_lock import InstanceLock
from .abstract_log_handler import AbstractLogHandler

_API_JAVA = 1
"""
Java based log handlers
"""
_API_PYTHON = 2
"""
Python log handlers
"""

try:
#
	from logging import CRITICAL, DEBUG, ERROR, INFO, NOTSET, WARNING
	from logging.handlers import RotatingFileHandler
	import logging

	if (hasattr(logging, "logMultiprocessing")): logging.logMultiprocessing = False
	_api_type = _API_PYTHON
#
except ImportError: _api_type = None

if (_api_type == None):
#
	from org.apache.log4j import Logger as logging
	from org.apache.log4j import RollingFileAppender as RotatingFileHandler
	from org.apache.log4j import SimpleLayout
	from org.apache.log4j.Level import DEBUG, ERROR, INFO
	from org.apache.log4j.Level import FATAL as CRITICAL
	from org.apache.log4j.Level import OFF as NOTSET
	from org.apache.log4j.Level import WARN as WARNING
	_api_type = _API_JAVA
#

class LogHandler(AbstractLogHandler):
#
	"""
"LogHandler" is the default logging endpoint writing messages to a file.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	appender_defined = False
	"""
Append log file handlers only once
	"""
	weakref_instance = None
	"""
LogHandler weakref instance
	"""
	weakref_lock = InstanceLock()
	"""
Thread safety weakref lock
	"""

	def __init__(self):
	#
		"""
Constructor __init__(LogHandler)

:since: v0.1.00
		"""

		global _api_type, _API_JAVA

		AbstractLogHandler.__init__(self)

		self.logger = None
		"""
Logger object
		"""
		self.log_file_pathname = None
		"""
Path and filename of the log file
		"""
		self.log_format_datetime = Settings.get("pas_core_log_datetime", "%m/%d/%Y %H:%M:%S")
		"""
Date/Time format
		"""
		self.log_file_size_max = int(Settings.get("pas_core_log_size_max", 104857600))
		"""
File size a log file gets rotated
		"""
		self.log_file_rotates = int(Settings.get("pas_core_log_rotates", 5))
		"""
Preserve the amount of files
		"""

		self.levels = {
			"debug": DEBUG,
			"error": ERROR,
			"info": INFO,
			"warning": WARNING
		}

		level = Settings.get("pas_core_log_level")
		if (level == None): level = Settings.get("core_log_level", "warning")
		self.level = (self.levels[level] if (level in self.levels) else WARNING)

		self.logger = logging.getLogger(self.ident)
		self.logger.setLevel(self.level)

		if (not LogHandler.appender_defined):
		#
			if (Settings.is_defined("pas_core_log_pathname") and os.access(path.normpath(Settings.get("pas_core_log_pathname")), os.W_OK)): self.log_file_pathname = path.normpath(Settings.get("pas_core_log_pathname"))
			elif (Settings.is_defined("pas_core_log_name") and (os.access(path.normpath("{0}/log/{1}".format(Settings.get("path_base"), Settings.get("pas_core_log_name"))), os.W_OK) or ((not os.access(path.normpath("{0}/log/{1}".format(Settings.get("path_base"), Settings.get("pas_core_log_name"))), os.F_OK)) and os.access(path.normpath("{0}/log".format(Settings.get("path_base"))), os.W_OK)))): self.log_file_pathname = path.normpath("{0}/log/{1}".format(Settings.get("path_base"), Settings.get("pas_core_log_name")))
			else: self.log_file_pathname = path.normpath("{0}/pas.log".format(Settings.get("path_base")))

			if (_api_type == _API_JAVA):
			#
				self.log_handler = RotatingFileHandler(SimpleLayout(), self.log_file_pathname)
				self.log_handler.setLevel(self.level)
				self.log_handler.setMaxBackupIndex(self.log_file_rotates)
				self.log_handler.setMaximumFileSize(self.log_file_size_max)

				logger_root = logging.getRootLogger()

				if (len(logger_root.getAllAppenders()) < 1): logger_root.addAppender(self.log_handler)
				else: self.logger.addAppender(self.log_handler)
			#
			else:
			#
				self.log_handler = RotatingFileHandler(self.log_file_pathname, maxBytes = self.log_file_size_max, backupCount = self.log_file_rotates)
				logger_root = logging.getLogger()

				if ((hasattr(logger_root, "hasHandlers") and logger_root.hasHandlers()) or (len(logger_root.handlers) > 0)): self.logger.addHandler(self.log_handler)
				else: logger_root.addHandler(self.log_handler)
			#

			LogHandler.appender_defined = True
		#
	#

	def add_logger(self, name):
	#
		"""
Add the logger name given to the active log handler.

:return: (object) Log handler
:since:  v0.1.00
		"""

		global _api_type, _API_JAVA

		if (_api_type == _API_JAVA): logging.getLogger(name).addAppender(self.log_handler)
		else: AbstractLogHandler.add_logger(self, name)
	#

	def debug(self, data):
	#
		"""
Debug message method

:param data: Debug data

:since: v0.1.00
		"""

		if (self.level == DEBUG): self._write(DEBUG, data)
	#

	def error(self, data):
	#
		"""
Error message method

:param data: Error data

:since: v0.1.00
		"""

		if (self.level != NOTSET): self._write(ERROR, data)
	#

	def info(self, data):
	#
		"""
Info message method

:param data: Info data

:since: v0.1.00
		"""

		if (self.level == DEBUG or self.level == INFO): self._write(INFO, data)
	#

	def warning(self, data):
	#
		"""
Warning message method

:param data: Warning data

:since: v0.1.00
		"""

		if (self.level != ERROR and self.level != NOTSET): self._write(WARNING, data)
	#

	def _write(self, level, data):
	#
		"""
"_write()" adds all messages to the logger instance.

:param level: Logging level
:param data: Logging data

:since: v0.1.00
		"""

		exception = isinstance(data, BaseException)
		message = strftime(self.log_format_datetime)

		if (exception):
		#
			level = CRITICAL
			message = "<exception> {0}".format(message)
		#
		elif (level == ERROR): message = "<error>     {0}".format(message)
		elif (level == WARNING): message = "<warning>   {0}".format(message)
		elif (level == INFO): message = "<info>      {0}".format(message)
		elif (level == DEBUG): message = "<debug>     {0}".format(message)

		message = "{0} {1}".format(message, self._get_line(data))

		if (level == CRITICAL): self.logger.critical(message)
		elif (level == ERROR): self.logger.error(message)
		elif (level == WARNING): self.logger.warning(message)
		elif (level == DEBUG): self.logger.debug(message)
		elif (level == INFO): self.logger.info(message)
	#

	@staticmethod
	def get_instance():
	#
		"""
Get the LogHandler singleton.

:return: (LogHandler) Object on success
:since:  v0.1.00
		"""

		_return = None

		with LogHandler.weakref_lock:
		#
			if (LogHandler.weakref_instance != None): _return = LogHandler.weakref_instance()

			if (_return == None):
			#
				_return = LogHandler()
				LogHandler.weakref_instance = ref(_return)
			#
		#

		return _return
	#
#

##j## EOF