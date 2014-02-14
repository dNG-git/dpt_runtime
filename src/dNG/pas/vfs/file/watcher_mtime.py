# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.vfs.file.WatcherMtime
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

import os

try: from urllib.parse import quote
except ImportError: from urllib import quote

from dNG.pas.data.logging.log_line import LogLine
from dNG.pas.runtime.instance_lock import InstanceLock
from dNG.pas.runtime.thread_lock import ThreadLock
from dNG.pas.vfs.abstract_watcher import AbstractWatcher

class WatcherMtime(AbstractWatcher):
#
	"""
"file:///" watcher using os.stat to detect changes.

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
WatcherMtime instance
	"""
	instance_lock = InstanceLock()
	"""
Thread safety instance lock
	"""

	def __init__(self):
	#
		"""
Constructor __init__(Watcher)

:since: v0.1.01
		"""

		self.lock = ThreadLock()
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
:since:  v0.1.01
		"""

		# pylint: disable=broad-except

		_return = False

		with self.lock:
		#
			if (self.watched_paths != None and _path in self.watched_paths and self.watched_paths[_path] != os.stat(_path).st_mtime):
			#
				_return = True
				url = "file:///{0}".format(quote(_path, "/"))

				try:
				#
					for callback in self.watched_callbacks[_path]: callback(WatcherMtime.EVENT_TYPE_MODIFIED, url)
				#
				except Exception as handled_exception: LogLine.error(handled_exception)
			#
		#

		return _return
	#

	def free(self):
	#
		"""
Frees all watcher callbacks for garbage collection.

:since: v0.1.01
		"""

		with self.lock:
		#
			if (self.watched_paths != None and len(self.watched_paths) > 0):
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
:since:  v0.1.01
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
:since:  v0.1.01
		"""

		with self.lock:
		#
			_return = (self.watched_paths != None and _path in self.watched_paths)
			if (_return and callback != None): _return = (callback in self.watched_callbacks[_path])
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

		with self.lock:
		#
			if (self.watched_callbacks != None):
			#
				if (_path not in self.watched_paths and os.access(_path, os.R_OK)):
				#
					self.watched_paths[_path] = os.stat(_path).st_mtime
					self.watched_callbacks[_path] = [ ]
				#

				if (callback not in self.watched_callbacks[_path]): self.watched_callbacks[_path].append(callback)
			#
		#

		return _return
	#

	def unregister(self, _path, callback):
	#
		"""
Handles deregistration of filesystem watches.

:param _path: Filesystem path watched
:param callback: Callback for the path

:return: (bool) True on success
:since:  v0.1.01
		"""

		_return = True

		with self.lock:
		#
			if (self.watched_paths != None and _path in self.watched_paths):
			#
				if (callback == None): self.watched_callbacks[_path] = [ ]
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
:since:  v0.1.00
		"""

		with WatcherMtime.instance_lock:
		#
			if (WatcherMtime.instance == None): WatcherMtime.instance = WatcherMtime()
		#

		return WatcherMtime.instance
	#

	@staticmethod
	def stop():
	#
		"""
Stops all watchers.

:since: v0.1.01
		"""

		with WatcherMtime.instance_lock:
		#
			if (WatcherMtime.instance != None): WatcherMtime.instance = None
		#
	#
#

##j## EOF