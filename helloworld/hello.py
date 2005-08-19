#!/usr/bin/env python
import pygtk
pygtk.require('2.0')

import gtk
import gobject

import panel_extension





def return_extension():
    return HelloApplet()
        
class HelloApplet(panel_extension.PanelExtension):
    def __init__(self):
        self.__gobject_init__
        panel_extension.PanelExtension.__init__(self)

    def _sweet(self):
        pass

    def __extension_init__(self):

        self.bundle = self.get_bundle()

        menu_file = self.bundle.open("hello.xml")

        self.setup_extension_menu_from_file (menu_file,
                                            [("Sweet", self._sweet),])

        self.label = gtk.Label("Hello, World! This is a longer fuckin label!")

        self.add(self.label)

        self.show_all()
        
        return True


gobject.type_register(HelloApplet)


