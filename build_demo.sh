#!/bin/bash

mkdir release/container
cp container/extension_container_applet.py release/container
cp container/extension_container_globals.py release/container
cp container/extension_bundle.py release/container
cp container/load_extensions.py release/container
cp container/panel_extension.py release/container
cp container/GNOME_ExtensionContainer.server release/container

mkdir release/blog
cp blog\ extension/blog.gpe release/blog
cp blog\ extension/blog_applet.py release/blog
cp blog\ extension/GNOME_BlogApplet.xml release/blog
cp blog\ extension/manifest.xml release/blog

mkdir release/hello
cp helloworld/hello.py release/hello
cp helloworld/hello.xml release/hello
cp helloworld/manifest.xml release/hello
cp helloworld/hello.gpe release/hello

mkdir release/mime
cp mime/gpe.xml release/mime
cp mime/gpe-installer release/mime
cp mime/gpe-installer.desktop release/mime

mkdir release/gebb
cp Gebb/Gebb.py release/gebb/gebb

tar -cvzf gnome-panel-extensions-0.0.1.tar.gz demo