# -*- coding: utf-8 -*-
##j## BOF

"""/*n// NOTE
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
NOTE_END //n*/"""
"""/**
* de.direct_netware.classes.pas_file_functions
*
* @internal  We are using JavaDoc to automate the documentation process for
*            creating the Developer's Manual. All sections including these
*            special comments will be removed from the release source code.
*            Use the following line to ensure 76 character sizes:
* ----------------------------------------------------------------------------
* @author    direct Netware Group
* @copyright (C) direct Netware Group - All rights reserved
* @package   pas_core
* @since     v0.1.00
* @license   http://www.direct-netware.de/redirect.php?licenses;w3c
*            W3C (R) Software License
*/"""

from ext_core.file import direct_file
from os import path
from pas_settings import direct_settings
import re,time

_direct_core_file_functions = None

class direct_file_functions (direct_file):
#
	"""
This wrapper class extends "ext_core/file.php" and sets our default
parameters.

@author    direct Netware Group
@copyright (C) direct Netware Group - All rights reserved
@since     v1.0.0
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

@param f_charset Charset to be added as information to XML output
@param f_parse_only Parse data only
@param f_time Current UNIX timestamp
@param f_timeout_count Retries before timing out
@param f_ext_xml_path Path to the XML parser files.
@param f_debug Debug flag
@since v0.1.00
		"""

		f_settings = direct_settings.get ()
		super(direct_file_functions,self).__init__ (f_settings['swg_umask_change'],f_settings['swg_chmod_files_change'],(time.time ()),f_settings['timeout'],f_settings['debug_reporting'])
	#

	@staticmethod
	def file_get (f_type,f_file_path):
	#
		"""
Let's work with files - use "file_get ()" to get content from a local file.
A time check will stop the reading process before a script timeout occurs.

@param  f_type Read mode to use. Options: "r", "s", "s0" and "s1" for ASCII
        (string); "a", "a0" and "a1" for ASCII (one line per array element)
        and "b" for binary. Use "a0" or "s0" to return the content as it is.
        "a1" and "s1" remove "<?php exit (); ?>" strings but whitespace
        characters at the start or end of the file content remain.
@param  f_file_path File path
@return (mixed) False on error
@since  v0.1.00
		"""

		f_file_object = direct_file_functions.get ()
		f_file_path = path.normpath (f_file_path)
		f_return = False

		if ((path.exists (f_file_path)) and (f_file_object != None)):
		#
			if (f_type == "b"): f_file_object.open (f_file_path,True,"rb")
			else: f_file_object.open (f_file_path,True,"r")

			if (f_file_object.resource_check ()):
			#
				f_file_content = f_file_object.read (0)
				f_file_object.close ()

				if (type (f_file_content) == str):
				#
					if (f_type != "b"):
					#
						f_return = ""
						f_file_content = f_file_content.replace ("\r","")

						if ((f_type != "a0") and (f_type != "s0")):
						#
							f_file_content = re.compile("^<\?php exit(.*?); \?>\n",re.I).sub ("",f_file_content)
							if ((f_type != "a1") and (f_type != "s1")): f_file_content = f_file_content.strip ()
						#
					#

					if ((f_type == "a") or (f_type == "a0") or (f_type == "a1")):
					#
						if (f_file_content): f_return = f_file_content.split ("\n")
						else: f_return = [ ]
					#
					else: f_return = f_file_content
				#
			#
		#
		elif (f_file_object != None): f_file_object.trigger_error ("pas/#echo(__FILEPATH__)# -direct_file->file_get ()- (#echo(__LINE__)#) reporting: Failed opening %s - file does not exist" % f_file_path,f_file_object.E_WARNING)

		return f_return
	#

	@staticmethod
	def file_write (f_data,f_file_path,f_type = ""):
	#
		"""
The following function will save given data (as f_data) to a file.

@param  f_data Data to write (array or string)
@param  f_file_path File path
@param  f_type Write mode to use. Options: "r", "s", "s0" and "s1" for ASCII
        (string); "a", "a0" and "a1" for ASCII (one line per array element)
        and "b" for binary. Use "a0" or "s0" to save the content as it is.
        "a1" and "s1" add "<?php exit (); ?>" strings but whitespace
        characters at the start or end of the file content remain.
@return (boolean) True on success
@since  v0.1.00
		"""

		f_file_object = direct_file_functions.get ()

		if (f_file_object == None): return False
		else:
		#
			if (type (f_data) == list): f_file_content = "\n".join (f_data)
			else: f_file_content = f_data

			if ((f_type == "a") or (f_type == "r") or (f_type == "s")): f_file_content = f_file_content.strip ()

			if (f_type == "b"): f_file_object.open (f_file_path,False,"wb")
			else: f_file_object.open (f_file_path,False,"w")

			if ((f_type == "a0") or (f_type == "b") or (f_type == "s0")): f_file_object.write (f_file_content)
			else: f_file_object.write ("<?php exit (); ?>\n%s" % f_file_content)

			return f_file_object.close ()
		#
	#

	@staticmethod
	def get ():
	#
		"""
Get the direct_file_functions singleton.

@return (direct_file_functions) Object on success
@since  v1.0.0
		"""

		global _direct_core_file_functions
		if (_direct_core_file_functions == None): _direct_core_file_functions = direct_file_functions ()
		return _direct_core_file_functions
	#

	@staticmethod
	def get_file_functions ():
	#
		"""
Get the direct_file_functions singleton.

@return (direct_file_functions) Object on success
@since  v1.0.0
		"""

		return direct_file_functions.get ()
	#
#

##j## EOF