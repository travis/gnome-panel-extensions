<!DOCTYPE html 
	PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
	"http://www.w3.org/TR/xhtml/DTD/xhtml1-strict.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">

<head>
 <title>panelextensions.gnome.org</title>
 <link rel="stylesheet" type="text/css" href="styles/global.css"/>




</head>

<body>
<?php 
include("titlebar.html");
?>
</div>
<?php
include("sidebar.html");
?>
</div>

 <div id="main">
<h2>Installation:</h2>
<p>
<ol>
<li>Download the gnome-panel-extensions-0.0.1.tar.gz from the download page to the left</li>
<li>Open up a new command line shell and <tt>cd</tt> to the directory you 
downloaded the installation package to.</li>
<li>Untar the file you downloaded, with a command like <tt>tar -xvzf gnome-panel-extensions-0.0.1.tar.gz</tt></li>
<li>Enter <tt>cd gnome-panel-extensions-0.0.1</tt></li>
<li>As root, run <tt>./install.py</tt></li>
</ol>
</p>
<h2>Adding Extensions to the GNOME panel:</h2>
<p>
<ol>
<li>Right click on the GNOME panel wherever you'd like to add a new extension and select "Add to panel..."</li>
<li>Scroll through the list and click the Extension Container applet</li>
<li>Left click on "Choose Extension"</li>
<li>In the dialog that appears, choose the extension you'd like to add. Voila!</li>
</ol>
</p>
<h2>Other useful links:</h2>
<p>
<a href="doc/tutorial.html">Extension Writing Tutorial</a> - An introduction to writing and creating panel extensions. A must read for developers!<br/>
</p>
  </div>



</body>


</html>
