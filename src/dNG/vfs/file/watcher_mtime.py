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

# pylint: disable=import-error,no-name-in-module

import os

try: from urllib.parse import quote
except ImportError: from urllib import quote

from dNG.runtime.exception_log_trap import ExceptionLogTrap
from dNG.runtime.instance_lock import InstanceLock
from dNG.runtime.thread_lock import ThreadLock
from dNG.vfs.abstract_watcher import AbstractWatcher

class WatcherMtime(AbstractWatcher):
#
	"""
"file:///" watcher using os.stat to detect changes.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	_instance = None
	"""
WatcherMtime instance
	"""
	_instance_lock = InstanceLock()
	"""
Thread safety instance lock
	"""

	def __init__(self):
	#
		"""
Constructor __init__(Watcher)

:since: v0.2.00
		"""

		self._lock = ThreadLock()
		"""
	Thread safety lock
		"""
		self.watched_callbacks = { }
		"""
Callbacks for watched files
		"""
		self.watched_paths = { }
		"""
Dict with latest modified timestamps
		"""
	#

	def check(self, _path):
	#
		"""
Checks a given path for changes if "is_synchronous()" is true.

:param _path: Filesystem path

:return: (bool) True if the given path URL has been changed since last check
         and "is_synchronous()" is true.
:since:  v0.2.00
		"""

		_return = False

		with self._lock:
		#
			if (self.watched_paths is not None and _path in self.watched_paths and self.watched_paths[_path] != os.stat(_path).st_mtime):
			#
				_return = True
				url = "file:///{0}".format(quote(_path, "/"))

				for callback in self.watched_callbacks[_path]:
				#
					with ExceptionLogTrap("pas_core"): callback(WatcherMtime.EVENT_TYPE_MODIFIED, url)
				#
			#
		#

		return _return
	#

	def free(self):
	#
		"""
Frees all watcher callbacks for garbage collection.

:since: v0.2.00
		"""

		with self._lock:
		#
			if (self.watched_paths is not None and len(self.watched_paths) > 0):
			#
				self.watched_callbacks = None
				self.watched_paths = None
			#
		#
	#

	def is_synchronous(self):
	#
		"""
Returns true if changes are only detected after "check()" has been
called.

:return: (bool) True if changes are not detected automatically
:since:  v0.2.00
		"""

		return True
	#

	def is_watched(self, _path, callback = None):
	#
		"""
Returns true if the filesystem path is already watched. It will return false
if a callback is given but not defined for the watched path.

:param _path: Filesystem path
:param callback: Callback to be checked for the watched filesystem path

:return: (bool) True if watched with the defined callback or any if not
         defined.
:since:  v0.2.00
		"""

		with self._lock:
		#
			_return = (self.watched_paths is not None and _path in self.watched_paths)
			if (_return and callback is not None): _return = (callback in self.watched_callbacks[_path])
		#

		return _return
	#

	def register(self, _path, callback):
	#
		"""
Handles registration of filesystem watches and its callbacks.

:param _path: Filesystem path to be watched
:param callback: Callback for the path

:return: (bool) True on success
:since:  v0.2.00
		"""

		_return = True

		with self._lock:
		#
			if (self.watched_callbacks is not None):
			#
				if (_path not in self.watched_paths):
				#
					self.watched_paths[_path] = (os.stat(_path).st_mtime if (os.access(_path, os.R_OK)) else -1)
					self.watched_callbacks[_path] = [ ]
				#

				if (callback not in self.watched_callbacks[_path]): self.watched_callbacks[_path].append(callback)
			#
		#

		return _return
	#

	def stop(self):
	#
		"""
Stops all watchers.

:since: v0.2.00
		"""

		if (WatcherMtime._instance is not None):
		# Thread safety
			with WatcherMtime._instance_lock:
			#
				if (WatcherMtime._instance is not None): WatcherMtime._instance = None
			#
		#

		self.free()
	#

	def unregister(self, _path, callback):
	#
		"""
Handles deregistration of filesystem watches.

:param _path: Filesystem path watched
:param callback: Callback for the path

:return: (bool) True on success
:since:  v0.2.00
		"""

		_return = True

		with self._lock:
		#
			if (self.watched_paths is not None and _path in self.watched_paths):
			#
				if (callback is None): self.watched_callbacks[_path] = [ ]
				elif (callback in self.watched_callbacks[_path]): self.watched_callbacks[_path].remove(callback)

				if (len(self.watched_callbacks[_path]) < 1):
				#
					del(self.watched_callbacks[_path])
					del(self.watched_paths[_path])
				#
			#
			else: _return = False
		#

		return _return
	#

	@staticmethod
	def get_instance():
	#
		"""
Get the WatcherMtime singleton.

:return: (WatcherMtime) Object on success
:since:  v0.2.00
		"""

		if (WatcherMtime._instance is None):
		# Thread safety
			with WatcherMtime._instance_lock:
			#
				if (WatcherMtime._instance is None): WatcherMtime._instance = WatcherMtime()
			#
		#

		return WatcherMtime._instance
	#
#

##j## EOF