#!/usr/bin/env python
import pygtk
pygtk.require('2.0')

import gtk
import gobject
import gnome
import gnome.ui
import gnomeapplet
import gconf
import string  # maybe someone can do this trick without string?

        
class ExtensionContainerApplet(gnomeapplet.Applet):
    def __init__(self):
        self.__gobject_init__()

    def init(self):
        
        self.show_all()


        return True
    
            

gobject.type_register(ExtensionContainerApplet)


def foo(applet, iid):
    print "Returning blogger applet"
    return applet.init()

gnomeapplet.bonobo_factory("OAFIID:GNOME_ExtensionContainerApplet_Factory", 
                            ExtensionContainerApplet.__gtype__, 
                            "ExtensionContainer", "0", foo)

print "Done waiting in factory, returning... If this seems wrong, perhaps there is another copy of the Blog factory running?"
