import pygtk
pygtk.require('2.0')

import gtk
import gobject

import panel_extension



def return_extension():
    return HelloExtension()
        
class HelloExtension(panel_extension.PanelExtension):
    def __init__(self):
        self.__gobject_init__()
        panel_extension.PanelExtension.__init__(self)

    def __extension_init__(self):
        self.bundle = self.get_bundle()
        
        menu_file = self.bundle.open("hello.xml")

        self.setup_extension_menu_from_file (menu_file,
                                            [("Sweet", self._sweet),])

        self.label = gtk.Label("Hello, World!")
        
        self.add(self.label)

        self.show_all()
        
    def _sweet(self, uicomponent, verb):
        self.label.set_text("Sweet!")



gobject.type_register(HelloExtension)

