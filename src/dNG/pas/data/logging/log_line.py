# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.logging.LogLine
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

from dNG.pas.module.named_loader import NamedLoader

class LogLine(object):
#
	"""
"LogLine" provides static methods to log a single line to the active log
handler.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	@staticmethod
	def debug(data):
	#
		"""
Debug message method

:param data: Debug data

:since: v0.1.00
		"""

		log_handler = NamedLoader.get_singleton("dNG.pas.data.logging.LogHandler", False)
		if (log_handler != None): log_handler.debug(data)
	#

	@staticmethod
	def error(data):
	#
		"""
Error message method

:param data: Error data

:since: v0.1.00
		"""

		log_handler = NamedLoader.get_singleton("dNG.pas.data.logging.LogHandler", False)
		if (log_handler != None): log_handler.error(data)
	#

	@staticmethod
	def info(data):
	#
		"""
Info message method

:param data: Info data

:since: v0.1.00
		"""

		log_handler = NamedLoader.get_singleton("dNG.pas.data.logging.LogHandler", False)
		if (log_handler != None): log_handler.info(data)
	#

	@staticmethod
	def warning(data):
	#
		"""
Warning message method

:param data: Warning data

:since: v0.1.00
		"""

		log_handler = NamedLoader.get_singleton("dNG.pas.data.logging.LogHandler", False)
		if (log_handler != None): log_handler.warning(data)
	#
#

##j## EOF