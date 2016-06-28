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

from dNG.pas.data.binary import Binary
from dNG.pas.module.named_loader import NamedLoader
from dNG.pas.runtime.io_exception import IOException
from dNG.pas.runtime.value_exception import ValueException
from .abstract_watcher import AbstractWatcher

class WatcherImplementation(object):
#
	"""
"WatcherImplementation" provides implementation independent methods to
access VFS watchers.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	EVENT_TYPE_CREATED = AbstractWatcher.EVENT_TYPE_CREATED
	"""
Created event
	"""
	EVENT_TYPE_DELETED = AbstractWatcher.EVENT_TYPE_DELETED
	"""
Deleted event
	"""
	EVENT_TYPE_MODIFIED = AbstractWatcher.EVENT_TYPE_MODIFIED
	"""
Created event
	"""

	@staticmethod
	def get_class(scheme):
	#
		"""
Returns an VFS watcher class for the given scheme.

:return: (object) VFS watcher class
:since:  v0.2.00
		"""

		_return = NamedLoader.get_class("dNG.pas.vfs.{0}.Watcher".format(scheme.replace("-", "_")))

		if (_return is None
		    or (not issubclass(_return, AbstractWatcher))
		   ): raise IOException("VFS watcher not defined for URL scheme '{0}'".format(scheme))

		return _return
	#

	@staticmethod
	def get_instance(scheme):
	#
		"""
Returns an VFS watcher instance for the given scheme.

:return: (object) VFS watcher instance
:since:  v0.2.00
		"""

		vfs_watcher_class = WatcherImplementation.get_class(scheme)
		return vfs_watcher_class()
	#

	@staticmethod
	def get_scheme_from_vfs_url(vfs_url):
	#
		"""
Returns the scheme of the VFS URL given.

:param vfs_url: VFS URL to extract the scheme from.

:return: (str) VFS URL scheme
:since:  v0.2.00
		"""

		vfs_url = Binary.str(vfs_url)
		if (type(vfs_url) is not str): raise ValueException("VFS URL given is invalid")

		vfs_url_data = vfs_url.split("://", 1)
		if (len(vfs_url_data) == 1): raise ValueException("VFS URL '{0}' is invalid".format(vfs_url))

		return vfs_url_data[0]
	#

	@staticmethod
	def get_scheme_from_vfs_url_if_supported(vfs_url):
	#
		"""
Returns the scheme of the VFS URL given if it is supported.

:param vfs_url: VFS URL to extract the scheme from.

:return: (str) VFS URL scheme if supported; None otherwise
:since:  v0.2.00
		"""

		_return = None

		try:
		#
			scheme = WatcherImplementation.get_scheme_from_vfs_url(vfs_url)

			if (NamedLoader.is_defined("dNG.pas.vfs.{0}.Watcher".format(scheme.replace("-", "_")))):
			#
				_return = scheme
			#
		#
		except ValueException: pass

		return _return
	#
#

##j## EOF