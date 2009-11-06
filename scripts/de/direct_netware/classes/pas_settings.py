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
* de.direct_netware.classes.pas_settings
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

_direct_core_settings = None

class direct_settings (dict):
#
	"""
Provides the direct_settings dict with correct path values predefined.

@author    direct Netware Group
@copyright (C) direct Netware Group - All rights reserved
@since     v1.0.0
@license   http://www.direct-netware.de/redirect.php?licenses;w3c
           W3C (R) Software License
	"""

	instance = None
	"""
The direct_settings instance
	"""

	"""
----------------------------------------------------------------------------
Extend the class
----------------------------------------------------------------------------
	"""

	def __init__ (self):
	#
		"""
Constructor __init__ (direct_settings)

@since v0.1.00
		"""

		global _direct_core_settings
		super(direct_settings,self).__init__ ()

		if (_direct_core_settings == None):
		#
			_direct_core_settings = self
			self.instance = self
		#
		else: self.instance = _direct_core_settings

		if (os.environ.has_key ("dNGpath")): self.instance['path_base'] = os.environ['dNGpath']
		else: self.instance['path_base'] = path.normpath ("../")

		if (os.environ.has_key ("dNGpathData")): self.instance['path_data'] = os.environ['dNGpathData']
		else: self.instance['path_data'] = path.normpath ("%s/data" % self.instance['path_base'] )

		if (os.environ.has_key ("dNGpathLang")): self.instance['path_lang'] = os.environ['dNGpathLang']
		else: self.instance['path_lang'] = path.normpath ("%s/lang" % self.instance['path_base'] )
	#

	def __missing__ (self,key):
	#
		"""
"__missing__" is called for missing keys in this dict.

@return (mixed) Defaults to none
@since  v1.0.0
		"""

		return None
	#

	@staticmethod
	def get ():
	#
		"""
Get the direct_settings singleton.

@return (direct_settings) Object on success
@since  v1.0.0
		"""

		global _direct_core_settings
		if (_direct_core_settings == None): _direct_core_settings = direct_settings ()
		return _direct_core_settings
	#

	@staticmethod
	def get_settings ():
	#
		"""
Get the direct_settings singleton.

@return (direct_settings) Object on success
@since  v1.0.0
		"""

		return direct_settings.get ()
	#
#

##j## EOF