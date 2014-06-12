# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.runtime.Iterator
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

from collections import Iterator as _Iterator

class Iterator(_Iterator):
#
	"""
"Iterator" provides an iterator class that is compatible with Python 2.x and
newer.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v0.1.01
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def next(self):
	#
		"""
python.org: Return the next item from the container. (Python 2.x)

:return: (object) Result object
:since:  v0.1.00
		"""

		return self.__next__()
	#
#

##j## EOF