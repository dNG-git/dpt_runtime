# -*- coding: utf-8 -*-
##j## BOF

"""
de.direct_netware.classes.pas_globals

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

class _direct_globals_dict (dict):
#
	"""
Provides the direct_globals dict.

@author    direct Netware Group
@copyright (C) direct Netware Group - All rights reserved
@package   pas_core
@since     v0.1.00
@license   http://www.direct-netware.de/redirect.php?licenses;w3c
           W3C (R) Software License
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

		dict.__init__ (self)
	#

	def __missing__ (self,key):
	#
		"""
Python.org: If a subclass of dict defines a method __missing__(), if the key
is not present, the d[key] operation calls that method with the key as
argument.

@param  key Key we are looking for
@return (mixed) Defaults to None
@since  v0.1.00
		"""

		return None
	#

	def get (self,*args):
	#
		"""
Python.org: Return the value for key if key is in the dictionary, else
default.

Implemented for IronPython which calls "__missing__ ()" in this case.

@param  args Positional arguments
@return (mixed) Defaults to none
@since  v0.1.00
		"""

		if (len (args) > 1):
		#
			if (args[0] in self): return dict.get (self,*args)
			else: return args[1]
		#
		else: return dict.get (self,*args)
	#
#

direct_globals = _direct_globals_dict ()

##j## EOF