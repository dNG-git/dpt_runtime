# -*- coding: utf-8 -*-
##j## BOF

"""
de.direct_netware.classes.pas_file_functions

@internal  We are using epydoc (JavaDoc style) to automate the documentation
           process for creating the Developer's Manual.
           Use the following line to ensure 76 character sizes:
----------------------------------------------------------------------------
@author    direct Netware Group
@copyright (C) direct Netware Group - All rights reserved
@package   pas_core
@since     v0.1.00
@license   http://www.direct-netware.de/redirect.php?licenses;w3c
           W3C (R) Software License
"""
"""n// NOTE
----------------------------------------------------------------------------
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
http://www.direct-netware.de/redirect.php?pas

This work is distributed under the W3C (R) Software License, but without any
warranty; without even the implied warranty of merchantability or fitness
for a particular purpose.
----------------------------------------------------------------------------
http://www.direct-netware.de/redirect.php?licenses;w3c
----------------------------------------------------------------------------
#echo(pasCoreVersion)#
pas/#echo(__FILEPATH__)#
----------------------------------------------------------------------------
NOTE_END //n"""

from os import path
import re,time

from .ext_core.file import direct_file
from .pas_globals import direct_globals
from .pas_pythonback import direct_str

_direct_core_file_functions = None
_direct_core_file_functions_counter = 0

class direct_file_functions (direct_file):
#
	"""
This wrapper class extends "ext_core/file.py" and sets our default
parameters.

@author    direct Netware Group
@copyright (C) direct Netware Group - All rights reserved
@package   pas_core
@since     v0.1.00
@license   http://www.direct-netware.de/redirect.php?licenses;w3c
           W3C (R) Software License
	"""

	"""
----------------------------------------------------------------------------
Extend the class
----------------------------------------------------------------------------
	"""

	def __init__ (self):
	#
		"""
Constructor __init__ (direct_file_functions)

@since v0.1.00
		"""

		direct_file.__init__ (self,direct_globals['settings']['swg_umask_change'],direct_globals['settings']['swg_chmod_files_change'],(time.time ()),direct_globals['settings']['timeout'])

		self.debug = direct_globals['debug']
		if (self.debug != None): self.debug.append ("#echo(__FILEPATH__)# -file_functions.__init__ (direct_file_functions)- (#echo(__LINE__)#)")
	#

	def file_get (file_type,file_pathname):
	#
		"""
Let's work with files - use "file_get ()" to get content from a local file.
A time check will stop the reading process before a script timeout occurs.

@param  file_type Read mode to use. Options: "r", "s", "s0" and "s1" for ASCII
        (string); "a", "a0" and "a1" for ASCII (one line per array element)
        and "b" for binary. Use "a0" or "s0" to return the content as it is.
        "a1" and "s1" remove "<?php exit (); ?>" strings but whitespace
        characters at the start or end of the file content remain.
@param  file_pathname File path
@return (mixed) File content on success; False on error
@since  v0.1.00
		"""

		file_type = direct_str (file_type)
		file_pathname = direct_str (file_pathname)
		f_file_object = direct_file_functions.py_get ()

		if (f_file_object.debug != None): f_file_object.debug.append ("#echo(__FILEPATH__)# -file_functions.file_get ({0},{1})- (#echo(__LINE__)#)".format (file_type,file_pathname))

		f_file_pathname_os = path.normpath (file_pathname)
		f_return = False

		if ((path.exists (f_file_pathname_os)) and (f_file_object != None)):
		#
			if (file_type == "b"): f_file_object.open (f_file_pathname_os,True,"rb")
			else: f_file_object.open (f_file_pathname_os,True,"r")

			if (f_file_object.resource_check ()):
			#
				f_file_content = f_file_object.read (0)
				f_file_object.close ()

				if (type (f_file_content) == str):
				#
					if (file_type != "b"):
					#
						f_return = ""
						f_file_content = f_file_content.replace ("\r","")

						if ((file_type != "a0") and (file_type != "s0")):
						#
							f_file_content = re.compile("^<\\?php exit(.*?); \\?>\n",re.I).sub ("",f_file_content)
							if ((file_type != "a1") and (file_type != "s1")): f_file_content = f_file_content.strip ()
						#
					#

					if ((file_type == "a") or (file_type == "a0") or (file_type == "a1")):
					#
						if (f_file_content): f_return = f_file_content.split ("\n")
						else: f_return = [ ]
					#
					else: f_return = f_file_content
				#
			#
		#
		elif (f_file_object != None): f_file_object.trigger_error (("#echo(__FILEPATH__)# -direct_file.file_get ()- (#echo(__LINE__)#) reporting: Failed opening {0} - file does not exist".format (file_pathname)),f_file_object.E_WARNING)

		return f_return
	#
	file_get = staticmethod (file_get)

	def file_write (data,file_pathname,file_type = ""):
	#
		"""
The following function will save given data (as data) to a file.

@param  data Data to write (array or string)
@param  file_pathname File path
@param  file_type Write mode to use. Options: "r", "s", "s0" and "s1" for ASCII
        (string); "a", "a0" and "a1" for ASCII (one line per array element)
        and "b" for binary. Use "a0" or "s0" to save the content as it is.
        "a1" and "s1" add "<?php exit (); ?>" strings but whitespace
        characters at the start or end of the file content remain.
@return (bool) True on success
@since  v0.1.00
		"""

		file_type = direct_str (file_type)
		file_pathname = direct_str (file_pathname)
		f_file_object = direct_file_functions.py_get ()

		if (f_file_object == None): return False
		else:
		#
			if (f_file_object.debug != None): f_file_object.debug.append ("#echo(__FILEPATH__)# -file_functions.file_write (data,{0},{1})- (#echo(__LINE__)#)".format (file_pathname,file_type))

			if (type (data) == list): f_file_content = "\n".join (data)
			else: f_file_content = data

			if ((file_type == "a") or (file_type == "r") or (file_type == "s")): f_file_content = f_file_content.strip ()

			if (file_type == "b"): f_file_object.open (file_pathname,False,"wb")
			else: f_file_object.open (file_pathname,False,"w")

			if ((file_type == "a0") or (file_type == "b") or (file_type == "s0")): f_file_object.write (f_file_content)
			else: f_file_object.write ("<?php exit (); ?>\n{0}".format (direct_str (f_file_content)))

			return f_file_object.close ()
		#
	#
	file_write = staticmethod (file_write)

	def py_del ():
	#
		"""
The last "py_del ()" call will activate the Python singleton destructor.

@since v0.1.00
		"""

		global _direct_core_file_functions,_direct_core_file_functions_counter

		_direct_core_file_functions_counter -= 1
		if (_direct_core_file_functions_counter == 0): _direct_core_file_functions = None
	#
	py_del = staticmethod (py_del)

	def py_get (count = False):
	#
		"""
Get the direct_file_functions singleton.

@param  count Count "get ()" request
@return (direct_file_functions) Object on success
@since  v0.1.00
		"""

		global _direct_core_file_functions,_direct_core_file_functions_counter

		if (_direct_core_file_functions == None): _direct_core_file_functions = direct_file_functions ()
		if (count): _direct_core_file_functions_counter += 1

		return _direct_core_file_functions
	#
	py_get = staticmethod (py_get)
#

##j## EOF