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

from .event import Event
from .io_exception import IOException

class ResultEvent(Event):
#
	"""
"ResultEvent" implements a result delivering event.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self, timeout = None):
	#
		"""
Constructor __init__(ResultEvent)

:since: v0.2.00
		"""

		Event.__init__(self)

		self.result = None
		"""
Result set
		"""
		self.result_set = False
		"""
Flag indicating that a result was set.
		"""
	#

	def clear(self):
	#
		"""
python.org: Reset the internal flag to false. 

:since: v0.2.00
		"""

		if (self.result_set): raise IOException("A ResultEvent can not be cleared after a result was set.")
		Event.clear(self)
	#

	def get_result(self):
	#
		"""
Returns the result being set previously.

:return: (mixed) Result set
:since:  v0.2.00
		"""

		if (not self.result_set): raise IOException("No result has been set for this ResultEvent.")
		return self.result
	#

	def is_result_set(self):
	#
		"""
Returns true after a result has been set.

:return: (bool) True if a result is set
:since:  v0.2.00
		"""

		return self.result_set
	#

	def set(self):
	#
		"""
python.org: Set the internal flag to true.

:since: v0.2.00
		"""

		self.set_result(None)
	#

	def set_result(self, result):
	#
		"""
Sets a result for this event and notifies all waiting threads afterwards.

:param result: Result

:since: v0.2.00
		"""

		self.result = result
		self.result_set = True

		Event.set(self)
	#
#

##j## EOF