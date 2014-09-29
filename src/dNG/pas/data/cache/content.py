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

from weakref import ref

from dNG.pas.data.settings import Settings
from dNG.pas.vfs.file.watcher import Watcher
from .abstract_file_content import AbstractFileContent
#from .abstract_value import AbstractValue

class Content(dict, Watcher, AbstractFileContent):
#
	"""
The cache singleton for content provides memory-based caching mechanisms for
files as well as timestamp based content.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v0.1.02
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	# pylint: disable=unused-argument

	_weakref_instance = None
	"""
Cache weakref instance
	"""

	def __init__(self):
	#
		"""
Constructor __init__(Content)

:since: v0.1.02
		"""

		dict.__init__(self)
		Watcher.__init__(self)
		AbstractFileContent.__init__(self)
		#AbstractValue.__init__(self)

		self.history = [ ]
		"""
Holds a history of requests and updates (newest first)
		"""
		self.max_size = int(Settings.get("pas_core_cache_memory_max_size", 104857600))
		"""
Max size of the cache
		"""
		self.size = 0
		"""
Size in bytes
		"""
	#

	def __repr__(self):
	#
		"""
python.org: Called by the repr() built-in function and by string conversions
(reverse quotes) to compute the "official" string representation of an
object.

:return: (str) String representation
:since:  v0.1.02
		"""

		return object.__repr__(self)
	#

	def get_file(self, file_pathname):
	#
		"""
Get the content from cache for the given file path and name.

:param file_pathname: Cached file path and name

:return: (mixed) Cached entry; None if no hit or changed
:since:  v0.1.02
		"""

		_return = None

		if (self.is_synchronous()): self.check("file:///{0}".format(file_pathname))

		if (file_pathname in self):
		# Thread safety
			with self._lock:
			#
				if (file_pathname in self):
				#
					_return = self[file_pathname]['entry']
					self.history.remove(file_pathname)
					self.history.insert(0, file_pathname)
				#
			#
		#

		return _return
	#

	def is_file_known(self, file_pathname):
	#
		"""
Return true if the given file path and name is cached.

:param file_pathname: Cached file path and name

:return: (bool) True if currently cached
:since:  v0.1.02
		"""

		return (file_pathname in self)
	#

	def set_file(self, file_pathname, cache_entry, cache_entry_size = None):
	#
		"""
Fill the cache for the given file path and name with the given cache entry.

:param file_pathname: File path and name
:param cache_entry: Cached entry data

:since: v0.1.02
		"""

		if (cache_entry_size == None): cache_entry_size = len(cache_entry)

		with self._lock:
		#
			if (file_pathname not in self):
			#
				is_valid = self.register("file:///{0}".format(file_pathname), self._uncache_changed)

				if (is_valid):
				#
					self[file_pathname] = { "entry": cache_entry, "size": cache_entry_size }
					self.history.insert(0, file_pathname)
					self.size += cache_entry_size

					if (self.size > self.max_size):
					#
						key = self.history.pop()

						self.size -= len(self[key]['size'])
						del(self[key])
					#
				#
			#
			elif (self[file_pathname]['entry'] != cache_entry):
			#
				self.size -= self[file_pathname]['size']
				self.history.remove(file_pathname)

				self[file_pathname] = { "entry": cache_entry, "size": cache_entry_size }
				self.history.insert(0, file_pathname)
				self.size += cache_entry_size
			#
		#
	#

	def _uncache_changed(self, event_type, url, changed_value = None):
	#
		"""
Remove changed files from the cache.

:param event_type: Filesystem watcher event type
:param url: Filesystem URL watched
:param changed_value: Changed filesystem value

:since: v0.1.02
		"""

		file_pathname = url[8:]

		if (file_pathname in self):
		#
			with self._lock:
			# Thread safety
				if (file_pathname in self):
				#
					self.size -= self[file_pathname]['size']
					self.history.remove(file_pathname)
					del(self[file_pathname])

					self.unregister(url, self._uncache_changed)
				#
			#
		#
	#

	@staticmethod
	def get_instance():
	#
		"""
Get the Content singleton.

:return: (Content) Object on success
:since:  v0.1.02
		"""

		_return = (None if (Content._weakref_instance == None) else Content._weakref_instance())

		if (_return == None):
		#
			_return = Content()
			Content._weakref_instance = ref(_return)
		#

		return _return
	#
#

##j## EOF