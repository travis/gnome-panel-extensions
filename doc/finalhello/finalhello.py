import pygtk
pygtk.require('2.0')

import gtk
import gobject
import gconf

import panel_extension
import hello_globals

def return_extension():
    return ImportHelloExtension()
        
class ImportHelloExtension(panel_extension.PanelExtension):
    def __init__(self):
        self.__gobject_init__()
        panel_extension.PanelExtension.__init__(self)

    def __extension_init__(self):
        self.bundle = self.get_bundle()

        menu_file = self.bundle.open("hello.xml")

        self.setup_extension_menu_from_file (menu_file,
                                            [("Sweet", self._sweet),])

        
        self.client = gconf.client_get_default()
        
        self.prefs_key = self.get_preferences_key("/final_hello_extension")

        use_image = self.client.get_bool(self.prefs_key+"/useimage")

        if use_image:
            

            
            image = self.bundle.open_gtk_image("hello.png")
            
            self.add(image)

            self.client.set_bool(self.prefs_key+"/useimage", False)
            
        else:
            self.label = gtk.Label(hello_globals.hello_text())

            self.add(self.label)

            self.client.set_bool(self.prefs_key+"/useimage", True)

        self.show_all()


    def _sweet(self, uicomponent, verb):
        try:
            self.label.set_text("Sweet!")
        except:
            pass


gobject.type_register(ImportHelloExtension)
        





