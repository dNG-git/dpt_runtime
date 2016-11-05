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

from pyinotify import Notifier

from .watcher_pyinotify import WatcherPyinotify
from .watcher_pyinotify_callback import WatcherPyinotifyCallback

class WatcherPyinotifySync(WatcherPyinotify):
    """
"file:///" watcher using pyinotify's (synchronous) Notifier.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    def check(self, _path):
        """
Checks a given path for changes if "is_synchronous()" is true.

:param _path: Filesystem path

:return: (bool) True if the given path URL has been changed since last check
         and "is_synchronous()" is true.
:since:  v0.2.00
        """

        if (self.pyinotify_instance.check_events()):
            self.pyinotify_instance.read_events()
            self.pyinotify_instance.process_events()
        #

        return False
    #

    def _init_notifier(self):
        """
Initializes the pyinotify instance.

:since: v0.2.00
        """

        self.pyinotify_instance = Notifier(self, WatcherPyinotifyCallback(self), timeout = 5)
    #

    def is_synchronous(self):
        """
Returns true if changes are only detected after "check()" has been
called.

:return: (bool) True if changes are not detected automatically
:since:  v0.2.00
        """

        return True
    #

    def stop(self):
        """
Stops all watchers.

:since: v0.2.00
        """

        if (WatcherPyinotifySync._instance is not None):
            with WatcherPyinotifySync._instance_lock:
                # Thread safety
                if (WatcherPyinotifySync._instance is not None): WatcherPyinotifySync._instance = None
            #
        #

        self.free()
    #

    @staticmethod
    def get_instance():
        """
Get the WatcherPyinotifySync singleton.

:return: (WatcherPyinotifySync) Object on success
:since:  v0.2.00
        """

        if (WatcherPyinotify._instance is None):
            with WatcherPyinotifySync._instance_lock:
                # Thread safety
                if (WatcherPyinotifySync._instance is None): WatcherPyinotifySync._instance = WatcherPyinotifySync()
            #
        #

        return WatcherPyinotifySync._instance
    #
#
