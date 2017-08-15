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

from threading import Event as _Event

from dNG.data.settings import Settings

class Event(object):
    """
python.org  An event manages a flag that can be set to true with the set()
method and reset to false with the clear() method.

This implementation falls back to a default timeout value if "wait()" is
called without specifing one.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v0.2.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    def __init__(self, *args, **kwargs):
        """
Constructor __init__(ResultEvent)

:since: v0.2.0
        """

        self._event = _Event(*args, **kwargs)
        """
Encapsulated event implementation
        """
        self.timeout = Settings.get("pas_global_event_timeout", 10)
        """
Event waiting timeout in seconds
        """
    #

    def clear(self):
        """
python.org: Reset the internal flag to false.

:since: v0.2.0
        """

        self._event.clear()
    #

    def is_set(self):
        """
python.org: Return true if and only if the internal flag is true.

:return: (bool) True if set
:since:  v0.2.0
        """

        return self._event.is_set()
    #

    def set(self):
        """
python.org: Set the internal flag to true.

:since: v0.2.0
        """

        self._event.set()
    #

    def wait(self, timeout = None):
        """
python.org: Block until the internal flag is true.

:param timeout: Timeout value in seconds. If zero or below the call blocks
                indefinitely.

:return: (bool) This method returns true if and only if the internal flag
         has been set to true, either before the wait call or after the wait
         starts, so it will always return True except if a timeout is given
         and the operation times out
:since:  v0.2.0
        """

        if (timeout is None): timeout = self.timeout
        elif (timeout <= 0): timeout = None

        return self._event.wait(timeout)
    #
#
