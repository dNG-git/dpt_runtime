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

from threading import local
import re

from dNG.pas.data.binary import Binary
from dNG.pas.data.settings import Settings
from dNG.pas.runtime.instance_lock import InstanceLock
from dNG.pas.runtime.value_exception import ValueException
from .l10n_instance import L10nInstance

class L10n(object):
#
	"""
Provides static l10n (localization) methods.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	default_lang = None
	"""
Default application language
	"""
	_instances = { }
	"""
L10n instances
	"""
	_instances_lock = InstanceLock()
	"""
Thread safety instances lock
	"""
	_local = local()
	"""
Local data handle
	"""

	@staticmethod
	def format_number(number, fractional_digits = -1, lang = None):
	#
		"""
Returns a formatted number.

:param number: Number as int or float
:param fractional_digits: Fractional digits to return
:param lang: Language code

:return: (str) Formatted value
:since:  v0.1.00
		"""

		return L10n.get_instance(lang).format_number(number, fractional_digits)
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

		file_path_name = ""
		file_path_name_list = file_basename.split(".")
		re_file_name = re.compile("\\W+")

		for basename in file_path_name_list:
		#
			if (basename):
			#
				basename = re_file_name.sub(" ", basename)
				file_path_name += ("/" if (len(file_path_name) > 0) else "") + basename
			#
		#

		file_path_name = "{0}/{1}/{2}.json".format(Settings.get("path_lang"), instance.get_lang(), file_path_name)
		instance.read_file(file_path_name)
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

		try: _dict = L10n.get_dict(lang)
		except ValueException: _dict = { }

		return (key in _dict)
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

		return L10n.get_dict(lang).get(key, (key if (default == None) else default))
	#

	@staticmethod
	def get_default_lang():
	#
		"""
Returns the defined default language of the current task.

:return: (str) Language code
:since:  v0.1.00
		"""

		_return = None

		if (hasattr(L10n._local, "lang")): _return = L10n._local.lang
		if (_return == None): _return = L10n.default_lang
		if (_return == None): _return = Settings.get("core_lang")

		return _return
	#

	@staticmethod
	def get_dict(lang = None):
	#
		"""
Returns all language strings for the given or default language currently
defined as a dict.

:param lang: Language code

:return: (dict) L10nInstance dict
:since:  v0.1.01
		"""

		if (lang == None): lang = L10n.get_default_lang()
		elif (L10n.default_lang == None): L10n.default_lang = lang

		if (lang == None): raise ValueException("Language not defined and default language is undefined.")

		if (lang not in L10n._instances):
		# Thread safe
			with L10n._instances_lock:
			#
				if (lang not in L10n._instances): L10n._instances[lang] = L10nInstance(lang)
			#
		#

		return L10n._instances[lang]
	#

	@staticmethod
	def get_instance(lang = None):
	#
		"""
Get the L10n dict instance of the given or default language.

:param lang: Language code

:return: (object) L10nInstance
:since:  v0.1.00
		"""

		return L10n.get_dict(lang)
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

		L10n._local.lang = lang
	#
#

##j## EOF