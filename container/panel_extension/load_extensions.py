'''
load_extensions module
(c) 2005 travis f vachon

The load_extensions module provides a class derived from gtk.Dialog that
creates a dialog to select and load panel applets.
'''
import os
import sys

if (__debug__):
    import traceback
    
import dircache #could use os.listdir, but this is nicer
import gtk
import gobject

import extension_container_globals
import extension_bundle

import gettext
_ = gettext.gettext


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








