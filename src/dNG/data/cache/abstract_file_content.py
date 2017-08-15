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

from dNG.runtime.not_implemented_exception import NotImplementedException

class AbstractFileContent(object):
    """
The abstract file cache defines methods to access cached data.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v0.2.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    # pylint: disable=unused-argument

    def get_file(self, file_path_name):
        """
Get the content from cache for the given file path and name.

:param file_path_name: Cached file path and name

:return: (mixed) Cached entry; None if no hit or changed
:since:  v0.2.0
        """

        raise NotImplementedException()
    #

    def is_file_known(self, file_path_name):
        """
Return true if the given file path and name is cached.

:param file_path_name: Cached file path and name

:return: (bool) True if currently cached
:since:  v0.2.0
        """

        raise NotImplementedException()
    #

    def set_file(self, file_path_name, cache_entry):
        """
Fill the cache for the given file path and name with the given cache entry.

:param file_path_name: File path and name
:param cache_entry: Cached entry data

:since: v0.2.0
        """

        raise NotImplementedException()
    #
#
