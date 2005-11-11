#!/usr/bin/env python
'''
Extension Container Applet
(c) 2005 travis f vachon

The Extension Container applet is designed to load and run GNOME
Panel Extensions. See http://www.gnome.org/~tvachon for more
details on these.
'''
import pygtk
pygtk.require('2.0')


import sys, traceback
import os

import gtk
import gobject
import gconf
import gnomeapplet

from panel_extension import load_extensions
from panel_extension import extension_container_globals
from panel_extension import extension_bundle

import gettext
_ = gettext.gettext


if len(sys.argv) == 2 and sys.argv[1] == "run-in-window":
    run_in_window = True
else:
    run_in_window = False

class NoBundleLoadedError(Exception):
    '''
    Raised when some object requests a loaded bundle before a bundle has been loaded.
    '''
    def __init__(self, *args):
        Exception.__init__(self, *args)
        self.wrapped_exc = sys.exc_info()

    
  
class ExtensionContainerApplet(gnomeapplet.Applet):
    '''
    ExtensionContainerApplet is a classic GNOME panel applet that runs new
    GNOME panel extensions. 
    '''
    def __init__(self):
        self.__gobject_init__()


    def init(self, bundleFileName=None):

        self.loaded_bundle = None

        self.prefs_key = self.get_preferences_key()
        self.client = gconf.client_get_default()

        self.ui_manager = gtk.UIManager()

        print "Container applet preferences located at %s" % self.prefs_key

        self.connect("destroy", self._cleanup)

        

        if bundleFileName == None:

            
            try: bundleFileName = self.client.get_string(self.prefs_key + "/bundle_file")
            except:

                bundleFileName = None
        
            

                
        try:
            self.bundle = self.load_bundle(bundleFileName)
        except:
        
            #Build loader button
            
            self.bundle = None

            load_button = self.loadToggleButton()
            
            self.add(load_button)

            #self.ui_manager.add_ui_from_string()

            self.show_all()

            print self.get_control()
                    
        return True


    def loadToggleButton(self):
        self.toggle = gtk.ToggleButton()
        

        button_box = gtk.HBox()
        button_box.pack_start(gtk.Label(_("Choose Extension")))


        self.toggle.add(button_box)
        
        self.toggle.connect("toggled", self._onToggle)
        self.toggle.connect("button-press-event", self._onToggleButtonPress)

        return self.toggle
    

    def load_dialog_closed(self):
        try:
            self.toggle.set_active(False)
        except:
            print "Toggle probably not being used"

    
    
    def load_bundle(self, bundleFileName):
        """
        Loads up bundle and returns initialized extension object.

        Returns a Bundle object, as defined in extension_bundle
             
        """

        if not os.path.isdir(extension_container_globals.extension_dir):
            os.mkdir(extension_container_globals.extension_dir)

        os.chdir(extension_container_globals.extension_dir)

        if bundleFileName == None:
            raise StandardError
        
        bundle = None
        
        widget = self.get_children()

        try: self.remove(widget[0])
        except: print "Could not remove label"

        try: self.load_window.destroy()
        except: print "Could not destroy load_dialog"

        try: bundle = extension_bundle.Bundle(bundleFileName)
        except:
            print "Could not create bundle"
            traceback.print_exc()
            raise

        
        self.loaded_bundle = bundle
            
        self.extension = bundle._get_extension()

        self.client.set_string(self.prefs_key + "/bundle_file", bundleFileName)


        self.extension._register_container_applet(self)
        self.add(self.extension)
        self.show_all()

        self.extension.__extension_init__() #run the applet code
            


    
    def get_loaded_bundle(self):
        if self.loaded_bundle:
            return self.loaded_bundle
        else:
            raise NoBundleLoadedError, "No bundle loaded, could not return"

    def _cleanup(self, uicomponent):
        
        print str(self.client) + " removing "+self.prefs_key+" in applet container"
        self.client.remove_dir(self.prefs_key)


        
    def _onToggle(self, toggle):
        if toggle.get_active():
            self.load_window = load_extensions.ExtensionLoaderDialogVBox(self)
            self.load_window.show()
            self.load_window.grab_focus()
        else:
            self.load_window.destroy()


    def _onToggleButtonPress(self, toggle, event):
        if event.button != 1:
            toggle.stop_emission("button-press-event")


        
            

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

gnomeapplet.bonobo_factory("OAFIID:GNOME_ExtensionContainerApplet_Factory", 
                            ExtensionContainerApplet.__gtype__, 
                            "ExtensionContainer", "0", foo)



print "Done waiting in factory, returning... If this seems wrong, perhaps there is another copy of the Container factory running?"

