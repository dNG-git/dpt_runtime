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
de.direct_netware.loader.pas_cls

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


from de.direct_netware.classes.exception.dNGException import dNGException
from de.direct_netware.classes.pas_debug import direct_debug
from optparse import OptionParser
import signal,sys

_direct_core_cls = None
_direct_core_cls_exit_callbacks = [ ]
_direct_core_cls_run_callbacks = [ ]

class direct_cls (object):
#
	"""
"direct_cls" makes it easy to build command line applications.

@author    direct Netware Group
@copyright (C) direct Netware Group - All rights reserved
@package   pas_core
@since     v1.0.0
@license   http://www.direct-netware.de/redirect.php?licenses;w3c
           W3C (R) Software License
	"""

	debug = None
	"""
Debug message container
	"""
	option_parser = None
	"""
OptionParser instance
	"""

	"""
----------------------------------------------------------------------------
Construct the class
----------------------------------------------------------------------------
	"""

	def __init__ (self):
	#
		"""
Constructor __init__ (direct_cls)

@since v0.1.00
		"""

		global _direct_core_cls
		_direct_core_cls = self

		self.debug = direct_debug.get ()
		self.option_parser = OptionParser ()

		if (self.debug != None): self.debug.append ("#echo(__FILEPATH__)# -cls_handler->__construct (direct_cls)- (#echo(__LINE__)#)")
	#

	def __del__ (self):
	#
		"""
Destructor __del__ (direct_cls)

@since v0.1.00
		"""

		self.del_direct_cls ()
	#

	def del_direct_cls (self):
	#
		"""
Destructor del_direct_cls (direct_cls)

@since v0.1.00
		"""

		direct_debug.py_del ()
	#

	def error (self,f_exception):
	#
		"""
Prints the stack trace on this error event.

@param f_exception Inner exception
@since v1.0.0
		"""

		dNGException.print_current_stack_trace (sys.stderr)
		if (self.debug != None): print (self.debug)
	#

	def exit (self):
	#
		"""
Executes registered callbacks before exiting this application.

@since v1.0.0
		"""

		if (self.debug != None): self.debug.append ("#echo(__FILEPATH__)# -cls_handler->exit ()- (#echo(__LINE__)#)")
		global _direct_core_cls_exit_callbacks

		for f_callback in _direct_core_cls_exit_callbacks: f_callback ()
	#

	def run (self):
	#
		"""
Executes registered callbacks for the active application.

@since v1.0.0
		"""

		if (self.debug != None): self.debug.append ("#echo(__FILEPATH__)# -cls_handler->run ()- (#echo(__LINE__)#)")
		global _direct_core_cls_run_callbacks

		( f_options,f_invalid_args ) = self.option_parser.parse_args ()
		self.option_parser = None

		for f_callback in _direct_core_cls_run_callbacks: f_callback (f_options,f_invalid_args)
	#

	def signal (self,f_signal,f_stack_frame):
	#
		"""
Handles an OS signal.

@param f_signal OS signal
@param f_stack_frame Stack frame
@since v1.0.0
		"""

		if (self.debug != None): self.debug.append ("#echo(__FILEPATH__)# -cls_handler->signal (+f_signal,+f_stack_frame)- (#echo(__LINE__)#)")
		self.exit ()
	#

	@staticmethod
	def register_exit_callback (f_function):
	#
		"""
Register a callback for the application exit event.

@param f_function Python callback
@since v1.0.0
		"""

		global _direct_core_cls_exit_callbacks
		_direct_core_cls_exit_callbacks.append (f_function)
	#

	@staticmethod
	def register_run_callback (f_function):
	#
		"""
Register a callback for the application activation event.

@param f_function Python callback
@since v1.0.0
		"""

		global _direct_core_cls_run_callbacks
		_direct_core_cls_run_callbacks.append (f_function)
	#
#

def direct_cls_signal (f_signal,f_stack_frame):
#
	"""
Callback function for OS signals.

@param f_signal OS signal
@param f_stack_frame Stack frame
@since v1.0.0
	"""

	global _direct_core_cls
	if (_direct_core_cls != None): _direct_core_cls.signal (f_signal,f_stack_frame)
	sys.exit (0)
#

signal.signal (signal.SIGABRT,direct_cls_signal)
signal.signal (signal.SIGTERM,direct_cls_signal)

try: signal.signal (signal.SIGCHLD,direct_cls_signal)
except AttributeError,g_unhandled_exception: pass

try: signal.signal (signal.SIGQUIT,direct_cls_signal)
except AttributeError,g_unhandled_exception: pass

##j## EOF