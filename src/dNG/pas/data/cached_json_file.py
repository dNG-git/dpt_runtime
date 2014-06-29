# -*- coding: utf-8 -*-
##j## BOF

"""
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
"""

from dNG.data.json_resource import JsonResource
from dNG.pas.data.logging.log_line import LogLine
from dNG.pas.runtime.value_exception import ValueException
from .cached_file import CachedFile

class CachedJsonFile(CachedFile):
#
	"""
"CachedJsonFile" provides access to JSON files on disk or cached.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	@staticmethod
	def read(file_pathname, required = False):
	#
		"""
Read and parse data from the given file or from cache.

:param file_pathname: File path and name of the JSON file
:param required: True if missing files or parser errors should throw
                 exceptions

:return: (mixed) Parsed JSON data; None on error
:since:  v0.1.01
		"""

		_return = None

		file_content = CachedFile.read(file_pathname, required)

		if (file_content != None):
		#
			json_resource = JsonResource()
			_return = json_resource.json_to_data(file_content)

			if (_return == None):
			#
				if (required): raise ValueException("{0} is not a valid JSON encoded file".format(file_pathname))
				LogLine.warning("{0} is not a valid JSON encoded file", file_pathname, context = "pas_core")
			#
		#

		return _return
	#
#

##j## EOF