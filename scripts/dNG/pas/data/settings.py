# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.settings
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

from dNG.data.file import direct_file
from dNG.data.json_parser import direct_json_parser
from .binary import direct_binary

class direct_settings(dict):
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
Constructor __init__(direct_settings)

:since: v0.1.00
		"""

		dict.__init__(self)

		self['path_system'] = path.normpath("{0}/../../../..".format(direct_binary.str(__file__)))
		self['path_base'] = (direct_binary.str(os.environ['dNGpath']) if ("dNGpath" in os.environ) else path.normpath("{0}/..".format(self['path_system'])))
		self['path_data'] = (direct_binary.str(os.environ['dNGpathData']) if ("dNGpathData" in os.environ) else path.normpath("{0}/data".format(self['path_base'])))
		self['path_lang'] = (direct_binary.str(os.environ['dNGpathLang']) if ("dNGpathLang" in os.environ) else path.normpath("{0}/lang".format(self['path_base'])))
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

	def return_instance(self):
	#
		"""
The last "return_instance()" call will activate the Python singleton
destructor.

:since: v0.1.00
		"""

		pass
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

		return (key in direct_settings.get_instance())
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

		instance = direct_settings.get_instance()
		return (instance.get_dict() if (key == None) else dict.get(instance, key, default))
	#

	@staticmethod
	def get_instance(count = False):
	#
		"""
Get the settings singleton.

:param count: Count "get()" request

:return: (direct_settings) Object on success
:since:  v0.1.00
		"""

		with direct_settings.synchronized:
		#
			if (direct_settings.instance == None):
			#
				direct_settings.instance = direct_settings()
				direct_settings.read_file("{0}/settings/core.json".format(direct_settings.instance['path_data']))
			#
		#

		return direct_settings.instance
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

		json_parser = direct_json_parser()
		data = json_parser.json2data(json)

		if (data == None): var_return = False
		else: direct_settings.get_instance().update(data)

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
		file_content = (None if (direct_settings.cache_instance == None) else direct_settings.cache_instance.get_file(file_pathname))

		if (file_content == None):
		#
			file_object = direct_file()

			if (file_object.open(file_pathname, True, "r")):
			#
				file_content = file_object.read()
				file_object.close()

				file_content = file_content.replace("\r", "")
				if (direct_settings.cache_instance != None): direct_settings.cache_instance.set_file(file_pathname, file_content)
			#
			elif (required): raise RuntimeError("{0} not found".format(file_pathname), 2)
			elif (direct_settings.log_handler != None): direct_settings.log_handler.debug("{0} not found".format(file_pathname))
		#

		if (file_content != None and (not direct_settings.import_raw_json(file_content))):
		#
			if (required): raise RuntimeError("{0} is not a valid JSON encoded settings file".format(file_pathname), 61)
			elif (direct_settings.log_handler != None): direct_settings.log_handler.warning("{0} is not a valid JSON encoded settings file".format(file_pathname))
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

		direct_settings.get_instance()[key] = value
	#

	@staticmethod
	def set_cache(cache_instance):
	#
		"""
Sets the cache instance.

:param cache_instance: log_handler to use

:since: v0.1.00
		"""

		if (direct_settings.log_handler != None): direct_settings.log_handler.debug("#echo(__FILEPATH__)# -settings.set_cache(cache_instance)- (#echo(__LINE__)#)")
		direct_settings.cache_instance = cache_instance
	#

	@staticmethod
	def set_log_handler(log_handler):
	#
		"""
Sets the log_handler.

:param log_handler: log_handler to use

:since: v0.1.00
		"""

		direct_settings.log_handler = log_handler
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