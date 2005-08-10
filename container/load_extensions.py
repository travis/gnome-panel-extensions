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


        

class ExtensionLoader(gtk.Frame):
    def __init__(self, extension_container):
        gtk.Frame.__init__(self)
        print str(self.get_parent())
        self.set_shadow_type(gtk.SHADOW_OUT)
        
        global gconf_prefix
        self.gconf_prefix = extension_container.get_preferences_key()

        print "Applet preferences located at " + self.gconf_prefix
        
        self.gconf_client = gconf.client_get_default()

        #set up interface

        (
            self.EXT_DESCRIPTION_COLUMN,
            self.BUNDLE_NAME_COLUMN,
            self.NUM_COLUMNS
        ) = range(3)

        extension_list_model = gtk.TreeStore(gobject.TYPE_STRING,
                                             gobject.TYPE_STRING)

      
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

        extension_list = []
        
        for bundle in bundle_list:
                                 
      
            try: ext_name = bundle.name
            except: ext_name = "No name found"

            try: ext_desc = bundle.description
            except: ext_desc = "No description found"

            cell_string = "<b>" + ext_name + "</b>\n<i>" + ext_desc + "</i>"

            itera = extension_list_model.append(None)
            extension_list_model.set(itera,
                                     self.EXT_DESCRIPTION_COLUMN, cell_string,
                                     self.BUNDLE_NAME_COLUMN, bundle.bundle_file_name)

            

        extension_tree_view = gtk.TreeView(extension_list_model)


        extension_tree_view.set_hover_selection(True)

        extension_tree_view.connect("row-activated", self._on_item_clicked, extension_list_model, extension_container)
        
        renderer = gtk.CellRendererText()
        renderer.set_property("xalign", 0.0)



        column = gtk.TreeViewColumn("Double click item to load", renderer, markup=self.EXT_DESCRIPTION_COLUMN)
        column.set_clickable(True)

        extension_tree_view.append_column(column)

        renderer = gtk.CellRendererText()
        renderer.set_property("visible", False)

        column = gtk.TreeViewColumn("Bundle Name", renderer, text=self.BUNDLE_NAME_COLUMN)
        

        self.add(extension_tree_view)

        self.show_all()


    def _on_item_clicked(self, treeview, path, view_column, model, extension_container):

        itera = model.get_iter(path)

        bundle_name = model.get_value(itera, self.BUNDLE_NAME_COLUMN)

        
        #try:
        extension_container.load_bundle(bundle_name)
        #except:
        #    print "Could not load " + bundle_name
        #    return 
        conf_value = gconf.Value(gconf.VALUE_STRING)

        conf_value.set_string(bundle_name)

        
        self.gconf_client.set_string(self.gconf_prefix + "/bundle_file", bundle_name)
        
        

