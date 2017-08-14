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

# pylint: disable=import-error, no-name-in-module

from dNG.data.json_resource import JsonResource
from dNG.data.logging.log_line import LogLine
from dNG.runtime.value_exception import ValueException

from .file_content import FileContent

class JsonFileContent(FileContent):
    """
"JsonFileContent" provides access to JSON files on disk or cached.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

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

        if (not isinstance(_return, dict)):
            file_content = FileContent._read_file(file_path_name, required)

            if (file_content is not None):
                _return = JsonResource.json_to_data(file_content)

                if (_return is None):
                    if (required): raise ValueException("{0} is not a valid JSON encoded file".format(file_path_name))
                    LogLine.warning("{0} is not a valid JSON encoded file", file_path_name, context = "pas_core")
                else: FileContent._set_cache(file_path_name, _return.copy(), len(file_content))
            #
        #

        return _return
    #
#
