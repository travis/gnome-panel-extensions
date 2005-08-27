#!/usr/bin/env python

import os
import sys
import shutil
import xml.dom.minidom

extension_dir = os.path.expandvars("$HOME/.panelextensions")

server_file = xml.dom.minidom.parse("container/GNOME_ExtensionContainer.server")
oaf_servers = server_file.getElementsByTagName("oaf_server")

for server in oaf_servers:
    if server.getAttribute("iid") == "OAFIID:GNOME_ExtensionContainerApplet_Factory":
        server.setAttribute("location", "/usr/lib/gnome-panel/extension_container_applet.py")

new_server_file = file("container/GNOME_ExtensionContainer.server",'w')
new_server_file.write(server_file.toprettyxml())

new_server_file.close()

shutil.copy( "container/GNOME_ExtensionContainer.server", "/usr/lib/bonobo/servers/")
shutil.copy( "container/extension_container_applet.py", "/usr/lib/gnome-panel")
shutil.copy( "container/extension_container.png", "/usr/share/pixmaps")

python_path = None
if os.path.isdir("/usr/lib/python2.4/site-packages"):
    python_path = "/usr/lib/python2.4/site-packages"
elif os.path.isdir("/usr/lib/python2.3/site-packages"):
    python_path = "/usr/lib/python2.3/site-packages"
elif os.path.isdir("/usr/lib/python2.3/site-packages"):
    python_path = "/usr/lib/python2.3/site-packages"
else:
    print "Python path = " + python_path

try: shutil.rmtree(os.path.join(python_path,"panel_extension"))
except: pass
shutil.copytree("container/panel_extension",os.path.join(python_path,"panel_extension"))
            
if not os.path.exists(extension_dir):
    os.mkdir(extension_dir)

shutil.copy("mime/gpe-installer","/usr/bin")

shutil.copy("mime/gpe-installer.desktop","/usr/share/applications")
desktop = os.popen('update-desktop-database /usr/share/applications', 'r')
print (desktop.read())
desktop.close()

shutil.copy("mime/gpe.xml","/usr/share/mime/packages")
mime = os.popen('update-mime-database /usr/share/mime', 'r')
print (mime.read())
mime.close()


shutil.copy("gebb/gebb","/usr/bin")
