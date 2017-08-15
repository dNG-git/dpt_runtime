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

from math import floor

from dNG.data.binary import Binary
from dNG.runtime.type_exception import TypeException

from .md5 import Md5

class Tmd5(object):
    """
To increase security while using an hardware efficient algorithm for power
constraint devices two additional steps are used for MD5 hashing.

All strings will be divided into three parts and reverted to make attacks
based on pre-calculated rainbox tables harder. Furthermore two salt strings
are used for hashing.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v0.2.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    @staticmethod
    def _align_string(source, target):
        """
Align the target string to the source string. It will be trimmed or
repeated and returned.

:param source: Source string
:param target: Target string

:return: (str) Triple MD5 string
:since:  v0.2.0
        """

        _return = ""

        source_length = len(source)
        target_length = len(target)

        if (source_length > 0 and target_length > 0):
            if (target_length > source_length): _return = target[target_length - source_length:]
            else:
                while (len(_return) < source_length): _return += (target if (len(_return) + target_length <= source_length) else target[:source_length - len(_return)])
            #
        #

        return _return
    #

    @staticmethod
    def hash(data, salt = ""):
        """
Generate the triple MD5 hash for the data given.

:param data: Input string
:param salt: Salt used during hashing

:return: (str) Triple MD5 string
:since:  v0.2.0
        """

        _return = ""

        data = Binary.str(data)
        if (not isinstance(data, str)): raise TypeException("Data must be of type str")

        data_length = len(data)

        salt = Binary.str(salt)
        if (type(salt) is not str): raise TypeException("Salt must be of type str")

        if (data_length > 0):
            salt = Tmd5._align_string(data, salt)

            data_remaining = data_length
            is_salt_used = (len(salt) > 0)
            part_length = int(floor(data_length / 3))
            return_length = 0

            """
We will now divide the string into three parts, revert each of them and put
it together to our result.
            """

            part = ("".join(chr(ord(char) ^ ord(saltchar)) for char, saltchar in zip(data[:part_length][::-1], salt[:part_length])) if (is_salt_used) else data[:part_length][::-1])
            _return = Md5.hash(part)

            data_remaining -= part_length
            return_length += part_length

            part = ("".join(chr(ord(char) ^ ord(saltchar)) for char, saltchar in zip(data[return_length:part_length + return_length][::-1], salt[return_length:part_length + return_length])) if (is_salt_used) else data[return_length:part_length + return_length][::-1])
            _return += Md5.hash(part)

            data_remaining -= part_length
            return_length += part_length

            part = ("".join(chr(ord(char) ^ ord(saltchar)) for char, saltchar in zip(data[return_length:data_remaining + return_length][::-1], salt[return_length:data_remaining + return_length])) if (is_salt_used) else data[return_length:data_remaining + return_length][::-1])
            _return += Md5.hash(part)
        #

        return _return
    #

    @staticmethod
    def password_hash(data, salt, pepper):
        """
Generate a password triple MD5 hash based on the data, salt and pepper
given.

:param data: Input string
:param salt: Salt used during hashing
:param pepper: Pepper used for unique hashing for this password

:return: (str) Triple MD5 string
:since:  v0.2.0
        """

        salt = Binary.str(salt)
        if (type(salt) is not str): raise TypeException("Salt must be of type str")

        pepper = Binary.str(pepper)
        if (type(pepper) is not str): raise TypeException("Pepper must be of type str")

        pepper = Tmd5._align_string(salt, pepper)
        if (len(pepper) > 0): salt = "".join(chr(ord(saltchar) ^ ord(pepperchar)) for saltchar, pepperchar in zip(salt, pepper))

        return Tmd5.hash(data, salt)
    #
#
