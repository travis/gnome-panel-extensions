#!/usr/bin/env python
import pygtk
pygtk.require('2.0')


import sys, traceback
import os

import gtk
import gobject
import gconf
import gnomeapplet

import load_extensions
import extension_container_globals
import extension_bundle

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

        #if (__debug__):
        #    self.log = file("log.txt", 'w')

        self.loaded_bundle = None

        self.prefs_key = self.get_preferences_key()
        self.client = gconf.client_get_default()
        
        print "Applet preferences located at %s" % self.prefs_key

        if bundleFileName == None:

            
            try: bundleFileName = self.client.get_string(self.prefs_key + "/bundle_file")
            except:
                #if (__debug__):
                #    self.log.write(self.prefs_key + "/bundle_file\n")
                #    self.log.write("Could not get bundle file name from gconf")
                #    traceback.print_exc(file=self.log)
                bundleFileName = None
        
            
        if not bundleFileName == None:
            #if (__debug__):
            #    self.log.write(bundleFileName)
                
            try: 
                self.bundle = self.load_bundle(bundleFileName)
            except:
                print "Could not load " + bundleFileName
                #if (__debug__):
                #    self.log.write("Could not load " + bundleFileName + "\n")

                

        else:
            self.bundle = None
            self.big_box = gtk.HBox()
            self.big_box.pack_start(gtk.Label("Menu"))
            self.toggle = gtk.ToggleButton()
            button_box = gtk.HBox()
            button_box.pack_start(gtk.Label("Load Extension"))
            self.toggle.add(button_box)
            self.toggle.connect("toggled", self._onLoadDialogToggle)

            self.big_box.pack_start(self.toggle)

            self.load_window = load_extensions.AlignedWindow(self.toggle)
            self.load_window.set_modal(True)

            self.loader = load_extensions.ExtensionLoader(self)

            self.load_window.add(self.loader)
            self.loader.show()



            if (__debug__):
                print "Load window started"
            
            self.add(self.big_box)
            self.connect("destroy", self._cleanup)
            self.show_all()
        
        return True
    
    
    def load_bundle(self, bundleFileName=''):
        """
        Loads up bundle and returns initialized extension object.

        Returns a Bundle object, as defined in extension_bundle
             
        """

        if not os.path.isdir(extension_container_globals.extension_dir):
            os.mkdir(extension_container_globals.extension_dir)

        os.chdir(extension_container_globals.extension_dir)

        bundle = None
        
        widget = self.get_children()

        try: self.remove(widget[0])
        except: print "Could not remove label"

        try: self.load_window.destroy()
        except: print "Could not destroy load_dialog"

        bundle = extension_bundle.Bundle(bundleFileName)
            
        try: bundle = extension_bundle.Bundle(bundleFileName)
        except:
            print "Could not create bundle"

        if bundle:
            self.loaded_bundle = bundle
            
            self.extension = bundle.get_extension()

            self.extension._register_container_applet(self)

            self.extension.__extension_init__() #run the applet code
            

            self.add(self.extension)
            self.show_all()        	
    
    def get_loaded_bundle(self):
        if self.loaded_bundle:
            return self.loaded_bundle
        else:
            raise NoBundleLoadedError, "No bundle loaded, could not return"

    def _cleanup(self, uicomponent):
        self.client.remove_dir(self.prefs_key)



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

gnomeapplet.bonobo_factory("OAFIID:GNOME_ExtensionContainerApplet_Factory", 
                            ExtensionContainerApplet.__gtype__, 
                            "ExtensionContainer", "0", foo)



print "Done waiting in factory, returning... If this seems wrong, perhaps there is another copy of the Container factory running?"

