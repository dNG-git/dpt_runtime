# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.Cache
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

from weakref import ref

from dNG.pas.vfs.file.watcher import Watcher

class Cache(dict, Watcher):
#
	"""
The cache singleton provides caching mechanisms.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v0.1.01
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
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
Constructor __init__(Cache)

:since: v0.1.01
		"""

		dict.__init__(self)
		Watcher.__init__(self)

		self.cache_max_size = 104857600
		"""
Max size of the cache
		"""
		self.history = [ ]
		"""
Holds a history of requests and updates (newest first)
		"""
		self.size = 0
		"""
Size in bytes
		"""
	#

	def get_file(self, file_pathname):
	#
		"""
Get the content from cache for the given file path and name.

:param file_pathname: Cached file path and name

:return: (mixed) Cached entry; None if no hit or changed
:since:  v0.1.01
		"""

		_return = None

		with self._lock:
		#
			if (self.is_synchronous()): self.check("file:///{0}".format(file_pathname))

			if (file_pathname in self):
			#
				_return = self[file_pathname]
				self.history.remove(file_pathname)
				self.history.insert(0, file_pathname)
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
:since:  v0.1.01
		"""

		with self._lock: return (file_pathname in self)
	#

	def set_file(self, file_pathname, cache_entry):
	#
		"""
Fill the cache for the given file path and name with the given cache entry.

:param file_pathname: File path and name
:param cache_entry: Cache entry

:since: v0.1.00
		"""

		with self._lock:
		#
			if (file_pathname not in self):
			#
				is_valid = self.register("file:///{0}".format(file_pathname), self.uncache_changed)

				if (is_valid):
				#
					self[file_pathname] = cache_entry
					self.history.insert(0, file_pathname)
					self.size += len(cache_entry)

					if (self.size > self.cache_max_size):
					#
						key = self.history.pop()

						self.size -= len(self[key])
						del(self[key])
					#
				#
			#
			elif (self[file_pathname] != cache_entry):
			#
				self.size -= len(self[file_pathname])
				self.history.remove(file_pathname)

				self[file_pathname] = cache_entry
				self.history.insert(0, file_pathname)
				self.size += len(cache_entry)
			#
		#
	#

	def uncache_changed(self, event_type, url, changed_value = None):
	#
		"""
Remove changed files from the cache.

:param event_type: Filesystem watcher event type
:param url: Filesystem URL watched
:param changed_value: Changed filesystem value

:since: v0.1.01
		"""

		with self._lock:
		#
			file_pathname = url[8:]

			if (file_pathname in self):
			#
				self.size -= len(self[file_pathname])
				self.history.remove(file_pathname)
				del(self[file_pathname])

				self.unregister(url, self.uncache_changed)
			#
		#
	#

	@staticmethod
	def get_instance():
	#
		"""
Get the Cache singleton.

:return: (Cache) Object on success
:since:  v0.1.00
		"""

		_return = (None if (Cache._weakref_instance == None) else Cache._weakref_instance())

		if (_return == None):
		#
			_return = Cache()
			Cache._weakref_instance = ref(_return)
		#

		return _return
	#
#

##j## EOF