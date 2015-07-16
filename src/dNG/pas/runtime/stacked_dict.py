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

class StackedDict(dict):
#
	"""
A stacked dictionary consists of a regular Python dict and stacked
additional ones used for key lookups.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v0.1.03
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self, *args, **kwargs):
	#
		"""
Constructor __init__(StackedDict)

:since: v0.1.03
		"""

		dict.__init__(self, *args, **kwargs)

		self.stacked_dicts = [ ]
		"""
Stacked additional dicts to be looked in.
		"""
	#

	def __contains__(self, item):
	#
		"""
python.org: Called to implement membership test operators.

:param item: Item to be looked up

:return: (bool) True if item is in self or a stacked dict.
:since:  v0.1.03
		"""

		_return = dict.__contains__(self, key)

		if (not _return):
		#
			for _dict in self.stacked_dicts:
			#
				if (key in _dict):
				#
					_return = True
					break
				#
			#
		#

		return _return
	#

	def __iter__(self):
	#
		"""
python.org: Return an iterator object.

:return: (object) Iterator object
:since:  v0.1.03
		"""

		for key in dict.__iter__(self): yield key

		for _dict in self.stacked_dicts:
		#
			for key in _dict: yield key
		#
	#

	def __getitem__(self, key):
	#
		"""
python.org: Called to implement evaluation of self[key].

:param key: Key

:return: (mixed) Value
:since:  v0.1.03
		"""

		_return = None

		is_found = False

		if (dict.__contains__(self, key)):
		#
			_return = dict.__getitem__(self, key)
			is_found = True
		#

		if (not is_found):
		#
			for _dict in self.stacked_dicts:
			#
				if (key in _dict):
				#
					is_found = True
					_return = _dict[key]
				#
			#
		#

		if (not is_found): raise KeyError(key)
		return _return
	#

	def __repr__(self):
	#
		"""
python.org: Called by the repr() built-in function and by string conversions
(reverse quotes) to compute the "official" string representation of an
object.

:return: (str) String representation
:since:  v0.1.00
		"""

		return object.__repr__(self)
	#

	def add_dict(self, _dict):
	#
		"""
Adds the given Python dictionary to the stack.

:param _dict: Dictionary

:since: v0.1.03
		"""

		if (_dict is not self
		    and _dict not in self.stacked_dicts
		   ): self.stacked_dicts.append(_dict)
	#

	def get(self, key, default = None):
	#
		"""
python.org: Return the value for key if key is in the dictionary, else
            default.

:param key: Key
:param default: Default return value

:return: (mixed) Value
:since:  v0.1.03
		"""

		_return = default

		try: _return = self[key]
		except KeyError: pass

		return _return
	#

	def remove_dict(self, _dict):
	#
		"""
Removes the given Python dictionary from the stack.

:param _dict: Dictionary

:since: v0.1.03
		"""

		if (_dict in self.stacked_dicts): self.stacked_dicts.remove(_dict)
	#
#

##j## EOF