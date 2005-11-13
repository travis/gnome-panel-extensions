#!/usr/bin/env python
'''Extension Container Applet.
(c) 2005 Travis F Vachon

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


The Extension Container applet is designed to load and run GNOME
Panel Extensions. See http://www.gnome.org/~tvachon for more
details on these.
'''
import pygtk
pygtk.require('2.0')


import sys, traceback
import os
import dircache

import gtk
import gobject
import gconf
import gnomeapplet

from panel_extension import extension_container_globals
from panel_extension import extension_bundle

import gettext
_ = gettext.gettext


if len(sys.argv) == 2 and sys.argv[1] == "run-in-window":
    run_in_window = True
else:
    run_in_window = False

class NoBundleLoadedError(Exception):
    '''Raised when some object requests a loaded bundle before a bundle has been loaded.
    '''
    def __init__(self, *args):
        Exception.__init__(self, *args)
        self.wrapped_exc = sys.exc_info()



class AppletDescription(gtk.EventBox):
    def __init__(self, extension_loader, bundle, bundle_name):
        gtk.EventBox.__init__(self)
        self.extension_loader = extension_loader
        self.bundle_name = bundle_name
        self.bundle = bundle
        if (__debug__):
            print bundle_name
            print str(bundle)

        self.set_above_child(True)
        
        self.hbox = gtk.HBox()
        self.hbox.set_size_request(400,-1)
        name = bundle.name
        description = bundle.description
        
        self.label = gtk.Label()
        self.label.set_line_wrap(True)
        self.label.set_markup("<b>" + name +"</b>" + "\n" + "<i>" + description + "</i>")
        self.label.set_alignment(0,0.5)

        


        preview_align = gtk.Alignment(0.5,0.5,0,0)
        preview_align.set_size_request(150, 94)

        #set up live preview. This actually embeds a copy of the applet
        #within the applet description. We slap an event box over it
        #so we don't get wierdness...
        try:
            self.live_preview = self.bundle._get_extension()
            self.live_preview._register_bundle(self.bundle)
            self.live_preview._set_live_preview(True)
            
        
            self.live_preview.__extension_init__()

            preview_align.add(self.live_preview)
        except:
            print "Could not create live preview"
            traceback.print_exc()

            try:
                icon = self.bundle.get_icon()
                preview_align.add(icon)
            except:
                print "Could not get icon file."
                

        self.hbox.pack_start(preview_align, expand=False, fill=False)

        self.hbox.pack_start(self.label, expand=False, fill=False)
        
        self.add(self.hbox)
        self.hbox.show_all()

        self.white = self.get_style().white
        self.tint = self.get_style().black

        self.modify_bg(gtk.STATE_NORMAL, self.white)
        
        self.show()

        self.old_fg = self.label.get_style().fg[0]

        self.connect("enter-notify-event", self._onEnter)
        self.connect("leave-notify-event", self._onLeave)
        self.connect("button-press-event", self._onButtonPress)

    def _onEnter(self, widget, event):
        
        self.label.modify_fg(gtk.STATE_NORMAL, self.white)
        self.modify_bg(gtk.STATE_NORMAL, self.tint)
        return True

    def _onLeave(self, widget, event):
        self.label.modify_fg(gtk.STATE_NORMAL, self.old_fg)
        self.modify_bg(gtk.STATE_NORMAL, self.white)
        return True

    def _onButtonPress(self, widget, event):
        self.extension_loader.load_bundle(self.bundle_name)
        return True

        

class ExtensionLoaderDialogVBox(gtk.Dialog):        
    def __init__(self, extension_container):
        gtk.Dialog.__init__(self,
                            title="Choose Extension",
                            parent=None,
                            buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_DELETE_EVENT))
        self.GET_NEW_EXTENSIONS_EVENT = 1
        self.add_button("Get New Extensions...", self.GET_NEW_EXTENSIONS_EVENT)
        self.connect('response', self._onResponse)
        self.connect('destroy', self._cleanup)

        self.extension_container = extension_container

        

        if os.path.exists(extension_container_globals.extension_dir):
            print "Found extension directory"
        else:
            os.mkdir(extension_container_globals.extension_dir, 0777)
            print "Created extension directory" + extension_container_globals.extension_dir

        os.chdir(extension_container_globals.extension_dir)
        
        extension_dir_list = dircache.listdir(extension_container_globals.extension_dir)

        self.desc_box = gtk.VBox()

        self.bundle_list = []
        self.description_list = []
        for bundle_name in extension_dir_list:
            if bundle_name.endswith(".gpe"):
                #bad sanity test, but more will occur in Bundle.__init__():
                try:
                    # a little bit of black magic...
                    # we need to give each module its own
                    # execution environment. this can probably be done
                    # with a sandbox at some point. in fact, that would
                    # probably be a good idea, given that we are executing
                    # arbitrary code without the user's input via livepreview

                    old_sys_modules = {}
                    for key in sys.modules:
                        old_sys_modules[key] = sys.modules[key]
                       
                   
                    
                    
                    try:
                        bundle = extension_bundle.Bundle(bundle_name)
                        self.bundle_list.append(bundle)
                        applet_desc = AppletDescription(self, bundle, bundle_name)
                        
                        self.description_list.append(applet_desc)
                        
                        self.desc_box.pack_start(applet_desc, expand=False, fill=False)

                    except:
                        print "Could not add " + bundle_name + " to list"
                        if (__debug__):
                            print "Exception:"
                            traceback.print_exc()
                finally:
                    sys.modules.clear()
                    for key in old_sys_modules:
                        sys.modules[key] = old_sys_modules[key]



        scroller = gtk.ScrolledWindow()
        scroller.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        scroller.set_size_request(-1, 300)

        scroller.add_with_viewport(self.desc_box)
                
        self.vbox.pack_start(scroller)

        self.vbox.show_all()

        self.show_all()

    def _onResponse(self, dialog, response_id):
        if response_id == gtk.RESPONSE_DELETE_EVENT:
        
            self.destroy()
        elif response_id == self.GET_NEW_EXTENSIONS_EVENT:
            import gnome
            gnome.url_show("http://panelextensions.gnome.org")
            self.destroy()
            
    def _cleanup(self, dialog):
        
        self.extension_container.load_dialog_closed()

    def load_bundle(self, bundle_file_name):
        try:
            self.extension_container.load_bundle(bundle_file_name)
        except:
            print "Could not load " + bundle_file_name
            raise

  
class ExtensionContainerApplet(gnomeapplet.Applet):
    '''ExtensionContainerApplet is a classic GNOME panel applet that runs new GNOME panel extensions.

    This class is meant to be used as is, and should probably not be modified except for bug fixes.
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

            self.show_all()

            print self.get_control()
                    
        return True


    def loadToggleButton(self):
        '''Construct button to launch the extension selection dialog.'''
        self.toggle = gtk.ToggleButton()
        

        button_box = gtk.HBox()
        button_box.pack_start(gtk.Label(_("Choose Extension")))


        self.toggle.add(button_box)
        
        self.toggle.connect("toggled", self._onToggle)
        self.toggle.connect("button-press-event", self._onToggleButtonPress)

        return self.toggle
    

    def load_dialog_closed(self):
        '''Callback for close button of extension selection dialog.'''
        try:
            self.toggle.set_active(False)
        except:
            print "Toggle probably not being used"

    
    
    def load_bundle(self, bundleFileName):
        """Loads up bundle and returns initialized extension object.

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
        '''Utility function to make bundle object available to panel_extension module.'''
        if self.loaded_bundle:
            return self.loaded_bundle
        else:
            raise NoBundleLoadedError, "No bundle loaded, could not return"

    def _cleanup(self, uicomponent):
        
        print str(self.client) + " removing "+self.prefs_key+" in applet container"
        self.client.remove_dir(self.prefs_key)


        
    def _onToggle(self, toggle):
        if toggle.get_active():
            self.load_window = ExtensionLoaderDialogVBox(self)
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


def return_applet(applet, iid):
    print "Returning container applet"
    return applet.init()



gnomeapplet.bonobo_factory("OAFIID:GNOME_ExtensionContainerApplet_Factory", 
                            ExtensionContainerApplet.__gtype__, 
                            "ExtensionContainer", "0", return_applet)



print "Done waiting in factory, returning... If this seems wrong, perhaps there is another copy of the Container factory running?"

