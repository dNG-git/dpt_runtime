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
* de.direct_netware.classes.pas_local
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

from os import path
import os

_direct_core_local = None

class direct_local (dict):
#
	"""
Provides the direct_local dict.

@author    direct Netware Group
@copyright (C) direct Netware Group - All rights reserved
@since     v1.0.0
@license   http://www.direct-netware.de/redirect.php?licenses;w3c
           W3C (R) Software License
	"""

	instance = None
	"""
The direct_local instance
	"""

	"""
----------------------------------------------------------------------------
Extend the class
----------------------------------------------------------------------------
	"""

	def __init__ (self):
	#
		"""
Constructor __init__ (direct_local)

@since v0.1.00
		"""

		global _direct_core_local
		super(direct_local,self).__init__ ()

		if (_direct_core_local == None):
		#
			_direct_core_local = self
			self.instance = self
		#
		else: self.instance = _direct_core_local
	#

	def __missing__ (self,key):
	#
		"""
"__missing__" is called for missing keys in this dict.

@return (string) Defaults to " <key> "
@since  v1.0.0
		"""

		return " %s " % key
	#

	@staticmethod
	def get ():
	#
		"""
Get the direct_local singleton.

@return (direct_local) Object on success
@since  v1.0.0
		"""

		global _direct_core_local
		if (_direct_core_local == None): _direct_core_local = direct_local ()
		return _direct_core_local
	#

	@staticmethod
	def get_local ():
	#
		"""
Get the direct_local singleton.

@return (direct_local) Object on success
@since  v1.0.0
		"""

		return direct_local.get ()
	#
#

##j## EOF