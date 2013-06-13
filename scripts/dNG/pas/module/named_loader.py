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

from os import path
from threading import RLock
import re

_mode = "base"

try:

	import importlib
	_mode = "lib"

except ImportError: import imp

from dNG.pas.data.settings import Settings

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
"NamedLoader" instance
	"""
	log_handler = None
	"""
The log_handler is called whenever debug messages should be logged or errors
happened.
	"""
	module_list = [ ]
	"""
List of modules loaded
	"""
	synchronized = RLock()
	"""
Lock used in multi thread environments.
	"""

	def __init__(self):
	#
		"""
Constructor __init__(NamedLoader)

:since: v0.1.00
		"""

		self.base_dir = None
		"""
Base directory we search for python files.
		"""
		self.config = { }
		"""
Underlying configuration array
		"""

		if (Settings.is_defined("pas_modules")): self.import_module_config(Settings.get("pas_modules"))
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
	def get_class(common_name):
	#
		"""
Get the class name for the given common name.

:param common_name: Common name
:param classprefix: A classname prefix

:access: protected
:return: (object) Loaded class
:since:  v0.1.00
		"""

		var_return = None

		loader = NamedLoader.get_loader()

		if (loader.is_registered(common_name)): ( package, classname ) = loader.get(common_name).rsplit(".", 1)
		else: ( package, classname ) = common_name.rsplit(".", 1)

		module_name = NamedLoader.RE_CAMEL_CASE_SPLITTER.sub("\\1_\\2", classname).lower()
		module = NamedLoader.load_module("{0}.{1}".format(package, module_name))

		if (hasattr(module, classname)): var_return = getattr(module, classname)
		return var_return
	#

	@staticmethod
	def get_instance(common_name, required = True):
	#
		"""
Returns a new instance based on its common name.

:param common_name: Common name
:param required: True if errors should throw exceptions

:return: (object) Requested object on success
:since:  v0.1.00
		"""

		var_return = None

		var_class = NamedLoader.get_class(common_name)

		if (var_class != None):
		#
			var_return = var_class.__new__(var_class)
			var_return.__init__()
		#
		elif (required): raise RuntimeError("{0} is not defined".format(common_name), 38)

		return var_return
	#

	@staticmethod
	def get_loader():
	#
		"""
Get the loader instance.

:access: protected
:return: (object) Loader instance
:since:  v0.1.00
		"""

		with NamedLoader.synchronized:
		#
			if (NamedLoader.instance == None): NamedLoader.instance = NamedLoader()
		#

		return NamedLoader.instance
	#

	@staticmethod
	def get_singleton(common_name, required = True):
	#
		"""
Returns a singleton based on its common name.

:param common_name: Common name
:param required: True if errors should throw exceptions

:return: (object) Requested object on success
:since:  v0.1.00
		"""

		var_return = None

		var_class = NamedLoader.get_class(common_name)

		if (var_class != None):
		#
			if (hasattr(var_class, "get_instance")): var_return = var_class.get_instance()
			elif (required): raise RuntimeError("{0} has not defined a singleton".format(common_name), 38)
		#
		elif (required): raise RuntimeError("{0} is not defined".format(common_name), 38)

		return var_return
	#

	@staticmethod
	def is_defined(common_name):
	#
		"""
Checks if a common name is defined or can be resolved to a class name.

:param common_name: Common name

:return: (bool) True if defined or resolvable
:since:  v0.1.00
		"""

		return (False if (NamedLoader.get_class(common_name) == None) else True)
	#

	@staticmethod
	def load_module(module):
	#
		"""
Get the class name for the given common name.

:param common_name: Common name
:param classprefix: A classname prefix

:access: protected
:return: (str) Class name
:since:  v0.1.00
		"""

		var_return = None

		package = module.rsplit(".", 1)[0]

		try:
		#
			if (package not in NamedLoader.module_list): NamedLoader.load_package(package)
			var_return = NamedLoader.load_py_file(module)
			if (var_return != None): NamedLoader.module_list.append(module)
		#
		except Exception as handled_exception:
		#
			if (NamedLoader.log_handler != None): NamedLoader.log_handler.error(handled_exception)
		#

		return var_return
	#

	@staticmethod
	def load_package(package):
	#
		"""
Get the class name for the given common name.

:param common_name: Common name
:param classprefix: A classname prefix

:access: protected
:return: (str) Class name
:since:  v0.1.00
		"""

		var_return = None

		try:
		#
			var_return = NamedLoader.load_py_file(package)
			if (var_return != None): NamedLoader.module_list.append(package)
		#
		except Exception as handled_exception:
		#
			if (NamedLoader.log_handler != None): NamedLoader.log_handler.error(handled_exception)
		#

		return var_return
	#

	@staticmethod
	def load_py_file(py_name):
	#
		"""
Get the class name for the given common name.

:param common_name: Common name
:param classprefix: A classname prefix

:access: protected
:return: (str) Class name
:since:  v0.1.00
		"""

		global _mode

		if (_mode == "lib"): return NamedLoader.load_py_file_lib(py_name)
		else: return NamedLoader.load_py_file_base(py_name)
	#

	@staticmethod
	def load_py_file_base(py_name):
	#
		"""
Get the class name for the given common name.

:param common_name: Common name
:param classprefix: A classname prefix

:access: protected
:return: (str) Class name
:since:  v0.1.00
		"""

		var_return = None

		exception = None
		( py_package_parent, py_file) = py_name.rsplit(".", 1)
		py_path = py_package_parent.replace(".", path.sep)

		imp.acquire_lock()

		try:
		#
			( file_obj, file_path, py_description ) = imp.find_module(py_file, [ path.normpath("{0}/{1}".format(NamedLoader.get_loader().get_base_dir(), py_path)) ])
			var_return = imp.load_module(py_name, file_obj, file_path, py_description)
			if (file_obj != None): file_obj.close()
		#
		except Exception as handled_exception: exception = handled_exception

		imp.release_lock()

		if (exception != None):
		#
			var_return = None
			if (NamedLoader.log_handler != None): NamedLoader.log_handler.error(exception)
		#

		return var_return
	#

	@staticmethod
	def load_py_file_lib(py_name):
	#
		"""
Get the class name for the given common name.

:param common_name: Common name
:param classprefix: A classname prefix

:access: protected
:return: (str) Class name
:since:  v0.1.00
		"""

		var_return = None

		exception = None

		try: var_return = importlib.import_module(py_name)
		except Exception as handled_exception: exception = handled_exception

		if (exception != None and NamedLoader.log_handler != None): NamedLoader.log_handler.error(exception)

		return var_return
	#

	@staticmethod
	def set_log_handler(log_handler):
	#
		"""
Sets the log_handler.

:param log_handler: log_handler to use

:since: v0.1.00
		"""

		NamedLoader.log_handler = log_handler
	#
#

##j## EOF