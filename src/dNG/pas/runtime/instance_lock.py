# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.runtime.InstanceLock
"""
"""n// NOTE
----------------------------------------------------------------------------
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
http://www.direct-netware.de/redirect.py?pas;core

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
http://www.direct-netware.de/redirect.py?licenses;mpl2
----------------------------------------------------------------------------
#echo(pasCoreVersion)#
#echo(__FILEPATH__)#
----------------------------------------------------------------------------
NOTE_END //n"""

from dNG.pas.data.settings import Settings
from .thread_lock import ThreadLock

class InstanceLock(ThreadLock):
#
	"""
"InstanceLock" is used to protect manipulation of a singleton.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v0.1.01
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self, timeout = None):
	#
		"""
Constructor __init__(InstanceLock)

:since: v0.1.01
		"""

		ThreadLock.__init__(self)

		self.timeout = (Settings.get("pas_global_singleton_lock_timeout", 3) if (timeout == None) else timeout)
	#
#

##j## EOF