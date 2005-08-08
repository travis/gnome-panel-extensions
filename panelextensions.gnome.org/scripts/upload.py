#!/usr/bin/env python
from mod_python import apache
import os
os.chdir('/home/travis/development/gnome-panel-extensions/panelextensions.gnome.org')

def test(req, bundle, uploadtype):
    import zipfile
    import shutil
    test = '''<?xml version="1.0"?>

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
        test += "Sorry, this does not appear to be a zipfile!\n"
        test += '</body>\n</html>\n'
        return test
    if (os.path.isfile("extensions/" + bundle.filename) and uploadtype == "new"):
        test += bundle.filename + " already exists, please rename your bundle."
        test += '</body>\n</html>\n'
        return test

    userid = True #ELIMINATE FOR NEXT IF ONCE AUTHENTICATION IS IMPLEMENTED!!!

    if uploadtype == "update" and userid == False:
        test += "You do not have permission to update" + bundle.filename 
        test += '</body>\n</html>\n'
        return test

    new_file = file("extensions/" + bundle.filename, 'w')

    shutil.copyfileobj(bundle.file, new_file)
    
    new_file.close()

    manifest_name = "extensions/manifests/" + bundle.filename.split('.')[0] + ".xml"

    manifest_file = file(manifest_name, 'w')

    manifest_file.write(bundle_file.read("manifest.xml"))

    manifest_file.close()
    
    test += bundle.filename + " successfully uploaded."
    test += '''
</body>
</html>
'''
    return test

def upload():
    
    extension_list = "No Extensions Available"

    return extension_list
    
