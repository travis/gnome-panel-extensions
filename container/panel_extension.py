#!/usr/bin/env python
import pygtk
pygtk.require('2.0')

import os
import sys
import gtk
import gobject
import zipfile

import gettext
_ = gettext.gettext

class NoAppletError(Exception):
	def __init__(self, *args):
		Exception.__init__(self, *args)
		self.wrapped_exc = sys.exc_info()
	
#A super class for all extensions
class PanelExtension(gtk.EventBox):
	

	def __init__(self, bundle=None):
		self.__gobject_init__()
		self.applet = None


	def __extension_init__(self):
		print "No extension init provided by extension."


	def get_bundle(self):
		if self.applet:
			return self.applet.get_loaded_bundle()
		else:
			raise NoAppletError, "No applet registered, cannot get bundle"

	def get_preferences_key(self):
		if self.applet:
			return self.applet.get_preferences_key()
		else:
			raise NoAppletError, "No applet file registered, can get preferences ket"
			

	def setup_extension_menu(self, xml, verbs):
		if self.applet:
			self.applet.setup_menu(xml, verbs, None)
		else:
			raise NoAppletError, "No applet file registered, can not create context menu"
		
	def setup_extension_menu_from_file(self, file, verbs):
		if self.applet:
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


	def _register_container_applet(self, applet):
		self.applet = applet

		

gobject.type_register(PanelExtension)

if __name__ == "__main__":
	test = PanelExtension("testbundle")
