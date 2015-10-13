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

import sys
import traceback

class TracedException(RuntimeError):
#
	"""
The extended "RuntimeError" is used to redirect exceptions to output
streams.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self, value, _exception = None):
	#
		"""
Constructor __init__(TracedException)

:param value: Exception message value
:param _exception: Inner exception

:since: v0.1.00
		"""

		RuntimeError.__init__(self, value)

		self.exc_cause = _exception
		"""
Inner exception if given
		"""
		self.exc_type = self.__class__
		"""
Exception type
		"""
		self.exc_value = self
		"""
Exception value
		"""
		self.exc_traceback = None
		"""
Exception traceback
		"""

		exc_type = None
		exc_value = None

		if (hasattr(self, "__traceback__")): exc_traceback = self.__traceback__
		else: ( exc_type, exc_value, exc_traceback ) = sys.exc_info()

		if (exc_value is not None):
		#
			self.exc_type = exc_type
			self.exc_value = exc_value
		#

		if (exc_traceback is not None): self.exc_traceback = exc_traceback
	#

	def __str__(self):
	#
		"""
python.org: Called by the str(object) and the built-in functions format()
and print() to compute the "informal" or nicely printable string
representation of an object.
		"""

		_return = RuntimeError.__str__(self)
		return (_return if (self.exc_cause is None) else "{0}\n{1}".format(_return, repr(self.exc_cause)))
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

		return "".join(traceback.format_exception(self.exc_type, self.exc_value, self.exc_traceback))
	#

	def print_stack_trace(self, out_stream = None):
	#
		"""
Prints the stack trace to the given output stream or stderr.

:param out_stream: Output stream

:since: v0.1.00
		"""

		if (out_stream is None): out_stream = sys.stderr
		out_stream.write(self.get_printable_trace())
	#

	@staticmethod
	def print_current_stack_trace(out_stream = None):
	#
		"""
Prints the stack trace to the given output stream or stderr.

:param out_stream: Output stream

:since: v0.1.00
		"""

		printable_trace = traceback.format_exc()

		if (out_stream is None): out_stream = sys.stderr
		out_stream.write(printable_trace)
	#
#

##j## EOF