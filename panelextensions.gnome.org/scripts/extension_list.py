#!/usr/bin/env python
from mod_python import apache
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
 <link rel="stylesheet" type="text/css" href="../../extensions/styles/extensions.css"/>




</head>

<body>
'''


def return_html_list(req):
    return_page = html_head()
    base_dir = os.path.split(os.path.split(req.filename)[0])[0]
    os.chdir(base_dir)
    
    extension_database = shelve.open("extensions/extension_data")

    extension_list = extension_database.values()

    for extension in extension_list:
        return_page += str(extension.name) + '<br/>'
        return_page += str(extension.description) + '<br/>'
        return_page += '<a href="../../extensions/bundles/%s">Upload</a><br/>'%extension.bundlename
        return_page += '<a href="../upload.py/delete?bundlename=%s">Delete</a><br/>'%extension.bundlename

    return return_page


    

