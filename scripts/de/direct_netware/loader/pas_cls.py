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
* de.direct_netware.loader.pas_cls
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
@since     v1.0.0
	"""

	option_parser = None
	run_callbacks = [ ]

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

		self.option_parser = OptionParser ()
		self.run_callbacks = [ ]
	#

	def error (self,f_exception):
	#
		"""
Prints the stack trace on this error event.

@param f_exception Inner exception
@since v1.0.0
		"""

		print (sys.exc_info ())
	#

	def exit (self):
	#
		"""
Executes registered callbacks before exiting this application.

@since v1.0.0
		"""

		global _direct_core_cls_exit_callbacks
		for f_callback in _direct_core_cls_exit_callbacks: f_callback ()
	#

	def run (self):
	#
		"""
Executes registered callbacks for the active application.

@since v1.0.0
		"""

		global _direct_core_cls_run_callbacks

		(f_options,f_invalid_args) = self.option_parser.parse_args ()
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