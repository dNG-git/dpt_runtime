# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.text.L10n
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

from threading import local
import re

from dNG.pas.data.binary import Binary
from dNG.pas.data.cached_json_file import CachedJsonFile
from dNG.pas.data.settings import Settings
from dNG.pas.runtime.instance_lock import InstanceLock

class L10n(dict):
#
	"""
Provides l10n (localization) methods on top of an dict.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	default_lang = None
	"""
Default application language
	"""
	instances = { }
	"""
L10n instances
	"""
	instances_lock = InstanceLock()
	"""
Thread safety instances lock
	"""
	local = local()
	"""
Local data handle
	"""

	def __init__(self, lang):
	#
		"""
Constructor __init__(L10n)

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

:return: (str) Language code
:since:  v0.1.00
		"""

		return self.lang
	#

	def read_file(self, file_pathname):
	#
		"""
Read all translations from the given file.

:param file_pathname: File path and name

:since: v0.1.00
		"""

		json_data = CachedJsonFile.read(file_pathname)
		if (type(json_data) == dict): self.update(json_data)
	#

	def write_file(self, file_pathname, template_pathname):
	#
		"""
Write all translations to the given file using the given template.

:param file_pathname: File path and name of the translation file
:param template_pathname: File path and name of the translation template
       file

:return: (bool) True on success
:since:  v0.1.00
		"""

		return False
	#

	@staticmethod
	def init(file_basename, lang = None):
	#
		"""
Load the given language section.

:param file_basename: File basename

:since: v0.1.00
		"""

		file_basename = Binary.str(file_basename)
		instance = L10n.get_instance(lang)

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

		instance.read_file("{0}/{1}/{2}.json".format(Settings.get("path_lang"), instance.get_lang(), file_pathname))
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

		try: instance = L10n.get_instance(lang)
		except Exception: instance = { }

		return (key in instance)
	#

	@staticmethod
	def get(key = None, default = None, lang = None):
	#
		"""
Returns the value with the specified key or the default one if undefined.

:param key: L10n key
:param default: Default value if not translated
:param lang: Language code

:return: (str) Value
:since:  v0.1.00
		"""

		instance = L10n.get_instance(lang)
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

		return (L10n.local.lang if (hasattr(L10n.local, "lang")) else L10n.default_lang)
	#

	@staticmethod
	def get_instance(lang = None):
	#
		"""
Get the L10n singleton for the given or default language.

:param lang: Language code

:return: (L10n) Object on success
:since:  v0.1.00
		"""

		with L10n.instances_lock:
		#
			if (lang == None): lang = L10n.get_default_lang()
			elif (L10n.default_lang == None): L10n.default_lang = lang

			if (lang == None): raise RuntimeError("Language not defined and default language is undefined.")
			if (lang not in L10n.instances): L10n.instances[lang] = L10n(lang)
		#

		return L10n.instances[lang]
	#

	@staticmethod
	def set_default_lang(lang):
	#
		"""
Defines the default language of the application.

:param lang: Language code

:since: v0.1.00
		"""

		L10n.default_lang = lang
	#

	@staticmethod
	def set_thread_lang(lang):
	#
		"""
Defines a default language for the calling thread.

:param lang: Language code

:since: v0.1.00
		"""

		L10n.local.lang = lang
	#
#

##j## EOF