# -*- coding: utf-8 -*-
##j## BOF

"""
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
"""

# pylint: disable=unused-argument

from dNG.pas.runtime.not_implemented_exception import NotImplementedException

class AbstractWatcher(object):
#
	"""
Abstract watcher for change events.

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
Created event
	"""
	EVENT_TYPE_DELETED = 2
	"""
Deleted event
	"""
	EVENT_TYPE_MODIFIED = 3
	"""
Created event
	"""

	def check(self, url):
	#
		"""
Checks a given URL for changes if "is_synchronous()" is true.

:param url: Resource URL

:since: v0.1.01
		"""

		raise NotImplementedException()
	#

	def disable(self):
	#
		"""
Disables this watcher and frees all callbacks for garbage collection.

:since: v0.1.01
		"""

		raise NotImplementedException()
	#

	def free(self):
	#
		"""
Frees all watcher callbacks for garbage collection.

:since: v0.1.01
		"""

		raise NotImplementedException()
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

		raise NotImplementedException()
	#

	def register(self, url, callback):
	#
		"""
Handles registration of resource URL watches and its callbacks.

:param url: Resource URL to be watched
:param callback: Callback for the path

:return: (bool) True on success
:since:  v0.1.01
		"""

		raise NotImplementedException()
	#

	def stop(self):
	#
		"""
Stops all watchers.

:since: v0.1.01
		"""

		pass
	#

	def unregister(self, url, callback):
	#
		"""
Handles deregistration of resource URL watches.

:param url: Resource URL watched
:param callback: Callback for the path

:return: (bool) True on success
:since:  v0.1.01
		"""

		raise NotImplementedException()
	#
#

##j## EOF