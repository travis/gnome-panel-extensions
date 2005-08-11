#!/usr/bin/env python
import zipfile
import xml.dom.minidom
import sys
import os
import pprint
import time

import getopt


def open_manifest():
    if not os.path.isfile(manifest_name):
        man_file = open(manifest_name, "w+")
        man_file.write('<?xml version="1.0" ?>\n<?xml-stylesheet type="text/css" href="styles/manifest.css" ?>\n<gpem> \n</gpem>\n')
        man_file.close() # if we don't close the file, it doesn't write right away

    man_file = open(manifest_name, "a+")

    return man_file



try:
    (option_list, my_args) = getopt.getopt(sys.argv[1:], "m:")
    
except getopt.GetoptError:
    print "Bad command line options"
    sys.exit()


option_list = dict(option_list)
manifest_name = option_list.get("-m", "manifest.xml")
   

    
if my_args[0] == "build":



    init_file = "" # this is a file which we expect to find in every bundle
                   
    if os.path.isfile(manifest_name):
        man_file = open(manifest_name, "r")
    else:
        print "Could not find", manifest_name
        sys.exit()
       

    try:
        manifest = xml.dom.minidom.parse(man_file)

    except:
        print manifest_name, "is not valid XML!"
        sys.exit()
    if len(my_args) >= 2:
        build_target = my_args[1]
    else:
        print "Please specify name of file to build"
        sys.exit()
        
    bundle = zipfile.ZipFile(build_target, 'w')

    #get attributes of gpem element
    init_file += 'name = "' + manifest.documentElement.getElementsByTagName("name")[0].firstChild.nodeValue + '"\n'
    init_file += 'description = "' + manifest.documentElement.getElementsByTagName("description")[0].firstChild.nodeValue + '"\n'
    init_file += 'bundle_file_name = "' + build_target + '"\n'


    files_to_add = manifest.getElementsByTagName("file")
    
    for addable_file in files_to_add:
        
        
        file_name = str(addable_file.getAttribute("name"))
        if addable_file.hasAttribute("type"):
            file_type = str(addable_file.getAttribute("type"))

            #menu clue in init.py script
            if file_type == "menu":
                init_file += 'xml_menu_file_name ="' + file_name + '"\n'

            #main script clue in init.py script
            elif file_type == "main":
                word_list = file_name.split('.')
                if (len(word_list) < 2) or not (word_list[1] == "py"):
                    print word_list[1] + str(len(word_list))
                    print "Main script must be a .py file"
                    sys.exit()

                else:
                    module_name = word_list[0]
                    init_file += 'import sys\nsys.path.insert(0, "' + build_target + '")\n'
                    init_file += 'import ' + module_name + '\n'


        
        bundle.write(file_name)

    bundle.write('manifest.xml')

    print "init file:\n" + init_file
    init_zinfo = zipfile.ZipInfo("__bundle_init__.py", time.localtime()[:6])
    bundle.writestr(init_zinfo, init_file)
    
    print build_target, "contains", bundle.namelist()
    
    sys.exit()

elif my_args[0] == "add":
    #add argv[2,3,...,n] to manifest

    man_file = open_manifest()
    # currently assumes all bad xml files can be destroyed FIXME


    try:
        manifest = xml.dom.minidom.parse(man_file)
    except:
        print manifest_name, "is not valid XML!"
        sys.exit()
        
    print manifest
 
    for file_name in my_args[1:]: #  [1:] because first arg is command (add)
        if not os.path.isfile(file_name):
            print "Cannot find", file_name
        else:
            file_element = manifest.createElement("file")
            file_element.setAttribute("name", file_name)
            manifest.documentElement.appendChild(file_element)
            print manifest.toxml()
    
    man_file.truncate(0)
    manifest.writexml(man_file)

elif my_args[0] == "add-menu":
    
    man_file = open_manifest()

    try:
        manifest = xml.dom.minidom.parse(man_file)
    except:
        print manifest_name, "is not valid XML!"
        sys.exit()
        
    print manifest

 
    file_name = my_args[1] 
    if not os.path.isfile(file_name):
        print "Cannot find", file_name
    else:
        file_element = manifest.createElement("file")
        file_element.setAttribute("name", file_name)
        file_element.setAttribute("type", "menu")
        manifest.documentElement.appendChild(file_element)
        
        print manifest.toxml()
    
    man_file.truncate(0)
    manifest.writexml(man_file)


elif my_args[0] == "add-main":
#add argv[2,3,...,n] to manifest
    man_file = open_manifest()

    try:
        manifest = xml.dom.minidom.parse(man_file)
    except:
        print manifest_name, "is not valid XML!"
        sys.exit()

    print manifest


    file_name = my_args[1]
    if not os.path.isfile(file_name):
        print "Cannot find", file_name
    else:
        file_element = manifest.createElement("file")
        file_element.setAttribute("name", file_name)
        file_element.setAttribute("type", "main")
        manifest.documentElement.appendChild(file_element)

        print manifest.toxml()
    
    man_file.truncate(0)
    manifest.writexml(man_file)


else:
    print "Valid commands include: FIXME!"
    


    
