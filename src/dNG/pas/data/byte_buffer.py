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

from io import BytesIO
from tempfile import TemporaryFile

from .binary import Binary
from .settings import Settings

class ByteBuffer(object):
#
	"""
"ByteBuffer" holds data in memory until a threshold is exhausted. You can
call "read()", "seek()" and "write()". Note that this class is not thread
safe.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	# pylint: disable=invalid-name

	def __init__(self):
	#
		"""
Constructor __init__(ByteBuffer)

:since: v0.1.00
		"""

		self.buffer = BytesIO()
		"""
Internal byte buffer.
		"""
		self.file_ptr = None
		"""
External file pointer.
		"""
		self.file_threshold = int(Settings.get("pas_core_byte_file_ptr_file_threshold", 5242880))
		"""
Threshold to write the internal buffer to an external file.
		"""
	#

	def read(self, n = -1):
	#
		"""
python.org: Read up to n bytes from the object and return them.

:param n: Size in bytes

:since: v0.1.00
		"""

		if (self.file_ptr == None): _return = (self.buffer.read() if (n < 0) else self.buffer.read(n))
		else: _return = (self.file_ptr.read() if (n < 0) else self.file_ptr.read(n))

		return _return
	#

	def seek(self, offset):
	#
		"""
python.org: Change the stream position to the given byte offset.

:param offset: Absolute offset in bytes

:since: v0.1.00
		"""

		return (self.buffer.seek(offset) if (self.file_ptr == None) else self.file_ptr.seek(offset))
	#

	def write(self, b):
	#
		"""
Write the given bytes or bytearray object, b, to the underlying raw stream
and return the number of bytes written.

:param b: Bytes data

:since: v0.1.00
		"""

		if (self.file_ptr == None):
		#
			_return = self.buffer.write(Binary.bytes(b))

			if (self.buffer.tell() > self.file_threshold):
			#
				self.file_ptr = TemporaryFile()

				self.buffer.seek(0)
				self.file_ptr.write(self.buffer.read())

				self.buffer.close()
				self.buffer = None
			#
		#
		else: _return = self.file_ptr.write(Binary.bytes(b))

		return _return
	#
#

##j## EOF