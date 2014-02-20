# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.Settings
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
from threading import RLock
from weakref import proxy
import os
import re

from dNG.data.file import File
from dNG.data.json_parser import JsonParser
from dNG.pas.runtime.io_exception import IOException
from dNG.pas.runtime.value_exception import ValueException
from .binary import Binary

class Settings(dict):
#
	"""
The settings singleton provides methods on top of an dict.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	RE_EXTENDED_JSON_COMMENT_LINE = re.compile("^\\W#.*$", re.M)
	"""
Comments in (invalid) JSON setting files are replaced before getting parsed.
	"""

	cache_instance = None
	"""
Cache instance
	"""
	instance = None
	"""
Settings instance
	"""
	lock = RLock()
	"""
Thread safety lock
	"""
	log_handler = None
	"""
The LogHandler is called whenever debug messages should be logged or errors
happened.
	"""

	def __init__(self):
	#
		"""
Constructor __init__(Settings)

:since: v0.1.00
		"""

		dict.__init__(self)

		self['path_system'] = path.normpath("{0}/../../../..".format(Binary.str(__file__)))
		self['path_base'] = (Binary.str(os.environ['dNGpath']) if ("dNGpath" in os.environ) else path.normpath("{0}/..".format(self['path_system'])))
		self['path_data'] = (Binary.str(os.environ['dNGpathData']) if ("dNGpathData" in os.environ) else path.normpath("{0}/data".format(self['path_base'])))
		self['path_lang'] = (Binary.str(os.environ['dNGpathLang']) if ("dNGpathLang" in os.environ) else path.normpath("{0}/lang".format(self['path_base'])))
	#

	@staticmethod
	def is_defined(key):
	#
		"""
Checks if a given key is a defined setting.

:param key: Settings key

:return: (bool) True if defined
:since:  v0.1.00
		"""

		return (key in Settings.get_instance())
	#

	@staticmethod
	def get(key, default = None):
	#
		"""
Returns the value with the specified key.

:param key: Settings key
:param default: Default value if not set

:return: (mixed) Value
:since:  v0.1.00
		"""

		instance = Settings.get_instance()
		return dict.get(instance, key, default)
	#

	@staticmethod
	def get_dict():
	#
		"""
Returns all settings currently defined as a dict.

:return: (dict) Settings dict
:since:  v0.1.00
		"""

		return Settings.get_instance()
	#

	@staticmethod
	def get_instance():
	#
		"""
Get the settings singleton.

:return: (Settings) Object on success
:since:  v0.1.00
		"""

		if (Settings.instance == None):
		#
			# Instance could be created in another thread so check again
			with Settings.lock:
			#
				if (Settings.instance == None):
				#
					Settings.instance = Settings()
					Settings.read_file("{0}/settings/core.json".format(Settings.instance['path_data']))
				#
			#
		#

		return Settings.instance
	#

	@staticmethod
	def import_json(json):
	#
		"""
Import a given JSON encoded string as an dict of settings.

:param json: JSON encoded dict of settings

:return: (bool) True on success
:since:  v0.1.00
		"""

		_return = True

		json_parser = JsonParser()
		json_data = json_parser.json2data(json)

		if (json_data == None): _return = False
		else: Settings.get_instance().update(json_data)

		return _return
	#

	@staticmethod
	def read_file(file_pathname, required = False):
	#
		"""
Read all settings from the given file.

:param file_pathname: File path and name of the settings file
:param required: True if missing files should throw exceptions

:since: v0.1.00
		"""

		# pylint: disable=maybe-no-member

		file_pathname = path.normpath(file_pathname)
		file_content = (None if (Settings.cache_instance == None) else Settings.cache_instance.get_file(file_pathname))

		if (file_content == None):
		#
			file_object = File()

			if (file_object.open(file_pathname, True, "r")):
			#
				file_content = file_object.read()
				file_object.close()

				file_content = file_content.replace("\r", "")
				file_content = Settings.RE_EXTENDED_JSON_COMMENT_LINE.sub("", file_content)
				if (Settings.cache_instance != None): Settings.cache_instance.set_file(file_pathname, file_content)
			#
			elif (required): raise IOException("{0} not found".format(file_pathname))
			elif (Settings.log_handler != None): Settings.log_handler.debug("{0} not found".format(file_pathname))
		#

		if (file_content != None and (not Settings.import_json(file_content))):
		#
			if (required): raise ValueException("{0} is not a valid JSON encoded settings file".format(file_pathname))
			if (Settings.log_handler != None): Settings.log_handler.warning("{0} is not a valid JSON encoded settings file".format(file_pathname))
		#
	#

	@staticmethod
	def set(key, value = None):
	#
		"""
Sets the value for the specified key.

:param key: Settings key
:param value: Value

:since: v0.1.00
		"""

		Settings.get_instance()[key] = value
	#

	@staticmethod
	def set_cache_instance(cache_instance):
	#
		"""
Sets the cache instance.

:param cache_instance: Cache instance to use

:since: v0.1.00
		"""

		if (Settings.log_handler != None): Settings.log_handler.debug("#echo(__FILEPATH__)# -settings.set_cache_instance(cache_instance)- (#echo(__LINE__)#)")
		Settings.cache_instance = proxy(cache_instance)
	#

	@staticmethod
	def set_log_handler(log_handler):
	#
		"""
Sets the LogHandler.

:param log_handler: LogHandler to use

:since: v0.1.00
		"""

		Settings.log_handler = proxy(log_handler)
	#

	@staticmethod
	def write_file(file_pathname, template_pathname):
	#
		"""
Write all settings to the given file using the given template.

:param file_pathname: File path and name of the settings file
:param template_pathname: File path and name of the settings template
       file

:return: (bool) True on success
:since:  v0.1.00
		"""

		return False
	#
#

##j## EOF