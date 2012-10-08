# -*- coding: utf-8 -*-
##j## BOF

"""
de.direct_netware.classes.pas_basic_functions
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

from os import path
import os,re,shutil,stat

try: import cPickle as pickle
except ImportError: import pickle

try: import hashlib
except ImportError: import md5 as hashlib

from .pas_debug import direct_debug
from .pas_file_functions import direct_file_functions
from .pas_globals import direct_globals
from .pas_logger import direct_logger
from .pas_settings import direct_settings
from .pas_pythonback import direct_str
from .pas_xml import direct_xml
from .pas_xml_bridge import direct_xml_bridge

_direct_core_basic_functions_counter = 0

class direct_basic_functions (object):
#
	"""
Parse settings, check input or support localisations are required
everywhere.

:author:    direct Netware Group
:copyright: direct Netware Group - All rights reserved
:package:   pas_core
:since:     v0.1.00
:license:   http://www.direct-netware.de/redirect.php?licenses;mpl2
            Mozilla Public License, v. 2.0
	"""

	debug = None
	"""
Debug message container
	"""
	logger = None
	"""
Logging object
	"""
	settings = None
	"""
Settings singleton
	"""
	settings_cache =[ ]
	"""
Setting files cache
	"""

	"""
----------------------------------------------------------------------------
Construct the class
----------------------------------------------------------------------------
	"""

	def __init__ (self):
	#
		"""
Constructor __init__ (direct_basic_functions)

:since: v0.1.00
		"""

		self.settings = direct_settings.py_get (True)
		if ("debug_reporting" not in self.settings): self.settings['debug_reporting'] = False
		if ("pas_lang" not in self.settings): self.settings['pas_lang'] = "en"
		if ("pas_memcache" not in self.settings): self.settings['pas_memcache'] = ""
		if ("timeout" not in self.settings): self.settings['timeout'] = 3600

		self.settings_get ("{0}/settings/pas_core.xml".format (self.settings['path_data']))

		if (self.settings['debug_reporting']):
		#
			self.debug = direct_debug.py_get (True)
			self.debug.append ("#echo(__FILEPATH__)# -basic_functions_class.__init__ (direct_basic_functions)- (#echo(__LINE__)#)")
		#
		else:
		#
			direct_globals['debug'] = None
			self.debug = None
			if (("pas_log_level" in self.settings) and (hasattr (direct_logger,self.settings['pas_log_level']))): self.logger = direct_logger.py_get (getattr (direct_logger,self.settings['pas_log_level']))
		#
	#

	def __del__ (self):
	#
		"""
Destructor __del__ (direct_basic_functions)

:since: v0.1.00
		"""

		self.del_direct_basic_functions ()
	#

	def del_direct_basic_functions (self):
	#
		"""
Destructor del_direct_basic_functions (direct_basic_functions)

:since: v0.1.00
		"""

		if ((direct_debug != None) and (self.debug != None)): direct_debug.py_del ()
		if ((direct_logger != None) and (self.logger != None)): direct_logger.py_del ()
		if (direct_settings != None): direct_settings.py_del ()
	#

	def md5 (self,data):
	#
		"""
Computes the MD5 for the given data

:param data: Input string

:return: (str) MD5 hexadecimal value
:since:  v0.1.00
		"""

		if (type (data) == str): f_data = data.encode ()
		else: f_data = data

		return hashlib.md5(f_data).hexdigest ()
	#

	def memcache_get_file (self,file_pathname):
	#
		"""
Reads a file from the memcache or the filesystem. Certain system files are
read in on each page call. These small files are stored in the memcache
(ramfs on UNIX for example) to increase the read performance.

:param file_pathname: The file (which may also exist in the memcache)

:return: (mixed) Data on success; false on error
:since:  v0.1.00
		"""

		file_pathname = direct_str (file_pathname)

		if (self.debug != None): self.debug.append ("#echo(__FILEPATH__)# -basic_functions_class.memcache_get_file ({0})- (#echo(__LINE__)#)".format (file_pathname))
		f_return = False

		f_continue_check = True

		if ((len (self.settings['pas_memcache']) > 0) and (self.settings['pas_memcache_files'])):
		#
			f_cache_file = "{0}/{1}.{2}".format (self.settings['pas_memcache'],self.settings['pas_memcache_id'],(self.md5 ("{0}.{1}".format (path.dirname (file_pathname),(path.basename (file_pathname))))))

			if (path.exists (f_cache_file)):
			#
				f_continue_check = False
				f_return = direct_file_functions.file_get ("s",f_cache_file)
			#

			if (f_continue_check):
			#
				try:
				#
					shutil.copyfile (file_pathname,f_cache_file)
					os.chmod (f_cache_file,(stat.S_IRUSR | stat.S_IWUSR))
					f_return = direct_file_functions.file_get ("s",f_cache_file)
				#
				except:
				#
					if (path.exists (file_pathname)): f_return = direct_file_functions.file_get ("s",file_pathname)
				#
			#
		#
		elif (path.exists (file_pathname)): f_return = direct_file_functions.file_get ("s",file_pathname)

		return f_return
	#

	def memcache_get_file_merged_xml (self,file_pathname):
	#
		"""
This function uses preparsed XML files to increase performance. Please node
that these files are only readable as Python Pickle files.

:param file_pathname: The XML file (which may also exist in the memcache)

:return: (mixed) Parsed merged XML array on success
:since:  v0.1.00
		"""

		file_pathname = direct_str (file_pathname)

		if (self.debug != None): self.debug.append ("#echo(__FILEPATH__)# -basic_functions_class.memcache_get_file_merged_xml ({0})- (#echo(__LINE__)#)".format (file_pathname))
		f_return = { }

		f_continue_check = True

		if ((len (self.settings['pas_memcache']) > 0) and (self.settings['pas_memcache_merged_xml_files'])):
		#
			f_cache_file = "{0}/{1}.{2}".format (self.settings['pas_memcache'],self.settings['pas_memcache_id'],(self.md5 ("{0}.{1}".format (path.dirname (file_pathname),(path.basename (file_pathname))))))

			if (path.exists (f_cache_file)):
			#
				f_continue_check = False
				f_file_data = direct_file_functions.file_get ("b",f_cache_file)

				try:
				#
					if (type (f_file_data) != bool): f_return = pickle.loads (f_file_data)
				#
				except: f_return = None
			#
		#

		if (f_continue_check):
		#
			if (path.exists (file_pathname)):
			#
				f_file_data = direct_file_functions.file_get ("s",file_pathname)
				f_xml_object = direct_xml_bridge.py_get ()

				if ((type (f_file_data) != bool) and (f_xml_object != None)):
				#
					f_return = f_xml_object.xml2array (f_file_data,False)

					if ((len (self.settings['pas_memcache']) > 0) and (self.settings['pas_memcache_merged_xml_files']) and (type (f_return) != bool)):
					#
						try:
						#
							f_file_data = pickle.dumps (f_return)
							if (direct_file_functions.file_write (f_file_data,f_cache_file,"b")): os.chmod (f_cache_file,(stat.S_IRUSR | stat.S_IWUSR))
						#
						except: pass
					#
				#
			#
		#

		return f_return
	#

	def memcache_write_file (self,data,file_pathname,file_type = "s0"):
	#
		"""
Writes data to a file (and deletes the old memcache copy).

:param data: Data string
:param file_pathname: Target file
:param file_type: Write mode to use. Options: "r", "s", "s0" and "s1" for
                  ASCII (str); "a", "a0" and "a1" for ASCII (one line per
                  array element) and "b" for binary. Use "a0" or "s0" to
                  save the content as it is. "a1" and "s1" add
                  "<?php exit (); ?>" strings but whitespace characters at
                  the start or end of the file content remain.

:return: (mixed) True on success
:since:  v0.1.00
		"""

		file_pathname = direct_str (file_pathname)
		file_type = direct_str (file_type)

		if (self.debug != None): self.debug.append ("#echo(__FILEPATH__)# -basic_functions_class.memcache_write_file (data,{0},{1})- (#echo(__LINE__)#)".format (file_pathname,file_type))

		if ((len (self.settings['pas_memcache']) > 0) and ((self.settings['pas_memcache_files']) or (self.settings['pas_memcache_merged_xml_files']))):
		#
			f_cache_file = "{0}/{1}.{2}".format (self.settings['pas_memcache'],self.settings['pas_memcache_id'],(self.md5 ("{0}.{1}".format (path.dirname (file_pathname),(path.basename (file_pathname))))))
			if (path.exists (f_cache_file)): os.unlink (f_cache_file)
		#

		return direct_file_functions.file_write (data,file_pathname,file_type)
	#

	def settings_get (self,file_pathname,required = False,use_cache = True):
	#
		"""
Reads settings from file (XML-encoded) and adds them to direct_settings.

:param file_pathname: The file containing settings
:param required: If the file is required (true) but does not exist,
                 an OSError exception is raised.
:param use_cache: False to read a settings file even if it has already
                  been parsed.

:return: (bool) True on success; false on error
:since:  v0.1.00
		"""

		file_pathname = direct_str (file_pathname)

		if (self.debug != None): self.debug.append ("#echo(__FILEPATH__)# -basic_functions_class.settings_get ({0},required,use_cache)- (#echo(__LINE__)#)".format (file_pathname))
		f_return = False

		f_continue_check = True

		if ((use_cache) and (self.md5 (file_pathname) in self.settings_cache)):
		#
			f_return = True
			f_continue_check = False
		#

		if (f_continue_check):
		#
			f_xml_dict = self.memcache_get_file_merged_xml (file_pathname)

			if (f_xml_dict != None):
			#
				f_re_key_replace = re.compile ("pas_settings_file_v(\\d+)_",re.I)
				self.settings_cache.append (self.md5 (file_pathname))

				for f_key in f_xml_dict:
				#
					f_xml_node_dict = f_xml_dict[f_key]

					if ("tag" in f_xml_node_dict):
					#
						f_key = f_re_key_replace.sub ("",f_key)
						if ((f_key not in self.settings) or (len (f_xml_node_dict['value']) > 0)): self.settings[f_key] = direct_str (f_xml_node_dict['value'])
					#
					elif ((type (f_xml_node_dict) == list) and (len (f_xml_node_dict) > 0) and ("tag" in f_xml_node_dict[0])):
					#
						f_key = f_re_key_replace.sub ("",f_key)
						self.settings[f_key] = [ ]

						for f_xml_sub_node_dict in f_xml_node_dict: self.settings[f_key].append (direct_str (f_xml_sub_node_dict['value']))
					#
				#

				f_return = True
			#
			elif (required): raise OSError ("The system could not load a required component.\n\n\"{0}\" was not found".format (file_pathname))
		#

		return f_return
	#

	def settings_write (self,settings,file_pathname):
	#
		"""
Writes the setting array to a file (XML-encoded).

:param settings: Settings array
:param file_pathname: The file containing settings

:return: (bool) True on success; false on error
:since:  v0.1.00
		"""

		file_pathname = direct_str (file_pathname)

		if (self.debug != None): self.debug.append ("#echo(__FILEPATH__)# -basic_functions_class.settings_write (settings,{0})- (#echo(__LINE__)#)".format (file_pathname))
		f_return = False

		f_xml_object = direct_xml.py_get ()

		if ((type (settings) == dict) and (f_xml_object != None)):
		#
			f_xml_object.node_add ("pas_settings_file_v1","",{ "xmlns": "urn:de-direct-netware-xmlns:pas.settings.v1" })

			for f_setting_key in settings:
			#
				f_setting_key = direct_str (f_setting_key)
				f_setting_value = direct_str (settings[f_setting_key])
				f_xml_object.node_add (("pas_settings_file_v1 {0}".format (f_setting_key.replace ("_"," "))),f_setting_value,{ "xml:space": "preserve" })
			#

			f_return = self.memcache_write_file (f_xml_object.cache_export (),file_pathname)
		#

		return f_return
	#

	def py_del ():
	#
		"""
The last "py_del ()" call will activate the Python singleton destructor.

:since: v0.1.00
		"""

		global _direct_core_basic_functions_counter

		_direct_core_basic_functions_counter -= 1
		if (_direct_core_basic_functions_counter == 0): direct_globals['basic_functions'] = None
	#
	py_del = staticmethod (py_del)

	def py_get (count = False):
	#
		"""
Get the direct_basic_functions singleton.

:param count: Count "get ()" request

:return: (direct_basic_functions) Object on success
:since:  v0.1.00
		"""

		global _direct_core_basic_functions_counter

		if ("basic_functions" not in direct_globals): direct_globals['basic_functions'] = direct_basic_functions ()
		if (count): _direct_core_basic_functions_counter += 1

		return direct_globals['basic_functions']
	#
	py_get = staticmethod (py_get)
#

##j## EOF