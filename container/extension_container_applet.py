#!/usr/bin/env python
import pygtk
pygtk.require('2.0')


import sys
import os
os.chdir("/home/travis/development/gnome-panel-extensions/container/")
os.chdir("/home/travis/.panelextensions/")
import gtk
import gobject
import gconf
import gnomeapplet

import StringIO

import xml.dom.minidom

import bonobo
import Bonobo

import zipfile

import manage_applets
import extension_container_globals
import extension_bundle

import gettext
_ = gettext.gettext


if len(sys.argv) == 2 and sys.argv[1] == "run-in-window":
    run_in_window = True
else:
    run_in_window = False

  
class ExtensionContainerApplet(gnomeapplet.Applet):
    '''
    ExtensionContainerApplet is a classic GNOME panel applet that runs new
    GNOME panel extensions. 
    '''
    def __init__(self):
        self.__gobject_init__()

    def init(self, bundleFileName=None):
        #    self.setup_menu_from_file ("/home/travis/development/gnome-panel-extensions/container/" ,"GNOME_ExtensionContainer.xml",
        #                              None, [(_("About"), self.nothing), (_("Pref"), self.nothing),(_("Manage"), self._manageExtensionsDialog)])

        global run_in_window

        prefs_key = self.get_preferences_key()

        print "Applet preferences located at %s" % prefs_key

        if bundleFileName == None:
            client = gconf.client_get_default()
            
            try: bundleFileName = client.get(prefs_key + "/bundle_file")
            except:
                print "Could not get bundle file name from gconf"
                bundleFileName = None
        
            
        if not bundleFileName == None:
            try: 
                self.bundle = self.load_bundle(bundleFileName)
            except:
                print "Could not load " + bundleFileName
        else:
            self.bundle = None
            self.big_box = gtk.HBox()
            self.big_box.pack_start(gtk.Label("Menu"))
            self.toggle = gtk.ToggleButton()
            button_box = gtk.HBox()
            button_box.pack_start(gtk.Label(_("Load Extension")))
            self.toggle.add(button_box)
            self.toggle.connect("toggled", self._onLoadDialogToggle)

            self.big_box.add(self.toggle)

            self.load_window = manage_applets.AlignedWindow(self.toggle)
            self.load_window.set_modal(True)

            self.loader = manage_applets.ExtensionLoader(self)

            self.load_window.add(self.loader)
            self.loader.show()
            
            self.add(self.big_box)
            self.show_all()
            



        print "Load dialog started"
      
                            

        

        
        return True
    
    
    def load_bundle(self, bundleFileName=''):
        """
        Loads up bundle and returns initialized extension object.

        Returns a Bundle object, as defined in extension_container_globals
             
        """
        
        os.chdir(extension_container_globals.extension_dir)

        bundle = None
        
        widget = self.get_children()

        try: self.remove(widget[0]) #dirty
        except: print "Could not remove label"

        self.load_window.destroy()
        #except: print "Could not destroy load_dialog"

        bundle = extension_bundle.Bundle(bundleFileName)
            
        try: bundle = extension_bundle.Bundle(bundleFileName)
        except:
            print "Could not create bundle"

        if bundle:
            self.extension = bundle.get_extension()

            self.extension._register_container_applet(self)
            self.extension.setup_menu()

            self.add(self.extension)
            self.show_all()        	
    





            
    def nothing():
        pass


    def _onLoadDialogToggle(self, button):
        if self.toggle.get_active():
            self.load_window.positionWindow()
            self.load_window.show()
            self.load_window.grab_focus()
        else:
            self.load_window.hide()

    

            

gobject.type_register(ExtensionContainerApplet)

if len(sys.argv) == 2 and sys.argv[1] == "run-in-window":
	main_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
	main_window.set_title("Python Applet")
	main_window.connect("destroy", gtk.mainquit)
	app = ExtensionContainerApplet()
	app.init()


        
	main_window.add(app)
	
	main_window.show_all()

	gtk.main()
	sys.exit()


def foo(applet, iid):
    print "Returning container applet"
    return applet.init()

# run in seperate window for testing

def start_bundle(bundleName):
    global bundleFile
    global foo
    global ExtensionContainerApplet
    bundleFile = bundleName
    
    gnomeapplet.bonobo_factory("OAFIID:GNOME_ExtensionContainerApplet_Factory", 
                            ExtensionContainerApplet.__gtype__, 
                            "ExtensionContainer", "0", foo)


start_bundle("test.gpe")
print "Done waiting in factory, returning... If this seems wrong, perhaps there is another copy of the Container factory running?"

