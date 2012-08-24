# -*- coding: utf-8 -*-
##j## BOF

"""
de.direct_netware.classes.exception.dNGException

@internal  We are using epydoc (JavaDoc style) to automate the documentation
           process for creating the Developer's Manual.
           Use the following line to ensure 76 character sizes:
----------------------------------------------------------------------------
@author    direct Netware Group
@copyright (C) direct Netware Group - All rights reserved
@package   pas_core
@since     v0.1.00
@license   http://www.direct-netware.de/redirect.php?licenses;w3c
           W3C (R) Software License
"""
"""n// NOTE
----------------------------------------------------------------------------
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
http://www.direct-netware.de/redirect.php?pas

This work is distributed under the W3C (R) Software License, but without any
warranty; without even the implied warranty of merchantability or fitness
for a particular purpose.
----------------------------------------------------------------------------
http://www.direct-netware.de/redirect.php?licenses;w3c
----------------------------------------------------------------------------
#echo(pasCoreVersion)#
pas/#echo(__FILEPATH__)#
----------------------------------------------------------------------------
NOTE_END //n"""

import traceback,sys

class dNGException (Exception):
#
	"""
The extended dNGException is used to redirect exceptions to output streams.

@author    direct Netware Group
@copyright (C) direct Netware Group - All rights reserved
@package   pas_core
@since     v0.1.00
@license   http://www.direct-netware.de/redirect.php?licenses;w3c
           W3C (R) Software License
	"""

	exc_cause = None
	exc_type = None
	exc_value = None
	exc_traceback = None

	"""
----------------------------------------------------------------------------
Extend the class
----------------------------------------------------------------------------
	"""

	def __init__ (self,value,py_exception = None):
	#
		"""
Constructor __init__ (dNGException)

@param value Exception message value
@param py_exception Inner exception
@since v0.1.00
		"""

		Exception.__init__ (self,value)
		( self.exc_type,self.exc_value,self.exc_traceback ) = sys.exc_info ()
		self.exc_cause = py_exception
	#

	def get_cause (self):
	#
		"""
Return the cause.

@return (mixed) Inner exception
@since  v0.1.00
		"""

		return self.exc_cause
	#

	def print_stack_trace (self,out_stream):
	#
		"""
Prints the stack trace to the given output stream.

@param out_stream Output stream
@since v0.1.00
		"""

		if (out_stream != None): traceback.print_exception (self.exc_type,self.exc_value,self.exc_traceback,file = out_stream)
	#

	def print_current_stack_trace (out_stream):
	#
		"""
Prints the stack trace to the given output stream.

@param out_stream Output stream
@since v0.1.00
		"""

		if (out_stream != None):
		#
			( f_exc_type,f_exc_value,f_exc_traceback ) = sys.exc_info ()
			traceback.print_exception (f_exc_type,f_exc_value,f_exc_traceback,file = out_stream)
		#
	#
	print_current_stack_trace = staticmethod (print_current_stack_trace)
#

##j## EOF