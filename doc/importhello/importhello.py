import pygtk
pygtk.require('2.0')

import gtk
import gobject

import panel_extension

import hello_globals



def return_extension():
    return ImportHelloExtension()
        
class ImportHelloExtension(panel_extension.PanelExtension):
    def __init__(self):
        self.__gobject_init__()
        panel_extension.PanelExtension.__init__(self)

    def __extension_init__(self):

        self.label = gtk.Label(hello_globals.hello_text())

        self.add(self.label)

        self.show_all()

gobject.type_register(ImportHelloExtension)
        





