# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.loader.Cli
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

from weakref import ref
import threading
import time

try: import signal
except ImportError: pass

_IMPLEMENTATION_JAVA = 1
"""
Java based Python implementation
"""
_IMPLEMENTATION_PYTHON = 2
"""
Native Python implementation
"""
_IMPLEMENTATION_MONO = 3
"""
Mono/.NET based Python implementation
"""

try:
#
	import java.lang.System
	_mode = _IMPLEMENTATION_JAVA
#
except ImportError: _mode = _IMPLEMENTATION_PYTHON

if (_mode == _IMPLEMENTATION_PYTHON):
#
	try:
	#
		import clr
		clr.AddReferenceByPartialName("IronPython")
		_mode = _IMPLEMENTATION_MONO
	#
	except ImportError: pass
#

from dNG.pas.data.traced_exception import TracedException

class Cli(object):
#
	"""
"Cli" makes it easy to build command line applications.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	IMPLEMENTATION_JAVA = _IMPLEMENTATION_JAVA
	"""
Java based Python implementation
	"""
	IMPLEMENTATION_PYTHON = _IMPLEMENTATION_PYTHON
	"""
Native Python implementation
	"""
	IMPLEMENTATION_MONO = _IMPLEMENTATION_MONO
	"""
Mono/.NET based Python implementation
	"""

	callbacks_run = [ ]
	"""
Callbacks for "run()"
	"""
	callbacks_shutdown = [ ]
	"""
Callbacks for "shutdown()"
	"""
	weakref_instance = None
	"""
"Cli" weakref instance
	"""

	def __init__(self):
	#
		"""
Constructor __init__(Cli)

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

		Cli.weakref_instance = ref(self)
	#

	def error(self, _exception):
	#
		"""
Prints the stack trace on this error event.

:param _exception: Inner exception

:since: v0.1.00
		"""

		if (isinstance(_exception, TracedException)): _exception.print_stack_trace()
		else: TracedException.print_current_stack_trace()
	#

	def run(self):
	#
		"""
Executes registered callbacks for the active application.

:since: v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -Cli.run()- (#echo(__LINE__)#)")

		if (self.arg_parser != None and hasattr(self.arg_parser, "parse_args")): args = self.arg_parser.parse_args()
		else: args = { }

		self.arg_parser = None

		try:
		#
			for callback in Cli.callbacks_run: callback(args)
			Cli.callbacks_run = [ ]

			self.mainloop_event.set()
			if (self.mainloop != None): self.mainloop()
		#
		except BaseException as handled_exception:
		#
			if (not isinstance(handled_exception, KeyboardInterrupt)): self.error(handled_exception)
		#

		self.shutdown()
	#

	def set_mainloop(self, callback):
	#
		"""
Register a callback for the application main loop.

:param callback: Python callback

:since: v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -Cli.set_mainloop(callback)- (#echo(__LINE__)#)")

		if (self.mainloop == None): self.mainloop = callback
		else: raise RuntimeError("Main loop already registered")
	#

	def set_log_handler(self, log_handler):
	#
		"""
Sets the log_handler.

:param log_handler: log_handler to use

:since: v0.1.00
		"""

		self.log_handler = log_handler
	#

	def _signal(self, os_signal, stack_frame):
	#
		"""
Handles an OS signal.

:param os_signal: OS signal
:param stack_frame: Stack frame

:since: v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -Cli._signal(os_signal, stack_frame)- (#echo(__LINE__)#)")
		self.shutdown()
	#

	def shutdown(self, _exception = None):
	#
		"""
Executes registered callbacks before shutting down this application.

:param _exception: Inner exception

:since: v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -Cli.shutdown()- (#echo(__LINE__)#)")

		"""
Cleanup unused objects
		"""

		for callback in Cli.callbacks_shutdown:
		#
			try: callback()
			except Exception as handled_exception: self.error(handled_exception)
		#

		Cli.callbacks_shutdown = [ ]

		"""
Check if all threads are joined before exiting the main thread.
		"""

		is_recheck_needed = True
		main_thread = threading.current_thread()

		while (is_recheck_needed):
		#
			is_recheck_needed = False

			for thread in threading.enumerate():
			#
				try:
				#
					if (thread != None and main_thread != thread and thread.is_alive() and (not thread.daemon)):
					#
						thread.join()
						is_recheck_needed = True
					#
				#
				except KeyboardInterrupt: pass
				except BaseException as handled_exception: self.error(handled_exception)
			#

			if (is_recheck_needed): time.sleep(1)
		#

		if (_exception != None): raise _exception
	#

	@staticmethod
	def get_instance():
	#
		"""
Get the cli singleton.

:return: (Cli) Object on success
:since:  v0.1.00
		"""

		return Cli.weakref_instance()
	#

	@staticmethod
	def get_py_mode():
	#
		"""
Returns the current Python engine (one of "java", "mono" and "py").

:return: (str) Active mode
:since:  v0.1.00
		"""

		global _mode
		return _mode
	#

	@staticmethod
	def register_mainloop(callback):
	#
		"""
Register a callback for the application main loop.

:param callback: Python callback

:since: v0.1.00
		"""

		instance = Cli.get_instance()
		if (instance != None): instance.set_mainloop(callback)
	#

	@staticmethod
	def register_run_callback(callback):
	#
		"""
Register a callback for the application activation event.

:param callback: Python callback

:since: v0.1.00
		"""

		Cli.callbacks_run.append(callback)
	#

	@staticmethod
	def register_shutdown_callback(callback):
	#
		"""
Register a callback for the application shutdown event.

:param callback: Python callback

:since: v0.1.00
		"""

		Cli.callbacks_shutdown.append(callback)
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

	instance = Cli.get_instance()
	if (instance != None): instance._signal(os_signal, stack_frame)
#

if (hasattr(signal, "SIGABRT")): signal.signal(signal.SIGABRT, direct_cls_signal)
if (hasattr(signal, "SIGTERM")): signal.signal(signal.SIGTERM, direct_cls_signal)
if (hasattr(signal, "SIGQUIT")): signal.signal(signal.SIGQUIT, direct_cls_signal)

##j## EOF