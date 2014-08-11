# -*- coding: utf-8 -*-
##j## BOF

"""
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
"""

# pylint: disable=import-error,unused-import

from errno import EINVAL, ESRCH
from time import sleep
from weakref import ref
import os
import threading

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
from dNG.pas.runtime.exception_log_trap import ExceptionLogTrap
from dNG.pas.runtime.thread import Thread
from dNG.pas.runtime.value_exception import ValueException

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

	# pylint: disable=unused-argument

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

	_callbacks_run = [ ]
	"""
Callbacks for "run()"
	"""
	_callbacks_shutdown = [ ]
	"""
Callbacks for "shutdown()"
	"""
	_weakref_instance = None
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
The LogHandler is called whenever debug messages should be logged or errors
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

		Cli._weakref_instance = ref(self)
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

		# pylint: disable=broad-except

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.run()- (#echo(__LINE__)#)", self, context = "pas_core")

		if (self.arg_parser != None and hasattr(self.arg_parser, "parse_args")): args = self.arg_parser.parse_args()
		else: args = { }

		self.arg_parser = None

		try:
		#
			for callback in Cli._callbacks_run: callback(args)
			Cli._callbacks_run = [ ]

			self.mainloop_event.set()
			if (self.mainloop != None): self.mainloop()
		#
		except Exception as handled_exception: self.error(handled_exception)
		finally: self.shutdown()
	#

	def set_mainloop(self, callback):
	#
		"""
Register a callback for the application main loop.

:param callback: Python callback

:since: v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.set_mainloop()- (#echo(__LINE__)#)", self, context = "pas_core")

		if (self.mainloop != None): raise ValueException("Main loop already registered")
		self.mainloop = callback
	#

	def set_log_handler(self, log_handler):
	#
		"""
Sets the LogHandler.

:param log_handler: LogHandler to use

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

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}._signal()- (#echo(__LINE__)#)", self, context = "pas_core")
		self.shutdown()
	#

	def shutdown(self, _exception = None):
	#
		"""
Executes registered callbacks before shutting down this application.

:param _exception: Inner exception

:since: v0.1.00
		"""

		# pylint: disable=raising-bad-type

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.shutdown()- (#echo(__LINE__)#)", self, context = "pas_core")

		Thread.set_inactive()

		"""
Cleanup unused objects
		"""

		for callback in Cli._callbacks_shutdown:
		#
			with ExceptionLogTrap(): callback()
		#

		Cli._callbacks_shutdown = [ ]
		if (_exception != None): raise _exception
	#

	def _wait_for_os_pid(self, pid):
	#
		"""
Waits for the given OS process ID to exit.

:param pid: OS process ID

:since: v1.0.1
		"""

		if (pid != None and pid > 0 and hasattr(os, "kill")):
		#
			for _ in range(0, 60):
			#
				try:
				#
					os.kill(pid, 0)
					sleep(0.5)
				#
				except OSError as handled_exception:
				#
					if (handled_exception.errno not in ( EINVAL, ESRCH )): raise
				#
			#
		#
	#

	@staticmethod
	def get_instance():
	#
		"""
Get the Cli singleton.

:return: (Cli) Object on success
:since:  v0.1.00
		"""

		return Cli._weakref_instance()
	#

	@staticmethod
	def get_py_mode():
	#
		"""
Returns the current Python engine (one of "java", "mono" and "py").

:return: (str) Active mode
:since:  v0.1.00
		"""

		# global: _mode
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

		if (callback not in Cli._callbacks_run): Cli._callbacks_run.append(callback)
	#

	@staticmethod
	def register_shutdown_callback(callback):
	#
		"""
Register a callback for the application shutdown event.

:param callback: Python callback

:since: v0.1.00
		"""

		if (callback not in Cli._callbacks_shutdown): Cli._callbacks_shutdown.append(callback)
	#
#

def _on_signal(os_signal, stack_frame):
#
	"""
Callback function for OS signals.

:param os_signal: OS signal
:param stack_frame: Stack frame

:since: v0.1.00
	"""

	# pylint: disable=protected-access

	instance = Cli.get_instance()
	if (instance != None): instance._signal(os_signal, stack_frame)
#

if (hasattr(signal, "SIGABRT")): signal.signal(signal.SIGABRT, _on_signal)
if (hasattr(signal, "SIGINT")): signal.signal(signal.SIGINT, _on_signal)
if (hasattr(signal, "SIGTERM")): signal.signal(signal.SIGTERM, _on_signal)
if (hasattr(signal, "SIGQUIT")): signal.signal(signal.SIGQUIT, _on_signal)

##j## EOF