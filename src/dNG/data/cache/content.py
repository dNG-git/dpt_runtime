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

from copy import copy
from weakref import ref

from dNG.data.settings import Settings
from dNG.vfs.file.watcher import Watcher

from .abstract_file_content import AbstractFileContent
#from .abstract_value import AbstractValue

class Content(Watcher, AbstractFileContent):
    """
The cache singleton for content provides memory-based caching mechanisms for
files as well as timestamp based content.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    # pylint: disable=unused-argument

    _weakref_instance = None
    """
Cache weakref instance
    """

    def __init__(self):
        """
Constructor __init__(Content)

:since: v0.2.00
        """

        Watcher.__init__(self)
        AbstractFileContent.__init__(self)
        #AbstractValue.__init__(self)

        self.cache = { }
        """
Dictionary of cached entries
        """
        self.history = [ ]
        """
Holds a history of requests and updates (newest first)
        """
        self.max_size = int(Settings.get("pas_core_cache_memory_max_size", 104857600))
        """
Max size of the cache
        """
        self.size = 0
        """
Size in bytes
        """
    #

    def get_file(self, file_path_name):
        """
Get the content from cache for the given file path and name.

:param file_path_name: Cached file path and name

:return: (mixed) Cached entry; None if no hit or changed
:since:  v0.2.00
        """

        _return = None

        if (self.is_synchronous): self.check("file:///{0}".format(file_path_name))

        if (file_path_name in self.cache):
            with self._lock:
                # Thread safety
                if (file_path_name in self.cache):
                    _return = self.cache[file_path_name]['entry']
                    self.history.remove(file_path_name)
                    self.history.insert(0, file_path_name)
                #
            #

            if (_return is not None and hasattr(_return, "copy")): _return = _return.copy()
        #

        return _return
    #

    def is_file_known(self, file_path_name):
        """
Return true if the given file path and name is cached.

:param file_path_name: Cached file path and name

:return: (bool) True if currently cached
:since:  v0.2.00
        """

        return (file_path_name in self.cache)
    #

    def set_file(self, file_path_name, cache_entry, cache_entry_size = None):
        """
Fill the cache for the given file path and name with the given cache entry.

:param file_path_name: File path and name
:param cache_entry: Cached entry data
:param cache_entry_size: Size of the cached entry data

:since: v0.2.00
        """

        if (cache_entry_size is None): cache_entry_size = len(cache_entry)

        with self._lock:
            if (file_path_name not in self.cache):
                is_valid = self.register("file:///{0}".format(file_path_name), self._uncache_changed)

                if (is_valid):
                    self.cache[file_path_name] = { "entry": cache_entry, "size": cache_entry_size }
                    self.history.insert(0, file_path_name)
                    self.size += cache_entry_size

                    if (self.size > self.max_size):
                        key = self.history.pop()

                        self.size -= len(self.cache[key]['size'])
                        del(self.cache[key])
                    #
                #
            elif (self.cache[file_path_name]['entry'] != cache_entry):
                self.size -= self.cache[file_path_name]['size']
                self.history.remove(file_path_name)

                self.cache[file_path_name] = { "entry": cache_entry, "size": cache_entry_size }
                self.history.insert(0, file_path_name)
                self.size += cache_entry_size
            #
        #
    #

    def _uncache_changed(self, event_type, url, changed_value = None):
        """
Remove changed files from the cache.

:param event_type: Filesystem watcher event type
:param url: Filesystem URL watched
:param changed_value: Changed filesystem value

:since: v0.2.00
        """

        file_path_name = url[8:]

        if (file_path_name in self.cache):
            with self._lock:
                # Thread safety
                if (file_path_name in self.cache):
                    self.size -= self.cache[file_path_name]['size']
                    self.history.remove(file_path_name)
                    del(self.cache[file_path_name])

                    self.unregister(url, self._uncache_changed)
                #
            #
        #
    #

    @staticmethod
    def get_instance():
        """
Get the Content singleton.

:return: (Content) Object on success
:since:  v0.2.00
        """

        _return = (None if (Content._weakref_instance is None) else Content._weakref_instance())

        if (_return is None):
            _return = Content()
            Content._weakref_instance = ref(_return)
        #

        return _return
    #
#
