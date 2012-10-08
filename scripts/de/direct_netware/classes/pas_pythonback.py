# -*- coding: utf-8 -*-
##j## BOF

"""
de.direct_netware.classes.pas_pythonback
"""
"""n// NOTE
----------------------------------------------------------------------------
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
http://www.direct-netware.de/redirect.php?pas

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
http://www.direct-netware.de/redirect.php?licenses;mpl2
----------------------------------------------------------------------------
#echo(pasCoreVersion)#
pas/#echo(__FILEPATH__)#
----------------------------------------------------------------------------
NOTE_END //n"""

try: unicode_settings = { "type": unicode,"str": unicode.encode,"unicode": str.decode }
except: unicode_settings = { "type": bytes,"str": bytes.decode,"unicode": str.encode }

def direct_str (data):
#
	"""
Returns the string representing the (maybe encoded) input data

:param data: Input string

:return: (str) String representation
:since:  v0.1.00
	"""

	global unicode_settings
	if (type (data) == unicode_settings['type']): data = unicode_settings['str'] (data,"utf-8")
	return data
#

def direct_bytes (data):
#
	"""
Returns the bytes representing the (maybe encoded) input data

:param data: Input string

:return: (bytes) Byte representation
:since:  v0.1.00
	"""

	global unicode_settings

	try:
	#
		if (bytes == unicode_settings['type']): data = direct_unicode (data)
		else: data = direct_str (data)
	#
	except: data = direct_str (data)

	return data
#

def direct_unicode (data):
#
	"""
Returns the unicode data representing the (maybe encoded) input data

:param data: Input string

:return: (bytes) Unicode representation
:since:  v0.1.00
	"""

	global unicode_settings
	if (type (data) == str): data = unicode_settings['unicode'] (data,"utf-8")
	return data
#

##j## EOF