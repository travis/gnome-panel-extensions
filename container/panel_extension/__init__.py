'''Panel_extension package.
(c)2005 Travis F Vachon

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License as
published by the Free Software Foundation; either version 2 of the
License, or (at your option) any later version.
 This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.
 You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
02111-1307, USA.

The panel_extension package provides modules needed to run GNOME
panel extensions. For more information on these, please see
http://www.gnome.org/~tvachon.
'''
import pygtk
pygtk.require('2.0')

import os
import sys
import gtk
import gobject

class NoAppletError(Exception):
	'''Raised when extensions are run without a container applet.

	Running extensions in this way make bundle resources and some
	pieces of the API unavailable.'''
	def __init__(self, *args):
		Exception.__init__(self, *args)
		self.wrapped_exc = sys.exc_info()
	

class PanelExtension(gtk.EventBox):
	'''A super class for all extensions.

	All panel extensions should subclass this class. PanelExtension
	provides a number of very useful functions for accessing bundle
	resources and system utilities like gconf preference keys.
	'''

	def __init__(self, bundle=None):
		self.__gobject_init__()
		self.applet = None
		self.bundle = None
		self.live_preview_mode = False


	def __extension_init__(self):
		print "No extension init provided by extension."


	def get_bundle(self):
		'''Returns the Bundle containing this extension.

		This function returns a Bundle object representing the
		bundle containing the extension which provides methods to
		access bundle resources.
		'''
		if self.bundle:
			return self.bundle
		elif self.applet:
			return self.applet.get_loaded_bundle()
		else:
			raise NoAppletError, "No applet registered, cannot get bundle"

	##@param key The name of the gconf key to create in /apps/panel/extensions.
 	def get_preferences_key(self, key):
		'''Returns a gconf preferences key for extensions.
		
		The provided key parameter should be unique or risk
		interaction with other extensions. They can be any
		combination of alphanumeric characters and underscores.
		A url should work well, for example:
		    www_gnome_org_tvachon_sampleextension
		'''
		return os.path.normpath("/apps/panel/extensions"+key)
				
			

	##
	#@param xml string containing Bonobo user interface XML
	#@param verbs Bonobo user interface verbs
	def setup_extension_menu(self, xml, verbs):
		'''Set up a context menu from string of XML.

		The XML must be Bonobo user interface XML. More information
		about this XML can be found at
		<a href="http://www.pycage.de/howto_bonobo.html">
		http://www.pycage.de/howto_bonobo.html</a>
		'''
		if self.live_preview_mode:
			pass
		
		elif self.applet:
			self.applet.setup_menu(xml, verbs, None)
		else:
			raise NoAppletError, "No applet file registered, can not create context menu"

	##
	#@file name of file in bundle containing interface xml
	def setup_extension_menu_from_file(self, file, verbs):
		'''Set up a context menu from XML contained in file in bundle.

		The file parameter should be a file in the bundle.
		The XML must be Bonobo user interface XML. More information
		about this XML can be found at
		<a href="http://www.pycage.de/howto_bonobo.html">
		http://www.pycage.de/howto_bonobo.html</a>
		'''
		if self.live_preview_mode:
			pass

		elif self.applet:
			old_wd = os.getcwd()
			os.chdir("/tmp/")
			#temporarily expand the xml file


			
			temp_xml_menu_file = open ('ext_tmp_menu.tmp', 'w')
			temp_xml_menu_file.write(file.read())
			temp_xml_menu_file.close()
			
			
			self.applet.setup_menu_from_file (os.getcwd() ,'ext_tmp_menu.tmp', None, verbs)
			#cleanup
			os.remove('ext_tmp_menu.tmp')
			#change the working directory back
			os.chdir(old_wd)

		else:
			raise NoAppletError, "No container applet registered, can not create context menu"

	def _set_live_preview(self, value):
		self.live_preview_mode = value

	def _register_container_applet(self, applet):
		self.applet = applet

	def _register_bundle(self, bundle):
		self.bundle = bundle
		

gobject.type_register(PanelExtension)

