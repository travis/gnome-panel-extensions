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
        import os
        import zipfile
        import xml.dom.minidom

        bundle_file = zipfile.ZipFile(bundle)

        manifest_dom = xml.dom.minidom.parseString(bundle_file.read("manifest.xml"))

        extension_name = manifest_dom.getElementsByTagName('name')[0].firstChild.nodeValue
        extension_desc = manifest_dom.getElementsByTagName('description')[0].firstChild.nodeValue
        
        extension_files = manifest_dom.getElementsByTagName('file')

        #try to find an icon to use:
        for element in extension_files:
            try:
                file_type = element.getAttribute('type')
            except:
                file_type = ''
                continue
            if file_type == 'icon':
                import shutil

                file_name = element.getAttribute('name')

                icon_name = file_name

                icon_file = open("../images/"+icon_name,'w')
                icon_file.write(bundle_file.read(file_name))
                icon_file.close()
                self.icon = icon_name

                
                
            
        
        self.name = extension_name
        self.description = extension_desc
        self.version += 1


    def set_icon(self, icon):
        if not (icon == None or icon.filename == ''):
            import os
            if self.icon:
                os.remove("../images/"+self.icon)
            import shutil
            icon_name = icon.filename

            icon_file = open("../images/"+icon_name,'w')
            shutil.copyfileobj(icon.file, icon_file)
            icon_file.close()
            self.icon = icon_name
            
        
            
def sidebar():
    sidebar = open("../sidebar.html",'r')
    return_text = sidebar.read()
    return_text =  return_text.replace('href="','href="../')
    sidebar.close()
    return return_text

def titlebar():
    titlebar = open("../titlebar.html",'r')
    return_text = titlebar.read()
    return_text = return_text.replace('href="','href="../')
    titlebar.close()
    return return_text
        



