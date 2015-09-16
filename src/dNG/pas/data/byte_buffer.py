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

from io import BytesIO
from tempfile import TemporaryFile

from dNG.pas.runtime.io_exception import IOException
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
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
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
		self.buffer_reset = False
		"""
True if the buffer has been reset.
		"""
		self.buffer_size = 0
		"""
Buffer size in bytes written.
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

	def _ensure_buffer_reset(self):
	#
		"""
Resets the buffer ones before first read.

:since: v0.1.03
		"""

		self.seek(0)
	#

	def _get_ptr(self):
	#
		"""
Returns the buffer object to use.

:return: (object) Buffer instance in use
:since:  v0.1.03
		"""

		return (self.buffer if (self.file_ptr is None) else self.file_ptr)
	#

	def get_size(self):
	#
		"""
Returns the current size of the buffer.

:return: (int) Size written in bytes
:since:  v0.1.03
		"""

		return self.buffer_size
	#

	def read(self, n = 0):
	#
		"""
python.org: Read up to n bytes from the object and return them.

:param n: How many bytes to read from the current position (0 means until
          EOF)

:return: (bytes) Data; None if EOF
:since:  v0.1.00
		"""

		self._ensure_buffer_reset()

		_ptr = self._get_ptr()
		return (_ptr.read() if (n < 1) else _ptr.read(n))
	#

	def readline(self, limit = -1):
	#
		"""
python.org: Read and return one line from the stream.

:param n: If limit is specified, at most limit bytes will be read.

:since: v0.1.00
		"""

		self._ensure_buffer_reset()

		_ptr = self._get_ptr()
		return (_ptr.readline() if (limit < 0) else _ptr.readline(limit))
	#

	def seek(self, offset):
	#
		"""
python.org: Change the stream position to the given byte offset.

:param offset: Seek to the given offset

:return: (int) Return the new absolute position.
:since: v0.1.00
		"""

		if (not self.buffer_reset): self.buffer_reset = True

		_ptr = self._get_ptr()
		return _ptr.seek(offset)
	#

	def tell(self):
	#
		"""
python.org: Return the current stream position as an opaque number.

:return: (int) Stream position
:since:  v0.1.00
		"""

		_ptr = self._get_ptr()
		return _ptr.tell()
	#

	def write(self, b):
	#
		"""
python.org: Write the given bytes or bytearray object, b, to the underlying
raw stream and return the number of bytes written.

:param b: Bytes data

:return: (int) Number of bytes written
:since:  v0.1.00
		"""

		if (self.buffer_reset): raise IOException("Can't write to a buffer that has been already read from")

		b = Binary.bytes(b)

		if (self.file_ptr is None):
		#
			_return = self.buffer.write(b)

			if (self.buffer.tell() > self.file_threshold):
			#
				self.file_ptr = TemporaryFile()

				self.buffer.seek(0)
				self.file_ptr.write(self.buffer.read())

				self.buffer.close()
				self.buffer = None
			#
		#
		else: _return = self.file_ptr.write(b)

		self.buffer_size += _return

		return _return
	#
#

##j## EOF