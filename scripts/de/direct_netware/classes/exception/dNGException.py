# -*- coding: utf-8 -*-
##j## BOF

"""/*n// NOTE
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
NOTE_END //n*/"""
"""/**
* de.direct_netware.classes.exception.dNGException
*
* @internal  We are using JavaDoc to automate the documentation process for
*            creating the Developer's Manual. All sections including these
*            special comments will be removed from the release source code.
*            Use the following line to ensure 76 character sizes:
* ----------------------------------------------------------------------------
* @author    direct Netware Group
* @copyright (C) direct Netware Group - All rights reserved
* @package   pas_core
* @since     v0.1.00
* @license   http://www.direct-netware.de/redirect.php?licenses;w3c
*            W3C (R) Software License
*/"""

from exceptions import Exception
import traceback,sys

class dNGException (Exception):
#
	"""
The extended dNGException is used to redirect exceptions to output streams.

@author    direct Netware Group
@copyright (C) direct Netware Group - All rights reserved
@since     v1.0.0
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

	def __init__ (self,f_value,fException = None):
	#
		"""
Constructor __init__ (dNGException)

@since v0.1.00
		"""

		super (dNGException,self).__init__ (f_value)
		(self.exc_type,self.exc_value,self.exc_traceback) = sys.exc_info ()
		self.exc_cause = fException
	#

	def getCause (self):
	#
		"""
Return the cause.

@return (mixed) Inner exception
@since  v1.0.0
		"""

		return self.exc_cause
	#

	def printStackTrace (self,f_out):
	#
		"""
Prints the stack trace to the given output stream.

@param f_out Output stream
@since v1.0.0
		"""

		if (f_out != None): traceback.print_exception (self.exc_type,self.exc_value,self.exc_traceback,file = f_out)
	#

	@staticmethod
	def excPrintStackTrace (f_out):
	#
		"""
Prints the stack trace to the given output stream.

@param f_out Output stream
@since v1.0.0
		"""

		if (f_out != None):
		#
			(fexc_type,fexc_value,fexc_traceback) = sys.exc_info ()
			traceback.print_exception (fexc_type,fexc_value,fexc_traceback,file = f_out)
		#
	#
#

##j## EOF