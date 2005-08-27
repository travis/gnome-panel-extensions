#!/usr/bin/env python
from mod_python import apache, Session
import os
import cgi
import shelve
my_globals = apache.import_module('gnome_panel_extensions_org_globals')

def html_head():
    return '''<?xml version="1.0"?>

<!DOCTYPE html 
	PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
	"http://www.w3.org/TR/xhtml/DTD/xhtml1-strict.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">

<head>
 <title>panelextensions.gnome.org</title>
 <link rel="stylesheet" type="text/css" href="../../styles/global.css"/>
 <link rel="stylesheet" type="text/css" href="../../styles/extensionlist.css"/>




</head>

<body>
'''


def return_html_list(req):
    return_page = html_head()
    base_dir = os.path.split(os.path.split(req.filename)[0])[0]
    os.chdir(base_dir)
    
    extension_database = shelve.open("extensions/extension_data")

    extension_list = extension_database.values()

    session = Session.Session(req)
    if session.is_new():
        session.invalidate()
        username=None
    else:
        username = session['userdata'].username

    return_page += 'New Extensions:<br/>'

    for extension in extension_list:
        return_page += '''
        <div class="extensiondescription">
        <img class="icon" href="" />
        <span class="name">%s</span>
        <span class="desc">%s</span>
        <span class="linkbox"><a href="../../extensions/bundles/%s">Download</a>
        '''%(str(extension.name),str(extension.description),extension.bundlename)

        if username == extension.username:
            return_page += '<a href="../upload.py/delete?bundlename=%s">Delete</a><br/>'%extension.bundlename


        return_page +="</span>\n</div>"

    return_page +="</body></html>"
        
        
    return return_page


    

