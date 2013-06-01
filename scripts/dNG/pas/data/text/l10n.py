# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.text.l10n
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
from threading import local, RLock
import re

from dNG.data.file import direct_file
from dNG.data.json_parser import direct_json_parser
from dNG.pas.data.binary import direct_binary
from dNG.pas.data.settings import direct_settings

class direct_l10n(dict):
#
	"""
Provides l10n (localisation) methods on top of an dict.

:author:    direct Netware Group
:copyright: direct Netware Group - All rights reserved
:package:   pas.core
:since:     v0.1.00
:license:   http://www.direct-netware.de/redirect.py?licenses;mpl2
            Mozilla Public License, v. 2.0
	"""

	log_handler = None
	"""
The log_handler is called whenever debug messages should be logged or errors
happened.
	"""
	default_lang = None
	"""
Default application language
	"""
	instances = { }
	"""
L10n instances
	"""
	local = local()
	"""
Local data handle
	"""
	synchronized = RLock()
	"""
Lock used in multi thread environments.
	"""

	def __init__(self, lang):
	#
		"""
Constructor __init__(direct_l10n)

:param lang: Language code

:since: v0.1.00
		"""

		dict.__init__(self)

		self.lang = lang
		"""
L10n language code
		"""
		self.strings = { }
		"""
Underlying l10n dict
		"""
	#

	def get_lang(self):
	#
		"""
Returns the language code of this instance.

:access: protected
:return: (str) Language code
:since:  v0.1.00
		"""

		return self.lang
	#

	def import_raw_json(self, json):
	#
		"""
Import a given JSON encoded string as an array of settings.

:param json: JSON encoded array of settings

:return: (bool) True on success
:since:  v0.1.00
		"""

		var_return = True

		json_parser = direct_json_parser()
		data = json_parser.json2data(json)

		if (data == None): var_return = False
		else: self.update(data)

		return var_return
	#

	def read_file(self, file_pathname):
	#
		"""
Read all settings from the given file.

:param json: JSON encoded array of language strings

:since: v0.1.00
		"""

		file_object = direct_file()
		file_pathname = path.normpath(file_pathname)

		if (file_object.open(file_pathname, True, "r")):
		#
			file_content = file_object.read()
			file_object.close()

			file_content = file_content.replace("\r", "")
			if ((not self.import_raw_json(file_content)) and direct_l10n.log_handler != None): direct_l10n.log_handler.warning("{0} is not a valid JSON encoded language file".format(file_pathname))
		#
		elif (direct_l10n.log_handler != None): direct_l10n.log_handler.info("{0} not found".format(file_pathname))
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

	def write_file(self, file_pathname, template_pathname):
	#
		"""
Write all settings from the given file.

:param json: JSON encoded array of settings

:since: v0.1.00
		"""

		pass
	#

	@staticmethod
	def init(file_basename, lang = None):
	#
		"""
Load the given language section.

:param file_basename: File basename

:since: v0.1.00
		"""

		file_basename = direct_binary.str(file_basename)
		instance = direct_l10n.get_instance(lang)

		file_pathname = ""
		file_pathname_list = file_basename.split(".")
		re_file_name = re.compile("\\W+")

		for basename in file_pathname_list:
		#
			if (basename):
			#
				basename = re_file_name.sub(" ", basename)
				file_pathname += ("/" if (len(file_pathname) > 0) else "") + basename
			#
		#

		instance.read_file("{0}/{1}/{2}.json".format(direct_settings.get("path_lang"), instance.get_lang(), file_pathname))
	#

	@staticmethod
	def is_defined(key, lang = None):
	#
		"""
Checks if a given key is a defined language string.

:param key: L10n key
:param lang: Language code

:return: (bool) True if defined
:since:  v0.1.00
		"""

		try: instance = direct_l10n.get_instance(lang)
		except: instance = { }

		return (key in instance)
	#

	@staticmethod
	def get(key = None, default = None, lang = None):
	#
		"""
Returns the value with the specified key or $key if undefined.

:param key: L10n key
:param default: Default value if not translated
:param lang: Language code

:return: (str) Value
:since:  v0.1.00
		"""

		instance = direct_l10n.get_instance(lang)
		return dict.get(instance, key, (key if (default == None) else default))
	#

	@staticmethod
	def get_default_lang():
	#
		"""
Returns the defined default language of the current task.

:return: (str) Language code
:since:  v0.1.00
		"""

		return (direct_l10n.local.lang if (hasattr(direct_l10n.local, "lang")) else direct_l10n.default_lang)
	#

	@staticmethod
	def get_instance(lang = None, count = False):
	#
		"""
Get the l10n singleton for the given or default language.

:param lang: Language code
:param count: Count "get()" request

:return: (direct_l10n) Object on success
:since:  v0.1.00
		"""

		with direct_l10n.synchronized:
		#
			if (lang == None): lang = direct_l10n.get_default_lang()
			elif (direct_l10n.default_lang == None): direct_l10n.default_lang = lang

			if (lang == None): raise RuntimeError("Language not defined and default language is undefined.", 22)
			elif (lang not in direct_l10n.instances): direct_l10n.instances[lang] = direct_l10n(lang)
		#

		return direct_l10n.instances[lang]
	#

	@staticmethod
	def set_default_lang(lang):
	#
		"""
Defines the default language of the application.

:param lang: Language code

:since: v0.1.00
		"""

		direct_l10n.default_lang = lang
	#

	@staticmethod
	def set_thread_lang(lang):
	#
		"""
Defines a default language for the calling thread.

:param lang: Language code

:since: v0.1.00
		"""

		direct_l10n.local.lang = lang
	#

	@staticmethod
	def set_log_handler(log_handler):
	#
		"""
Sets the log_handler.

:param log_handler: log_handler to use

:since: v0.1.00
		"""

		direct_l10n.log_handler = log_handler
	#
#

##j## EOF