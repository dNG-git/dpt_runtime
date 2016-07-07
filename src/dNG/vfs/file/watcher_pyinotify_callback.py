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

from pyinotify import ProcessEvent
from weakref import ref

try: from urllib.parse import quote
except ImportError: from urllib import quote

from dNG.runtime.exception_log_trap import ExceptionLogTrap
from dNG.vfs.abstract_watcher import AbstractWatcher

class WatcherPyinotifyCallback(ProcessEvent):
#
	"""
Processes pyinotify events and calls defined callbacks.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	# pylint: disable=invalid-name

	def __init__(self, manager):
	#
		"""
Constructor __init__(WatcherPyinotifyCallback)

:since: v0.2.00
		"""

		ProcessEvent.__init__(self)

		self.manager_weakref = ref(manager)
		"""
pyinotify manager instance
		"""
	#

	def _process_callbacks(self, event_type, _path, changed_value = None):
	#
		"""
Handles all inotify events.

:param event_type: Event type defined in AbstractWatcher
:param _path: Filesystem path
:param changed_value: Changed value (e.g. name of deleted or created file)

:since: v0.2.00
		"""

		manager = self.manager_weakref()

		if (manager and manager.is_watched(_path)):
		#
			callbacks = manager.get_callbacks(_path)
			url = "file:///{0}".format(quote(_path, "/"))

			for callback in callbacks:
			#
				with ExceptionLogTrap("pas_core"): callback(event_type, url, changed_value)
			#
		#
	#

	def process_IN_ATTRIB(self, event):
	#
		"""
Handles "IN_ATTRIB" inotify events.

:param event: pyinotify event

:since: v0.2.00
		"""

		self._process_callbacks(AbstractWatcher.EVENT_TYPE_MODIFIED, event.pathname)
	#

	def process_IN_CLOSE_WRITE(self, event):
	#
		"""
Handles "IN_CLOSE_WRITE" inotify events.

:param event: pyinotify event

:since: v0.2.00
		"""

		self._process_callbacks(AbstractWatcher.EVENT_TYPE_MODIFIED, event.pathname)
	#

	def process_IN_CREATE(self, event):
	#
		"""
Handles "IN_CREATE" inotify events.

:param event: pyinotify event

:since: v0.2.00
		"""

		self._process_callbacks(AbstractWatcher.EVENT_TYPE_CREATED, event.path, event.name)
	#

	def process_IN_DELETE(self, event):
	#
		"""
Handles "IN_DELETE" inotify events.

:param event: pyinotify event

:since: v0.2.00
		"""

		self._process_callbacks(AbstractWatcher.EVENT_TYPE_DELETED, event.path, event.name)
	#

	def process_IN_DELETE_SELF(self, event):
	#
		"""
Handles "IN_DELETE_SELF" inotify events.

:param event: pyinotify event

:since: v0.2.00
		"""

		manager = self.manager_weakref()
		if (manager): manager.unregister(event.pathname, None, True)

		self._process_callbacks(AbstractWatcher.EVENT_TYPE_DELETED, event.pathname)
	#

	def process_IN_MOVE_SELF(self, event):
	#
		"""
Handles "IN_MOVE_SELF" inotify events.

:param event: pyinotify event

:since: v0.2.00
		"""

		manager = self.manager_weakref()
		if (manager): manager.unregister(event.pathname, None, True)

		self._process_callbacks(AbstractWatcher.EVENT_TYPE_DELETED, event.pathname)
	#

	def process_IN_MOVED_FROM(self, event):
	#
		"""
Handles "IN_MOVED_TO" inotify events.

:param event: pyinotify event

:since: v0.2.00
		"""

		self._process_callbacks(AbstractWatcher.EVENT_TYPE_DELETED, event.path, event.name)
	#

	def process_IN_MOVED_TO(self, event):
	#
		"""
Handles "IN_MOVED_TO" inotify events.

:param event: pyinotify event

:since: v0.2.00
		"""

		self._process_callbacks(AbstractWatcher.EVENT_TYPE_CREATED, event.path, event.name)
	#
#

##j## EOF