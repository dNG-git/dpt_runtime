# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.logging.log_line
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

from dNG.pas.module.named_loader import direct_named_loader

class direct_log_line(object):
#
	"""
"direct_log_line" provides static methods to log a single line to the active
log handler.

:author:    direct Netware Group
:copyright: direct Netware Group - All rights reserved
:package:   pas.core
:since:     v0.1.00
:license:   http://www.direct-netware.de/redirect.py?licenses;mpl2
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

		log_handler = direct_named_loader.get_singleton("dNG.pas.data.logging.log_handler", False)

		if (log_handler != None):
		#
			log_handler.debug(data)
			log_handler.return_instance()
		#
	#

	@staticmethod
	def error(data):
	#
		"""
Error message method

:param data: Error data

:since: v0.1.00
		"""

		log_handler = direct_named_loader.get_singleton("dNG.pas.data.logging.log_handler", False)

		if (log_handler != None):
		#
			log_handler.error(data)
			log_handler.return_instance()
		#
	#

	@staticmethod
	def info(data):
	#
		"""
Info message method

:param data: Info data

:since: v0.1.00
		"""

		log_handler = direct_named_loader.get_singleton("dNG.pas.data.logging.log_handler", False)

		if (log_handler != None):
		#
			log_handler.info(data)
			log_handler.return_instance()
		#
	#

	@staticmethod
	def warning(data):
	#
		"""
Warning message method

:param data: Warning data

:since: v0.1.00
		"""

		log_handler = direct_named_loader.get_singleton("dNG.pas.data.logging.log_handler", False)

		if (log_handler != None):
		#
			log_handler.warning(data)
			log_handler.return_instance()
		#
	#
#

##j## EOF