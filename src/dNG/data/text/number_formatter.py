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

class NumberFormatter(object):
#
	"""
"NumberFormatter" provides a static method to format numbers.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	@staticmethod
	def format(number, _format, fractional_digits = -1):
	#
		"""
Returns a formatted number.

:param number: Number as int or float
:param _format: Format to apply
:param fractional_digits: Fractional digits to return

:return: (str) Formatted value
:since:  v0.2.00
		"""

		_return = ""

		normalized_number = (str(round(number))
		                     if (fractional_digits < 0) else
		                     "{0:.{1:d}f}".format(number, fractional_digits)
		                    )

		digits = normalized_number.split(".")

		if (len(digits) == 2): digit_position = -1
		else:
		#
			_format = _format[:-2]
			digit_position = 0
		#

		digits_length = len(digits[0])

		for format_char in _format[::-1]:
		#
			if (digit_position == -1):
			#
				digit_position += 1
				if (len(digits) == 2): _return = digits[1]
			#
			elif (format_char == "#"):
			#
				digit_position += 1
				_return = digits[0][-1 * digit_position] + _return
			#
			else: _return = format_char + _return

			if (digits_length == digit_position): break
		#

		if (digits_length > digit_position): _return = digits[0][:-1 * digit_position] + _return

		return _return
	#
#

##j## EOF