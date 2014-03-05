# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.module.NamedLoader
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

# pylint: disable=import-error

from os import path
from sys import modules as sys_modules
from weakref import proxy
import re

_MODE_IMP = 1
"""
Use "imp" based methods for import
"""
_MODE_IMPORT_MODULE = 2
"""
Use "import_module" for import
"""

_mode = _MODE_IMP

try:

	from importlib import import_module
	_mode = _MODE_IMPORT_MODULE

except ImportError: import imp

from dNG.pas.data.settings import Settings
from dNG.pas.runtime.io_exception import IOException
from dNG.pas.runtime.thread_lock import ThreadLock
from dNG.pas.runtime.type_exception import TypeException

class NamedLoader(object):
#
	"""
"NamedLoader" provides singletons and objects based on a callable
common name.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	RE_CAMEL_CASE_SPLITTER = re.compile("([a-z0-9]|[A-Z]+(?![A-Z]+$))([A-Z])")
	"""
CamelCase RegExp
	"""

	instance = None
	"""
"NamedLoader" weakref instance
	"""
	lock = ThreadLock()
	"""
Thread safety lock
	"""
	log_handler = None
	"""
The LogHandler is called whenever debug messages should be logged or errors
happened.
	"""

	def __init__(self):
	#
		"""
Constructor __init__(NamedLoader)

:since: v0.1.00
		"""

		self.base_dir = Settings.get("pas_global_modules_base_dir", None)
		"""
Base directory we search for python files.
		"""
		self.config = { }
		"""
Underlying configuration array
		"""
	#

	def get(self, common_name):
	#
		"""
Returns the registered class name for the specified common name.

:param common_name: Common name

:return: (str) Class name
:since:  v0.1.00
		"""

		return (self.config[common_name] if (common_name in self.config) else None)
	#

	def get_base_dir(self):
	#
		"""
Returns the base directory for scanning and loading python files.

:return: (str) Relative path
:since:  v0.1.00
		"""

		if (self.base_dir == None): self.base_dir = Settings.get("path_system")
		return self.base_dir
	#

	def is_registered(self, common_name):
	#
		"""
Checks if a given common name is known.

:param common_name: Common name

:return: (bool) True if defined
:since:  v0.1.00
		"""

		return (common_name in self.config)
	#

	def set_base_dir(self, base_dir):
	#
		"""
Sets the base directory for scanning and loading python files.

:param common_name: Common name

:param base_dir: Path

:since: v0.1.00
		"""

		self.base_dir = base_dir
	#

	@staticmethod
	def get_class(common_name, autoload = True):
	#
		"""
Get the class name for the given common name.

:param common_name: Common name
:param autoload: True to load the class module automatically if not done
                 already.

:return: (object) Loaded class; None on error
:since:  v0.1.00
		"""

		loader = NamedLoader._get_loader()

		if (loader.is_registered(common_name)): ( package, classname ) = loader.get(common_name).rsplit(".", 1)
		else: ( package, classname ) = common_name.rsplit(".", 1)

		module_name = "{0}.{1}".format(package, NamedLoader.RE_CAMEL_CASE_SPLITTER.sub("\\1_\\2", classname).lower())

		if (autoload): module = NamedLoader._load_module(module_name)
		else: module = NamedLoader._get_module(module_name)

		return (None if (module == None) else getattr(module, classname, None))
	#

	@staticmethod
	def get_instance(common_name, required = True, **kwargs):
	#
		"""
Returns a new instance based on its common name.

:param common_name: Common name
:param required: True if errors should throw exceptions
:param autoload: True to load the class automatically if not done already

:return: (object) Requested object on success
:since:  v0.1.00
		"""

		_return = None

		_class = NamedLoader.get_class(common_name)

		if (_class == None): _return = None
		else:
		#
			_return = _class.__new__(_class, **kwargs)
			_return.__init__(**kwargs)
		#

		if (_return == None and required): raise IOException("{0} is not defined".format(common_name))
		return _return
	#

	@staticmethod
	def _get_loader():
	#
		"""
Get the loader instance.

:return: (object) Loader instance
:since:  v0.1.00
		"""

		if (NamedLoader.instance == None):
		#
			# Instance could be created in another thread so check again
			with NamedLoader.lock:
			#
				if (NamedLoader.instance == None): NamedLoader.instance = NamedLoader()
			#
		#

		return NamedLoader.instance
	#

	@staticmethod
	def get_singleton(common_name, required = True, **kwargs):
	#
		"""
Returns a singleton based on its common name.

:param common_name: Common name
:param required: True if errors should throw exceptions

:return: (object) Requested object on success
:since:  v0.1.00
		"""

		_class = NamedLoader.get_class(common_name)

		if (_class == None and required): raise IOException("{0} is not defined".format(common_name))
		if ((not hasattr(_class, "get_instance")) and required): raise TypeException("{0} has not defined a singleton".format(common_name))

		return _class.get_instance(**kwargs)
	#

	@staticmethod
	def is_defined(common_name, autoload = True):
	#
		"""
Checks if a common name is defined or can be resolved to a class name.

:param common_name: Common name
:param autoload: True to load the class module automatically if not done
                 already.

:return: (bool) True if defined or resolvable
:since:  v0.1.00
		"""

		return (False if (NamedLoader.get_class(common_name, autoload) == None) else True)
	#

	@staticmethod
	def _get_module(name):
	#
		"""
Return the inititalized Python module defined by the given name.

:param name: Python module name

:return: (object) Python module; None if unknown
:since:  v0.1.00
		"""

		_return = sys_modules.get(name, None)

		if (_return != None and hasattr(_return, "__initializing__")):
		#
			if (getattr(_return, "__initializing__", True)):
			#
				with NamedLoader.lock: _return = sys_modules.get(name, None)
			#
		#

		return _return
	#

	@staticmethod
	def _load_module(name):
	#
		"""
Load the Python module defined by the given name.

:param name: Python module name

:return: (object) Python module; None if unknown
:since:  v0.1.00
		"""

		package = name.rsplit(".", 1)[0]

		NamedLoader._load_package(package)
		return NamedLoader._load_py_file(name)
	#

	@staticmethod
	def _load_package(name):
	#
		"""
Load the Python package defined by the given name.

:param name: Python module name

:return: (object) Python package; None if unknown
:since:  v0.1.00
		"""

		return NamedLoader._load_py_file(name)
	#

	@staticmethod
	def _load_py_file(name):
	#
		"""
Load the Python file defined by the given name.

:param name: Python file name

:return: (object) Python file; None if unknown
:since:  v0.1.00
		"""

		# global: _mode, _MODE_IMPORT_MODULE
		# pylint: disable=broad-except
		_return = NamedLoader._get_module(name)

		if (_return == None):
		#
			# Module could be imported in another thread so check again
			with NamedLoader.lock:
			#
				_return = sys_modules.get(name, None)

				if (_return == None):
				#
					try:
					#
						if (_mode == _MODE_IMPORT_MODULE): _return = NamedLoader._load_py_file_importlib(name)
						else: _return = NamedLoader._load_py_file_imp(name)
					#
					except Exception as handled_exception:
					#
						if (NamedLoader.log_handler != None): NamedLoader.log_handler.error(handled_exception)
					#
				#
			#
		#

		return _return
	#

	@staticmethod
	def _load_py_file_imp(name):
	#
		"""
Load the Python file with "imp" defined by the given name.

:param name: Python file name

:return: (object) Python file; None if unknown
:since:  v0.1.00
		"""

		# pylint: disable=broad-except

		_return = None

		exception = None
		( package_parent, _file) = name.rsplit(".", 1)
		_path = package_parent.replace(".", path.sep)

		imp.acquire_lock()

		try:
		#
			( file_obj, file_path, description ) = imp.find_module(_file, [ path.normpath("{0}/{1}".format(NamedLoader._get_loader().get_base_dir(), _path)) ])
			_return = imp.load_module(name, file_obj, file_path, description)
			if (file_obj != None): file_obj.close()
		#
		except ImportError: pass
		except Exception as handled_exception: exception = handled_exception

		imp.release_lock()

		if (exception != None):
		#
			_return = None
			if (NamedLoader.log_handler != None): NamedLoader.log_handler.error(exception)
		#

		return _return
	#

	@staticmethod
	def _load_py_file_importlib(name):
	#
		"""
Load the Python package with "importlib" defined by the given name.

:param name: Python module name

:return: (object) Python package; None if unknown
:since:  v0.1.00
		"""

		# pylint: disable=broad-except

		_return = None

		exception = None

		try: _return = import_module(name)
		except ImportError: pass
		except Exception as handled_exception: exception = handled_exception

		if (exception != None and NamedLoader.log_handler != None): NamedLoader.log_handler.error(exception)

		return _return
	#

	@staticmethod
	def set_log_handler(log_handler):
	#
		"""
Sets the LogHandler.

:param log_handler: LogHandler to use

:since: v0.1.00
		"""

		NamedLoader.log_handler = proxy(log_handler)
	#
#

##j## EOF