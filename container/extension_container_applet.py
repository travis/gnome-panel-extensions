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
import StringIO

import xml.dom.minidom

import bonobo
import Bonobo

import zipfile

import manage_applets
import extension_container_globals

import gettext
_ = gettext.gettext



class InvalidBundle(StandardError):
    '''
    Used to indicate a bundle is either non-existent or is missing
    a necessary piece.
    '''

class Bundle(object):
    '''
    Bundle is a class to contain a bundle which provides
    methods to allow for easy extraction of files
    from the bundle.
    '''
    def __init__(self, bundleFileName):
        # Check sanity of bundle file        
        if zipfile.is_zipfile(bundleFileName):
            self.bundleFile = zipfile.ZipFile(bundleFileName)

            print bundleFileName

            sys.path.insert(0, os.path.join(extension_container_globals.extension_dir, bundleFileName))
            # Allows us to import python scripts in the bundle file
            # as if they were in a directory
            
            
        else:
           
            print "Sorry, ", bundleFileName, "is not a gnome-extension-bundle file"
            raise InvalidBundle, bundleFileName+"is not a zip file"

        if not self.bundleFile.namelist().count("manifest.gpem") == 1:
            print "Raise NOT A BUNDLE exception"
            # Since all bundles must contain manifest.gpem
            raise InvalidBundle, "Bundle does not contain manifest.gpem"
        
        

        self.manifest_dom = xml.dom.minidom.parseString(self.bundleFile.read('manifest.gpem'))
        bundleFileList = self.manifest_dom.getElementsByTagName('file')

        for fileElement in bundleFileList:
            fileType = fileElement.getAttribute('type')
            
            if fileType == 'main':
                
                try:
                    module_name = fileElement.getAttribute('name').split('.')
                    
                    if module_name[1] == 'py':
                        module_name = module_name[0]
                    else:
                        print "Raise exception"
                        return
                    
                    self.main_module = __import__(module_name)
                    
                    
                    
                except:
                    print "Could not import main module"
                    raise 
        

    def info(self):
        print self.manifest_dom

    def get_extension(self):
        return self.main_module.return_extension(self)
        

    def open(self, filename):
        return StringIO.StringIO(self.bundle_file.read(filename))
  
class ExtensionContainerApplet(gnomeapplet.Applet):
    '''
    ExtensionContainerApplet is a classic GNOME panel applet that runs new
    GNOME panel extensions. 
    '''
    def __init__(self):
        self.__gobject_init__()

    def init(self, bundleFileName=''):
    #    self.setup_menu_from_file ("/home/travis/development/gnome-panel-extensions/container/" ,"GNOME_ExtensionContainer.xml",
     #                              None, [(_("About"), self.nothing), (_("Pref"), self.nothing),(_("Manage"), self._manageExtensionsDialog)])
        
        self.bundle = self.load_bundle(bundleFileName)

        self.extension = self.bundle.get_extension()

        self.extension._register_container_applet(self)
        self.extension.setup_menu()

        self.add(self.extension)

        #sys.exit()
        #except:
        #    label = gtk.Label("No bundle loaded")
        #    self.add(label)

        
        self.prefs_key = self.get_preferences_key()
        print "Applet prefs located at %s" % (self.prefs_key)


        self.show_all()        	

        

        
        return True
    
    
    def load_bundle(self, bundleFileName=''):
        """
        Loads up bundle and returns initialized extension object.
        Returns a manifest dom object which appears to be the bundle.

        Methods included in the dom object 'd' include:
             d.getElementByTagName(tagName)
             
        """
        
        os.chdir(extension_container_globals.extension_dir)

        bundle = None
        
        widget = self.get_children()

        try: self.remove(widget[0]) #dirty 
        except:
            print "could not remove label"
            
        try: bundle = Bundle(bundleFileName)
        except:
            print "Could not create bundle"
            label = gtk.Label("Could not load " + bundleFileName)
            self.add(label)
            self.show_all()
            raise

        return bundle



            
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

