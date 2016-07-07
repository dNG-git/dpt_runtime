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

from dNG.data.traced_exception import TracedException

class OperationNotSupportedException(TracedException):
#
	"""
This exception should be used if specific API calls or parameter values are
not supported in a given implementation.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self, value = "Operation not supported", _exception = None):
	#
		"""
Constructor __init__(OperationNotSupportedException)

:param value: Exception message value
:param _exception: Inner exception

:since: v0.2.00
		"""

		TracedException.__init__(self, value, _exception)
	#
#

##j## EOF