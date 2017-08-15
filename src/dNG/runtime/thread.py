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

from threading import Thread as _Thread

from dNG.data.logging.log_line import LogLine

from .exception_log_trap import ExceptionLogTrap

class Thread(_Thread):
    """
"Thread" represents a deactivatable Thread implementation.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v0.2.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    _active = True
    """
True if new non-daemon threads are allowed to be started.
    """

    def run(self):
        """
python.org: Method representing the thread’s activity.

:since: v0.2.0
        """

        with ExceptionLogTrap("pas_core"): _Thread.run(self)
    #

    def start(self):
        """
python.org: Start the thread's activity.

:since: v0.2.0
        """

        if (self.daemon or Thread._active): _Thread.start(self)
        else: LogLine.debug("{0!r} prevented new non-daemon thread", self, context = "pas_core")
    #

    @staticmethod
    def set_inactive():
        """
Prevents new non-daemon threads to be started.

:since: v0.2.0
        """

        Thread._active = False
    #
#
