#!/usr/bin/env python
from mod_python import apache
import sys
import os
import shelve
import sha as encrypt
#__import__('gnome_panel_extensions_org_globals')
scripts_dir = '/home/travis/development/gnome-panel-extensions/panelextensions.gnome.org/scripts'
sys.path.insert(0,scripts_dir)
os.chdir(os.path.join(scripts_dir,"users"))
import gnome_panel_extensions_org_globals as my_globals

def register(req, username, password, password_verify, email, email_verify):
    return_page = '''<?xml version="1.0"?>

<!DOCTYPE html 
	PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
	"http://www.w3.org/TR/xhtml/DTD/xhtml1-strict.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">

<head>
 <title>Upload</title>
 <link rel="stylesheet" type="text/css" href="../../../styles/global.css"/>

</head>
</body>
'''
    
    database = shelve.open('user_data')


    if not database.has_key(username):
        user = my_globals.User()




        user.username = username
        
        password_hash = encrypt.new(password)
        user.password = password_hash.digest()
        
        
        database[username] = user
        
        return_page += 'Added ' + username + '.'

    else:
        return_page += 'User ' + username + ' already exists. Please choose a new username.'
        return_page += '''
<form method="POST"
      action="delete_user">
  <input type="hidden" name="username" value="%s"/>
  <input type="submit" value="Delete User"/>
</form>
''' % username
    return_page += '''
</body>
</html>
'''
    return return_page

def delete_user(req, username):
    database = shelve.open('user_data')
    return_page = '''<?xml version="1.0"?>

<!DOCTYPE html 
	PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
	"http://www.w3.org/TR/xhtml/DTD/xhtml1-strict.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">

<head>
 <title>Upload</title>
 <link rel="stylesheet" type="text/css" href="../../../styles/global.css"/>

</head>
</body>
'''

    try:
        del database[username]
        return_page += 'Deleted ' + username + '.'
    except KeyError:
        return_page += 'No user ' + username + '. Could not delete.'

    return_page += '''
</body>
</html>
'''
    return return_page

    
