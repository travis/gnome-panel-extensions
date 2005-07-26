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


#A super class for all extensions
class PanelExtension(gtk.EventBox):
	def __init__(self,bundleFile='None'):
		self.__gobject_init__()
		if os.path.isfile(bundleFile):
			sys.path.insert(0, bundleFile)
			self.bundleFile = bundleFile
		else:
			print "Could not find", bundleFile

		
			

	def setup_extension_menu(xml, verbs):
		if self.applet:
			self.applet.setup_menu(xml, verbs, None)
		else:
			print "No applet file registered, can not create context menu"
		
	def setup_extension_menu_from_file(file_name, verbs):
		if self.applet:
			old_wd = os.getcwd()
			os.chdir("/tmp/")
			#temporarily expand the xml file
			
			temp_xml_menu_file = open (file_name, 'w')
			temp_xml_menu_file.write(self.bundleFile.read(file_name))
			temp_xml_menu_file.close()
			
			
			self.setup_menu_from_file (os.getcwd() ,file_name, None, verbs)
			#cleanup on aisle 10
			os.remove(file_name)
			#change the working directory back
			os.chdir(old_wd)

		else:
			print "No container applet registered, can not create context menu"


	def _register_container_applet(applet):
		self.applet = applet
		

gobject.type_register(PanelExtension)

if __name__ == "__main__":
	test = PanelExtension("testbundle")
