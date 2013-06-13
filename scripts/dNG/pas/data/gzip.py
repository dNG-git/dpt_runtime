# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.Gzip
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

from struct import pack
from zlib import compressobj, crc32, Z_FINISH

from .binary import Binary

class Gzip(object):
#
	"""
"Gzip" creates a Gzip compressed stream similar to the
"zlib.compressobj" object.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v0.1.01
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self, level = 6):
	#
		"""
Constructor __init__(Gzip)

:since: v0.1.01
		"""

		self.compressor = compressobj(level)
		"""
Deflate compressor instance
		"""
		self.crc32 = None
		"""
CRC32 from previous run
		"""
		self.header = None
		"""
Gzip header
		"""
		self.size = 0
		"""
Total size of compressed data
		"""

		if (level == 9): deflate_flag = 2
		elif (level == 1): deflate_flag = 4
		else: deflate_flag = 0

		self.header = pack("<8s2B", Binary.bytes("\x1f\x8b" + ("\x00" if (level == 0) else "\x08") + "\x00\x00\x00\x00\x00"), deflate_flag, 255)

	#

	def compress(self, string):
	#
		"""
python.org: Compress string, returning a string containing compressed data
for at least part of the data in string.

:param string: Original string

:return: (bytes) Compressed string
:since:  v0.1.01
		"""

		data = Binary.bytes(string)

		self.crc32 = (crc32(data) if (self.crc32 == None) else crc32(data, self.crc32))
		self.size += len(data)

		if (self.header != None):
		#
			var_return = self.header + self.compressor.compress(data)[2:]
			self.header = None
		#
		else: var_return = self.compressor.compress(data)

		return var_return
	#

	def flush(self, mode = Z_FINISH):
	#
		"""
python.org: All pending input is processed, and a string containing the
remaining compressed output is returned.

:param mode: Flush mode

:since: v0.1.01
		"""

		if (mode != Z_FINISH): raise RuntimeError("Gzip flush only supports Z_FINISH", 1)
		return self.compressor.flush(Z_FINISH) + pack("<2I", self.crc32 & 0xffffffff, int(self.size % 4294967296))
	#
#

##j## EOF