# -*- coding: utf-8 -*-

"""
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?pas;core

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;mpl2
----------------------------------------------------------------------------
#echo(pasCoreVersion)#
#echo(__FILEPATH__)#
"""

# pylint: disable=import-error

from contextlib import contextmanager
from os import path
from weakref import proxy
import re
import sys

from dNG.data.settings import Settings
from dNG.runtime.io_exception import IOException
from dNG.runtime.thread_lock import ThreadLock
from dNG.runtime.type_exception import TypeException

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

class NamedLoader(object):
    """
"NamedLoader" provides singletons and objects based on a callable
common name.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    RE_CAMEL_CASE_SPLITTER = re.compile("([a-z0-9])([A-Z]+)")
    """
CamelCase RegExp
    """

    _instance = None
    """
"NamedLoader" weakref instance
    """
    _lock = ThreadLock()
    """
Thread safety lock
    """
    _log_handler = None
    """
The LogHandler is called whenever debug messages should be logged or errors
happened.
    """

    def __init__(self):
        """
Constructor __init__(NamedLoader)

:since: v0.2.0
        """

        self._base_dir = Settings.get("pas_global_modules_base_dir")
        """
Base directory we search for python files.
        """
        self.config = { }
        """
Underlying configuration array
        """
    #

    @property
    def base_dir(self):
        """
Returns the base directory for scanning and loading python files.

:return: (str) Relative path
:since:  v1.0.0
        """

        if (self._base_dir is None): self._base_dir = Settings.get("path_system")
        return self._base_dir
    #

    @base_dir.setter
    def base_dir(self, base_dir):
        """
Sets the base directory for scanning and loading python files.

:param base_dir: Path

:since: v1.0.0
        """

        self._base_dir = base_dir
    #

    def get(self, common_name):
        """
Returns the registered class name for the specified common name.

:param common_name: Common name

:return: (str) Class name
:since:  v0.2.0
        """

        return (self.config[common_name] if (common_name in self.config) else None)
    #

    def is_registered(self, common_name):
        """
Checks if a given common name is known.

:param common_name: Common name

:return: (bool) True if defined
:since:  v0.2.0
        """

        return (common_name in self.config)
    #

    @staticmethod
    def get_class(common_name, autoload = True):
        """
Get the class name for the given common name.

:param common_name: Common name
:param autoload: True to load the class module automatically if not done
                 already.

:return: (object) Loaded class; None on error
:since:  v0.2.0
        """

        loader = NamedLoader._get_loader()

        if (loader.is_registered(common_name)): ( package, classname ) = loader.get(common_name).rsplit(".", 1)
        else: ( package, classname ) = common_name.rsplit(".", 1)

        module_name = "{0}.{1}".format(package, NamedLoader.RE_CAMEL_CASE_SPLITTER.sub("\\1_\\2", classname).lower())

        if (autoload): module = NamedLoader._load_module(module_name, classname)
        else: module = NamedLoader._get_module(module_name, classname)

        return (None if (module is None) else getattr(module, classname, None))
    #

    @staticmethod
    def get_instance(common_name, required = True, **kwargs):
        """
Returns a new instance based on its common name.

:param common_name: Common name
:param required: True if exceptions should be thrown if the class is not
                 defined.
:param autoload: True to load the class automatically if not done already

:return: (object) Requested object on success
:since:  v0.2.0
        """

        _return = None

        _class = NamedLoader.get_class(common_name)

        if (_class is None): _return = None
        else:
            _return = _class.__new__(_class, **kwargs)
            _return.__init__(**kwargs)
        #

        if (_return is None and required): raise IOException("{0} is not defined".format(common_name))
        return _return
    #

    @staticmethod
    def _get_loader():
        """
Get the loader instance.

:return: (object) Loader instance
:since:  v0.2.0
        """

        if (NamedLoader._instance is None):
            with NamedLoader._lock:
                # Thread safety
                if (NamedLoader._instance is None): NamedLoader._instance = NamedLoader()
            #
        #

        return NamedLoader._instance
    #

    @staticmethod
    def get_singleton(common_name, required = True, **kwargs):
        """
Returns a singleton based on its common name.

:param common_name: Common name
:param required: True if exceptions should be thrown if the class is not
                 defined.

:return: (object) Requested object on success
:since:  v0.2.0
        """

        _return = None

        _class = NamedLoader.get_class(common_name)

        if (_class is None and required): raise IOException("{0} is not defined".format(common_name))

        if (hasattr(_class, "get_instance")): _return = _class.get_instance(**kwargs)
        elif (required): raise TypeException("{0} has not defined a singleton".format(common_name))

        return _return
    #

    @staticmethod
    def is_defined(common_name, autoload = True):
        """
Checks if a common name is defined or can be resolved to a class name.

:param common_name: Common name
:param autoload: True to load the class module automatically if not done
                 already.

:return: (bool) True if defined or resolvable
:since:  v0.2.0
        """

        return (NamedLoader.get_class(common_name, autoload) is not None)
    #

    @staticmethod
    def _get_module(name, classname = None):
        """
Returns the inititalized Python module defined by the given name.

:param name: Python module name
:param classname: Class name to load in this module used to verify that it
                  is initialized.

:return: (object) Python module; None if unknown
:since:  v0.2.0
        """

        _return = sys.modules.get(name)

        if (_return is not None and classname is not None and (not hasattr(_return, classname))):
            with NamedLoader._lock: _return = sys.modules.get(name)
        #

        return _return
    #

    @staticmethod
    def _load_module(name, classname = None):
        """
Load the Python module defined by the given name.

:param name: Python module name
:param classname: Class name to load in this module used to verify that it
                  is initialized.

:return: (object) Python module; None if unknown
:since:  v0.2.0
        """

        _return = NamedLoader._get_module(name, classname)

        if (_return is None):
            package = name.rsplit(".", 1)[0]

            NamedLoader._load_package(package)
            _return = NamedLoader._load_py_file(name, classname)
        #

        return _return
    #

    @staticmethod
    def _load_package(name):
        """
Load the Python package defined by the given name.

:param name: Python module name

:return: (object) Python package; None if unknown
:since:  v0.2.0
        """

        return NamedLoader._load_py_file(name)
    #

    @staticmethod
    def _load_py_file(name, classname = None):
        """
Load the Python file defined by the given name.

:param name: Python file name
:param classname: Class name to load in this module used to verify that it
                  is initialized.

:return: (object) Python file; None if unknown
:since:  v0.2.0
        """

        # global: _mode, _MODE_IMPORT_MODULE
        # pylint: disable=broad-except

        _return = NamedLoader._get_module(name, classname)

        if (_return is None):
            with NamedLoader._lock:
                # Thread safety
                _return = sys.modules.get(name)

                if (_return is None):
                    try:
                        if (_mode == _MODE_IMPORT_MODULE): _return = NamedLoader._load_py_file_importlib(name)
                        else: _return = NamedLoader._load_py_file_imp(name)
                    except Exception as handled_exception:
                        if (NamedLoader._log_handler is not None): NamedLoader._log_handler.error(handled_exception, context = "pas_core")
                    #
                #
            #
        #

        return _return
    #

    @staticmethod
    def _load_py_file_imp(name):
        """
Load the Python file with "imp" defined by the given name.

:param name: Python file name

:return: (object) Python file; None if unknown
:since:  v0.2.0
        """

        _return = None

        ( package_parent, _file) = name.rsplit(".", 1)
        _path = package_parent.replace(".", path.sep)

        with _load_py_file_imp_lock():
            try:
                ( file_obj, file_path, description ) = imp.find_module(_file, [ path.join(NamedLoader._get_loader().base_dir, _path) ])
                _return = imp.load_module(name, file_obj, file_path, description)
                if (file_obj is not None): file_obj.close()
            except ImportError as handled_exception:
                if (NamedLoader._log_handler is not None): NamedLoader._log_handler.debug(handled_exception, context = "pas_core")
            #
        #

        return _return
    #

    @staticmethod
    def _load_py_file_importlib(name):
        """
Load the Python package with "importlib" defined by the given name.

:param name: Python module name

:return: (object) Python package; None if unknown
:since:  v0.2.0
        """

        _return = None

        try: _return = import_module(name)
        except ImportError as handled_exception:
            if (NamedLoader._log_handler is not None): NamedLoader._log_handler.debug(handled_exception, context = "pas_core")
        #

        return _return
    #

    @staticmethod
    def set_log_handler(log_handler):
        """
Sets the LogHandler.

:param log_handler: LogHandler to use

:since: v0.2.0
        """

        NamedLoader._log_handler = proxy(log_handler)
    #
#

@contextmanager
def _load_py_file_imp_lock():
    """
Helper method to lock and unlock the importer safely.

:since: v0.2.0
    """

    imp.acquire_lock()
    yield
    imp.release_lock()
#
