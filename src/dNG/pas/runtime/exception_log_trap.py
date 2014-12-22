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
#echo(pasDatabaseVersion)#
#echo(__FILEPATH__)#
"""

import traceback

from dNG.pas.data.logging.log_line import LogLine

class ExceptionLogTrap(object):
#
	"""
"ExceptionLogTrap" provides a context where exceptions are catched, logged
and suppressed.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self, context = None):
	#
		"""
Constructor __init__(ExceptionLogTrap)

:param context: Logging context

:since: v0.1.00
		"""

		self.context = context
		"""
Logging context
		"""
	#

	def __enter__(self):
	#
		"""
python.org: Enter the runtime context related to this object.

:since: v0.1.00
		"""

		pass
	#

	def __exit__(self, exc_type, exc_value, _traceback):
	#
		"""
python.org: Exit the runtime context related to this object.

:return: (bool) True to suppress exceptions
:since:  v0.1.00
		"""

		if (exc_type is not None
		    or exc_value is not None
		   ):
		#
			traceback_string = "".join(traceback.format_exception(exc_type, exc_value, _traceback))
			LogLine.error("Exception: {0}\n{1}".format(exc_value, traceback_string), context = self.context)
		#

		return True
	#
#

##j## EOF