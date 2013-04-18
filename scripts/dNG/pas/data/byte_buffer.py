# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.byte_buffer
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

from tempfile import TemporaryFile

try: from cStringIO import StringIO
except ImportError: from StringIO import StringIO

from dNG.pas.data.settings import direct_settings
from dNG.pas.pythonback import direct_bytes

class direct_byte_buffer(object):
#
	"""
"direct_byte_buffer" holds data in memory until a threshold is exhausted. You
can call "read()", "seek()" and "write()". Note that this class is not thread
safe.

:author:    direct Netware Group
:copyright: (C) direct Netware Group - All rights reserved
:package:   pas.core
:since:     v0.1.00
:license:   http://www.direct-netware.de/redirect?licenses;mpl2
            Mozilla Public License, v. 2.0
	"""

	def __init__(self):
	#
		"""
Constructor __init__(direct_byte_file_ptr)

:since: v0.1.00
		"""

		self.buffer = StringIO()
		"""
External file pointer.
		"""
		self.file_ptr = None
		"""
External file pointer.
		"""
		self.file_threshold = int(direct_settings.get("pas_core_byte_file_ptr_file_threshold", 5242880))
		"""
Threshold to write a given received request body element to an external file.
		"""
	#

	def read(self, n = -1):
	#
		"""
python.org: Read up to n bytes from the object and return them.

:param n: Size in bytes

:since: v0.1.00
		"""

		if (self.file_ptr == None): var_return = (self.buffer.read() if (n < 0) else self.buffer.read(n))
		else: var_return = (self.file_ptr.read() if (n < 0) else self.file_ptr.read(n))

		return var_return
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
			var_return = self.buffer.write(direct_bytes(b))

			if (self.buffer.tell() > self.file_threshold):
			#
				self.file_ptr = TemporaryFile()

				self.buffer.seek(0)
				self.file_ptr.write(self.buffer.read())

				self.buffer.close()
				self.buffer = None
			#
		#
		else: var_return = self.file_ptr.write(direct_bytes(b))

		return var_return
	#
#

##j## EOF