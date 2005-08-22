import pygtk
try: pygtk.require('2.0')
except: pass
import gtk

import zipfile
import sys
import os
import extension_container_globals

import StringIO
class InvalidBundle(StandardError):
    '''
    Used to indicate a bundle is either non-existent or is missing
    a necessary piece.
    '''

class Bundle(object):
    '''
    Bundle is a class to contain a bundle which provides
    methods to allow for easy extraction of files
    from the bundle.
    '''
    def __init__(self, bundle_file_name):
        # Check sanity of bundle file        
        if zipfile.is_zipfile(bundle_file_name):
            self.bundle_file = zipfile.ZipFile(bundle_file_name)

        else:
           
            print "Sorry, ", bundle_file_name, "is not a gnome-extension-bundle file"
            raise InvalidBundle, bundle_file_name+" is not a zip file."

        if not self.bundle_file.namelist().count("manifest.xml") == 1:
     
            # Since all bundles must contain manifest.xml
            raise InvalidBundle, "Bundle does not contain manifest.xml"

        #Looks like bundle is sane. Sweet.
        
        sys.path.insert(0, os.path.join(extension_container_globals.extension_dir, bundle_file_name))
        # Allows us to import python scripts in the bundle file
        # as if they were in a directory
        
        self.init = __import__("__bundle_init__")
        del sys.modules["__bundle_init__"]

        self.name = self.init.name
        self.description = self.init.description


    def get_extension(self):
        self.main_script = __import__(self.init.main_script)
        del sys.modules[self.init.main_script]

        return self.main_script.return_extension()
        

    def open(self, filename):
        return StringIO.StringIO(self.bundle_file.read(filename))

    def open_gtk_image(self, filename):
        pixbuf_l = gtk.gdk.PixbufLoader()

        pixbuf_l.write(self.bundle_file.read(filename))

        pixbuf = pixbuf_l.get_pixbuf()

        pixbuf_l.close()

        image = gtk.Image()

        image.set_from_pixbuf(pixbuf)

        return image

        
