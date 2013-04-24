# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.cache
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

from dNG.pas.module.named_loader import direct_named_loader

try:
#
	from pyinotify import IN_CLOSE_WRITE, ProcessEvent, ThreadedNotifier, WatchManager
	_direct_cache_mode = "inotify"
#
except ImportError: _direct_cache_mode = "fs"

if (_direct_cache_mode == "fs"):
#
	class ProcessEvent(object):
	#
		"""
Dummy ProcessEvent class for unsupported pyinotify

:author:    direct Netware Group
:copyright: direct Netware Group - All rights reserved
:package:   pas.core
:since:     v0.1.00
:license:   http://www.direct-netware.de/redirect.py?licenses;mpl2
            Mozilla Public License, v. 2.0
		"""

		pass
	#

class direct_cache(dict, ProcessEvent):
#
	"""
The settings singleton provides methods on top of an dict.

:author:    direct Netware Group
:copyright: direct Netware Group - All rights reserved
:package:   pas.core
:since:     v0.1.00
:license:   http://www.direct-netware.de/redirect.py?licenses;mpl2
            Mozilla Public License, v. 2.0
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
	watchmanager_instance = None
	"""
pyinotify WatchManager instance
	"""

	def __init__(self):
	#
		"""
Constructor __init__(direct_cache)

:since: v0.1.00
		"""

		global _direct_cache_mode

		dict.__init__(self)

		self.cache_max_size = 104857600
		"""
Max size of the cache
		"""
		self.history = [ ]
		"""
Holds a history of requests and updates (newest first)
		"""
		self.log_handler = direct_named_loader.get_singleton("dNG.pas.data.logging.log_handler", False)
		"""
The log_handler is called whenever debug messages should be logged or errors
happened.
		"""
		self.size = 0
		"""
Size in bytes
		"""
		self.watched_files = { }
		"""
pyinotify watch fds or dict with latest modified timestamps
		"""

		if (self.log_handler != None): self.log_handler.debug("pas.cache mode is '{0}'".format(_direct_cache_mode))
	#

	def __del__(self):
	#
		"""
Destructor __del__(direct_cache)

:since: v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.return_instance()
	#

	def get_file(self, file_pathname):
	#
		"""
Get the settings singleton.

:param count: Count "get()" request

:return: (direct_settings) Object on success
:since:  v0.1.00
		"""

		global _direct_cache_mode
		var_return = None

		direct_cache.synchronized.acquire()

		if (_direct_cache_mode == "fs" and file_pathname in self.watched_files and self.watched_files[file_pathname] != os.stat(file_pathname).st_mtime):
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

		direct_cache.synchronized.release()

		return var_return
	#

	def process_IN_CLOSE_WRITE(self, event):
	#
		direct_cache.synchronized.acquire()

		self.size -= len(self[event.pathname])
		self.history.remove(event.pathname)
		del(self[event.pathname])

		if (event.pathname in self.watched_files):
		#
			direct_cache.watchmanager_instance.rm_watch(self.watched_files[event.pathname])
			del(self.watched_files[event.pathname])
		#

		direct_cache.synchronized.release()
	#

	def return_instance(self):
	#
		"""
The last "return_instance()" call will free the singleton reference.

:since: v0.1.00
		"""

		direct_cache.synchronized.acquire()

		if (direct_cache != None):
		#
			if (direct_cache.ref_count > 0): direct_cache.ref_count -= 1

			if (direct_cache.ref_count == 0):
			#
				direct_cache.instance = None

				if (direct_cache.pyinotify_instance != None):
				#
					direct_cache.pyinotify_instance.stop()
					direct_cache.pyinotify_instance = None
				#
			#
		#

		direct_cache.synchronized.release()
	#

	def set_file(self, file_pathname, cache_entry):
	#
		"""
Get the settings singleton.

:param count: Count "get()" request

:return: (direct_settings) Object on success
:since:  v0.1.00
		"""

		global _direct_cache_mode

		direct_cache.synchronized.acquire()

		if (file_pathname not in self):
		#
			if (_direct_cache_mode == "inotify"): self.watched_files.update(direct_cache.watchmanager_instance.add_watch(file_pathname, IN_CLOSE_WRITE))
			else: self.watched_files[file_pathname] = os.stat(file_pathname).st_mtime

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
		elif (self[file_pathname] != cache_entry):
		#
			self.size -= len(self[file_pathname])
			self.history.remove(file_pathname)

			self[file_pathname] = cache_entry
			self.history.insert(0, file_pathname)
			self.size += len(cache_entry)
		#

		direct_cache.synchronized.release()
	#

	@staticmethod
	def get_instance(count = True):
	#
		"""
Get the cache singleton.

:param count: Count "get()" request

:return: (direct_cache) Object on success
:since:  v0.1.00
		"""

		global _direct_cache_mode

		direct_cache.synchronized.acquire()

		if (direct_cache.instance == None):
		#
			direct_cache.instance = direct_cache()

			if (_direct_cache_mode == "inotify"):
			#
				if (direct_cache.watchmanager_instance == None): direct_cache.watchmanager_instance = WatchManager()

				direct_cache.pyinotify_instance = ThreadedNotifier(direct_cache.watchmanager_instance, direct_cache.instance, timeout = 5)
				direct_cache.pyinotify_instance.start()
			#
		#

		if (count): direct_cache.ref_count += 1

		direct_cache.synchronized.release()

		return direct_cache.instance
	#
#

##j## EOF