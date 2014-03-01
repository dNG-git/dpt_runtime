# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.vfs.file.Watcher
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

# pylint: disable=import-error,no-name-in-module

try: from urllib.parse import unquote, urlsplit
except ImportError:
#
	from urllib import unquote
	from urlparse import urlsplit
#

from dNG.pas.data.logging.log_line import LogLine
from dNG.pas.runtime.thread_lock import ThreadLock
from dNG.pas.vfs.abstract_watcher import AbstractWatcher

_IMPLEMENTATION_INOTIFY = 1
"""
pyinotify implementation
"""
_IMPLEMENTATION_INOTIFY_SYNC = 2
"""
Synchronous pyinotify implementation
"""
_IMPLEMENTATION_MTIME = 3
"""
Filesystem mtime implementation
"""

try:
#
	from .watcher_pyinotify import WatcherPyinotify
	from .watcher_pyinotify_sync import WatcherPyinotifySync
	_mode = _IMPLEMENTATION_INOTIFY
#
except ImportError:
#
	_mode = _IMPLEMENTATION_MTIME
	WatcherPyinotify = None
#

from .watcher_mtime import WatcherMtime

class Watcher(AbstractWatcher):
#
	"""
"file:///" watcher for change events.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v0.1.01
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	IMPLEMENTATION_INOTIFY = _IMPLEMENTATION_INOTIFY
	"""
pyinotify implementation
	"""
	IMPLEMENTATION_INOTIFY_SYNC = _IMPLEMENTATION_INOTIFY_SYNC
	"""
Synchronous pyinotify implementation
	"""
	IMPLEMENTATION_MTIME = _IMPLEMENTATION_MTIME
	"""
Filesystem mtime implementation
	"""

	def __init__(self):
	#
		"""
Constructor __init__(Watcher)

:since: v0.1.01
		"""

		self.implementation = None
		"""
Watcher implementation instance
		"""
		self.lock = ThreadLock()
		"""
Thread safety lock
		"""
		self.watcher_class = None
		"""
Watcher implementation class
		"""

		self.set_implementation()
	#

	def check(self, url):
	#
		"""
Checks a given URL for changes if "is_synchronous()" is true.

:param url: Resource URL

:since: v0.1.01
		"""

		_path = self._get_path(url)

		with self.lock:
		#
			if (
				self.watcher_class != None and
				_path != None and
				_path.strip() != ""
			): self.watcher_class.get_instance().check(_path)
		#
	#

	def disable(self):
	#
		"""
Disables this watcher and frees all callbacks for garbage collection.

:since: v0.1.01
		"""

		with self.lock:
		#
			self.stop()
			self.implementation = None
		#
	#

	def free(self):
	#
		"""
Frees all watcher callbacks for garbage collection.

:since: v0.1.01
		"""

		with self.lock:
		#
			if (self.watcher_class != None): self.watcher_class.get_instance().free()
		#
	#

	def _get_path(self, url):
	#
		"""
Return the local filesystem path for the given "file:///" URL.

:param url: Filesystem URL

:return: (str) Filesystem path; None if not a "file:///" URL
:since:  v0.1.01
		"""

		url_elements = urlsplit(url)
		return (unquote(url_elements.path[1:]) if (url_elements.scheme == "file") else None)
	#

	def _init_watcher_class(self):
	#
		"""
Initializes the watcher instance.

:since: v0.1.01
		"""

		if (self.implementation != None and self.watcher_class == None):
		#
			if (
				WatcherPyinotify != None and
				self.implementation == _IMPLEMENTATION_INOTIFY
			): self.watcher_class = WatcherPyinotify
			elif (
				WatcherPyinotify != None and
				self.implementation == _IMPLEMENTATION_INOTIFY_SYNC
			): self.watcher_class = WatcherPyinotifySync
			else: self.watcher_class = WatcherMtime

			LogLine.debug("pas.vfs.file.Watcher mode is {0}".format(
				"synchronous"
				if (self.is_synchronous())
				else
				"asynchronous"
			))
		#
	#

	def is_synchronous(self):
	#
		"""
Returns true if changes are only detected after "check()" has been
called.

:return: (bool) True if changes are not detected automatically
:since:  v0.1.01
		"""

		with self.lock:
		#
			self._init_watcher_class()
			return (False if (self.watcher_class == None) else self.watcher_class.get_instance().is_synchronous())
		#
	#

	def is_watched(self, url, callback = None):
	#
		"""
Returns true if the resource URL is already watched. It will return false
if a callback is given but not defined for the watched URL.

:param url: Resource URL
:param callback: Callback to be checked for the watched resource URL

:return: (bool) True if watched with the defined callback or any if not
         defined.
:since:  v0.1.01
		"""

		_path = self._get_path(url)

		with self.lock:
		#
			if (self.watcher_class == None or _path == None or _path.strip() == ""): return False
			else: return self.watcher_class.get_instance().is_watched(_path, callback)
		#
	#

	def register(self, url, callback):
	#
		"""
Handles registration of resource URL watches and its callbacks.

:param url: Resource URL to be watched

:return: (bool) True on success
:since:  v0.1.01
		"""

		_path = self._get_path(url)

		with self.lock:
		#
			self._init_watcher_class()

			if (self.watcher_class == None or _path == None or _path.strip() == ""): return False
			else: return self.watcher_class.get_instance().register(_path, callback)
		#
	#

	def set_implementation(self, implementation = None):
	#
		"""
Set the filesystem watcher implementation to use.

:param implementation: Implementation identifier

:since: v0.1.01
		"""

		# global: _IMPLEMENTATION_INOTIFY, _IMPLEMENTATION_INOTIFY_SYNC, _IMPLEMENTATION_MTIME, _mode

		with self.lock:
		#
			if (self.watcher_class != None): self.stop()
		#

		if (
			_mode == _IMPLEMENTATION_INOTIFY and
			(implementation == None or implementation == _IMPLEMENTATION_INOTIFY)
		): self.implementation = _IMPLEMENTATION_INOTIFY
		elif (
			_mode == _IMPLEMENTATION_INOTIFY and
			implementation == _IMPLEMENTATION_INOTIFY_SYNC
		): self.implementation = _IMPLEMENTATION_INOTIFY_SYNC
		else: self.implementation = _IMPLEMENTATION_MTIME
	#

	def stop(self):
	#
		"""
Stops all watchers.

:since: v0.1.01
		"""

		with self.lock:
		#
			if (self.watcher_class != None):
			#
				self.watcher_class.get_instance().stop()
				self.watcher_class = None
			#
		#
	#

	def unregister(self, url, callback):
	#
		"""
Handles deregistration of resource URL watches.

:param url: Resource URL watched

:return: (bool) True on success
:since:  v0.1.01
		"""

		_path = self._get_path(url)

		with self.lock:
		#
			if (self.watcher_class == None or _path == None or _path.strip() == ""): return False
			else: return self.watcher_class.get_instance().unregister(_path, callback)
		#
	#
#

##j## EOF