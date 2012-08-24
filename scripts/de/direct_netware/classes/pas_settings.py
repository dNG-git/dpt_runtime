# -*- coding: utf-8 -*-
##j## BOF

"""
de.direct_netware.classes.pas_settings

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

from os import path
import os

from .pas_globals import direct_globals
from .pas_pythonback import direct_str

class direct_settings (dict):
#
	"""
Provides the direct_settings dict with correct path values predefined.

@author    direct Netware Group
@copyright (C) direct Netware Group - All rights reserved
@package   pas_core
@since     v0.1.00
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

		dict.__init__ (self)

		if ("settings" in direct_globals): self.instance = direct_globals['settings']
		else: self.instance = self

		if ("dNGpath" in os.environ): self.instance['path_base'] = direct_str (os.environ['dNGpath'])
		else: self.instance['path_base'] = path.normpath ("{0}/../../../../..".format (direct_str (__file__)))

		if ("dNGpathData" in os.environ): self.instance['path_data'] = direct_str (os.environ['dNGpathData'])
		else: self.instance['path_data'] = path.normpath ("{0}/data".format (self.instance['path_base']))

		if ("dNGpathLang" in os.environ): self.instance['path_lang'] = direct_str (os.environ['dNGpathLang'])
		else: self.instance['path_lang'] = path.normpath ("{0}/lang".format (self.instance['path_base']))
	#

	def __missing__ (self,key):
	#
		"""
Python.org: If a subclass of dict defines a method __missing__(), if the key
is not present, the d[key] operation calls that method with the key as
argument.

@param  key Key we are looking for
@return (mixed) Defaults to none
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
@since  v1.0.5
		"""

		if (len (args) > 1):
		#
			if (args[0] in self): return dict.get (self,*args)
			else: return args[1]
		#
		else: return dict.get (self,*args)
	#

	def py_del ():
	#
		"""
The last "py_del ()" call will activate the Python singleton destructor.

@since v0.1.00
		"""

		pass
	#
	py_del = staticmethod (py_del)

	def py_get (count = False):
	#
		"""
Get the direct_settings singleton.

@param  count Count "get ()" request
@return (direct_settings) Object on success
@since  v0.1.00
		"""

		if ("settings" not in direct_globals): direct_globals['settings'] = direct_settings ()
		return direct_globals['settings']
	#
	py_get = staticmethod (py_get)
#

##j## EOF