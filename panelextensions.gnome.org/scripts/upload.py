#!/usr/bin/env python
from mod_python import apache, Session
import os, shutil
import zipfile
my_globals = apache.import_module("gnome_panel_extensions_org_globals")

def html_foot():
    return '''
</body>
</html>
'''


def upload(req, bundle, uploadtype, category):
    
    import shelve
    base_dir = os.path.split(os.path.split(req.filename)[0])[0]
    os.chdir(base_dir)

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
    temp_bundle_name = os.path.join("extensions/tmp",bundle.filename)

    temp_file = file(temp_bundle_name, 'w')
    
    shutil.copyfileobj(bundle.file, temp_file)
    
    temp_file.close()

    try:

        if not zipfile.is_zipfile(temp_bundle_name):
            return_page += "Sorry, this does not appear to be a zipfile!\n"
            return_page += '</body>\n</html>\n'
            return return_page

        session = Session.Session(req)
        if session.is_new():
            return_page += 'You must be logged in to upload'
            session.invalidate()
            return_page += html_foot()
            return return_page
        else:
            extension_database = shelve.open("extensions/extension_data")
            user = session['userdata']
            if uploadtype == 'update':
                try: extension = extension_database[bundle.filename]
                except:
                    return_page += 'Bundle '+bundle.filename+' does not exist.'
                    return_page += html_foot()
                    return return_page
                if extension.username == user.username:
                    try:
                        extension.load(temp_bundle_name)
                    except:
                        return_page += 'Could not update '+bundle.filename+':<br/>'
                        import traceback
                        return_page += traceback.format_exc()
                        return_page += html_foot()
                        return return_page
                
                    extension.category = category    
                    extension_database[bundle.filename] = extension
                    shutil.copyfile(temp_bundle_name, os.path.join("extensions/bundles/",bundle.filename))


                    return_page += bundle.filename + ' updated successfully!'
                    return_page += html_foot()
                    return return_page 
                else:
                    return_page += 'You do not have permission to update '+bundle.filename+'.'
                    return_page += html_foot()
                    return return_page
                

            elif uploadtype == 'new':
                if not extension_database.has_key(bundle.filename):
                    extension = my_globals.Extension()
                    extension.username = session['userdata'].username
                    extension.bundlename = bundle.filename
                    extension.load(temp_bundle_name)
                    extension.category = category
                    extension_database[bundle.filename] = extension

                    shutil.copyfile(temp_bundle_name, os.path.join("extensions/bundles/",bundle.filename))

                    return_page += bundle.filename + " successfully uploaded!"
                    return_page += html_foot()
                    return return_page
                else:
                    return_page += bundle.filename + ' already exists, please rename your bundle.<br/><a href="delete?bundlename=%s">Delete</a>'% bundle.filename
                    return_page += '</body>\n</html>\n'
                    
                    return return_page
            else:
                return_page += 'Unknown upload type!'
                return_page += html_foot()

                return return_page
    finally:
        os.remove(temp_bundle_name)
            

       

    
    
    



def delete(req, bundlename):
    import shelve

    return_page = ''
    
    base_dir = os.path.split(os.path.split(req.filename)[0])[0]
    os.chdir(base_dir)
    
    extension_database = shelve.open("extensions/extension_data")
    try: del extension_database[bundlename]
    except KeyError: return_page += 'Database does not contain bundle '+bundlename
    else:
        import traceback
        return_page += 'Could not remove database entry:<br/>'+traceback.format_exc()
    try: os.remove("extensions/manifests/", (bundlename.split('.')[0] + ".xml"))
    except: return_page += 'Could not delete '+bundlename.split('.')[0] + ".xml."
    try: os.remove(os.path.join("extensions/bundles/", bundlename))
    except: return_page += 'Could not delete '+bundlename+'.'

    return return_page
    
    

    
