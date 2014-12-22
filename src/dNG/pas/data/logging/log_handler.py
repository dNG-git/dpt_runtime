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

# pylint: disable=import-error,undefined-variable

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

if (_api_type is None):
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
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	_appender_defined = False
	"""
Append log file handlers only once
	"""
	_weakref_instance = None
	"""
LogHandler weakref instance
	"""
	_weakref_lock = InstanceLock()
	"""
Thread safety weakref lock
	"""

	# pylint: disable=maybe-no-member

	def __init__(self):
	#
		"""
Constructor __init__(LogHandler)

:since: v0.1.00
		"""

		# global: _api_type, _API_JAVA

		AbstractLogHandler.__init__(self)

		self.logger = None
		"""
Logger object
		"""
		self.log_file_path_name = None
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

		self.level_map = { "debug": DEBUG,
		                   "error": ERROR,
		                   "info": INFO,
		                   "warning": WARNING
		                 }

		level = Settings.get("pas_core_log_level")
		if (level is None): level = Settings.get("core_log_level", "warning")
		self.level['global'] = self.level_map.get(level, WARNING)

		self.logger = logging.getLogger(self.ident)
		self.logger.setLevel(DEBUG)

		if (not LogHandler._appender_defined):
		#
			log_file_path_name = Settings.get("pas_core_log_path_name")

			if (Settings.is_defined("pas_core_log_path_name")):
			#
				log_file_path_name = path.normpath(log_file_path_name)

				if (os.access(log_file_path_name, os.W_OK)
				    or ((not os.access(log_file_path_name, os.F_OK)) and os.access(path.split(log_file_path_name)[0], os.W_OK))
				   ): self.log_file_path_name = log_file_path_name
			#

			if (self.log_file_path_name is None and Settings.is_defined("pas_core_log_name")):
			#
				log_file_path_name = path.join(Settings.get("path_base"), "log", Settings.get("pas_core_log_name"))

				if (os.access(log_file_path_name, os.W_OK)
				    or ((not os.access(log_file_path_name, os.F_OK)) and os.access(path.join(Settings.get("path_base"), "log"), os.W_OK))
				   ): self.log_file_path_name = log_file_path_name
			#

			if (self.log_file_path_name is None): self.log_file_path_name = path.join(Settings.get("path_base"), "pas.log")

			if (_api_type == _API_JAVA):
			#
				try: self.log_handler = RotatingFileHandler(SimpleLayout(), self.log_file_path_name, encoding = "utf-8")
				except TypeError: self.log_handler = RotatingFileHandler(SimpleLayout(), self.log_file_path_name)

				self.log_handler.setLevel(DEBUG)
				self.log_handler.setMaxBackupIndex(self.log_file_rotates)
				self.log_handler.setMaximumFileSize(self.log_file_size_max)

				logger_root = logging.getRootLogger()

				if (len(logger_root.getAllAppenders()) < 1): logger_root.addAppender(self.log_handler)
				else: self.logger.addAppender(self.log_handler)
			#
			else:
			#
				self.log_handler = RotatingFileHandler(self.log_file_path_name, maxBytes = self.log_file_size_max, backupCount = self.log_file_rotates)
				logger_root = logging.getLogger()

				if ((hasattr(logger_root, "hasHandlers") and logger_root.hasHandlers()) or (len(logger_root.handlers) > 0)): self.logger.addHandler(self.log_handler)
				else: logger_root.addHandler(self.log_handler)
			#

			LogHandler._appender_defined = True
		#
	#

	def add_logger(self, name):
	#
		"""
Add the logger name given to the active log handler.

:return: (object) Log handler
:since:  v0.1.00
		"""

		# global: _api_type, _API_JAVA

		if (_api_type == _API_JAVA): logging.getLogger(name).addAppender(self.log_handler)
		else: AbstractLogHandler.add_logger(self, name)
	#

	def debug(self, data, *args, **kwargs):
	#
		"""
Debug message method

:param data: Debug data
:param context: Logging context

:since: v0.1.00
		"""

		# pylint: disable=star-args

		context = kwargs.get("context", "global")
		if (self._get_implementation_level(context) == DEBUG): self._write(DEBUG, data, *args)
	#

	def error(self, data, *args, **kwargs):
	#
		"""
Error message method

:param data: Error data
:param context: Logging context

:since: v0.1.00
		"""

		# pylint: disable=star-args

		context = kwargs.get("context", "global")
		if (self._get_implementation_level(context) != NOTSET): self._write(ERROR, data, *args)
	#

	def info(self, data, *args, **kwargs):
	#
		"""
Info message method

:param data: Info data
:param context: Logging context

:since: v0.1.00
		"""

		# pylint: disable=star-args

		level = self._get_implementation_level(kwargs.get("context", "global"))
		if (level in ( DEBUG, INFO)): self._write(INFO, data, *args)
	#

	def _load_context_level(self, context):
	#
		"""
Determines the context specific log level.

:param context: Logging context

:since: v0.1.00
		"""

		context_level_setting = "{0}_log_level".format(context)

		if (context != "global"):
		#
			self.set_level((Settings.get(context_level_setting)
			                if (Settings.is_defined(context_level_setting)) else
			                self.get_level("global")
			               ),
			               context
			              )
		#
	#

	def warning(self, data, *args, **kwargs):
	#
		"""
Warning message method

:param data: Warning data
:param context: Logging context

:since: v0.1.00
		"""

		# pylint: disable=star-args

		level = self._get_implementation_level(kwargs.get("context", "global"))
		if (level not in ( ERROR, NOTSET)): self._write(WARNING, data, *args)
	#

	def _write(self, level, data, *args):
	#
		"""
"_write()" adds all messages to the logger instance.

:param level: Logging level
:param data: Logging data

:since: v0.1.00
		"""

		# pylint: disable=star-args

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

		message = "{0} {1}".format(message, self._get_line(data, *args))

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

		with LogHandler._weakref_lock:
		#
			if (LogHandler._weakref_instance is not None): _return = LogHandler._weakref_instance()

			if (_return is None):
			#
				_return = LogHandler()
				LogHandler._weakref_instance = ref(_return)
			#
		#

		return _return
	#
#

##j## EOF