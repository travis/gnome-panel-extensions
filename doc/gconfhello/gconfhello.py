import pygtk
pygtk.require('2.0')

import gtk
import gobject
import gconf

import panel_extension

def return_extension():
    return ImportHelloExtension()
        
class ImportHelloExtension(panel_extension.PanelExtension):
    def __init__(self):
        self.__gobject_init__()
        panel_extension.PanelExtension.__init__(self)

    def __extension_init__(self):


        self.client = gconf.client_get_default()
        
        self.prefs_key = self.get_preferences_key("/gconf_hello_extension")

        use_image = self.client.get_bool(self.prefs_key+"/useimage")

        if use_image:
            
            bundle = self.get_bundle()
            
            image = bundle.open_gtk_image("hello.png")
            
            self.add(image)

            self.client.set_bool(self.prefs_key+"/useimage", False)
            
        else:
            label = gtk.Label("I'm text!")

            self.add(label)

            self.client.set_bool(self.prefs_key+"/useimage", True)

        self.show_all()

gobject.type_register(ImportHelloExtension)
        





