# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.MimeType
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
from weakref import ref
import mimetypes

from dNG.data.file import File
from dNG.data.json_parser import JsonParser
from dNG.pas.module.named_loader import NamedLoader
from .settings import Settings
from .logging.log_line import LogLine

class MimeType(object):
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

	synchronized = RLock()
	"""
Lock used in multi thread environments.
	"""
	weakref_instance = None
	"""
MimeType weakref instance
	"""

	def __init__(self):
	#
		"""
Constructor __init__(MimeType)

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

		_return = None

		if (extension != None):
		#
			extension = (extension[1:].lower() if (extension[:1] == ".") else extension.lower())

			if (extension in self.extensions and self.extensions[extension] in self.mimetypes):
			#
				_return = self.mimetypes[self.extensions[extension]].copy()
				_return['mimetype'] = self.extensions[extension]
			#
			else:
			#
				mimetype = mimetypes.guess_type("file.{0}".format(extension), False)[0]
				if (mimetype != None): _return = { "mimetype": mimetype, "extension": extension, "type": "unknown" }
			#

			if (mimetype != None and mimetype != _return['mimetype']): _return = None
		#
		elif (mimetype != None):
		#
			if (mimetype in self.mimetypes): _return = self.mimetypes[mimetype]
			elif (mimetypes.guess_extension(mimetype, False) != None): _return = { "mimetype": mimetype, "type": "unknown" }
		#

		return _return
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
			_return = (self.mimetypes[mimetype]['extensions'] if ("extensions" in self.mimetypes[mimetype]) else [ ])
			if (type(_return) != list): _return = [ _return ]
		#
		else: _return = None

		return _return
	#

	def import_raw_json(self, json):
	#
		"""
Import a given JSON encoded string as an array of settings.

:param json: JSON encoded array of settings

:return: (bool) True on success
:since:  v0.1.01
		"""

		_return = True

		json_parser = JsonParser()
		data = json_parser.json2data(json)

		if (data == None): _return = False
		else:
		#
			self.extensions = { }
			self.mimetypes = { }

			for mimetype in data:
			#
				if ("type" not in data[mimetype]):
				#
					_type = mimetype.split("/", 1)[0]
					data[mimetype]['type'] = ("unknown" if (_type not in data or "type" not in data[_type]) else data[_type]['type'])
				#

				self.mimetypes[mimetype] = data[mimetype]

				if ("extensions" in data[mimetype] and type(data[mimetype]['extensions']) == list):
				#
					for extension in data[mimetype]['extensions']:
					#
						if (extension not in self.extensions): self.extensions[extension] = mimetype
						else: LogLine.warning("Extension '{0}' declared for more than one mimetype".format(self.extensions[extension]))
					#
				# 
				elif ("extension" in data[mimetype]):
				#
					if (data[mimetype]['extension'] not in self.extensions): self.extensions[data[mimetype]['extension']] = mimetype
					else: LogLine.warning("Extension '{0}' declared for more than one mimetype".format(self.extensions[data[mimetype]['extension']]))
				#
			#
		#

		return _return
	#

	def refresh(self):
	#
		"""
Read all settings from the given file.

:param json: JSON encoded array of language strings

:since: v0.1.01
		"""

		cache_instance = NamedLoader.get_singleton("dNG.pas.data.Cache", False)

		file_pathname = path.normpath("{0}/settings/core_mimetypes.json".format(Settings.get("path_data")))
		file_content = (None if (cache_instance == None) else cache_instance.get_file(file_pathname))

		if (file_content == None):
		#
			file_object = File()

			if (file_object.open(file_pathname, True, "r")):
			#
				file_content = file_object.read()
				file_object.close()

				file_content = file_content.replace("\r", "")
				if (cache_instance != None): cache_instance.set_file(file_pathname, file_content)
			#
			else: LogLine.info("{0} not found".format(file_pathname))
		#
		elif (self.mimetypes != None): file_content = None

		if (file_content != None and (not self.import_raw_json(file_content))): LogLine.warning("{0} is not a valid JSON encoded language file".format(file_pathname))
	#

	@staticmethod
	def get_instance():
	#
		"""
Get the MimeType singleton for the given or default language.

:return: (MimeType) Object on success
:since:  v0.1.01
		"""

		_return = None

		with MimeType.synchronized:
		#
			if (MimeType.weakref_instance != None): _return = MimeType.weakref_instance()

			if (_return == None):
			#
				_return = MimeType()
				MimeType.weakref_instance = ref(_return)
			#

			_return.refresh()
		#

		return _return
	#
#

##j## EOF