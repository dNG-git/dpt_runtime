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

from os import path

from dNG.data.file import File
from dNG.pas.data.logging.log_line import LogLine
from dNG.pas.module.named_loader import NamedLoader
from dNG.pas.runtime.io_exception import IOException

class FileContent(object):
#
	"""
"FileContent" provides generic access to files on disk or cached.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v0.1.02
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	@staticmethod
	def is_changed(file_pathname):
	#
		"""
Returns false if the file is cached and not modified.

:param file_pathname: File path and name

:return: (bool) True if not cached or modified
:since:  v0.1.02
		"""

		_return = False

		cache_instance = NamedLoader.get_singleton("dNG.pas.data.cache.Content", False)
		file_pathname = path.normpath(file_pathname)

		if (cache_instance == None): _return = True
		else:
		#
			file_content = cache_instance.get_file(file_pathname)
			if (file_content == None): _return = True
		#

		return _return
	#

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

		if (_return == None):
		#
			_return = FileContent._read_file(file_pathname, required)

			if (_return != None):
			#
				cache_instance = NamedLoader.get_singleton("dNG.pas.data.cache.Content", False)
				if (cache_instance != None): cache_instance.set_file(file_pathname, _return)
			#
		#

		return _return
	#

	@staticmethod
	def _read_cache(file_pathname, required):
	#
		"""
Read data from cache.

:param file_pathname: File path and name
:param required: True if missing files should throw an exception

:return: (mixed) File data; None on error
:since: v0.1.02
		"""

		cache_instance = NamedLoader.get_singleton("dNG.pas.data.cache.Content", False)
		return (None if (cache_instance == None) else cache_instance.get_file(file_pathname))
	#

	@staticmethod
	def _read_file(file_pathname, required):
	#
		"""
Read data from the given file or from cache.

:param file_pathname: File path and name
:param required: True if missing files should throw an exception

:return: (mixed) File data; None on error
:since:  v0.1.02
		"""

		_return = None

		file_object = File()

		if (file_object.open(file_pathname, True, "r")):
		#
			_return = file_object.read()
			file_object.close()

			_return = _return.replace("\r", "")
		#
		elif (required): raise IOException("{0} not found".format(file_pathname))
		else: LogLine.debug("{0} not found", file_pathname, context = "pas_core")

		return _return
	#
#

##j## EOF