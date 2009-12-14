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
#echo(pasCoreVersion)#
pas/#echo(__FILEPATH__)#
----------------------------------------------------------------------------
NOTE_END //n*/"""
"""
de.direct_netware.classes.pas_xml

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

from ext_core.xml_writer import direct_xml_writer
from pas_debug import direct_debug
from pas_local import direct_local
from pas_settings import direct_settings
import time

_direct_core_xml = None
_direct_core_xml_counter = 0

class direct_xml (direct_xml_writer):
#
	"""
This class extends the bridge between PAS and XML to work with XML and
create valid documents.

@author    direct Netware Group
@copyright (C) direct Netware Group - All rights reserved
@package   pas_core
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

		if ("lang_charset" in f_local): super(direct_xml,self).__init__ (f_local['lang_charset'],(time.time ()),f_settings['timeout'])
		else: super(direct_xml,self).__init__ ("UTF-8",(time.time ()),f_settings['timeout'])

		self.debug = direct_debug.get ()
		if (self.debug != None): self.debug.append ("#echo(__FILEPATH__)# -xml->__construct (direct_xml)- (#echo(__LINE__)#)")
	#

	def __del__ (self):
	#
		"""
Destructor __del__ (direct_xml)

@since v0.1.00
		"""

		self.del_direct_xml ()
	#

	def del_direct_xml (self):
	#
		"""
Destructor del_direct_xml (direct_xml)

@since v0.1.00
		"""

		direct_debug.py_del ()
		self.del_direct_xml_writer ()
	#

	@staticmethod
	def get_parser (f_count = False):
	#
		"""
Get the direct_xml singleton.

@param  bool Count "get ()" request
@return (direct_xml) Object on success
@since  v1.0.0
		"""

		global _direct_core_xml,_direct_core_xml_counter

		if (_direct_core_xml == None): _direct_core_xml = direct_xml ()
		if (f_count): _direct_core_xml_counter += 1

		return _direct_core_xml
	#

	@staticmethod
	def get_xml (f_count = False):
	#
		"""
Get the direct_xml singleton.

@param  bool Count "get ()" request
@return (direct_xml) Object on success
@since  v1.0.0
		"""

		return direct_xml.get_parser (f_count)
	#

	@staticmethod
	def py_del ():
	#
		"""
The last "py_del ()" call will activate the Python singleton destructor.

@since  v1.0.0
		"""

		global _direct_core_xml,_direct_core_xml_counter

		_direct_core_xml_counter -= 1
		if (_direct_core_xml_counter == 0): _direct_core_xml = None
	#
#

##j## EOF