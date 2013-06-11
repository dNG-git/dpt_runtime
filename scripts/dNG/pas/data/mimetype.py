# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.mimetype
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
import mimetypes

from dNG.data.file import direct_file
from dNG.data.json_parser import direct_json_parser
from dNG.pas.module.named_loader import direct_named_loader
from .settings import direct_settings
from .logging.log_line import direct_log_line

class direct_mimetype(object):
#
	"""
Provides MimeType related methods on top of Python basic ones.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v0.1.01
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	instance = None
	"""
Settings instance
	"""
	synchronized = RLock()
	"""
Lock used in multi thread environments.
	"""

	def __init__(self):
	#
		"""
Constructor __init__(direct_mimetype)

:since: v0.1.01
		"""

		self.extensions = { }
		"""
Mimetype extension list
		"""
		self.mimetypes = None
		"""
Mimetype definitions
		"""
	#

	def get(self, extension = None, mimetype = None):
	#
		"""
Returns the value with the specified key or $key if undefined.

:param key: L10n key
:param default: Default value if not translated
:param lang: Language code

:return: (str) Value
:since:  v0.1.01
		"""

		var_return = None

		if (extension != None):
		#
			extension = (extension[1:].lower() if (extension[:1] == ".") else extension.lower())

			if (extension in self.extensions and self.extensions[extension] in self.mimetypes):
			#
				var_return = self.mimetypes[self.extensions[extension]].copy()
				var_return['mimetype'] = self.extensions[extension]
			#
			else:
			#
				mimetype = mimetypes.guess_type("file.{0}".format(extension), False)[0]
				if (mimetype != None): var_return = { "mimetype": mimetype, "extension": extension, "type": "unknown" }
			#

			if (mimetype != None and mimetype != var_return['mimetype']): var_return = None
		#
		elif (mimetype != None):
		#
			if (mimetype in self.mimetypes): var_return = self.mimetypes[mimetype]
			elif (mimetypes.guess_extension(mimetype, False) != None): var_return = { "mimetype": mimetype, "type": "unknown" }
		#

		return var_return
	#

	def get_extensions(self, mimetype):
	#
		"""
Returns the defined default language of the current task.

:return: (str) Language code
:since:  v0.1.01
		"""

		if (mimetype != None or mimetype in self.mimetypes):
		#
			var_return = (self.mimetypes[mimetype]['extensions'] if ("extensions" in self.mimetypes[mimetype]) else [ ])
			if (type(var_return) != list): var_return = [ var_return ]
		#
		else: var_return = None

		return var_return
	#

	def import_raw_json(self, json):
	#
		"""
Import a given JSON encoded string as an array of settings.

:param json: JSON encoded array of settings

:return: (bool) True on success
:since:  v0.1.01
		"""

		var_return = True

		json_parser = direct_json_parser()
		data = json_parser.json2data(json)

		if (data == None): var_return = False
		else:
		#
			self.mimetypes = { }

			for mimetype in data:
			#
				if ("type" not in data[mimetype]):
				#
					var_type = mimetype.split("/", 1)[0]
					data[mimetype]['type'] = ("unknown" if (var_type not in data or "type" not in data[var_type]) else data[var_type]['type'])
				#

				self.mimetypes[mimetype] = data[mimetype]

				if ("extensions" in data[mimetype] and type(data[mimetype]['extensions']) == list):
				#
					for extension in data[mimetype]['extensions']:
					#
						if (extension not in self.extensions): self.extensions[extension] = mimetype
						else: direct_log_line.warning("Extension '{0}' declared for more than one mimetype".format(self.extensions[extension]))
					#
				# 
				elif ("extension" in data[mimetype]):
				#
					if (data[mimetype]['extension'] not in self.extensions): self.extensions[data[mimetype]['extension']] = mimetype
					else: direct_log_line.warning("Extension '{0}' declared for more than one mimetype".format(self.extensions[data[mimetype]['extension']]))
				#
			#
		#

		return var_return
	#

	def refresh(self):
	#
		"""
Read all settings from the given file.

:param json: JSON encoded array of language strings

:since: v0.1.01
		"""

		cache_instance = direct_named_loader.get_singleton("dNG.pas.data.cache", False)

		try:
		#
			file_pathname = path.normpath("{0}/settings/core_mimetypes.json".format(direct_settings.get("path_data")))
			file_content = (None if (cache_instance == None) else cache_instance.get_file(file_pathname))

			if (file_content == None):
			#
				file_object = direct_file()

				if (file_object.open(file_pathname, True, "r")):
				#
					file_content = file_object.read()
					file_object.close()

					file_content = file_content.replace("\r", "")
					if (cache_instance != None): cache_instance.set_file(file_pathname, file_content)
				#
				else: direct_log_line.info("{0} not found".format(file_pathname))
			#
			elif (self.mimetypes != None): file_content = None

			if (file_content != None and (not self.import_raw_json(file_content))): direct_log_line.warning("{0} is not a valid JSON encoded language file".format(file_pathname))
		#
		except Exception as handled_exception: direct_log_line.error(handled_exception)

		if (cache_instance != None): cache_instance.return_instance()
	#

	def return_instance(self):
	#
		"""
The last "return_instance()" call will activate the Python singleton
destructor.

:since: v0.1.01
		"""

		pass
	#

	@staticmethod
	def get_instance(lang = None, count = False):
	#
		"""
Get the l10n singleton for the given or default language.

:param lang: Language code
:param count: Count "get()" request

:return: (direct_l10n) Object on success
:since:  v0.1.01
		"""

		with direct_mimetype.synchronized:
		#
			if (direct_mimetype.instance == None): direct_mimetype.instance = direct_mimetype()
			direct_mimetype.instance.refresh()
		#

		return direct_mimetype.instance
	#
#

##j## EOF