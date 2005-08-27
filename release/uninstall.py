#!/usr/bin/env python

import os
import sys
import shutil

extension_dir = os.path.expandvars("$HOME/.panelextensions")


try: os.remove("/usr/lib/bonobo/servers/GNOME_ExtensionContainer.server")
except: print "Could not remove server file"
try: os.remove("/usr/lib/gnome-panel/extension_container_applet.py")
except: print "Could not remove applet"
try: os.remove("/usr/share/pixmaps/extension_container.png")
except: print "Could not remove container icon"

try: shutil.rmtree("/usr/lib/python2.4/site-packages/panel_extension")
except:
    try: shutil.rmtree("/usr/lib/python2.3/site-packages/panel_extension")
    except:
        try: shutil.rmtree("/usr/lib/python2.2/site-packages/panel_extension")
        except:
            print "Could not find python installation or could not remove "

            

try: os.remove("/usr/bin/gpe-installer")
except: print "Could not remove gpe installer"

try:
    os.remove("/usr/share/applications/gpe-installer.desktop")
    desktop = os.popen('update-desktop-database /usr/share/applications', 'r')
    print (desktop.read())
    desktop.close()
except: "could not remove gpe desktop file"
try:
    os.remove("/usr/share/mime/packages/gpe.xml")
    mime = os.popen('update-mime-database /usr/share/mime', 'r')
    print (mime.read())
    mime.close()
except: print "Could not remove gpe mime file"

try: os.remove("/usr/bin/gebb")
except: print "Could not remove gebb"
