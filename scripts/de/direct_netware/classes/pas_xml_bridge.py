# -*- coding: utf-8 -*-
##j## BOF

"""
de.direct_netware.classes.pas_xml_bridge

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

from threading import local

from .ext_core.xml_reader import direct_xml_reader
from .pas_globals import direct_globals
from .pas_local import direct_local

_direct_core_xml_bridge = local ()

class direct_xml_bridge (direct_xml_reader):
#
	"""
This class provides a bridge between PAS and XML to read XML on the fly.

@author    direct Netware Group
@copyright (C) direct Netware Group - All rights reserved
@package   pas_core
@since     v0.1.00
@license   http://www.direct-netware.de/redirect.php?licenses;w3c
           W3C (R) Software License
	"""

	def __init__ (self,parse_only = True):
	#
		"""
Constructor __init__ (direct_xml_bridge)

@param parse_only Parse data only
@since v0.1.00
		"""

		f_local = direct_local.py_get ()

		if ("lang_charset" in f_local): direct_xml_reader.__init__ (self,f_local['lang_charset'],parse_only,-1,direct_globals['settings']['timeout'])
		else: direct_xml_reader.__init__ (self,"UTF-8",parse_only,-1,direct_globals['settings']['timeout'])

		self.debug = direct_globals['debug']
		if (self.debug != None): self.debug.append ("#echo(__FILEPATH__)# -xml_bridge.__init__ (direct_xml_bridge)- (#echo(__LINE__)#)")
	#

	def __del__ (self):
	#
		"""
Destructor __del__ (direct_xml_bridge)

@since v0.1.00
		"""

		self.del_direct_xml_bridge ()
	#

	def del_direct_xml_bridge (self):
	#
		"""
Destructor del_direct_xml_bridge (direct_xml_bridge)

@since v0.1.00
		"""

		self.del_direct_xml_reader ()
	#

	def py_del ():
	#
		"""
The last "py_del ()" call will activate the Python singleton destructor.

@since v0.1.00
		"""

		global _direct_core_xml_bridge

		if (not hasattr (_direct_core_xml_bridge,"counter")): _direct_core_xml_bridge.counter = 0
		else: _direct_core_xml_bridge.counter -= 1

		if (_direct_core_xml_bridge.counter == 0): _direct_core_xml_bridge.object = None
	#
	py_del = staticmethod (py_del)

	def py_get (count = False):
	#
		"""
Get the direct_xml_bridge singleton.

@param  count Count "get ()" request
@return (direct_xml_bridge) Object on success
@since  v0.1.00
		"""

		global _direct_core_xml_bridge

		if (not hasattr (_direct_core_xml_bridge,"object")):
		#
			_direct_core_xml_bridge.object = None
			_direct_core_xml_bridge.counter = 0
		#

		if (_direct_core_xml_bridge.object == None): _direct_core_xml_bridge.object = direct_xml_bridge ()
		if (count): _direct_core_xml_bridge.counter += 1

		return _direct_core_xml_bridge.object
	#
	py_get = staticmethod (py_get)
#

##j## EOF