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

# pylint: disable=unused-argument

from dNG.pas.runtime.not_implemented_exception import NotImplementedException
from dNG.pas.runtime.value_exception import ValueException
from dNG.pas.data.binary import Binary

class Abstract(object):
#
	"""
Provides the abstract VFS implementation for an object.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v0.1.03
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	TYPE_DIRECTORY = 2
	"""
Directory (or collection like) type
	"""
	TYPE_FILE = 1
	"""
File type
	"""
	TYPE_LINK = 4
	"""
Link type
	"""

	def __del__(self):
	#
		"""
Destructor __del__(Abstract)

:since: v0.1.03
		"""

		self.close()
	#

	def close(self):
	#
		"""
python.org: Flush and close this stream.

:since: v0.1.03
		"""

		raise NotImplementedException()
	#

	def flush(self):
	#
		"""
python.org: Flush the write buffers of the stream if applicable.

:since: v0.1.03
		"""

		raise NotImplementedException()
	#

	def get_implementing_instance(self):
	#
		"""
Returns the implementing instance.

:return: (mixed) Implementing instance
:since:  v0.1.03
		"""

		raise NotImplementedException()
	#

	def get_name(self):
	#
		"""
Returns the name of this VFS object.

:return: (str) VFS object name
:since:  v0.1.03
		"""

		raise NotImplementedException()
	#

	def get_size(self):
	#
		"""
Returns the size in bytes.

:return: (int) Size in bytes
:since:  v0.1.03
		"""

		raise NotImplementedException()
	#

	def get_type(self):
	#
		"""
Returns the type of this object.

:return: (int) Object type
:since:  v0.1.03
		"""

		raise NotImplementedException()
	#

	def get_uri(self):
	#
		"""
Returns the URI of this VFS object.

:return: (str) VFS URI
:since:  v0.1.03
		"""

		raise NotImplementedException()
	#

	def is_directory(self):
	#
		"""
Returns true if the object is representing a directory (or collection).

:return: (bool) True if directory
:since:  v0.1.03
		"""

		return (self.get_type() & Abstract.TYPE_DIRECTORY == Abstract.TYPE_DIRECTORY)
	#

	def is_eof(self):
	#
		"""
Checks if the pointer is at EOF.

:return: (bool) True on success
:since:  v0.1.03
		"""

		raise NotImplementedException()
	#

	def is_file(self):
	#
		"""
Returns true if the object is representing a file.

:return: (bool) True if file
:since:  v0.1.03
		"""

		return (self.get_type() & Abstract.TYPE_FILE == Abstract.TYPE_FILE)
	#

	def is_link(self):
	#
		"""
Returns true if the object is representing a link to another object.

:return: (bool) True if link
:since:  v0.1.03
		"""

		return (self.get_type() & Abstract.TYPE_LINK == Abstract.TYPE_LINK)
	#

	def is_valid(self):
	#
		"""
Returns true if the object is available.

:return: (bool) True on success
:since:  v0.1.03
		"""

		raise NotImplementedException()
	#

	def new(self, _type, vfs_uri):
	#
		"""
Creates a new VFS object.

:param _type: VFS object type
:param vfs_uri: VFS URI

:since: v0.1.03
		"""

		raise NotImplementedException()
	#

	def open(self, vfs_uri, readonly = False):
	#
		"""
Opens a VFS object.

:param vfs_uri: VFS URI
:param readonly: Open object in readonly mode

:since: v0.1.03
		"""

		raise NotImplementedException()
	#

	def read(self, n = 0, timeout = -1):
	#
		"""
python.org: Read up to n bytes from the object and return them.

:param n: How many bytes to read from the current position (0 means until
          EOF)
:param timeout: Timeout to use (defaults to construction time value)

:return: (bytes) Data; None if EOF
:since:  v0.1.03
		"""

		raise NotImplementedException()
	#

	def scan(self):
	#
		"""
Scan over objects of a collection like a directory.

:return: (object) Child VFS object
:since:  v0.1.03
		"""

		raise NotImplementedException()
	#

	def seek(self, offset):
	#
		"""
python.org: Change the stream position to the given byte offset.

:param offset: Seek to the given offset

:return: (int) Return the new absolute position.
:since:  v0.1.03
		"""

		raise NotImplementedException()
	#

	def tell(self):
	#
		"""
python.org: Return the current stream position as an opaque number.

:return: (int) Stream position
:since:  v0.1.03
		"""

		raise NotImplementedException()
	#

	def truncate(self, new_size):
	#
		"""
python.org: Resize the stream to the given size in bytes.

:param new_size: Cut file at the given byte position

:return: (int) New file size
:since:  v0.1.03
		"""

		raise NotImplementedException()
	#

	def write(self, b, timeout = -1):
	#
		"""
python.org: Write the given bytes or bytearray object, b, to the underlying
raw stream and return the number of bytes written.

:param b: (Over)write file with the given data at the current position
:param timeout: Timeout to use (defaults to construction time value)

:return: (int) Number of bytes written
:since:  v0.1.03
		"""

		raise NotImplementedException()
	#

	@staticmethod
	def _get_id_from_vfs_uri(vfs_uri):
	#
		"""
Returns the ID part of the VFS URI given.

:return: (str) VFS URI ID
:since:  v0.1.03
		"""

		vfs_uri = Binary.str(vfs_uri)
		if (type(vfs_uri) is not str): raise ValueException("VFS URI given is invalid")

		vfs_uri_data = vfs_uri.split("://", 1)
		if (len(vfs_uri_data) == 1): raise ValueException("VFS URI '{0}' is invalid".format(vfs_uri))

		_return = vfs_uri_data[1]

		if (_return in ( "", "/" )): _return = ""
		else: _return = (_return[1:] if (_return[:1] == "/") else _return).strip()

		return _return
	#

	@staticmethod
	def _get_scheme_from_vfs_uri(vfs_uri):
	#
		"""
Returns the scheme of the VFS URI given.

:return: (str) VFS URI scheme
:since:  v0.1.03
		"""

		if (type(vfs_uri) is not str): raise ValueException("VFS URI given is invalid")

		vfs_uri_data = vfs_uri.split("://", 1)
		if (len(vfs_uri_data) == 1): raise ValueException("VFS URI '{0}' is invalid".format(vfs_uri))

		return vfs_uri_data[0]
	#
#

##j## EOF