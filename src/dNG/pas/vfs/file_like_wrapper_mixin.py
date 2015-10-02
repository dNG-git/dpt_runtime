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

from dNG.pas.runtime.io_exception import IOException

class FileLikeWrapperMixin(object):
#
	"""
The "FileLikeWrapper" instance redirects FileIO to the registered wrapped
instance.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v0.1.03
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	_FILE_WRAPPED_METHODS = ( "flush",
	                          "read",
	                          "seek",
	                          "tell",
	                          "truncate",
	                          "write"
	                        )
	"""
File IO methods implemented by an wrapped resource.
	"""

	def __init__(self):
	#
		"""
Constructor __init__(FileLikeWrapperMixin)

:since: v0.1.03
		"""

		self._wrapped_resource = None
		"""
Wrapped file-like resource
		"""
	#

	def __getattribute__(self, name):
	#
		"""
python.org: Called unconditionally to implement attribute accesses for
instances of the class.

:param name: Attribute name

:return: (mixed) Instance attribute
:since:  v0.1.03
		"""

		if (name in ( "__class__", "_wrapped_resource" )
		    or name not in self.__class__._FILE_WRAPPED_METHODS
		   ): _return = object.__getattribute__(self, name)
		else:
		#
			wrapped_resource = self._wrapped_resource
			if (wrapped_resource is None): raise IOException("'{0}' not available".format(name))
			_return = getattr(wrapped_resource, name)
		#

		return _return
	#

	def close(self):
	#
		"""
python.org: Flush and close this stream.

:since: v0.1.03
		"""

		if (self._wrapped_resource is not None):
		#
			try: self._wrapped_resource.close()
			finally: self._wrapped_resource = None
		#
	#

	def _set_wrapped_resource(self, resource):
	#
		"""
Sets the wrapped resource for this object.

:param resource: Resource providing the file-like API

:since: v0.1.03
		"""

		self._wrapped_resource = resource
	#
#

##j## EOF