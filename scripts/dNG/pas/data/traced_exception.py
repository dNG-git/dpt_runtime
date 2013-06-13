# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.TracedException
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

import sys
import traceback

class TracedException(Exception):
#
	"""
The extended "Exception" is used to redirect exceptions to output
streams.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self, value, py_exception = None):
	#
		"""
Constructor __init__(Exception)

:param value: Exception message value
:param py_exception: Inner exception

:since: v0.1.00
		"""

		Exception.__init__(self, value)

		self.exc_cause = py_exception
		"""
Inner exception if given
		"""
		self.exc_type = None
		"""
Exception type
		"""
		self.exc_value = None
		"""
Exception value
		"""
		self.exc_traceback = None
		"""
Exception traceback
		"""

		( self.exc_type, self.exc_value, self.exc_traceback ) = sys.exc_info()
	#

	def __str__(self):
	#
		"""
python.org: Called by the str(object) and the built-in functions format()
and print() to compute the "informal" or nicely printable string
representation of an object.
		"""

		var_return = (repr(self) if (self.exc_traceback == None) else "{0} {1}: {2}".format(self.exc_type, self.exc_value, self.get_printable_trace()))
		return (var_return if (self.exc_cause == None) else "{0} {1}".format(var_return, repr(self.exc_cause)))
	#

	def get_cause(self):
	#
		"""
Return the cause.

:return: (mixed) Inner exception
:since:  v0.1.00
		"""

		return self.exc_cause
	#

	def get_printable_trace(self):
	#
		"""
Returns the stack trace.

:return: (str) Exception stack trace
:since:  v0.1.00
		"""

		try: return "".join(traceback.format_exception(self.exc_type, self.exc_value, self.exc_traceback))
		except: return "Traceback failed"
	#

	def print_stack_trace(self, out_stream = None):
	#
		"""
Prints the stack trace to the given output stream or stderr.

:param out_stream: Output stream

:since: v0.1.00
		"""

		traceback.print_exception(self.exc_type, self.exc_value, self.exc_traceback, file = (out_stream if (out_stream != None) else sys.stderr))
	#

	@staticmethod
	def print_current_stack_trace (out_stream = None):
	#
		"""
Prints the stack trace to the given output stream or stderr.

:param out_stream: Output stream

:since: v0.1.00
		"""

		( exc_type, exc_value, exc_traceback ) = sys.exc_info()
		traceback.print_exception(exc_type, exc_value, exc_traceback, file = (out_stream if (out_stream != None) else sys.stderr))
	#
#

##j## EOF