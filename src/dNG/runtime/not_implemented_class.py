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

# pylint: disable=invalid-name

from .not_implemented_exception import NotImplementedException

class _NotImplementedMetaClass(type):
    """
The "_NotImplementedMetaClass" is used as a Python 2 and Python 3 compatible
metaclass to raise "dNG.runtime.NotImplementedException" for class methods.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    def __getattr__(self, name):
        """
python.org: Called when an attribute lookup has not found the attribute in
the usual places (i.e. it is not an instance attribute nor is it found in the
class tree for self).

:param name: Attribute name

:return: (mixed) Instance attribute
:since:  v1.0.0
        """

        raise NotImplementedException()
    #
#

class _NotImplementedClass(object):
    """
The "_NotImplementedClass" is used in connection with the
"_NotImplementedMetaClass" to raise "dNG.runtime.NotImplementedException"
for all class and instance method calls.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    def __getattr__(self, name):
        """
python.org: Called when an attribute lookup has not found the attribute in
the usual places (i.e. it is not an instance attribute nor is it found in the
class tree for self).

:param name: Attribute name

:return: (mixed) Instance attribute
:since:  v1.0.0
        """

        raise NotImplementedException()
    #
#

NotImplementedClass = _NotImplementedMetaClass(_NotImplementedClass.__name__[1:], ( _NotImplementedClass, ), { })
"""
The "NotImplementedClass" is used for features not available or implemented
on a specific installation.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v0.2.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
"""
