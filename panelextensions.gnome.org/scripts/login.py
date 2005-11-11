#!/usr/bin/env python
from mod_python import apache, Session
import sys
import os

import md5 as encrypt
my_globals = apache.import_module("gnome_panel_extensions_org_globals")

def test(req):
    
    user = my_globals.User()

    return os.path.split(req.filename)[0]

def open_user_database(req):
    import shelve

    scripts_dir = os.path.split(req.filename)[0]
    os.chdir(scripts_dir)
    database = shelve.open('../users/user_data')
    return database

def html_head():
    return '''<?xml version="1.0"?>

<!DOCTYPE html 
	PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
	"http://www.w3.org/TR/xhtml/DTD/xhtml1-strict.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">

<head>
 <title>Upload</title>
 <link rel="stylesheet" type="text/css" href="../../styles/global.css"/>
 <link rel="stylesheet" type="text/css" href="../../styles/login.css"/>
</head>
</body>
'''

def html_foot():
    return '''
</body>
</html>
'''

def delete_user(req, username):
    
    return_page = html_head()

    database = open_user_database(req)

    try:
        del database[username]
        return_page += 'Deleted ' + username + '.'
    except KeyError:
        return_page += 'No user ' + username + '. Could not delete.'


    return_page += html_foot()
    return return_page

def login(req, username, password):
    return_page = html_head()


    session = Session.Session(req)
    if session.is_new():
        database = open_user_database(req)
        
        if (database.has_key(username) and
            database[username].password == encrypt.new(password).digest()):
            
            session['userdata']=database[username]
            session.save()
            user = session['userdata']
            return_page += 'You are logged in as '+user.username+'.'
            return_page +='''
<a href="logout">Logout</a>
'''
            
        else:
            return_page += 'Either the user name or password is incorrect.'
    

    else:
        try:
            user = session['userdata']
            return_page += 'You are already logged in as '+user.username + '.'
        except KeyError:
            return_page += 'There was a problem creating '+ username + '.'
    
    return_page += html_foot()
    return return_page

def login_check(req, username):

    return_page = html_head()
    
    session = Session.Session(req)

    if session.is_new():
        return_page += 'Not logged in!'
        session.invalidate()
    else:
        user = session['userdata']
        return_page += 'You are logged in as ' + user.username + '.'

    return_page += html_foot()

    return return_page
def logout(req):

    return_page = html_head()

    session = Session.Session(req)

    if session.is_new():
        session.invalidate()
        return_page += 'Not logged in!'
    
    else:
        return_page += session['userdata'].username + ' logged out.'
        return_page +='''
<br/>
<a href="login_box">Login</a>
'''

        session.invalidate()
        
    return_page += html_foot()
    return return_page
        
        


def register(req, username, password, password_verify, email, email_verify):
    
    return_page = html_head()
    
    database = open_user_database(req)

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
    return_page += html_foot()
    
    return return_page


def login_box(req):

    return_page = html_head()
    session = Session.Session(req)
    if session.is_new():
        return_page += '''
<form id="loginBoxForm" 
      method="POST" 
      action="login"
      >


    User name:
    <br/>
    <input type="text" name="username" size="15" maxlength="80"/>
    <br/>
    Password:
    <br/>
       <input type="password" 
	      name="password" 
	      size="15" 
	      maxlength="80"/>
    <br/>

    <input id="submitButton" type="submit" value="Login"/>
    
</form>
'''
    else:
        return_page += '<span id="personalGreeter">'
        return_page += 'Hello, '+session['userdata'].username
        return_page += '</span>'
        return_page +='''
<a href="logout">Logout</a>
'''

    return_page += html_foot()

    return return_page
