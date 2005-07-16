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
		else:
			print "Could not find", bundleFile

		label = gtk.Label('Hello!')

		self.add(label)
		self.show_all()
			
		

gobject.type_register(PanelExtension)



test = PanelExtension("testbundle")
#print GTK_IS_WIDGET(test)
