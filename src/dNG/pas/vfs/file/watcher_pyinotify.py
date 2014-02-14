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

# pylint: disable=import-error,unused-argument

from pyinotify import IN_ATTRIB, IN_CLOSE_WRITE, IN_CREATE, IN_DELETE, IN_DELETE_SELF, IN_MODIFY, IN_MOVE_SELF, IN_MOVED_FROM, IN_MOVED_TO, ThreadedNotifier, WatchManager
from os import path

from dNG.pas.runtime.instance_lock import InstanceLock
from dNG.pas.runtime.thread_lock import ThreadLock
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
	instance_lock = InstanceLock()
	"""
Thread safety instance lock
	"""

	def __init__(self):
	#
		"""
Constructor __init__(WatcherPyinotify)

:since: v0.1.01
		"""

		WatchManager.__init__(self)

		self.lock = ThreadLock()
		"""
	Thread safety lock
		"""
		self.pyinotify_instance = None
		"""
pyinotify instance
		"""
		self.watched_callbacks = { }
		"""
Callbacks for watched files
		"""
		self.watched_path_files = { }
		"""
pyinotify watch fds
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

		with self.lock:
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

	def is_synchronous(self):
	#
		"""
Returns true if changes are only detected after "check()" has been
called.

:return: (bool) True if changes are not detected automatically
:since:  v0.1.01
		"""

		return False
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

		_return = False

		with self.lock:
		#
			if (_path in self.watched_callbacks): _return = (True if (callback == None) else (callback in self.watched_callbacks[_path]))
			elif (not path.isdir(_path)): _return = self.is_watched(path.split(_path)[0], callback)
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

		with self.lock:
		#
			if (_path in self.watched_callbacks): _return = self.watched_callbacks[_path]
			elif (not path.isdir(_path)): _return = self.get_callbacks(path.split(_path)[0])
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

		# pylint: disable=no-member

		_return = True

		with self.lock:
		#
			if (path.isdir(_path)): directory_path = _path
			else: directory_path = path.split(_path)[0]

			if (directory_path not in self.watched_paths):
			#
				inotify_result = self.add_watch(directory_path, (IN_ATTRIB | IN_CLOSE_WRITE | IN_CREATE | IN_DELETE | IN_DELETE_SELF | IN_MODIFY | IN_MOVE_SELF | IN_MOVED_FROM | IN_MOVED_TO))

				if (inotify_result[directory_path] < 0): _return = False
				else: self.watched_paths.update(inotify_result)
			#

			if (_return):
			#
				if (directory_path not in self.watched_path_files): self.watched_path_files[directory_path] = [ _path ]
				elif (_path not in self.watched_path_files[directory_path]): self.watched_path_files[directory_path].append(_path)

				if (_path not in self.watched_callbacks): self.watched_callbacks[_path] = [ callback ]
				elif (callback not in self.watched_callbacks[_path]): self.watched_callbacks[_path].append(callback)
			#
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

		# pylint: disable=no-member

		_return = True

		with self.lock:
		#
			is_directory = path.isdir(_path)

			if (is_directory): directory_path = _path
			else: directory_path = path.split(_path)[0]

			if (directory_path in self.watched_path_files and _path in self.watched_paths):
			#
				if (callback == None or _deleted): self.watched_callbacks[_path] = [ ]
				elif (callback in self.watched_callbacks[_path]): self.watched_callbacks[_path].remove(callback)

				if (len(self.watched_callbacks[_path]) < 1): del(self.watched_callbacks[_path])

				if (is_directory and _deleted):
				#
					for filepath in self.watched_path_files[directory_path]: self.unregister(filepath, None, True)
				#

				if (len(self.watched_path_files[directory_path]) < 1):
				#
					if (not _deleted): self.rm_watch(self.watched_paths[directory_path])
					del(self.watched_path_files[directory_path])
					del(self.watched_paths[directory_path])
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

		with WatcherPyinotify.instance_lock:
		#
			if (WatcherPyinotify.instance == None): WatcherPyinotify.instance = WatcherPyinotify()
		#

		return WatcherPyinotify.instance
	#

	@staticmethod
	def stop():
	#
		"""
Stops all watchers.

:since: v0.1.01
		"""

		with WatcherPyinotify.instance_lock:
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