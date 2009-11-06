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
* de.direct_netware.classes.pas_xml
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

from ext_core.xml_writer import direct_xml_writer
from pas_local import direct_local
from pas_settings import direct_settings
import time

_direct_core_xml = None

class direct_xml (direct_xml_writer):
#
	"""
This class extends the bridge between PAS and XML to work with XML and
create valid documents.

@author    direct Netware Group
@copyright (C) direct Netware Group - All rights reserved
@since     v1.0.0
@license   http://www.direct-netware.de/redirect.php?licenses;w3c
           W3C (R) Software License
	"""

	def __init__ (self):
	#
		"""
Constructor __init__ (direct_xml)

@since v0.1.00
		"""

		f_local = direct_local.get ()
		f_settings = direct_settings.get ()

		if (f_local.has_key ("lang_charset")): super(direct_xml,self).__init__ (f_local['lang_charset'],(time.time ()),f_settings['timeout'],f_settings['debug_reporting'])
		else: super(direct_xml,self).__init__ ("UTF-8",(time.time ()),f_settings['timeout'],f_settings['debug_reporting'])
	#

	@staticmethod
	def get ():
	#
		"""
Get the direct_xml singleton.

@return (direct_xml) Object on success
@since  v1.0.0
		"""

		global _direct_core_xml
		if (_direct_core_xml == None): _direct_core_xml = direct_xml ()
		return _direct_core_xml
	#

	@staticmethod
	def get_xml ():
	#
		"""
Get the direct_xml singleton.

@return (direct_xml) Object on success
@since  v1.0.0
		"""

		return direct_xml.get ()
	#
#

##j## EOF