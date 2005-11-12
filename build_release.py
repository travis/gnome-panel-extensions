#!/usr/bin/python
import os
from os import mkdir
from shutil import copy as cp
os.system("rm -rf gnome-panel-extensions-0.0.2")

mkdir("gnome-panel-extensions-0.0.2")


mkdir("gnome-panel-extensions-0.0.2/container")
cp("container/extension_container_applet.py","gnome-panel-extensions-0.0.2/container")
cp("container/GNOME_ExtensionContainer.server", "gnome-panel-extensions-0.0.2/container")
cp("container/extension_puzzle.svg", "gnome-panel-extensions-0.0.2/container")

mkdir("gnome-panel-extensions-0.0.2/container/panel_extension")
filenames = os.listdir("container/panel_extension")
for name in filenames:
    if name.endswith(".py"):
        cp("container/panel_extension/"+name,"gnome-panel-extensions-0.0.2/container/panel_extension")



mkdir("gnome-panel-extensions-0.0.2/mime")
cp("mime/gpe.xml", "gnome-panel-extensions-0.0.2/mime")
cp("mime/gpe-installer", "gnome-panel-extensions-0.0.2/mime")
cp("mime/gpe-installer.desktop","gnome-panel-extensions-0.0.2/mime")



mkdir("gnome-panel-extensions-0.0.2/gebb")
cp("gebb/gebb", "gnome-panel-extensions-0.0.2/gebb")
os.chmod("gnome-panel-extensions-0.0.2/gebb/gebb", 0755)



mkdir("gnome-panel-extensions-0.0.2/doc")

cp("doc/tutorial.html", "gnome-panel-extensions-0.0.2/doc")
cp("doc/addtopanel.png", "gnome-panel-extensions-0.0.2/doc")
cp("doc/chooseextension.png", "gnome-panel-extensions-0.0.2/doc")

dirnames = os.listdir("doc")

for dirname in dirnames:
    if os.path.isdir(os.path.join("doc/",dirname)) and not (dirname == ".svn" or dirname == "CVS"):
        mkdir(os.path.join("gnome-panel-extensions-0.0.2/doc",dirname))
        filenames = os.listdir(os.path.join("doc/",dirname))

        for filename in filenames:

            if not filename.endswith("~") and not (filename == ".svn" or filename == "CVS"):
                cp(os.path.join(os.path.join("doc/",dirname),filename),os.path.join("gnome-panel-extensions-0.0.2/doc/",dirname))

cp("release/install.py", "gnome-panel-extensions-0.0.2")
cp("release/uninstall.py", "gnome-panel-extensions-0.0.2")
cp("release/README", "gnome-panel-extensions-0.0.2")
cp("release/INSTALL", "gnome-panel-extensions-0.0.2")

os.system('tar -cvzf gnome-panel-extensions-0.0.2.tar.gz gnome-panel-extensions-0.0.2')

cp("gnome-panel-extensions-0.0.2.tar.gz","panelextensions.gnome.org/release")
