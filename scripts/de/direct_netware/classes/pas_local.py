# -*- coding: utf-8 -*-
##j## BOF

"""
de.direct_netware.classes.pas_local
"""
"""n// NOTE
----------------------------------------------------------------------------
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
http://www.direct-netware.de/redirect.php?pas

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
http://www.direct-netware.de/redirect.php?licenses;mpl2
----------------------------------------------------------------------------
#echo(pasCoreVersion)#
pas/#echo(__FILEPATH__)#
----------------------------------------------------------------------------
NOTE_END //n"""

from threading import local

from .pas_pythonback import direct_str

_direct_core_local = local ()

class direct_local (dict):
#
	"""
Provides the direct_local dict.

:author:    direct Netware Group
:copyright: direct Netware Group - All rights reserved
:package:   pas_core
:since:     v0.1.00
:license:   http://www.direct-netware.de/redirect.php?licenses;mpl2
            Mozilla Public License, v. 2.0
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

:since: v0.1.00
		"""

		global _direct_core_local
		dict.__init__ (self)

		if (hasattr (_direct_core_local,"object")): self.instance = _direct_core_local.object
		else: self.instance = self
	#

	def __missing__ (self,key):
	#
		"""
Python.org: If a subclass of dict defines a method __missing__(), if the key
is not present, the d[key] operation calls that method with the key as
argument.

:param key: Key we are looking for

:return: (str) Defaults to " <key> "
:since:  v0.1.00
		"""

		return " {0} ".format (direct_str (key))
	#

	def get (self,*args):
	#
		"""
Python.org: Return the value for key if key is in the dictionary, else
default.

Implemented for IronPython which calls "__missing__ ()" in this case.

:param args: Positional arguments

:return: (mixed) Defaults to none
:since:  v0.1.00
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

:since: v0.1.00
		"""

		pass
	#
	py_del = staticmethod (py_del)

	def py_get (count = False):
	#
		"""
Get the direct_local singleton.

:param count: Count "get ()" request

:return: (direct_local) Object on success
:since:  v0.1.00
		"""

		global _direct_core_local
		if (not hasattr (_direct_core_local,"object")): _direct_core_local.object = direct_local ()
		return _direct_core_local.object
	#
	py_get = staticmethod (py_get)
#

##j## EOF