#!/usr/bin/env python
import pygtk
pygtk.require('2.0')

import gtk
import gobject
import gnome
import gnome.ui
import gnomeapplet
import gconf
import panel_extension
import string  # maybe someone can do this trick without string?

from gettext import gettext as _, bindtextdomain, textdomain

from gnomeblog import blog_poster
from gnomeblog import aligned_window
from gnomeblog import blogger_prefs
from gnomeblog import gnome_blog_globals

bindtextdomain('gnome-blog', gnome_blog_globals.localedir)
textdomain('gnome-blog')

icon_theme = gtk.icon_theme_get_default()
icon_info = icon_theme.lookup_icon('gnome-blog', -1, 0)
gtk.window_set_default_icon_from_file(icon_info.get_filename())

def return_extension():
    return BloggerApplet()
        
class BloggerApplet(panel_extension.PanelExtension):
    def __init__(self):
        self.__gobject_init__
        panel_extension.PanelExtension.__init__(self)


    def __extension_init__(self):

        self.mybundle = self.get_bundle()

        menu_file = self.mybundle.open("GNOME_BlogApplet.xml")

        self.setup_extension_menu_from_file (menu_file,
                                            [(_("About"), self._showAboutDialog),
                                             ("Pref", self._openPrefs)])

        self.toggle = gtk.ToggleButton()
        self.applet_tooltips = gtk.Tooltips()

        button_box = gtk.HBox()
        button_box.pack_start(gtk.Label(_("Blog")))
        self.arrow = gtk.Arrow(gtk.ARROW_DOWN, gtk.SHADOW_IN)
        button_box.pack_start(self.arrow)

        self.toggle.add(button_box)
        
        self.add(self.toggle)
        self.toggle.connect("toggled", self._onToggle)
        self.toggle.connect("button-press-event", self._onButtonPress)
        
        self.show_all()

        self.poster_window = aligned_window.AlignedWindow(self.toggle)
        self.poster_window.set_modal(True)
        accel_group = gtk.AccelGroup()
        self.poster_window.add_accel_group(accel_group)
        prefs_prefix = self.get_preferences_prefix()
        self.prefs_key = prefs_prefix + "/blog_poster_extension"
        print "Applet prefs located at %s" % (self.prefs_key)
        self.poster = blog_poster.BlogPoster(prefs_key=self.prefs_key, on_entry_posted=self._onEntryPosted)
        self.poster_window.add(self.poster)
        self.poster.show()

        self.client = gconf.client_get_default()
        value = self.client.get_bool(self.prefs_key + "/initialized")
        if value == None or value == False:
#            self.poster._showPrefDialog()
#            self._showPrefDialog()
            self.client.set_bool(self.prefs_key + "/initialized", True)

#        self._createToolTip(client)
        
        return True
    
    
    

    def _showAboutDialog(self, uicomponent, verb):
        gnome.ui.About(gnome_blog_globals.name, gnome_blog_globals.version, "Copyright 2003 Seth Nickell",
                       _("A GNOME Web Blogging Applet"),["Seth Nickell <seth@gnome.org>"],[],
                       "",gtk.gdk.pixbuf_new_from_file(gnome_blog_globals.image_dir + "/gnome-blog.png")).show()

    def _showPrefDialog(self):
        prefs_dialog = blogger_prefs.BloggerPrefs(self.prefs_key)
        prefs_dialog.show()
        prefs_dialog.run()
        prefs_dialog.hide()
        
    def _openPrefs(self, uicomponent, verb):
        self._showPrefDialog()
        
    def _onToggle(self, toggle):
        if toggle.get_active():
            self.poster_window.positionWindow()            
            self.poster_window.show()
            self.poster.grab_focus()
        else:
            self.poster_window.hide()

    def _onEntryPosted(self):
        self.toggle.set_active(False)

    def _onButtonPress(self, toggle, event):
        if event.button != 1:
            toggle.stop_emission("button-press-event")
            
    def _createToolTip(self,client):
        # take the XML_RPC value from GConf
        blog_url = client.get_string(self.prefs_key + "/xmlrpc_url")
        # split the URL up into http:, '', domainname, extra
        blog_split = string.split(blog_url,"/",3);
        # join back up the URL into http://domainname
        blog_url = string.join(blog_split[:3],"/")

        tooltip = _("Create a blog entry for %s at %s") % \
                  ( client.get_string(self.prefs_key + "/blog_username"), \
                    blog_url )
        
        # Set tooltip to the applet button
        self.applet_tooltips.set_tip(self.toggle,tooltip)        

        

gobject.type_register(BloggerApplet)


