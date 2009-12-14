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
#echo(pasCoreVersion)#
pas/#echo(__FILEPATH__)#
----------------------------------------------------------------------------
NOTE_END //n*/"""
"""
de.direct_netware.classes.pas_basic_functions

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

from exceptions import OSError
from os import path
from pas_debug import direct_debug
from pas_file_functions import direct_file_functions
from pas_settings import direct_settings
from pas_xml import direct_xml
from pas_xml_bridge import direct_xml_bridge
import re,shutil,stat

try: import cPickle as pyPickle
except Exception,g_handled_exception: import pickle as pyPickle

try: import hashlib as pyHashlib
except Exception,g_handled_exception: import md5 as pyHashlib

_direct_core_basic_functions = None
_direct_core_basic_functions_counter = 0

class direct_basic_functions (object):
#
	"""
Parse settings, check input or support localisations are required
everywhere.

@author    direct Netware Group
@copyright (C) direct Netware Group - All rights reserved
@package   pas_core
@since     v1.0.0
@license   http://www.direct-netware.de/redirect.php?licenses;w3c
           W3C (R) Software License
	"""

	debug = None
	"""
Debug message container
	"""
	settings = None
	"""
Settings singleton
	"""
	settings_cache =[ ]
	"""
Settings singleton
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

@since v0.1.00
		"""

		self.settings = direct_settings.get (True)
		if (not "debug_reporting" in self.settings): self.settings['debug_reporting'] = False
		if (not "pas_lang" in self.settings): self.settings['pas_lang'] = "en"
		if (not "pas_memcache" in self.settings): self.settings['pas_memcache'] = ""
		if (not "timeout" in self.settings): self.settings['timeout'] = 3600

		self.settings_get ("%s/settings/pas_core.xml" % self.settings['path_data'])

		if (self.settings['debug_reporting']):
		#
			self.debug = direct_debug.get (True)
			self.debug.append ("#echo(__FILEPATH__)# -basic_functions_class->__construct (direct_basic_functions)- (#echo(__LINE__)#)")
		#
		else: self.debug = None
	#

	def __del__ (self):
	#
		"""
Destructor __del__ (direct_basic_functions)

@since v0.1.00
		"""

		self.del_direct_basic_functions ()
	#

	def del_direct_basic_functions (self):
	#
		"""
Destructor del_direct_basic_functions (direct_basic_functions)

@since v0.1.00
		"""

		direct_debug.py_del ()
		direct_settings.py_del ()
	#

	def md5 (self,f_data):
	#
		"""
Computes the MD5 for the given data

@param  f_data Input string
@return (string) MD5 hexadecimal value
@since  v0.1.00
		"""

		if (self.debug != None): self.debug.append ("#echo(__FILEPATH__)# -basic_functions_class->md5 (+f_data)- (#echo(__LINE__)#)")
		return pyHashlib.md5(f_data).hexdigest ()
	#

	def memcache_get_file (self,f_file):
	#
		"""
Reads a file from the memcache or the filesystem. Certain system files are
read in on each page call. These small files are stored in the memcache
(ramfs on UNIX for example) to increase the read performance.

@param  f_file The file (which may also exist in the memcache)
@return (mixed) Data on success; false on error
@since  v0.1.00
		"""

		if (self.debug != None): self.debug.append ("#echo(__FILEPATH__)# -basic_functions_class->memcache_get_file (%s)- (#echo(__LINE__)#)" % f_file)

		f_continue_check = True
		f_return = False

		if ((len (self.settings['pas_memcache']) > 0) and (self.settings['pas_memcache_files'])):
		#
			f_cache_file = "%s/%s.%s" % ( self.settings['pas_memcache'],self.settings['pas_memcache_id'],self.md5 ("%s.%s" % ( path.dirname (f_file),path.basename (f_file) )) )

			if (path.exists (f_cache_file)):
			#
				f_continue_check = False
				f_return = direct_file_functions.file_get ("s",f_cache_file)
			#

			if (f_continue_check):
			#
				try:
				#
					shutil.copyfile (f_file,f_cache_file)
					os.chmod (f_cache_file,(stat.S_IRUSR | stat.S_IWUSR))
					f_return = direct_file_functions.file_get ("s",f_cache_file)
				#
				except Exception,f_handled_exception:
				#
					if (path.exists (f_file)): f_return = direct_file_functions.file_get ("s",f_file)
				#
			#
		#
		elif (path.exists (f_file)): f_return = direct_file_functions.file_get ("s",f_file)

		return f_return
	#

	def memcache_get_file_merged_xml (self,f_file):
	#
		"""
This function uses preparsed XML files to increase performance. Please node
that these files are only readable as Python Pickle files.

@param  f_file The XML file (which may also exist in the memcache)
@return (mixed) Parsed merged XML array on success
@since  v0.1.00
		"""

		if (self.debug != None): self.debug.append ("#echo(__FILEPATH__)# -basic_functions_class->memcache_get_file_merged_xml (%s)- (#echo(__LINE__)#)" % f_file)

		f_continue_check = True
		f_return = { }

		if ((len (self.settings['pas_memcache']) > 0) and (self.settings['pas_memcache_merged_xml_files'])):
		#
			f_cache_file = "%s/%s.%s" % ( self.settings['pas_memcache'],self.settings['pas_memcache_id'],self.md5 ("%s.%s" % ( path.dirname (f_file),path.basename (f_file) )) )

			if (path.exists (f_cache_file)):
			#
				f_continue_check = False
				f_file_data = direct_file_functions.file_get ("b",f_cache_file)

				try:
				#
					if (type (f_file_data) != bool): f_return = pyPickle.loads (f_file_data)
				#
				except Exception,f_handled_exception: f_return = None
			#
		#

		if (f_continue_check):
		#
			if (path.exists (f_file)):
			#
				f_file_data = direct_file_functions.file_get ("s",f_file)
				f_xml_object = direct_xml_bridge.get_xml_bridge ()

				if ((type (f_file_data) != bool) and (f_xml_object != None)):
				#
					f_return = f_xml_object.xml2array (f_file_data,False)

					if ((len (self.settings['pas_memcache']) > 0) and (self.settings['pas_memcache_merged_xml_files']) and (type (f_return) != bool)):
					#
						try:
						#
							f_file_data = pyPickle.dumps (f_return)
							if (direct_file_functions.file_write (f_file_data,f_cache_file,"b")): os.chmod (f_cache_file,(stat.S_IRUSR | stat.S_IWUSR))
						#
						except Exception,f_unhandled_exception: pass
					#
				#
			#
		#

		return f_return
	#

	def memcache_write_file (self,f_data,f_file,f_type = "s0"):
	#
		"""
Writes data to a file (and deletes the old memcache copy).

@param  f_data Data string
@param  f_file Target file
@param  f_type Write mode to use. Options: "r", "s", "s0" and "s1" for ASCII
        (string); "a", "a0" and "a1" for ASCII (one line per array element)
        and "b" for binary. Use "a0" or "s0" to save the content as it is.
        "a1" and "s1" add "<?php exit (); ?>" strings but whitespace
        characters at the start or end of the file content remain.
@return (mixed) True on success
@since  v0.1.00
		"""

		if (self.debug != None): self.debug.append ("#echo(__FILEPATH__)# -basic_functions_class->memcache_write_file (+f_data,%s,%s)- (#echo(__LINE__)#)" % ( f_file,f_type ))

		if ((len (self.settings['pas_memcache']) > 0) and ((self.settings['pas_memcache_files']) or (self.settings['pas_memcache_merged_xml_files']))):
		#
			f_cache_file = "%s/%s.%s" % ( self.settings['pas_memcache'],self.settings['pas_memcache_id'],self.md5 ("%s.%s" % ( path.dirname (f_file),path.basename (f_file) )) )
			if (path.exists (f_cache_file)): os.unlink (f_cache_file)
		#

		return direct_file_functions.file_write (f_data,f_file,f_type)
	#

	def settings_get (self,f_file,f_required = False,f_use_cache = True):
	#
		"""
Reads settings from file (XML-encoded) and adds them to direct_settings.

@param  f_file The file containing settings
@param  f_required If the file is required (true) but does not exist,
        an OSError exception is raised.
@param  f_use_cache False to read a settings file even if it has already
        been parsed.
@return (boolean) True on success; false on error
@since  v0.1.00
		"""

		if (self.debug != None): self.debug.append ("#echo(__FILEPATH__)# -basic_functions_class->settings_get (%s,+f_required,+f_use_cache)- (#echo(__LINE__)#)" % f_file)

		f_continue_check = True
		f_file_object = direct_file_functions.get ()
		f_return = False

		if (f_file_object != None):
		#
			if (f_use_cache):
			#
				if ((self.md5 (f_file)) in self.settings_cache):
				#
					f_return = True
					f_continue_check = False
				#
			#

			if (f_continue_check):
			#
				f_xml_array = self.memcache_get_file_merged_xml (f_file)

				if (f_xml_array != None):
				#
					f_re_key_replace = re.compile ("pas_settings_file_v(\\d+)_",re.I)
					self.settings_cache.append (self.md5 (f_file))

					for f_key in f_xml_array:
					#
						f_xml_node_array = f_xml_array[f_key]

						if ("tag" in f_xml_node_array):
						#
							f_key = f_re_key_replace.sub ("",f_key)
							self.settings[f_key] = f_xml_node_array['value']
						#
						elif ((type (f_xml_node_array) == list) and (len (f_xml_node_array) > 0) and ("tag" in f_xml_node_array[0])):
						#
							f_key = f_re_key_replace.sub ("",f_key)
							self.settings[f_key] = [ ]

							for f_xml_sub_node_array in f_xml_node_array: self.settings[f_key].append (f_xml_sub_node_array['value'])
						#
					#

					f_return = True
				#
				elif (f_required): raise OSError ("The system could not load a required component.\n\n\"%s\" was not found" % f_file)
			#
		#

		return f_return
	#

	def settings_write (self,f_settings,f_file):
	#
		"""
Writes the setting array to a file (XML-encoded).

@param  f_settings Settings array
@param  f_file The file containing settings
@return (boolean) True on success; false on error
@since  v0.1.00
		"""

		if (self.debug != None): self.debug.append ("#echo(__FILEPATH__)# -basic_functions_class->settings_write (+f_settings,%s)- (#echo(__LINE__)#)" % f_file)

		f_return = False
		f_xml_object = direct_xml.get_xml ()

		if ((type (f_settings) == dict) and (f_xml_object != None)):
		#
			f_xml_object.node_add ("pas_settings_file_v1","",{ "xmlns": "urn:de.direct-netware.xmlns:pas.settings.v1" })

			for f_setting_key in f_settings:
			#
				f_setting_value = f_settings[f_setting_key]
				f_xml_object.node_add ("pas_settings_file_v1 %s" % (f_setting_key.replace ("_"," ")),f_setting_value,{ "xml:space": "preserve" })
			#

			f_return = self.memcache_write_file (f_xml_object.cache_export (),f_file)
		#

		return f_return
	#

	@staticmethod
	def get (f_count = False):
	#
		"""
Get the direct_basic_functions singleton.

@param  bool Count "get ()" request
@return (direct_basic_functions) Object on success
@since  v1.0.0
		"""

		global _direct_core_basic_functions,_direct_core_basic_functions_counter

		if (_direct_core_basic_functions == None): _direct_core_basic_functions = direct_basic_functions ()
		if (f_count): _direct_core_basic_functions_counter += 1

		return _direct_core_basic_functions
	#

	@staticmethod
	def get_basic_functions (f_count = False):
	#
		"""
Get the direct_basic_functions singleton.

@param  bool Count "get ()" request
@return (direct_basic_functions) Object on success
@since  v1.0.0
		"""

		return direct_basic_functions.get (f_count)
	#

	@staticmethod
	def py_del ():
	#
		"""
The last "py_del ()" call will activate the Python singleton destructor.

@since  v1.0.0
		"""

		global _direct_core_basic_functions,_direct_core_basic_functions_counter

		_direct_core_basic_functions_counter -= 1
		if (_direct_core_basic_functions_counter == 0): _direct_core_basic_functions = None
	#
#

##j## EOF