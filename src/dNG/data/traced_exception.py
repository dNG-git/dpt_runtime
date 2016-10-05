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

try: import traceback
except ImportError: traceback = None

class TracedException(RuntimeError):
#
	"""
The extended "RuntimeError" is used to redirect exceptions to output
streams.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self, value, _exception = None):
	#
		"""
Constructor __init__(TracedException)

:param value: Exception message value
:param _exception: Inner exception

:since: v0.2.00
		"""

		super(TracedException, self).__init__(value)

		self.exc_cause = _exception
		"""
Inner exception if given
		"""
		self.exc_trace_list = None
		"""
Exception traceback list
		"""

		exc_traceback = getattr(self, "__traceback__", None)

		if (traceback is not None):
		#
			self.exc_trace_list = (traceback.format_stack()[:-1]
			                       if (exc_traceback is None) else
			                       traceback.format_tb(exc_traceback)
			                      )
		#
		elif (exc_traceback is not None): self.exc_trace_list = [ repr(exc_traceback) ]
	#

	def __str__(self):
	#
		"""
python.org: Called by the str(object) and the built-in functions format()
and print() to compute the "informal" or nicely printable string
representation of an object.

:return: (str) The "informal" or nicely printable string representation
:since:  v0.2.00
		"""

		_return = RuntimeError.__str__(self)
		return (_return if (self.exc_cause is None) else "{0} ({1!r})".format(_return, self.exc_cause))
	#

	def get_cause(self):
	#
		"""
Return the cause.

:return: (mixed) Inner exception
:since:  v0.2.00
		"""

		return self.exc_cause
	#

	def get_printable_trace(self):
	#
		"""
Returns the stack trace.

:return: (str) Exception stack trace
:since:  v0.2.00
		"""

		_return = "{0!r}: {1!s}\n".format(self.__class__, self)

		if (self.exc_trace_list is not None): _return = "{0}{1}".format(_return, "".join(self.exc_trace_list))
		if (self.exc_cause is not None): _return = "{0}{1}".format(_return, repr(self.exc_cause))

		return _return
	#

	def print_stack_trace(self, out_stream = None):
	#
		"""
Prints the stack trace to the given output stream or stderr.

:param out_stream: Output stream

:since: v0.2.00
		"""

		if (out_stream is None): out_stream = sys.stderr
		out_stream.write(self.get_printable_trace())
	#

	def with_traceback(self, tb):
	#
		"""
python.org: This method sets tb as the new traceback for the exception and
returns the exception object.

:param tb: New traceback for the exception

:return: (object) Manipulated exception instance
:since:  v0.2.00
		"""

		self.exc_trace_list = ([ repr(tb) ] if (traceback is None) else traceback.format_tb(tb))
		RuntimeError.with_traceback(self, tb)

		return self
	#

	@staticmethod
	def print_current_stack_trace(out_stream = None):
	#
		"""
Prints the stack trace to the given output stream or stderr.

:param out_stream: Output stream

:since: v0.2.00
		"""

		printable_trace = ("{0!r}: {1!s}\n{2!r}".format(sys.exc_info()[:3])
		                   if (traceback is None) else
		                   traceback.format_exc()
		                  )

		if (out_stream is None): out_stream = sys.stderr
		out_stream.write(printable_trace)
	#
#

##j## EOF