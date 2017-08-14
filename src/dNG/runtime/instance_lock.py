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

from dNG.data.settings import Settings

from .thread_lock import ThreadLock

class InstanceLock(ThreadLock):
    """
"InstanceLock" is used to protect manipulation of a singleton.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    def __init__(self, timeout = None):
        """
Constructor __init__(InstanceLock)

:since: v0.2.00
        """

        ThreadLock.__init__(self)

        self._timeout = (Settings.get("pas_global_singleton_lock_timeout", 3) if (timeout is None) else timeout)
    #
#
