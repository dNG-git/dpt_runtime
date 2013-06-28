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
import os

from dNG.data.file import File
from dNG.data.json_parser import JsonParser
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

	cache_instance = None
	"""
Cache instance
	"""
	instance = None
	"""
Settings instance
	"""
	log_handler = None
	"""
The log_handler is called whenever debug messages should be logged or errors
happened.
	"""
	synchronized = RLock()
	"""
Lock used in multi thread environments.
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

	def get_dict(self):
	#
		"""
Get the underlying settings dict.

:access: protected
:return: (dict) Settings instance
:since:  v0.1.00
		"""

		return self
	#

	def set_dict(self, settings):
	#
		"""
Set the underlying settings dict.

:param settings: New settings dict

:access: protected
:since:  v0.1.00
		"""

		self.clear()
		self.update(settings)
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
	def get(key = None, default = None):
	#
		"""
Returns the value with the specified key or all settings.

:param key: Settings key or NULL to receive all settings.
:param default: Default value if not set

:return: (mixed) Value
:since:  v0.1.00
		"""

		instance = Settings.get_instance()
		return (instance.get_dict() if (key == None) else dict.get(instance, key, default))
	#

	@staticmethod
	def get_instance():
	#
		"""
Get the settings singleton.

:return: (Settings) Object on success
:since:  v0.1.00
		"""

		with Settings.synchronized:
		#
			if (Settings.instance == None):
			#
				Settings.instance = Settings()
				Settings.read_file("{0}/settings/core.json".format(Settings.instance['path_data']))
			#
		#

		return Settings.instance
	#

	@staticmethod
	def import_raw_json(json):
	#
		"""
Import a given JSON encoded string as an dict of settings.

:param json: JSON encoded dict of settings

:return: (bool) True on success
:since:  v0.1.00
		"""

		var_return = True

		json_parser = JsonParser()
		data = json_parser.json2data(json)

		if (data == None): var_return = False
		else: Settings.get_instance().update(data)

		return var_return
	#

	@staticmethod
	def read_file(file_pathname, required = False):
	#
		"""
Read all settings from the given file.

:param json: JSON encoded dict of settings
:param required: True if missing files should throw exceptions

:since: v0.1.00
		"""

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
				if (Settings.cache_instance != None): Settings.cache_instance.set_file(file_pathname, file_content)
			#
			elif (required): raise RuntimeError("{0} not found".format(file_pathname), 2)
			elif (Settings.log_handler != None): Settings.log_handler.debug("{0} not found".format(file_pathname))
		#

		if (file_content != None and (not Settings.import_raw_json(file_content))):
		#
			if (required): raise RuntimeError("{0} is not a valid JSON encoded settings file".format(file_pathname), 61)
			elif (Settings.log_handler != None): Settings.log_handler.warning("{0} is not a valid JSON encoded settings file".format(file_pathname))
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
	def set_cache(cache_instance):
	#
		"""
Sets the cache instance.

:param cache_instance: log_handler to use

:since: v0.1.00
		"""

		if (Settings.log_handler != None): Settings.log_handler.debug("#echo(__FILEPATH__)# -settings.set_cache(cache_instance)- (#echo(__LINE__)#)")
		Settings.cache_instance = cache_instance
	#

	@staticmethod
	def set_log_handler(log_handler):
	#
		"""
Sets the log_handler.

:param log_handler: log_handler to use

:since: v0.1.00
		"""

		Settings.log_handler = log_handler
	#

	@staticmethod
	def write_file(file_pathname, template_pathname):
	#
		"""
Write all settings from the given file.

:param json: JSON encoded dict of settings

:since: v0.1.00
		"""

		pass
	#
#

##j## EOF