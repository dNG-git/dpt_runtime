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

from os import path

from dNG.data.file import File
from dNG.data.logging.log_line import LogLine
from dNG.module.named_loader import NamedLoader
from dNG.runtime.io_exception import IOException

class FileContent(object):
    """
"FileContent" provides generic access to files on disk or cached.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    @staticmethod
    def is_changed(file_path_name):
        """
Returns false if the file is cached and not modified.

:param file_path_name: File path and name

:return: (bool) True if not cached or modified
:since:  v0.2.00
        """

        _return = False

        cache_instance = NamedLoader.get_singleton("dNG.data.cache.Content", False)
        file_path_name = path.normpath(file_path_name)

        if (cache_instance is None): _return = True
        else:
            file_content = cache_instance.get_file(file_path_name)
            if (file_content is None): _return = True
        #

        return _return
    #

    @staticmethod
    def read(file_path_name, required = False):
        """
Read data from the given file or from cache.

:param file_path_name: File path and name
:param required: True if missing files should throw an exception

:return: (mixed) File data; None on error
:since:  v0.2.00
        """

        _return = FileContent._read_cache(file_path_name, required)

        if (_return is None):
            _return = FileContent._read_file(file_path_name, required)

            if (_return is not None):
                cache_instance = NamedLoader.get_singleton("dNG.data.cache.Content", False)
                if (cache_instance is not None): cache_instance.set_file(file_path_name, _return)
            #
        #

        return _return
    #

    @staticmethod
    def _read_cache(file_path_name, required):
        """
Read data from cache.

:param file_path_name: File path and name
:param required: True if missing files should throw an exception

:return: (mixed) File data; None on error
:since:  v0.2.00
        """

        cache_instance = NamedLoader.get_singleton("dNG.data.cache.Content", False)
        return (None if (cache_instance is None) else cache_instance.get_file(file_path_name))
    #

    @staticmethod
    def _read_file(file_path_name, required):
        """
Read data from the given file or from cache.

:param file_path_name: File path and name
:param required: True if missing files should throw an exception

:return: (mixed) File data; None on error
:since:  v0.2.00
        """

        _return = None

        file_object = File()

        if (file_object.open(file_path_name, True, "r")):
            _return = file_object.read()
            file_object.close()

            if (_return is not None): _return = _return.replace("\r", "")
        elif (required): raise IOException("{0} not found".format(file_path_name))
        else: LogLine.debug("{0} not found", file_path_name, context = "pas_core")

        return _return
    #

    @staticmethod
    def _set_cache(file_path_name, cache_entry, cache_entry_size = None):
        """
Fill the cache for the given file path and name with the given cache entry.

:param file_path_name: File path and name
:param cache_entry: Cached entry data
:param cache_entry_size: Size of the cached entry data

:since: v0.2.00
        """

        cache_instance = NamedLoader.get_singleton("dNG.data.cache.Content", False)
        if (cache_instance is not None): cache_instance.set_file(file_path_name, cache_entry, cache_entry_size)
    #
#
