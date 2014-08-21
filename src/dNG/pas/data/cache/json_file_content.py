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

from dNG.data.json_resource import JsonResource
from dNG.pas.data.logging.log_line import LogLine
from dNG.pas.module.named_loader import NamedLoader
from dNG.pas.runtime.value_exception import ValueException
from .file_content import FileContent

class JsonFileContent(FileContent):
#
	"""
"JsonFileContent" provides access to JSON files on disk or cached.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v0.1.02
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	@staticmethod
	def read(file_pathname, required = False):
	#
		"""
Read data from the given file or from cache.

:param file_pathname: File path and name
:param required: True if missing files should throw an exception

:return: (mixed) File data; None on error
:since:  v0.1.02
		"""

		# pylint: disable=maybe-no-member

		_return = FileContent._read_cache(file_pathname, required)

		if (not isinstance(_return, dict)):
		#
			file_content = FileContent._read_file(file_pathname, required)

			if (file_content != None):
			#
				cache_instance = NamedLoader.get_singleton("dNG.pas.data.cache.Content", False)
				_return = JsonResource().json_to_data(file_content)

				if (_return == None):
				#
					if (required): raise ValueException("{0} is not a valid JSON encoded file".format(file_pathname))
					LogLine.warning("{0} is not a valid JSON encoded file", file_pathname, context = "pas_core")
				#
				elif (cache_instance != None): cache_instance.set_file(file_pathname, _return, len(file_content))
			#
		#

		return _return
	#
#

##j## EOF