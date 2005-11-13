import pygtk
pygtk.require('2.0')

import gtk
import gobject

import panel_extension



def return_extension():
    return ImportHelloExtension()
        
class ImportHelloExtension(panel_extension.PanelExtension):
    def __init__(self):
        self.__gobject_init__()
        panel_extension.PanelExtension.__init__(self)

    def __extension_init__(self):

        bundle = self.get_bundle()

        image = bundle.open_gtk_image("hello.png")

        self.add(image)

        self.show_all()

gobject.type_register(ImportHelloExtension)
        





