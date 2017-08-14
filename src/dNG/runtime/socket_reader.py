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

from select import select
from time import time

from dNG.data.settings import Settings

from .io_exception import IOException

class SocketReader(object):
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
        """
Constructor __init__(SocketReader)

:since: v0.2.00
        """

        self.socket = socket
        """
Underlying lock instance
        """
        self._timeout = timeout
        """
Lock timeout in seconds
        """

        if (self._timeout is None or self._timeout <= 0):
            self._timeout = int(Settings.get("pas_global_socket_data_timeout", 30))
        #
    #

    @property
    def timeout(self):
        """
Returns the lock timeout in seconds.

:return: (float) Timeout value
:since:  v1.0.0
        """

        return self._timeout
    #

    @timeout.setter
    def timeout(self, timeout):
        """
Sets a new lock timeout.

:param timeout: New timeout value in seconds

:since: v1.0.0
        """

        self._timeout = timeout
    #

    def recv(self, size):
        """
Read data from socket.

:param size: Size to receive

:return: (bytes) Socket data received; Socket reached EOF (closed) if
         len(returned) < size
:since: v0.2.00
        """

        _return = None

        data_size = 0
        is_socket_valid = True
        timeout_time = time() + self.timeout

        while (is_socket_valid and data_size < size and time() < timeout_time):
            socket_fd = self.socket.fileno()

            if (socket_fd < 0): raise IOException("Connection reset by peer")
            if (len(select([ socket_fd ], [ ], [ ], self.timeout)[0]) < 1): raise IOException("Timeout occurred before receiving data")

            data = self.socket.recv(size - data_size)
            data_size_received = len(data)

            if (_return is None): _return = data
            elif (data_size_received > 0): _return += data

            data_size += data_size_received
            if (data_size_received == 0): is_socket_valid = False
        #

        return _return
    #
#
