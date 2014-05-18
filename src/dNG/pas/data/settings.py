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
from dNG.data.json_resource import JsonResource
from dNG.pas.runtime.io_exception import IOException
from dNG.pas.runtime.value_exception import ValueException
from .binary import Binary

class Settings(object):
#
	"""
The settings singleton provides a central configuration facility.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	RE_EXTENDED_JSON_COMMENT_LINE = re.compile("^\\s*#.*$", re.M)
	"""
Comments in (invalid) JSON setting files are replaced before getting parsed.
	"""

	_cache_instance = None
	"""
Cache instance
	"""
	_instance = None
	"""
Settings instance
	"""
	_lock = RLock()
	"""
Thread safety lock
	"""
	_log_handler = None
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

		self.dict = { "path_system": path.normpath("{0}/../../../..".format(Binary.str(__file__))) }
		"""
Underlying dict
		"""

		self.dict['path_base'] = (Binary.str(os.environ['dNGpath']) if ("dNGpath" in os.environ) else path.normpath("{0}/..".format(self.dict['path_system'])))
		self.dict['path_data'] = (Binary.str(os.environ['dNGpathData']) if ("dNGpathData" in os.environ) else path.normpath("{0}/data".format(self.dict['path_base'])))
		self.dict['path_lang'] = (Binary.str(os.environ['dNGpathLang']) if ("dNGpathLang" in os.environ) else path.normpath("{0}/lang".format(self.dict['path_base'])))
	#

	def update(self, other):
	#
		"""
python.org: Update the dictionary with the key/value pairs from other,
overwriting existing keys.

:param other: Other dictionary

:since: v0.1.01
		"""

		with Settings._lock: self.dict.update(other)
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

		return (key in Settings.get_dict())
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

		return Settings.get_dict().get(key, default)
	#

	@staticmethod
	def get_dict():
	#
		"""
Returns all settings currently defined as a dict.

:return: (dict) Settings dict
:since:  v0.1.00
		"""

		return Settings.get_instance().dict
	#

	@staticmethod
	def get_lang_associated(key, lang, default = None):
	#
		"""
Returns the value associated with the given language. Otherwise the default
one with the specified key is returned. Default is used if both values are
not defined.

:param key: Settings key
:param lang: Language code
:param default: Default value if not set

:return: (mixed) Value
:since:  v0.1.00
		"""

		_dict = Settings.get_dict()

		key_with_lang = "{0}_{1}".format(key, lang)
		_return = (_dict[key_with_lang] if (key_with_lang in _dict) else None)

		if (_return == None): _return = (_dict[key] if (key in _dict) else default)

		return _return
	#

	@staticmethod
	def get_instance():
	#
		"""
Get the settings singleton.

:return: (Settings) Object on success
:since:  v0.1.00
		"""

		if (Settings._instance == None):
		# Thread safety
			with Settings._lock:
			#
				if (Settings._instance == None):
				#
					Settings._instance = Settings()
					Settings.read_file("{0}/settings/core.json".format(Settings._instance.dict['path_data']))
				#
			#
		#

		return Settings._instance
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

		json_resource = JsonResource()
		json_data = json_resource.json_to_data(json)

		if (json_data == None): _return = False
		else: Settings.get_instance().update(json_data)

		return _return
	#

	@staticmethod
	def is_file_known(file_pathname):
	#
		"""
Return true if the given file path and name is cached.

:param file_pathname: File path and name of the settings file

:return: (bool) True if currently cached
:since:  v0.1.01
		"""

		file_pathname = path.normpath(file_pathname)
		return (False if (Settings._cache_instance == None) else Settings._cache_instance.is_file_known(file_pathname))
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
		file_content = (None if (Settings._cache_instance == None) else Settings._cache_instance.get_file(file_pathname))

		if (file_content == None):
		#
			file_object = File()

			if (file_object.open(file_pathname, True, "r")):
			#
				file_content = file_object.read()
				file_object.close()

				file_content = file_content.replace("\r", "")
				file_content = Settings.RE_EXTENDED_JSON_COMMENT_LINE.sub("", file_content)
				if (Settings._cache_instance != None): Settings._cache_instance.set_file(file_pathname, file_content)
			#
			elif (required): raise IOException("{0} not found".format(file_pathname))
			elif (Settings._log_handler != None): Settings._log_handler.debug("{0} not found".format(file_pathname))
		#

		if (file_content != None and (not Settings.import_json(file_content))):
		#
			if (required): raise ValueException("{0} is not a valid JSON encoded settings file".format(file_pathname))
			if (Settings._log_handler != None): Settings._log_handler.warning("{0} is not a valid JSON encoded settings file".format(file_pathname))
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

		Settings.get_dict()[key] = value
	#

	@staticmethod
	def set_cache_instance(cache_instance):
	#
		"""
Sets the cache instance.

:param cache_instance: Cache instance to use

:since: v0.1.00
		"""

		if (Settings._log_handler != None): Settings._log_handler.debug("#echo(__FILEPATH__)# -settings.set_cache_instance(cache_instance)- (#echo(__LINE__)#)")
		Settings._cache_instance = proxy(cache_instance)
	#

	@staticmethod
	def set_log_handler(log_handler):
	#
		"""
Sets the LogHandler.

:param log_handler: LogHandler to use

:since: v0.1.00
		"""

		Settings._log_handler = proxy(log_handler)
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