# -*- coding: utf-8 -*-
##j## BOF

"""
de.direct_netware.loader.pas_cls
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

import sys,threading,time

try:
#
	import java.lang.System
	_direct_core_mode = "java"
#
except ImportError: _direct_core_mode = None

try:
#
	import clr
	clr.AddReferenceByPartialName ("IronPython")
	_direct_core_mode = "mono"
#
except ImportError: pass

if (_direct_core_mode != "mono"): import signal

from de.direct_netware.classes.exception.dNGException import dNGException
from de.direct_netware.classes.pas_globals import direct_globals

_direct_core_cls = None
_direct_core_cls_counter = None
_direct_core_cls_exit_callbacks = [ ]
_direct_core_cls_run_callbacks = [ ]
if (_direct_core_mode == None): _direct_core_mode = "py"

class direct_cls (object):
#
	"""
"direct_cls" makes it easy to build command line applications.

:author:    direct Netware Group
:copyright: direct Netware Group - All rights reserved
:package:   pas_core
:since:     v0.1.00
:license:   http://www.direct-netware.de/redirect.php?licenses;mpl2
            Mozilla Public License, v. 2.0
	"""

	argparser = None
	"""
Argument parser instance
	"""
	debug = None
	"""
Debug message container
	"""
	mainloop = None
	"""
Callable main loop without arguments
	"""
	mainloop_event = None
	"""
Mainloop event
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

:since: v0.1.00
		"""

		global _direct_core_cls
		_direct_core_cls = self

		self.debug = direct_globals['debug']
		self.mainloop = None
		self.mainloop_event = threading.Event ()

		if (self.debug != None): self.debug.append ("#echo(__FILEPATH__)# -cls_handler.__init__ (direct_cls)- (#echo(__LINE__)#)")
	#

	def del_direct_cls (self):
	#
		"""
Destructor del_direct_cls (direct_cls)

:since: v0.1.00
		"""

		pass
	#

	def error (self,py_exception):
	#
		"""
Prints the stack trace on this error event.

:param py_exception: Inner exception

:since: v0.1.00
		"""

		dNGException.print_current_stack_trace (sys.stderr)
		if (self.debug != None): print (self.debug)
	#

	def exit (self,py_exception = None):
	#
		"""
Executes registered callbacks before exiting this application.

:param py_exception: Inner exception

:since: v0.1.00
		"""

		if (self.debug != None): self.debug.append ("#echo(__FILEPATH__)# -cls_handler.exit ()- (#echo(__LINE__)#)")
		global _direct_core_cls_exit_callbacks

		for f_callback in _direct_core_cls_exit_callbacks: f_callback ()

		if (py_exception == None): sys.exit (0)
		else: raise (py_exception)
	#

	def run (self):
	#
		"""
Executes registered callbacks for the active application.

:since: v0.1.00
		"""

		if (self.debug != None): self.debug.append ("#echo(__FILEPATH__)# -cls_handler.run ()- (#echo(__LINE__)#)")
		global _direct_core_cls_run_callbacks

		if ((self.argparser != None) and (hasattr (self.argparser,"parse_args"))): f_args = self.argparser.parse_args ()
		else: f_args = { }

		self.argparser = None

		try:
		#
			for f_callback in _direct_core_cls_run_callbacks: f_callback (f_args)
		#
		except Exception as f_handled_exception: self.exit (f_handled_exception)

		try:
		#
			self.mainloop_event.set ();

			if (self.mainloop == None):
			#
				f_active = True
				f_main_thread = threading.current_thread ()

				while (f_active):
				#
					f_active = False

					try:
					#
						for f_thread in (threading.enumerate ()):
						#
							if ((f_thread != None) and (f_main_thread != f_thread) and (f_thread.is_alive ()) and (not f_thread.daemon)): f_thread.join ()
						#
					#
					except KeyboardInterrupt as f_handled_exception: raise f_handled_exception
					except: f_active = True

					if (f_active): time.sleep (1)
				#
			#
			else: self.mainloop ()

			self.exit ()
		#
		except KeyboardInterrupt: self.exit ()
	#

	def set_mainloop (self,py_function):
	#
		"""
Register a callback for the application main loop.

:param py_function: Python callback

:since: v0.1.00
		"""

		if (self.debug != None): self.debug.append ("#echo(__FILEPATH__)# -cls_handler.set_mainloop (py_function)- (#echo(__LINE__)#)")

		if (self.mainloop == None): self.mainloop = py_function
		else: raise RuntimeError ("Main loop already registered")
	#

	def signal (self,os_signal,stack_frame):
	#
		"""
Handles an OS signal.

:param os_signal: OS signal
:param stack_frame: Stack frame

:since: v0.1.00
		"""

		if (self.debug != None): self.debug.append ("#echo(__FILEPATH__)# -cls_handler.signal (os_signal,stack_frame)- (#echo(__LINE__)#)")
		self.exit ()
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
Get the direct_cls singleton.

:return: (direct_cls) Object on success
:since:  v0.1.00
		"""

		global _direct_core_cls
		return _direct_core_cls
	#
	py_get = staticmethod (py_get)

	def py_get_mode ():
	#
		"""
Returns the current Python engine (one of "java", "mono" and "py").

:return: (str) Active mode
:since:  v0.1.00
		"""

		global _direct_core_mode
		return _direct_core_mode
	#
	py_get_mode = staticmethod (py_get_mode)

	def register_exit_callback (py_function):
	#
		"""
Register a callback for the application exit event.

:param py_function: Python callback

:since: v0.1.00
		"""

		global _direct_core_cls_exit_callbacks
		_direct_core_cls_exit_callbacks.append (py_function)
	#
	register_exit_callback = staticmethod (register_exit_callback)

	def register_mainloop (py_function):
	#
		"""
Register a callback for the application main loop.

:param py_function: Python callback

:since: v0.1.00
		"""

		global _direct_core_cls
		_direct_core_cls.set_mainloop (py_function)
	#
	register_mainloop = staticmethod (register_mainloop)

	def register_run_callback (py_function):
	#
		"""
Register a callback for the application activation event.

:param py_function: Python callback

:since: v0.1.00
		"""

		global _direct_core_cls_run_callbacks
		_direct_core_cls_run_callbacks.append (py_function)
	#
	register_run_callback = staticmethod (register_run_callback)
#

def direct_cls_signal (os_signal,stack_frame):
#
	"""
Callback function for OS signals.

:param os_signal: OS signal
:param stack_frame: Stack frame

:since: v0.1.00
	"""

	global _direct_core_cls
	if (_direct_core_cls != None): _direct_core_cls.signal (os_signal,stack_frame)
#

if (_direct_core_mode != "mono"):
#
	signal.signal (signal.SIGABRT,direct_cls_signal)
	signal.signal (signal.SIGTERM,direct_cls_signal)

	if (_direct_core_mode == "py"):
	#
		try: signal.signal (signal.SIGQUIT,direct_cls_signal)
		except AttributeError: pass
	#
#

##j## EOF