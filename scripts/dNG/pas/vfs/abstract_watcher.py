# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.vfs.AbstractWatcher
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

class AbstractWatcher(object):
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

	EVENT_TYPE_CREATED = 1
	"""
Filesystem created event
	"""
	EVENT_TYPE_DELETED = 2
	"""
Filesystem deleted event
	"""
	EVENT_TYPE_MODIFIED = 3
	"""
Filesystem created event
	"""

	def check(self, url):
	#
		"""
Get the content from cache for the given file path and name.

TODO: Check if this works for directories with mtime

:param _path: Filesystem path

:return: (mixed) Cached entry; None if no hit or changed
:since:  v0.1.01
		"""

		raise RuntimeError("Not implemented", 38)
	#

	def free(self):
	#
		"""
Frees all watcher callbacks for garbage collection.

:since: v0.1.01
		"""

		raise RuntimeError("Not implemented", 38)
	#

	def is_synchronous(self):
	#
		"""
Returns true if changes are only detected after "check()" has been
called.

:return: (bool) True if changes are detected automatically
:since:  v0.1.01
		"""

		return True
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

		raise RuntimeError("Not implemented", 38)
	#

	def register(self, url, callback):
	#
		"""
Handles registration of filesystem watches and its callbacks.

:param url: Filesystem URL to be watched

:return: (bool) True on success
:since:  v0.1.01
		"""

		raise RuntimeError("Not implemented", 38)
	#

	def unregister(self, url, callback):
	#
		"""
Handles unregistration of filesystem watches.

:param url: Filesystem URL watched

:return: (bool) True on success
:since:  v0.1.01
		"""

		raise RuntimeError("Not implemented", 38)
	#

	@staticmethod
	def stop():
	#
		"""
Stops all watchers.

:since: v0.1.01
		"""

		pass
	#
#

##j## EOF