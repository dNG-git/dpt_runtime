# -*- coding: utf-8 -*-
##j## BOF

"""
de.direct_netware.classes.pas_debug

@internal  We are using epydoc (JavaDoc style) to automate the documentation
           process for creating the Developer's Manual.
           Use the following line to ensure 76 character sizes:
----------------------------------------------------------------------------
@author    direct Netware Group
@copyright (C) direct Netware Group - All rights reserved
@package   pas_core
@since     v0.1.00
@license   http://www.direct-netware.de/redirect.php?licenses;mpl2
           Mozilla Public License, v. 2.0
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

from .pas_globals import direct_globals
from .pas_logger import direct_logger

class direct_debug (list):
#
	"""
Provides a debug singleton Python list.

@author    direct Netware Group
@copyright (C) direct Netware Group - All rights reserved
@package   pas_core
@since     v0.1.00
@license   http://www.direct-netware.de/redirect.php?licenses;mpl2
           Mozilla Public License, v. 2.0
	"""

	logger = None
	"""
Logging object
	"""

	"""
----------------------------------------------------------------------------
Extend the class
----------------------------------------------------------------------------
	"""

	def __init__ (self):
	#
		"""
Constructor __init__ (direct_debug)

@since v0.1.00
		"""

		list.__init__ (self)
		self.logger = direct_logger.py_get ()
	#

	def __del__ (self):
	#
		"""
Destructor __del__ (direct_debug)

@since v0.1.00
		"""

		self.del_direct_debug ()
	#

	def del_direct_debug (self):
	#
		"""
Destructor del_direct_debug (direct_debug)

@since v0.1.00
		"""

		if (direct_logger != None): direct_logger.py_del ()
	#

	def append (self,item,value = None,return_value = False):
	#
		"""
"append ()" method to save the last 50 debug messages.

@param  item Item to append
@param  value Value to return
@param  return_value True to return the given value
@return (direct_debug) Object on success
@since  v0.1.00
		"""

		if (len (self) > 50): self.pop (0)

		list.append (self,item)
		self.logger.write (direct_logger.DEBUG,item)

		if (return_value): return value
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

	def py_get (debug = False,count = True):
	#
		"""
Get the direct_debug singleton.

@param  debug True if debugging is activated
@param  count Count "get ()" request
@return (direct_debug) Object on success
@since  v0.1.00
		"""

		if (((debug == True) or (debug == "1")) and ("debug" not in direct_globals)): direct_globals['debug'] = direct_debug ()
		return direct_globals['debug']
	#
	py_get = staticmethod (py_get)
#

##j## EOF