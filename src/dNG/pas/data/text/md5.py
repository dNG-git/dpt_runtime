# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.text.Md5
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

try: import hashlib
except ImportError: import md5 as hashlib

from dNG.pas.data.binary import Binary

class Md5(object):
#
	"""
Abstraction layer for the one-line MD5 hasing method.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v0.1.01
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	@staticmethod
	def hash(data):
	#
		"""
Generate the MD5 hash for the data given.

:param data: Input string

:return: (str) Triple MD5 string
:since:  v0.1.01
		"""

		return hashlib.md5(Binary.bytes(data)).hexdigest()
	#
#

##j## EOF