#!/usr/bin/env python
import pygtk
pygtk.require('2.0')


import sys
import os
os.chdir("/home/travis/development/gnome-panel-extensions/container/")
os.chdir("/home/travis/.panelextensions/")
import gtk
import gobject
import gnomeapplet
import bonobo
import Bonobo

import zipfile

import manage_applets
import extension_container_globals

import gettext
_ = gettext.gettext

bundleFile = None
  
class ExtensionContainerApplet(gnomeapplet.Applet):
    '''
    ExtensionContainerApplet is a classic GNOME panel applet that runs new
    GNOME panel extensions. 
    '''
    def __init__(self):
        self.__gobject_init__()
        
    def init(self, bundleFileName=None):
        self.setup_menu_from_file ("/home/travis/development/gnome-panel-extensions/container/" ,"GNOME_ExtensionContainer.xml",
                                   None, [(_("About"), self.nothing), (_("Pref"), self.nothing),(_("Manage"), self._manageExtensionsDialog)])
        
        self.load_bundle("test.gpe")#bundleFileName)

        sys.exit()
        #except:
        #    label = gtk.Label("No bundle loaded")
        #    self.add(label)

        
        self.prefs_key = self.get_preferences_key()
        print "Applet prefs located at %s" % (self.prefs_key)


        #bonobo.activate()
        #print dir(bonobo)
        #   list = bonobo.activation.query("has(repo_ids, 'IDL:GNOME/Vertigo/PanelShell:1.0')")
        #  for i in list: print dir(i)
        #panel = bonobo.get_object ('OAFIID:GNOME_PanelShell','Bonobo/Unknown')

        #        print dir(panel)
        #print dir(panel)
        self.show_all()        	

        

        
        return True
    
    
    def load_bundle(self, bundleFileName):
        """
        Loads up bundle and returns initialized extension object
        """

        if not zipfile.is_zipfile(bundleFileName):
            print "Sorry, ", bundleFileName, "is not a gnome-extension-bundle file"
        else:
            widget = self.get_children()

            try: self.remove(widget[0]) #dirty 
            except: print "could not remove label"

            sys.path.insert(0, bundleFileName)

            manifest_file = open("manifest.gpem", 'r')

            print manifest_file.read()
            
            
            try:
                import __extension_init__ as bundleInit
                self.bundleFile = zipfile.ZipFile(bundleFileName)
                label = gtk.Label("Loaded " + bundleFileName)
                self.add(label)
                self.show_all()
                
            except:
                label = gtk.Label("Could not load " + bundleFileName)
                self.add(label)
                self.show_all()

            return bundleInit
        
#    def setup_extension_menu(self):
#        """
#        setup_context_menu_from_file uses a variable defined in the init.py file
#        in a bundle to find the variables needed to use gnomeapplet.Applet's
#        setup_menu function. It will also unpack the needed file
#        and import the xml into menu_xml
#        """
#        if self.bundleInit:
#
#            xml_menu_name = str(self.bundleFile.read(self.bundleInit.xml_menu_file_name))
#            print xml_menu_name
#            self.setup_menu(xml_menu_name, [(_("Test"), self.nothing)],None)
#
#            
#
#            
#
#        
#        #       print "Could not load bundle menu"
#        else:
#            print "Bundle not loaded, could not create menu"
#
#    def setup_extension_menu_from_file(self, xml_menu_file_name, verbs):
#        if self.bundleInit:
#            #change the working directory to /tmp
#            old_wd = os.getcwd()
#            os.chdir("/tmp/")
#            #temporarily expand the xml file
#            
#            temp_xml_menu_file = open (xml_menu_file_name, 'w')
#            temp_xml_menu_file.write(self.bundleFile.read(xml_menu_file_name))
#            temp_xml_menu_file.close()
#
#
#            self.setup_menu_from_file (os.getcwd() ,xml_menu_file_name, None, verbs)
#            
#            #cleanup on aisle 10
#            os.remove(xml_menu_file_name)
#            #change the working directory back
#            os.chdir(old_wd)
#        else:
#            print "Bundle not loaded, could not create menu"
            
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
    return applet.init("test.gpe")

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

