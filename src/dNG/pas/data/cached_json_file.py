# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.CachedJsonFile
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

from dNG.data.json_parser import JsonParser
from dNG.pas.data.logging.log_line import LogLine
from .cached_file import CachedFile
from .traced_exception import TracedException

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
			json_parser = JsonParser()
			_return = json_parser.json2data(file_content)

			if (_return == None):
			#
				if (required): raise TracedException("{0} is not a valid JSON encoded file".format(file_pathname))
				LogLine.warning("{0} is not a valid JSON encoded file".format(file_pathname))
			#
		#

		return _return
	#
#

##j## EOF