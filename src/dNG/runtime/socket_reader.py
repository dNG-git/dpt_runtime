# -*- coding: utf-8 -*-
##j## BOF

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

from select import select
from time import time

from dNG.data.settings import Settings

from .io_exception import IOException

class SocketReader(object):
#
	"""
"SocketReader" provides a "recv()" method implementing time limited read
operations from blocking and non-blocking sockets.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self, socket, timeout = None):
	#
		"""
Constructor __init__(ThreadLock)

:since: v0.2.00
		"""

		self.socket = socket
		"""
Underlying lock instance
		"""
		self.timeout = timeout
		"""
Lock timeout in seconds
		"""

		if (self.timeout is None or self.timeout <= 0):
		#
			self.timeout = int(Settings.get("pas_global_socket_data_timeout", 30))
		#
	#

	def recv(self, size):
	#
		"""
Read data from socket.

:param size: Size to receive

:return: (bytes) Socket data received
:since: v0.2.00
		"""

		_return = None

		data_size = 0
		timeout_time = time() + self.timeout

		while (data_size < size and time() < timeout_time):
		#
			if (len(select([ self.socket.fileno() ], [ ], [ ], self.timeout)[0]) < 1): raise IOException("Timeout occurred before receiving data")
			data = self.socket.recv(size - data_size)

			if (_return is None): _return = data
			else: _return += data

			data_size += len(data)
		#

		return _return
	#
#

##j## EOF