# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.vfs.file.watcher
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

try: from urllib.parse import urlsplit
except ImportError: from urlparse import urlsplit

from dNG.pas.data.logging.log_line import LogLine
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
except ImportError: _mode = _IMPLEMENTATION_MTIME

if (_mode == _IMPLEMENTATION_MTIME): from .watcher_mtime import WatcherMtime

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

	synchronized = RLock()
	"""
Lock used in multi thread environments.
	"""

	def __init__(self):
	#
		"""
Constructor __init__(Watcher)

:since: v0.1.01
		"""

		self.implementation = False
		"""
Watcher implementation to use
		"""

		self.set_implementation()

		LogLine.debug("pas.vfs.file.Watcher mode is {0}".format("synchronous" if (self.is_synchronous()) else "asynchronous"))
	#

	def check(self, url):
	#
		"""
Get the content from cache for the given file path and name.

TODO: Check if this works for directories with mtime

:param _path: Filesystem path

:return: (mixed) Cached entry; None if no hit or changed
:since:  v0.1.01
		"""

		_path = self._get_path(url)

		if (_path == None or _path.strip() == ""): return False
		else: return self.implementation.get_instance().check(_path)
	#

	def free(self):
	#
		"""
Frees all watcher callbacks for garbage collection.

:since: v0.1.01
		"""

		self.implementation.get_instance().free()
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
		return (url_elements.path[1:] if (url_elements.scheme == "file") else None)
	#

	def is_synchronous(self):
	#
		"""
Returns true if changes are only detected after "check()" has been
called.

:return: (bool) True if changes are detected automatically
:since:  v0.1.01
		"""

		return self.implementation.is_synchronous()
	#

	def is_watched(self, url, callback = None):
	#
		"""
Returns true if the filesystem path is already watched. It will return false
if a callback is given but not defined for the watched path.

:param url: Filesystem URL
:param callback: Callback to be checked for the watched filesystem path

:return: (bool) True if watched with the defined callback if applicable
:since:  v0.1.01
		"""

		_path = self._get_path(url)

		if (_path == None or _path.strip() == ""): return False
		else: return self.implementation.get_instance().is_watched(_path, callback)
	#

	def register(self, url, callback):
	#
		"""
Handles registration of filesystem watches and its callbacks.

:param url: Filesystem URL to be watched

:return: (bool) True on success
:since:  v0.1.01
		"""

		_path = self._get_path(url)

		if (_path == None or _path.strip() == ""): return False
		else: return self.implementation.get_instance().register(_path, callback)
	#

	def set_implementation(self, implementation = None):
	#
		"""
Set the filesystem watcher implementation to use.

:param implementation: Implementation identifier

:since: v0.1.01
		"""

		global _IMPLEMENTATION_INOTIFY, _IMPLEMENTATION_INOTIFY_SYNC, _IMPLEMENTATION_MTIME, _mode

		with Watcher.synchronized:
		#
			if (_mode == _IMPLEMENTATION_INOTIFY and (implementation == None or implementation == _IMPLEMENTATION_INOTIFY)): self.implementation = WatcherPyinotify
			elif (_mode == _IMPLEMENTATION_INOTIFY and implementation == _IMPLEMENTATION_INOTIFY_SYNC): self.implementation = WatcherPyinotifySync
			else: self.implementation = WatcherMtime
		#
	#

	def unregister(self, url, callback):
	#
		"""
Handles unregistration of filesystem watches.

:param url: Filesystem URL watched

:return: (bool) True on success
:since:  v0.1.01
		"""

		_path = self._get_path(url)

		if (_path == None or _path.strip() == ""): return False
		else: return self.implementation.get_instance().unregister(_path, callback)
	#
#

##j## EOF