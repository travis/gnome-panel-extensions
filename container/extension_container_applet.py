#!/usr/bin/env python
import pygtk
pygtk.require('2.0')


import sys
import gtk
import gobject
import gnomeapplet
import zipfile
import panel_extension
import first_extension
import manage_applets
import extension_container_globals

import gettext
_ = gettext.gettext


  
class ExtensionContainerApplet(gnomeapplet.Applet):
	def __init__(self):
		self.__gobject_init__()

	def init(self):
        	self.setup_menu_from_file (None, "GNOME_ExtensionContainer.xml",
                	                   None, [(_("About"), self.nothing), (_("Pref"), self.nothing),(_("Manage"), self._manageExtensionsDialog)])
		
		self.prefs_key = self.get_preferences_key()
		print "Applet prefs located at %s" % (self.prefs_key)


		test = first_extension.FirstExtension()
		self.add(test)
	
	


		return True
    

	def run_bundle(bundleFile):

		if not is_zipfile(bundleFile):
			print "Sorry, ", bundleFile, "is not a gnome-extension-bundle file"
		else:
			pass
		

	def nothing():
		pass

	def _manageExtensionsDialog(self, uicomponent, verb):	
		manage_dialog = manage_applets.ManageApplets(self.prefs_key)
		manage_dialog.show()
		manage_dialog.run()
		manage_dialog.hide()

            

gobject.type_register(ExtensionContainerApplet)


def foo(applet, iid):
    print "Returning container applet"
    return applet.init()

# run in seperate window for testing
if len(sys.argv) == 2 and sys.argv[1] == "run-in-window":
	main_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
	main_window.set_title("Python Applet")
	main_window.connect("destroy", gtk.mainquit)
	app = ExtensionContainerApplet()
	app.init()

	main_window.add(app)
	
	main_window.show_all()

	man = manage_applets.ManageApplets("/blah")
	man.show()
	man.run()
	man.hide()
	

	gtk.main()
	sys.exit()

gnomeapplet.bonobo_factory("OAFIID:GNOME_ExtensionContainerApplet_Factory", 
                            ExtensionContainerApplet.__gtype__, 
                            "ExtensionContainer", "0", foo)

print "Done waiting in factory, returning... If this seems wrong, perhaps there is another copy of the Blog factory running?"
