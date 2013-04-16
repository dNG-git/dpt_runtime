# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.loader.cli
"""
"""n// NOTE
----------------------------------------------------------------------------
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
http://www.direct-netware.de/redirect.py?pas;core

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
http://www.direct-netware.de/redirect.py?licenses;mpl2
----------------------------------------------------------------------------
#echo(pasCoreVersion)#
#echo(__FILEPATH__)#
----------------------------------------------------------------------------
NOTE_END //n"""

import threading, time
import gc

from dNG.pas.data.exception import direct_exception

try:
#
	import java.lang.System
	_direct_cli_mode = "java"
#
except ImportError: _direct_cli_mode = None

try:
#
	import clr
	clr.AddReferenceByPartialName("IronPython")
	_direct_cli_mode = "mono"
#
except ImportError: pass

if (_direct_cli_mode != "mono"): import signal
if (_direct_cli_mode == None): _direct_cli_mode = "py"

class direct_cli(object):
#
	"""
"direct_cli" makes it easy to build command line applications.

:author:    direct Netware Group
:copyright: direct Netware Group - All rights reserved
:package:   pas.core
:since:     v0.1.00
:license:   http://www.direct-netware.de/redirect.py?licenses;mpl2
            Mozilla Public License, v. 2.0
	"""

	callbacks_run = [ ]
	"""
Callbacks for "run()"
	"""
	callbacks_shutdown = [ ]
	"""
Callbacks for "shutdown()"
	"""
	instance = None
	"""
"direct_cli" instance
	"""

	def __init__(self):
	#
		"""
Constructor __init__(direct_cli)

:since: v0.1.00
		"""

		self.arg_parser = None
		"""
ArgumentParser instance
		"""
		self.log_handler = None
		"""
The log_handler is called whenever debug messages should be logged or errors
happened.
		"""
		self.mainloop = None
		"""
Callable main loop without arguments
		"""
		self.mainloop_event = threading.Event()
		"""
Mainloop event
		"""

		direct_cli.instance = self
	#

	def error(self, py_exception):
	#
		"""
Prints the stack trace on this error event.

:param py_exception: Inner exception

:access: protected
:since:  v0.1.00
		"""

		if (isinstance(py_exception, direct_exception)): py_exception.print_stack_trace()
		else: direct_exception.print_current_stack_trace()
	#

	def return_instance(self):
	#
		"""
The last "return_instance()" call will activate the Python singleton
destructor.

:since: v0.1.00
		"""

		pass
	#

	def run(self):
	#
		"""
Executes registered callbacks for the active application.

:since: v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -cli.run()- (#echo(__LINE__)#)")

		if (self.arg_parser != None and hasattr(self.arg_parser, "parse_args")): args = self.arg_parser.parse_args()
		else: args = { }

		self.arg_parser = None

		for callback in direct_cli.callbacks_run:
		#
			try: callback(args)
			except Exception as handled_exception: self.shutdown(handled_exception)
		#

		try:
		#
			self.mainloop_event.set()

			if (self.mainloop == None):
			#
				active = True
				main_thread = threading.current_thread()

				while (active):
				#
					active = False

					try:
					#
						for thread in threading.enumerate():
						#
							if (thread != None and main_thread != thread and thread.is_alive() and (not thread.daemon)): thread.join()
						#
					#
					except KeyboardInterrupt as handled_exception: raise
					except: active = True

					if (active): time.sleep(1)
				#
			#
			else: self.mainloop()

			self.shutdown()
		#
		except KeyboardInterrupt: self.shutdown()
	#

	def set_mainloop(self, py_function):
	#
		"""
Register a callback for the application main loop.

:param py_function: Python callback

:since: v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -cli.set_mainloop(py_function)- (#echo(__LINE__)#)")

		if (self.mainloop == None): self.mainloop = py_function
		else: raise RuntimeError("Main loop already registered")
	#

	def set_log_handler(self, log_handler):
	#
		"""
Sets the log_handler.

:param log_handler: log_handler to use

:since: v0.1.00
		"""

		if (log_handler != None): log_handler.debug("#echo(__FILEPATH__)# -cli.set_log_handler(log_handler)- (#echo(__LINE__)#)")
		self.log_handler = log_handler
	#

	def signal(self, os_signal, stack_frame):
	#
		"""
Handles an OS signal.

:param os_signal: OS signal
:param stack_frame: Stack frame

:access: protected
:since:  v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -cli.signal(os_signal, stack_frame)- (#echo(__LINE__)#)")
		self.shutdown()
	#

	def shutdown(self, py_exception = None):
	#
		"""
Executes registered callbacks before shutting down this application.

:param py_exception: Inner exception

:since: v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -cli_handler.shutdown()- (#echo(__LINE__)#)")

		"""
Cleanup unused objects
		"""

		gc.collect()

		for callback in direct_cli.callbacks_shutdown:
		#
			try: callback()
			except Exception as handled_exception: self.error(handled_exception)
		#

		if (py_exception != None): raise py_exception
	#

	@staticmethod
	def get_instance(count = False):
	#
		"""
Get the cli singleton.

:param count: Count "get()" request

:return: (direct_cli) Object on success
:since:  v0.1.00
		"""

		return direct_cli.instance
	#

	@staticmethod
	def get_py_mode():
	#
		"""
Returns the current Python engine (one of "java", "mono" and "py").

:return: (str) Active mode
:since:  v0.1.00
		"""

		global _direct_cli_mode
		return _direct_cli_mode
	#

	@staticmethod
	def register_mainloop(py_function):
	#
		"""
Register a callback for the application main loop.

:param py_function: Python callback

:since: v0.1.00
		"""

		direct_cli.instance.set_mainloop(py_function)
	#

	@staticmethod
	def register_run_callback(py_function):
	#
		"""
Register a callback for the application activation event.

:param py_function: Python callback

:since: v0.1.00
		"""

		direct_cli.callbacks_run.append(py_function)
	#

	@staticmethod
	def register_shutdown_callback(py_function):
	#
		"""
Register a callback for the application shutdown event.

:param py_function: Python callback

:since: v0.1.00
		"""

		direct_cli.callbacks_shutdown.append(py_function)
	#
#

def direct_cls_signal(os_signal, stack_frame):
#
	"""
Callback function for OS signals.

:param os_signal: OS signal
:param stack_frame: Stack frame

:since: v0.1.00
	"""

	if (direct_cli.instance != None): direct_cli.instance.signal(os_signal, stack_frame)
#

if (hasattr(signal, "SIGABRT")): signal.signal(signal.SIGABRT, direct_cls_signal)
if (hasattr(signal, "SIGTERM")): signal.signal(signal.SIGTERM, direct_cls_signal)
if (hasattr(signal, "SIGQUIT")): signal.signal(signal.SIGQUIT, direct_cls_signal)

##j## EOF