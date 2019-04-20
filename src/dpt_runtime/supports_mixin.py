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

class SupportsMixin(object):
    """
This mixin allows asking if a specific feature is supported by the current
instance.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    dpt
:subpackage: runtime
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    def __init__(self):
        """
Constructor __init__(SupportsMixin)

:since: v1.0.0
        """

        self.supported_features = { }
        """
Dictionary of supported features of this instance. The value is either a
boolean or a callback.
        """
    #

    def is_supported(self, feature):
        """
Returns true if the feature requested is supported by this instance.

:param feature: Feature name string

:return: (bool) True if supported
:since:  v1.0.0
        """

        _return = False

        if (feature in self.supported_features):
            _return = (self.supported_features[feature]
                       if (type(self.supported_features[feature]) is bool) else
                       self.supported_features[feature]()
                      )
        #

        return _return
    #
#
