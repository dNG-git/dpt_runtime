# -*- coding: utf-8 -*-

"""
direct Python Toolbox
All-in-one toolbox to encapsulate Python runtime variants
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?dpt;runtime

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;mpl2
----------------------------------------------------------------------------
#echo(dptRuntimeVersion)#
#echo(__FILEPATH__)#
"""

from .traced_exception_mixin import TracedExceptionMixin

class TypeException(TypeError, TracedExceptionMixin):
    """
This exception is replacing "TypeError" and provides the current stack
trace.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    dpt
:subpackage: runtime
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    def __init__(self, value, _exception = None):
        """
Constructor __init__(TypeException)

:param value: Exception message value
:param _exception: Inner exception

:since: v1.0.0
        """

        super(TypeException, self).__init__(value)
        TracedExceptionMixin.__init__(self, _exception)
    #

    __str__ = TracedExceptionMixin.__str__
    """
python.org: Called by the str(object) and the built-in functions format()
and print() to compute the "informal" or nicely printable string
representation of an object.

:return: (str) The "informal" or nicely printable string representation
:since:  v1.0.0
    """

    with_traceback = TracedExceptionMixin.with_traceback
    """
python.org: This method sets tb as the new traceback for the exception and
returns the exception object.

:param tb: New traceback for the exception

:return: (object) Manipulated exception instance
:since:  v1.0.0
    """
#
