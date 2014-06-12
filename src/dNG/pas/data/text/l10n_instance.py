# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.text.L10nInstance
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

from dNG.pas.data.binary import Binary
from dNG.pas.data.cached_json_file import CachedJsonFile

class L10nInstance(dict):
#
	"""
L10n (localization) methods on top of an dict.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self, lang):
	#
		"""
Constructor __init__(L10n)

:param lang: Language code

:since: v0.1.00
		"""

		dict.__init__(self)

		self.files = [ ]
		"""
L10n files initialized
		"""
		self.lang = lang
		"""
L10n language code
		"""
	#

	def get(self, key, default = None):
	#
		"""
python.org: Return the value for key if key is in the dictionary, else default.

:return: (str) L10n value
:since:  v0.1.01
		"""

		return Binary.str(dict.get(self, key, default))
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

		if (file_pathname not in self.files or CachedJsonFile.is_changed(file_pathname)):
		#
			json_data = CachedJsonFile.read(file_pathname)
			if (type(json_data) == dict): self.update(json_data)
		#
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
#

##j## EOF