# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.text.l10n
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

from math import floor

try: import hashlib
except ImportError: import md5 as hashlib

from dNG.pas.pythonback import direct_bytes, direct_str

class direct_tmd5(object):
#
	"""
To increase security we are using two additional steps for MD5. All strings
will be divided into three parts and reverted to make attacks based on
pre-encoded dictionary words against our triple MD5 strings harder.

Furthermore "bytemix" data can be applied to each part as a hash.

:author:    direct Netware Group
:copyright: direct Netware Group - All rights reserved
:package:   pas.core
:since:     v0.1.00
:license:   http://www.direct-netware.de/redirect.py?licenses;mpl2
            Mozilla Public License, v. 2.0
	"""

	@staticmethod
	def encode(data, bytemix = ""):
	#
		"""
Generate the triple MD5 hash for the data given.

:param data: Input string
:param bytemix: Bytemix to use for TMD5 (None for none)

:return: (str) Triple MD5 string
:since:  v0.1.00
		"""

		var_return = ""

		bytemix = direct_str(bytemix)
		data = direct_str(data)
		data_length = (len(data) if (type(data) == str) else 0)

		if (type(bytemix) == str and data_length > 0):
		#
			bytemix_length = len(bytemix)
			bytemixing = False
			data_remaining = data_length
			part_length = int(floor(data_length / 3))
			return_length = 0

			if (bytemix_length > 0):
			#
				bytemixing = True

				if (bytemix_length > data_length): bytemix_expanded = bytemix[bytemix_length - data_length:]
				else:
				#
					bytemix_expanded = ""
					while (len(bytemix_expanded) < data_length): bytemix_expanded += (bytemix if (len(bytemix_expanded) + bytemix_length <= data_length) else bytemix[:data_length - len(bytemix_expanded)])
				#
			#
			else: bytemix_expanded = ""

			"""
We will now divide the string into three parts, revert each of them and put
it together to our result.
			"""

			part = ("".join(chr(ord(char) | ord(bytechar)) for char, bytechar in zip(data[:part_length][::-1], bytemix_expanded[:part_length])) if (bytemixing) else data[:part_length][::-1])
			var_return = hashlib.md5(direct_bytes(part)).hexdigest()

			data_remaining -= part_length
			return_length += part_length

			part = ("".join(chr(ord(char) | ord(bytechar)) for char, bytechar in zip(data[return_length:part_length + return_length][::-1], bytemix_expanded[return_length:part_length + return_length])) if (bytemixing) else data[return_length:part_length + return_length][::-1])
			var_return += hashlib.md5(direct_bytes(part)).hexdigest()

			data_remaining -= part_length
			return_length += part_length

			part = ("".join(chr(ord(char) | ord(bytechar)) for char, bytechar in zip(data[return_length:data_remaining + return_length][::-1], bytemix_expanded[return_length:data_remaining + return_length])) if (bytemixing) else data[return_length:data_remaining + return_length][::-1])
			var_return += hashlib.md5(direct_bytes(part)).hexdigest()
		#

		return var_return
	#
#

##j## EOF