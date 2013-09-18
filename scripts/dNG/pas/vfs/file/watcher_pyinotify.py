# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.vfs.file.WatcherPyinotify
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

from pyinotify import IN_ATTRIB, IN_CLOSE_WRITE, IN_CREATE, IN_DELETE, IN_DELETE_SELF, IN_MODIFY, ThreadedNotifier, WatchManager
from threading import RLock
from os import path

from .watcher_pyinotify_callback import WatcherPyinotifyCallback

class WatcherPyinotify(WatchManager):
#
	"""
"file:///" watcher using pyinotify's ThreadedNotifier.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v0.1.01
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	instance = None
	"""
WatcherPyinotify weakref instance
	"""
	synchronized = RLock()
	"""
Lock used in multi thread environments.
	"""

	def __init__(self):
	#
		"""
Constructor __init__(WatcherPyinotify)

:since: v0.1.01
		"""

		WatchManager.__init__(self)

		self.pyinotify_instance = None
		"""
pyinotify instance
		"""
		self.watched_callbacks = { }
		"""
Callbacks for watched files
		"""
		self.watched_paths = { }
		"""
pyinotify watch fds
		"""

		self._init_notifier()
	#

	def check(self, _path):
	#
		"""
Checks a given path for changes if "is_synchronous()" is true.

:param _path: Filesystem path

:return: (bool) True if the given path URL has been changed since last check
         and "is_synchronous()" is true.
:since:  v0.1.01
		"""

		return False
	#

	def free(self):
	#
		"""
Frees all watcher callbacks for garbage collection.

:since: v0.1.01
		"""

		with WatcherPyinotify.synchronized:
		#
			if (len(self.watched_paths) > 0):
			#
				self.pyinotify_instance.stop()
				self.watched_callbacks = { }
				self.watched_paths = { }
			#
		#
	#

	def _init_notifier(self):
	#
		"""
Initializes the pyinotify instance.

:since: v0.1.01
		"""

		self.pyinotify_instance = ThreadedNotifier(self, WatcherPyinotifyCallback(self), timeout = 5)
		self.pyinotify_instance.start()
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
:since:  v0.1.01
		"""

		with WatcherPyinotify.synchronized:
		#
			_return = (_path in self.watched_paths)
			if (_return and callback != None): _return = (callback in self.watched_callbacks[_path])
		#

		return _return
	#

	def get_callbacks(self, _path):
	#
		"""
Returns all registered callbacks for the given path.

:param _path: Filesystem path

:since: v0.1.01
		"""

		_return = [ ]

		with WatcherPyinotify.synchronized:
		#
			if (_path in self.watched_callbacks): _return = self.watched_callbacks[_path]
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
:since:  v0.1.01
		"""

		_return = True

		with WatcherPyinotify.synchronized:
		#
			if (_path not in self.watched_paths):
			#
				inotify_result = self.add_watch(_path, ((IN_ATTRIB | IN_CREATE | IN_DELETE | IN_DELETE_SELF | IN_MODIFY) if (path.isdir(_path)) else (IN_CLOSE_WRITE | IN_DELETE_SELF)))

				if (inotify_result[_path] < 0): _return = False
				else:
				#
					self.watched_paths.update(inotify_result)
					self.watched_callbacks[_path] = [ ]
				#
			#

			if (_return and callback not in self.watched_callbacks[_path]): self.watched_callbacks[_path].append(callback)
		#

		return _return
	#

	def unregister(self, _path, callback, _deleted = False):
	#
		"""
Handles deregistration of filesystem watches.

:param _path: Filesystem path watched
:param callback: Callback for the path
:param _deleted: File has been deleted

:return: (bool) True on success
:since:  v0.1.01
		"""

		_return = True

		with WatcherPyinotify.synchronized:
		#
			if (_path in self.watched_paths):
			#
				if (callback == None or _deleted): self.watched_callbacks[_path] = [ ]
				elif (callback in self.watched_callbacks[_path]): self.watched_callbacks[_path].remove(callback)

				if (len(self.watched_callbacks[_path]) < 1):
				#
					if (not _deleted): self.rm_watch(self.watched_paths[_path])
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
Get the WatcherPyinotify singleton.

:return: (WatcherPyinotify) Object on success
:since:  v0.1.00
		"""

		with WatcherPyinotify.synchronized:
		#
			if (WatcherPyinotify.instance == None): WatcherPyinotify.instance = WatcherPyinotify()
		#

		return WatcherPyinotify.instance
	#

	@staticmethod
	def is_synchronous():
	#
		"""
Returns true if changes are only detected after "check()" has been
called.

:return: (bool) True if changes are not detected automatically
:since:  v0.1.01
		"""

		return False
	#

	@staticmethod
	def stop():
	#
		"""
Stops all watchers.

:since: v0.1.01
		"""

		with WatcherPyinotify.synchronized:
		#
			if (WatcherPyinotify.instance != None):
			#
				WatcherPyinotify.instance.pyinotify_instance.stop()
				WatcherPyinotify.instance = None
			#
		#
	#
#

##j## EOF