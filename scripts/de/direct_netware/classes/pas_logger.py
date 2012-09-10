# -*- coding: utf-8 -*-
##j## BOF

"""
de.direct_netware.classes.pas_logger

@internal  We are using epydoc (JavaDoc style) to automate the documentation
           process for creating the Developer's Manual.
           Use the following line to ensure 76 character sizes:
----------------------------------------------------------------------------
@author    direct Netware Group
@copyright (C) direct Netware Group - All rights reserved
@package   pas_core
@since     v0.1.00
@license   http://www.direct-netware.de/redirect.php?licenses;mpl2
           Mozilla Public License, v. 2.0
"""
"""n// NOTE
----------------------------------------------------------------------------
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
http://www.direct-netware.de/redirect.php?pas

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
http://www.direct-netware.de/redirect.php?licenses;mpl2
----------------------------------------------------------------------------
#echo(pasCoreVersion)#
pas/#echo(__FILEPATH__)#
----------------------------------------------------------------------------
NOTE_END //n"""

from os import path
from time import strftime
import re

try:
#
	from logging import CRITICAL,DEBUG,ERROR,INFO,WARNING
	from logging.handlers import RotatingFileHandler
	import logging

	if (hasattr (logging,"logMultiprocessing")): logging.logMultiprocessing = False 
	_direct_core_logger_mode = "py"
#
except ImportError: _direct_core_logger_mode = None

if (_direct_core_logger_mode == None):
#
	from org.apache.log4j import RollingFileAppender as RotatingFileHandler
	from org.apache.log4j import SimpleLayout
	from org.apache.log4j.Level import DEBUG,ERROR,INFO
	from org.apache.log4j.Level import FATAL as CRITICAL
	from org.apache.log4j.Level import WARN as WARNING
	_direct_core_logger_mode = "java"
#

from .pas_globals import direct_globals
from .pas_pythonback import direct_str

_direct_core_logger_counter = 0

class direct_logger (RotatingFileHandler):
#
	"""
Provide logging functionality on top of
"logging.handlers.RotatingFileHandler".

@author    direct Netware Group
@copyright (C) direct Netware Group - All rights reserved
@package   pas_core
@since     v0.1.00
@license   http://www.direct-netware.de/redirect.php?licenses;mpl2
           Mozilla Public License, v. 2.0
	"""

	CRITICAL = CRITICAL
	"""
Static logging.CRITICAL
	"""
	DEBUG = DEBUG
	"""
Static logging.DEBUG
	"""
	ERROR = ERROR
	"""
Static logging.ERROR
	"""
	INFO = INFO
	"""
Static logging.INFO
	"""
	WARNING = WARNING
	"""
Static logging.WARNING
	"""
	logger = None
	"""
Logger object
	"""

	def __init__ (self,logging_mode = ERROR):
	#
		"""
Constructor __init__ (direct_logger)

@param logging_mode Logging level
@since v0.1.00
		"""

		global _direct_core_logger_mode

		if (_direct_core_logger_mode == "java"):
		#
			self.logger = Logger.getLogger ('PASlogger')
			self.logger.setLevel (logging_mode)
		#
		else:
		#
			self.logger = logging.getLogger ('PASlogger')
			self.logger.setLevel (logging_mode)
		#

		if ("pas_log_pathname" in direct_globals['settings']): direct_globals['settings']['pas_log'] = direct_globals['settings']['pas_log_pathname']
		elif ("pas_log" in direct_globals['settings']): direct_globals['settings']['pas_log'] = path.normpath ("{0}/{1}".format (direct_globals['settings']['path_base'],direct_globals['settings']['pas_log']))
		else: direct_globals['settings']['pas_log'] = path.normpath ("{0}/logging.log".format (direct_globals['settings']['path_base']))

		if ("pas_log_datetime" not in direct_globals['settings']): direct_globals['settings']['pas_log_datetime'] = "%m/%d/%Y %H:%M:%S"
		if ("pas_log_size_max" not in direct_globals['settings']): direct_globals['settings']['pas_log_size_max'] = 104857600
		if ("pas_log_rotates" not in direct_globals['settings']): direct_globals['settings']['pas_log_rotates'] = 5

		if (_direct_core_logger_mode == "java"):
		#
			RotatingFileHandler.__init__ (self,SimpleLayout (),direct_globals['settings']['pas_log'])
			self.setMaxBackupIndex (direct_globals['settings']['pas_log_rotates'])
			self.setMaximumFileSize (direct_globals['settings']['pas_log_size_max'])

			self.logger.addAppender (self)
			self.logger.setLevel (logging_mode)
		#
		else:
		#
			RotatingFileHandler.__init__ (self,direct_globals['settings']['pas_log'],maxBytes = direct_globals['settings']['pas_log_size_max'],backupCount = direct_globals['settings']['pas_log_rotates'])
			self.logger.addHandler (self)
		#
	#

	def getEffectiveLevel (self):
	#
		"""
Static "write ()" method to append INFO log messages.

@param data Logging data
@since v0.1.00
		"""

		return self.logger.getEffectiveLevel ()
	#

	def write (self,level,data):
	#
		"""
"write ()" adds all messages to the logger instance.

@param level Logging level
@param data Logging data
@since v0.1.00
		"""

		try:
		#
			f_exception = isinstance (data,Exception)
			if (not f_exception): data = repr (data)
		#
		except: f_exception = False

		f_stamp = strftime (direct_globals['settings']['pas_log_datetime'])

		if (f_exception): f_stamp = "[exception] {0}".format (f_stamp)
		elif (level == self.CRITICAL): f_stamp = "[critical]  {0}".format (f_stamp)
		elif (level == self.ERROR): f_stamp = "[error]     {0}".format (f_stamp)
		elif (level == self.WARNING): f_stamp = "[warning]   {0}".format (f_stamp)
		elif (level == self.INFO): f_stamp = "[info]      {0}".format (f_stamp)
		elif (level == self.DEBUG): f_stamp = "[debug]     {0}".format (f_stamp)

		if (f_exception): data = repr (data)
		else: data = direct_str (data)

		if ((data.find ("\n") > -1) or (data.find ("\r") > -1)):
		#
			data = "{0} \"{1}\"".format (f_stamp,data)
			data = re.compile ("[\n\r]+").sub ("\"; \"",data)
		#
		else: data = "{0} {1}".format (f_stamp,data)

		if (level == self.CRITICAL): self.logger.critical (data)
		if (level == self.DEBUG): self.logger.debug (data)
		if (level == self.ERROR): self.logger.error (data)
		if (level == self.INFO): self.logger.info (data)
		if (level == self.WARNING): self.logger.warning (data)
	#

	def critical (data):
	#
		"""
Static "write ()" method to append CRITICAL log messages.

@param data Logging data
@since v0.1.00
		"""

		direct_logger.py_get(count = False).write (CRITICAL,data)
	#
	critical = staticmethod (critical)

	def debug (data):
	#
		"""
Static "write ()" method to append ERROR log messages.

@param data Logging data
@since v0.1.00
		"""

		direct_logger.py_get(count = False).write (DEBUG,data)
	#
	debug = staticmethod (debug)

	def info (data):
	#
		"""
Static "write ()" method to append INFO log messages.

@param data Logging data
@since v0.1.00
		"""

		direct_logger.py_get(count = False).write (INFO,data)
	#
	info = staticmethod (info)

	def error (data):
	#
		"""
Static "write ()" method to append ERROR log messages.

@param data Logging data
@since v0.1.00
		"""

		direct_logger.py_get(count = False).write (ERROR,data)
	#
	error = staticmethod (error)

	def warning (data):
	#
		"""
Static "write ()" method to append WARNING log messages.

@param data Logging data
@since v0.1.00
		"""

		direct_logger.py_get(count = False).write (WARNING,data)
	#
	warning = staticmethod (warning)

	def py_del ():
	#
		"""
The last "py_del ()" call will activate the Python singleton destructor.

@since v0.1.00
		"""

		global _direct_core_logger_counter

		_direct_core_logger_counter -= 1
		if (_direct_core_logger_counter == 0): direct_globals['logger'] = None
	#
	py_del = staticmethod (py_del)

	def py_get (logging_mode = None,count = True):
	#
		"""
Get the direct_logger singleton.

@param  logging_mode Logging mode
@param  count Count "get ()" request
@return (direct_debug) Object on success
@since  v0.1.00
		"""

		global _direct_core_logger_counter

		if ("logger" not in direct_globals):
		#
			if (logging_mode == None):
			#
				if (direct_globals['settings']['debug_reporting'] == False): logging_mode = direct_logger.ERROR
				else: logging_mode = direct_logger.DEBUG
			#

			direct_globals['logger'] = direct_logger (logging_mode)
		#

		if (count): _direct_core_logger_counter += 1

		return direct_globals['logger']
	#
	py_get = staticmethod (py_get)
#

##j## EOF