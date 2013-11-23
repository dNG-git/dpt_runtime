# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.CachedFile
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

from dNG.data.file import File
from dNG.pas.data.logging.log_line import LogLine
from dNG.pas.module.named_loader import NamedLoader
from .traced_exception import TracedException

class CachedFile(object):
#
	"""
"CachedFile" provides generic access to files on disk or cached.

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

		cache_instance = NamedLoader.get_singleton("dNG.pas.data.Cache", False)
		file_pathname = path.normpath(file_pathname)
		_return = (None if (cache_instance == None) else cache_instance.get_file(file_pathname))

		if (_return == None):
		#
			file_object = File()

			if (file_object.open(file_pathname, True, "r")):
			#
				_return = file_object.read()
				file_object.close()

				_return = _return.replace("\r", "")
				if (cache_instance != None): cache_instance.set_file(file_pathname, _return)
			#
			elif (required): raise TracedException("{0} not found".format(file_pathname))
			else: LogLine.debug("{0} not found".format(file_pathname))
		#

		return _return
	#
#

##j## EOF