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

from threading import RLock
import os

from .logging.log_line import LogLine

try:
#
	from pyinotify import IN_CLOSE_WRITE, Notifier, ProcessEvent, ThreadedNotifier, WatchManager
	_mode = "inotify"
#
except ImportError: _mode = "fs"

if (_mode == "fs"):
#
	class ProcessEvent(object):
	#
		"""
Dummy ProcessEvent class for unsupported pyinotify

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
		"""

		pass
	#

class Cache(dict, ProcessEvent):
#
	"""
The cache singleton provides caching mechanisms.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	USE_FS = 1
	"""
Use filesystem mtimes to detect changes
	"""
	USE_INOTIFY = 2
	"""
Use inotify to detect changes
	"""

	instance = None
	"""
Cache instance
	"""
	pyinotify_instance = None
	"""
pyinotify instance
	"""
	ref_count = 0
	"""
Instances used
	"""
	synchronized = RLock()
	"""
Lock used in multi thread environments.
	"""
	use_thread = True
	"""
If the pyinotify instance should run in a separate thread
	"""
	use_pyinotify = False
	"""
Use pyinotify if available
	"""
	watchmanager_instance = None
	"""
pyinotify WatchManager instance
	"""

	def __init__(self):
	#
		"""
Constructor __init__(Cache)

:since: v0.1.00
		"""

		dict.__init__(self)

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
		self.watched_files = { }
		"""
pyinotify watch fds or dict with latest modified timestamps
		"""

		LogLine.debug("pas.cache mode is '{0}'".format("inotify" if (Cache.use_pyinotify) else "fs"))
	#

	def get_file(self, file_pathname):
	#
		"""
Get the content from cache for the given file path and name.

:param file_pathname: Cached file path and name

:return: (mixed) Cached entry; None if no hit or changed
:since:  v0.1.00
		"""

		var_return = None

		with Cache.synchronized:
		#
			if (Cache.use_pyinotify):
			#
				if (not Cache.use_thread): Cache.pyinotify_instance.check_events()
			#
			elif (file_pathname in self.watched_files and self.watched_files[file_pathname] != os.stat(file_pathname).st_mtime):
			#
				self.size -= len(self[file_pathname])
				self.history.remove(file_pathname)
				del(self[file_pathname])
			#
	
			if (file_pathname in self):
			#
				var_return = self[file_pathname]
				self.history.remove(file_pathname)
				self.history.insert(0, file_pathname)
			#
		#

		return var_return
	#

	def process_IN_CLOSE_WRITE(self, event):
	#
		"""
Handles "IN_CLOSE_WRITE" inotify events.

:param event: Inotify event

:since: v0.1.00
		"""

		with Cache.synchronized:
		#
			self.size -= len(self[event.pathname])
			self.history.remove(event.pathname)
			del(self[event.pathname])

			if (event.pathname in self.watched_files):
			#
				Cache.watchmanager_instance.rm_watch(self.watched_files[event.pathname])
				del(self.watched_files[event.pathname])
			#
		#
	#

	def return_instance(self):
	#
		"""
The last "return_instance()" call will free the singleton reference.

:since: v0.1.00
		"""

		with Cache.synchronized:
		#
			if (Cache.instance != None):
			#
				if (Cache.ref_count > 0): Cache.ref_count -= 1
	
				if (Cache.ref_count == 0):
				#
					Cache.instance = None
	
					if (Cache.pyinotify_instance != None):
					#
						try: Cache.pyinotify_instance.stop()
						except: pass
	
						Cache.pyinotify_instance = None
					#
				#
			#
		#
	#

	def set_file(self, file_pathname, cache_entry):
	#
		"""
Fill the cache for the given file path and name with the given cache entry.

:param file_pathname: File path and name
:param cache_entry: Cache entry

:since: v0.1.00
		"""

		with Cache.synchronized:
		#
			if (file_pathname not in self):
			#
				is_valid = True

				if (Cache.use_pyinotify):
				#
					inotify_result = Cache.watchmanager_instance.add_watch(file_pathname, IN_CLOSE_WRITE)

					if (inotify_result[file_pathname] < 0): is_valid = False
					else: self.watched_files.update(inotify_result)
				#
				else: self.watched_files[file_pathname] = os.stat(file_pathname).st_mtime

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

	@staticmethod
	def get_instance(count = True):
	#
		"""
Get the cache singleton.

:param count: Count "get()" request

:return: (Cache) Object on success
:since:  v0.1.00
		"""

		with Cache.synchronized:
		#
			if (Cache.instance == None):
			#
				Cache.instance = Cache()

				if (Cache.use_pyinotify):
				#
					if (Cache.watchmanager_instance == None): Cache.watchmanager_instance = WatchManager()

					if (Cache.use_thread):
					#
						Cache.pyinotify_instance = ThreadedNotifier(Cache.watchmanager_instance, Cache.instance, timeout = 5)
						Cache.pyinotify_instance.start()
					#
					else: Cache.pyinotify_instance = Notifier(Cache.watchmanager_instance, Cache.instance, timeout = 5)
				#
			#

			if (count): Cache.ref_count += 1
		#

		return Cache.instance
	#

	@staticmethod
	def set_implementation(implementation = None):
	#
		"""
Set the filesystem change implementation to use.

:param implementation: Implementation identifier

:since: v0.1.00
		"""

		global _mode

		with Cache.synchronized:
		#
			if (implementation == Cache.USE_INOTIFY and _mode == "inotify"): Cache.use_pyinotify = True
			else: Cache.use_pyinotify = False
		#
	#
#

##j## EOF