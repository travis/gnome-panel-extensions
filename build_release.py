#!/usr/bin/python
import os
from os import mkdir
from shutil import copy as cp
os.system("rm -rf gnome-panel-extensions-0.0.1")

mkdir("gnome-panel-extensions-0.0.1")


mkdir("gnome-panel-extensions-0.0.1/container")
cp("container/extension_container_applet.py","gnome-panel-extensions-0.0.1/container")
cp("container/GNOME_ExtensionContainer.server", "gnome-panel-extensions-0.0.1/container")
cp("container/extension_container.png", "gnome-panel-extensions-0.0.1/container")

mkdir("gnome-panel-extensions-0.0.1/container/panel_extension")
filenames = os.listdir("container/panel_extension")
for name in filenames:
    if name.endswith(".py"):
        cp("container/panel_extension/"+name,"gnome-panel-extensions-0.0.1/container/panel_extension")



mkdir("gnome-panel-extensions-0.0.1/mime")
cp("mime/gpe.xml", "gnome-panel-extensions-0.0.1/mime")
cp("mime/gpe-installer", "gnome-panel-extensions-0.0.1/mime")
cp("mime/gpe-installer.desktop","gnome-panel-extensions-0.0.1/mime")



mkdir("gnome-panel-extensions-0.0.1/gebb")
cp("gebb/gebb", "gnome-panel-extensions-0.0.1/gebb")
os.chmod("gnome-panel-extensions-0.0.1/gebb/gebb", 0755)



mkdir("gnome-panel-extensions-0.0.1/doc")

cp("doc/tutorial.html", "gnome-panel-extensions-0.0.1/doc")
cp("doc/addtopanel.png", "gnome-panel-extensions-0.0.1/doc")
cp("doc/chooseextension.png", "gnome-panel-extensions-0.0.1/doc")

dirnames = os.listdir("doc")

for dirname in dirnames:
    if os.path.isdir(os.path.join("doc/",dirname)) and not dirname == ".svn":
        mkdir(os.path.join("gnome-panel-extensions-0.0.1/doc",dirname))
        filenames = os.listdir(os.path.join("doc/",dirname))

        for filename in filenames:

            if not filename.endswith("~") and not filename == ".svn":
                cp(os.path.join(os.path.join("doc/",dirname),filename),os.path.join("gnome-panel-extensions-0.0.1/doc/",dirname))

cp("release/install.py", "gnome-panel-extensions-0.0.1")
cp("release/uninstall.py", "gnome-panel-extensions-0.0.1")
cp("release/README", "gnome-panel-extensions-0.0.1")
cp("release/INSTALL", "gnome-panel-extensions-0.0.1")

os.system('tar -cvzf gnome-panel-extensions-0.0.1.tar.gz gnome-panel-extensions-0.0.1')

cp("gnome-panel-extensions-0.0.1.tar.gz","panelextensions.gnome.org/release")
