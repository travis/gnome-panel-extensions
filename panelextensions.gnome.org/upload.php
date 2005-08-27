<!DOCTYPE html 
	PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
	"http://www.w3.org/TR/xhtml/DTD/xhtml1-strict.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">

<head>
 <title>panelextensions upload page</title>
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
<form method="POST" enctype="multipart/form-data" action="cgi-bin/upload.pyg">


<p>
Select bundle file:<br/>
    <input type="file" name="bundle" size="32" maxlength="80"/>
</p>

    <p>
Category:<br/>
    <select name="category">

      <option>Network</option>
      <option>Sound & Video</option>
      <option>System</option>
      <option>Utility</option>
      <option>World Wide Web</option>
    </select>
    </p>

<p>    
Select icon (Leave blank to use icon from bundle):<br/>
<input type="file" name="icon" size="32" maxlength="80">
</p>
    <p>
       <input type="radio" name="uploadtype" value="new"/> New
       <input type="radio" name="uploadtype" value="update"/> Update
    </p>
    
    <input type="submit" value="Upload"/>
</form>
</div>

</body>


</html>
