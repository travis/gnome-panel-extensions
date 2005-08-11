import os
import sys
import dircache #could use os.listdir, but this is nicer
import gtk
import gtk.glade
import gobject
import gconf
import extension_container_globals

import gettext
_ = gettext.gettext



gconf_prefix = None
import gtk

class AlignedWindow(gtk.Window):
    '''
    This class shamelessly ripped from the gnomeblog python module by ....
    FIXME add citations
    '''
    def __init__(self, widgetToAlignWith):
        gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
        self.set_decorated(False)
        
        self.widgetToAlignWith = widgetToAlignWith

    def positionWindow(self):
        # Get our own dimensions & position
        self.realize()
        gtk.gdk.flush()
        ourWidth  = (self.window.get_geometry())[2]
        ourHeight = (self.window.get_geometry())[3]

        # Get the dimensions/position of the widgetToAlignWith
        self.widgetToAlignWith.realize()
        (entryX, entryY) = self.widgetToAlignWith.window.get_origin()
        entryWidth  = (self.widgetToAlignWith.window.get_geometry())[2]
        entryHeight = (self.widgetToAlignWith.window.get_geometry())[3]

        # Get the screen dimensions
        screenHeight = gtk.gdk.screen_height()
        screenWidth = gtk.gdk.screen_width()

        if entryX + ourWidth < screenWidth:
            # Align to the left of the entry
            newX = entryX
        else:
            # Align to the right of the entry
            newX = (entryX + entryWidth) - ourWidth

        if entryY + entryHeight + ourHeight < screenHeight:
            # Align to the bottom of the entry
            newY = entryY + entryHeight
        else:
            newY = entryY - ourHeight

        # -"Coordinates locked in captain."
        # -"Engage."
        self.move(newX, newY)
        self.show()


class AppletDescription(gtk.EventBox):
    def __init__(self, extension_loader, bundle_name, name="No name", description="No Description"):
        gtk.EventBox.__init__(self)
        self.extension_loader = extension_loader
        self.bundle_name = bundle_name
        
        self.label = gtk.Label()
        self.label.set_markup("<b>" + name +"</b>" + "\n" + "<i>" + description + "</i>")
        self.add(self.label)
        self.label.show()
        self.show()

        self.old_fg = self.label.get_style().fg[0]
        self.old_bg = self.get_style().bg[0]

        self.connect("enter-notify-event", self._onEnter)
        self.connect("leave-notify-event", self._onLeave)
        self.connect("button-press-event", self._onButtonPress)

    def _onEnter(self, widget, event):
        self.old_fg = self.label.get_style().fg[0]
        self.old_bg = self.get_style().bg[0]

        self.label.modify_fg(gtk.STATE_NORMAL, self.get_style().white)
        self.modify_bg(gtk.STATE_NORMAL, self.get_style().dark[0])
        return True

    def _onLeave(self, widget, event):
        self.label.modify_fg(gtk.STATE_NORMAL, self.old_fg)
        self.modify_bg(gtk.STATE_NORMAL, self.old_bg)
        return True

    def _onButtonPress(self, widget, event):
        self.extension_loader.load_bundle(self.bundle_name)
        return True
        
        

class ExtensionLoader(gtk.Frame):
    def __init__(self, extension_container):
        gtk.Frame.__init__(self)

        self.extension_container = extension_container

        self.gconf_prefix = extension_container.get_preferences_key()
        print "Applet preferences located at " + self.gconf_prefix
        
        self.gconf_client = gconf.client_get_default()

        #set up interface

        self.set_shadow_type(gtk.SHADOW_OUT)
        
      
        if os.path.exists(extension_container_globals.extension_dir):
            print "Found extension directory"
        else:
            os.mkdir(extension_container_globals.extension_dir, 0777)
            print "Created extension directory" + extension_container_globals.extension_dir

        sys.path.insert(0, extension_container_globals.extension_dir)
        extension_dir_list = dircache.listdir(extension_container_globals.extension_dir)

        bundle_list = []

        
        for bundle_name in extension_dir_list:
            if bundle_name.endswith(".gpe"):

                bundle_path = os.path.join(extension_container_globals.extension_dir, bundle_name)

                sys.path.insert(0, bundle_path)
                try:
                    bundle_list.append(__import__("__bundle_init__"))
                    del sys.modules["__bundle_init__"]

                except:
                    print "Could not load " + bundle_name
                    
                sys.path.remove(bundle_path)
                #if we don't do this, __import__ will just create more references to the first thing we import

        self.label_box = gtk.VBox()
        
        for bundle in bundle_list:
                                 
      
            try: ext_name = bundle.name
            except: ext_name = "No name found"

            try: ext_desc = bundle.description
            except: ext_desc = "No description found"

            

            applet_desc = AppletDescription(self, bundle.bundle_file_name, ext_name, ext_desc)
            
            self.label_box.pack_start(applet_desc)
            


        self.label_box.show_all()
        self.add(self.label_box)
        self.show_all()


    def load_bundle(self, bundle_file_name):
        try:
            self.extension_container.load_bundle(bundle_file_name)
        except:
            print "Could not load " + bundle_file_name
            return 

                
        self.gconf_client.set_string(self.gconf_prefix + "/bundle_file", bundle_file_name)
        

        

