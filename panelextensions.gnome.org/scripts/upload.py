#!/usr/bin/env python
from mod_python import apache
import os
os.chdir('/home/travis/development/gnome-panel-extensions/panelextensions.gnome.org')

def upload(req, bundle, uploadtype):
    import zipfile
    import shutil
    return_page = '''<?xml version="1.0"?>

<!DOCTYPE html 
	PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
	"http://www.w3.org/TR/xhtml/DTD/xhtml1-strict.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">

<head>
 <title>Upload</title>
 <link rel="stylesheet" type="text/css" href="../../styles/global.css"/>

</head>
</body>
'''
    
    
    try:
        bundle_file = zipfile.ZipFile(bundle.file)
    except zipfile.BadZipfile:
        return_page += "Sorry, this does not appear to be a zipfile!\n"
        return_page += '</body>\n</html>\n'
        return return_page
    if (os.path.isfile("extensions/" + bundle.filename) and uploadtype == "new"):
        return_page += bundle.filename + " already exists, please rename your bundle."
        return_page += '</body>\n</html>\n'
        return return_page

    userid = True #ELIMINATE FOR NEXT IF ONCE AUTHENTICATION IS IMPLEMENTED!!!

    if uploadtype == "update" and userid == False:
        return_page += "You do not have permission to update" + bundle.filename 
        return_page += '</body>\n</html>\n'
        return return_page

    new_file = file("extensions/" + bundle.filename, 'w')

    shutil.copyfileobj(bundle.file, new_file)
    
    new_file.close()

    manifest_name = "extensions/manifests/" + bundle.filename.split('.')[0] + ".xml"

    manifest_file = file(manifest_name, 'w')

    manifest_file.write(bundle_file.read("manifest.xml"))

    manifest_file.close()
    
    return_page += bundle.filename + " successfully uploaded."
    return_page += '''
</body>
</html>
'''
    return return_page


    
