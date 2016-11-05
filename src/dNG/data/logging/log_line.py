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

from dNG.module.named_loader import NamedLoader

class LogLine(object):
    """
"LogLine" provides static methods to log a single line to the active log
handler.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    @staticmethod
    def debug(data, *args, **kwargs):
        """
Debug message method

:param data: Debug data
:param context: Logging context

:since: v0.2.00
        """

        # pylint: disable=star-args

        log_handler = NamedLoader.get_singleton("dNG.data.logging.LogHandler", False)
        if (log_handler is not None): log_handler.debug(data, *args, **kwargs)
    #

    @staticmethod
    def error(data, *args, **kwargs):
        """
Error message method

:param data: Error data
:param context: Logging context

:since: v0.2.00
        """

        # pylint: disable=star-args

        log_handler = NamedLoader.get_singleton("dNG.data.logging.LogHandler", False)
        if (log_handler is not None): log_handler.error(data, *args, **kwargs)
    #

    @staticmethod
    def info(data, *args, **kwargs):
        """
Info message method

:param data: Info data
:param context: Logging context

:since: v0.2.00
        """

        # pylint: disable=star-args

        log_handler = NamedLoader.get_singleton("dNG.data.logging.LogHandler", False)
        if (log_handler is not None): log_handler.info(data, *args, **kwargs)
    #

    @staticmethod
    def warning(data, *args, **kwargs):
        """
Warning message method

:param data: Warning data
:param context: Logging context

:since: v0.2.00
        """

        # pylint: disable=star-args

        log_handler = NamedLoader.get_singleton("dNG.data.logging.LogHandler", False)
        if (log_handler is not None): log_handler.warning(data, *args, **kwargs)
    #
#
