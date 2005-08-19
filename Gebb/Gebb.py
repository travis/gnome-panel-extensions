#!/usr/bin/env python
import zipfile
import xml.dom.minidom
import sys
import os
import pprint
import time

import getopt

MANIFEST_NAME = "manifest.xml"

def get_manifest():
    if not os.path.isfile(MANIFEST_NAME):
        man_file = open(MANIFEST_NAME, "w+")
        man_file.write('<?xml version="1.0" ?>\n<?xml-stylesheet type="text/xsl" href="styles/manifest.xsl" ?>\n<gpem> \n</gpem>\n')
        man_file.close()

    man_file = open(MANIFEST_NAME, 'r')

    try:
        manifest = xml.dom.minidom.parse(man_file)
    except:
        print MANIFEST_NAME, "is not valid XML!"
        raise
        sys.exit()

    man_file.close()

    return manifest

def write_manifest(manifest):
    man_file = open(MANIFEST_NAME, 'w')
    manifest.writexml(man_file)
    man_file.close()
    


def print_usage():
    print '''
Usage: %s [options] <command> [command-options-and-arguments]

Options:
  -v: verbose mode (print extra information)
  --help: prints this message and exits

Commands:
  add <one or more filename[s]>
  add-main <filename> 
  build <filename>
  set-desc <single or multi word description>
  set-name <single or multi word name>
''' % os.path.split(sys.argv[0])[1]

try:
    (option_list, my_args) = getopt.getopt(sys.argv[1:], "v", ["help"])
    
except getopt.GetoptError:
    print "Bad command line options"
    sys.exit()


option_list = dict(option_list)
#MANIFEST_NAME = option_list.get("-m", "manifest.xml")
if option_list.has_key("--help"):
    print_usage()
    sys.exit()

verbose_mode = option_list.has_key("-v")



if len(my_args) == 0:
    print_usage()
    sys.exit()

    
if my_args[0] == "build":

    #Check well formedness of command
    if len(my_args) == 2:
        build_target = my_args[1]
    elif len(my_args > 2):
        print_usage()
        sys.exit()
    else:
        print "Please specify name of file to build"
        sys.exit()

                   
    manifest = get_manifest()
        
    bundle = zipfile.ZipFile(build_target, 'w')

    #Set up and add __bundle_init__ script
    init_file = ""
    init_file += 'name = "' + manifest.documentElement.getElementsByTagName("name")[0].firstChild.nodeValue.strip() + '"\n'
    init_file += 'description = "' + manifest.documentElement.getElementsByTagName("description")[0].firstChild.nodeValue.strip() + '"\n'
    init_file += 'bundle_file_name = "' + build_target + '"\n'

    if (verbose_mode):
        print "init file:\n" + init_file
        
    init_zinfo = zipfile.ZipInfo("__bundle_init__.py", time.localtime()[:6])
    bundle.writestr(init_zinfo, init_file)


    #Add specified files to bundle
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

                    init_file += 'main_script = "' + module_name + '"\n'
        
        bundle.write(file_name)


    #set bundle name
    manifest.documentElement.setAttribute("bundlename", build_target)

    write_manifest(manifest)

    bundle.write(MANIFEST_NAME)


    
    if (verbose_mode):
        print build_target, "contains", bundle.namelist()
    


elif my_args[0] == "add":
    #add argv[2,3,...,n] to manifest

 
    manifest = get_manifest()
        
    for file_name in my_args[1:]: #  [1:] because first arg is command (add)
        if not os.path.isfile(file_name):
            print "Cannot find", file_name
        else:
            file_element = manifest.createElement("file")
            file_element.setAttribute("name", file_name)
            manifest.documentElement.appendChild(file_element)

    if (verbose_mode):
        print manifest.toxml()
    
    write_manifest(manifest)


elif my_args[0] == "add-main":
    #add argv[2] to manifest
    file_name = my_args[1]
    if not os.path.isfile(file_name):
        print "Cannot find", file_name
        sys.exit()
    else:
        manifest = get_manifest()

        file_tag_list = manifest.getElementsByTagName("file")

        main_file_list = []
        for file_node in file_tag_list:
            if file_node.hasAttribute('type') and (file_node.getAttribute('type') == 'main'):
                main_file_list.append(file_node)

        if len(main_file_list) > 1:
            print
            print MANIFEST_NAME + " has more than one main script element! Please fix this manually or delete " + MANIFEST_NAME + " and rebuild it."
            sys.exit()
        
        else:
            file_element = manifest.createElement("file")
            file_element.setAttribute("name", file_name)
            file_element.setAttribute("type", "main")
            
            if len(main_file_list) == 1:
                manifest.documentElement.replaceChild(file_element,main_file_list[0])
            else:
                manifest.documentElement.appendChild(file_element)

        if (verbose_mode):
            print manifest.toxml()


        write_manifest(manifest)


elif my_args[0] == "set-desc":
    #add argv[2,3,...,n] to manifest
    manifest = get_manifest()

    desc_tag_list = manifest.getElementsByTagName("description")

    if len(desc_tag_list) > 1:
        print
        print MANIFEST_NAME + " has more than one description element! Please fix this manually or delete " + MANIFEST_NAME + " and rebuild it."
        sys.exit()
    else:
        desc_element = manifest.createElement("description")


        description_string = ""
        for word in my_args[1:]: #  [1:] because first arg is command (add)
            description_string += word+" "
            
        desc_text_node = manifest.createTextNode(description_string)
        desc_element.appendChild(desc_text_node)

        
        if len(desc_tag_list) == 1:
            manifest.documentElement.replaceChild(desc_element, desc_tag_list[0])
        else:
            manifest.documentElement.appendChild(desc_element)
            
    if (verbose_mode):
        print manifest.toxml()


    write_manifest(manifest)


elif my_args[0] == "set-name":
    #set name element in manifest
    manifest = get_manifest()

    name_tag_list = manifest.getElementsByTagName("name")

    if len(name_tag_list) > 1:
        print
        print MANIFEST_NAME + " has more than one name element! Please fix this manually or delete " + MANIFEST_NAME + " and rebuild it."
        sys.exit()
    else:
        name_element = manifest.createElement("name")


        name_string = ""
        for word in my_args[1:]: #  [1:] because first arg is command (add)
            name_string += word+" "
            
        name_text_node = manifest.createTextNode(name_string)
        name_element.appendChild(name_text_node)

        
        if len(name_tag_list) == 1:
            manifest.documentElement.replaceChild(name_element, name_tag_list[0])
        else:
            manifest.documentElement.appendChild(name_element)
            
    if (verbose_mode):
        print manifest.toxml()


    write_manifest(manifest)


else:
    print_usage()
    


    
