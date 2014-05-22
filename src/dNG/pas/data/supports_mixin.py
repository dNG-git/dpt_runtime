# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.SupportsMixin
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

class SupportsMixin(object):
#
	"""
This mixin allows asking if a specific feature is supported by the current
instance.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self):
	#
		"""
Constructor __init__(SupportsMixin)

:since: v0.1.00
		"""

		self.supported_features = { }
		"""
Dictionary of supported features of this instance. The value is either a
boolean or a callback.
		"""
	#

	def is_supported(self, feature):
	#
		"""
Returns true if the feature requested is supported by this instance.

:param feature: Feature name string

:return: (bool) True if supported
:since:  v0.1.01
		"""

		_return = False

		if (feature in self.supported_features):
		#
			_return = (self.supported_features[feature]
			           if (type(self.supported_features[feature]) == bool) else
			           self.supported_features[feature]()
			          )
		#

		return _return
	#
#

##j## EOF