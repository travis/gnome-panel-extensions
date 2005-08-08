#!/usr/bin/env python
import os
import cgi
MANIFEST_DIRECTORY = "extensions/manifests/"

html_header = '''<?xml version="1.0"?>

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

def xslt_output(dir_list):
    '''
    Return html by applying xslt stylesheet.
    
    For use with xslt to produce actual html output since XLink is not
    supported by browsers. This is actually much more versatile but will
    probably be a little slower because of the extra processing.
    '''
    import libxslt
    import libxml2
    global MANIFEST_DIRECTORY
    global html_header

    styledoc = libxml2.parseFile("extensions/styles/manifest.xslt")
    style = libxslt.parseStylesheetDoc(styledoc)
    html_extension_list = html_header
    
    for file_name in dir_list:
        print MANIFEST_DIRECTORY + file_name
        if os.path.isfile(MANIFEST_DIRECTORY + file_name):

            doc = libxml2.parseFile(MANIFEST_DIRECTORY + file_name)
            result = style.applyStylesheet(doc, None)
            html_extension_list += style.saveResultToString(result)
            
    html_extension_list += '''
</body>
</html>'''



            
    return html_extension_list

def return_html_list():
    global MANIFEST_DIRECTORY
    os.chdir("/home/travis/development/gnome-panel-extensions/panelextensions.gnome.org/")
    html_extension_list = "No extensions found"

    dir_list = os.listdir(MANIFEST_DIRECTORY)
    print str(dir_list)
    if dir_list:
        html_extension_list = xslt_output(dir_list)

    return html_extension_list


    
print return_html_list()
