class User(object):

    def __init__(self):
        self.username = None
        self.password = None
        self.email = None
    
class Extension(object):

    def __init__(self):
        self.bundlename = None
        self.category = None
        self.description = None
        self.icon = None
        self.name = None
        self.username = None
        self.version = 0

    def load(self,bundle):
        import zipfile
        bundle_file = zipfile.ZipFile(bundle)
        import xml.dom.minidom
        manifest_dom = xml.dom.minidom.parseString(bundle_file.read("manifest.xml"))

        extension_name = manifest_dom.getElementsByTagName('name')[0].firstChild.nodeValue
        extension_desc = manifest_dom.getElementsByTagName('description')[0].firstChild.nodeValue
        
        
        self.name = extension_name
        self.description = extension_desc
        self.version += 1
            

            

        



