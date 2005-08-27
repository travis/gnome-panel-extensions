<!DOCTYPE html 
	PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
	"http://www.w3.org/TR/xhtml/DTD/xhtml1-strict.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">

<head>
 <title>panelextensions register page</title>
 <link rel="stylesheet" type="text/css" href="styles/global.css"/>
 <link rel="stylesheet" type="text/css" href="styles/register.css"/>

 <script language="JavaScript" type="text/javascript">

   var password_match_err = false;
   var email_valid_err = false;
   var email_match_err = false;

   function validateForm(){

      var submit_error = document.getElementById('submitError');
      
      blank_fields = ( (document.getElementById('password').value=='')
                     |(document.getElementById('passwordVerify').value=='')
		     |(document.getElementById('email').value=='')
		     |(document.getElementById('emailVerify').value=='')
		    )

      if (password_match_err
          ||email_valid_err
	  ||email_match_err
	  ||blank_fields){

          submit_error.style.display = 'block';
          return false;
      }
      else {
          submit_error.style.display = 'none';
	  return true;
      }
   }


   var password_blurred = false;
   var password_verify_blurred = false;

   function passwordBlurred(){
       if (!password_blurred){
           password_blurred = true;
	   checkPasswords();
       }
   }
   

   function passwordVerifyBlurred(){
       if (!password_verify_blurred){
           password_verify_blurred = true;
	   checkPasswords();
       }
   }      

   function checkPasswords() {

       if (password_blurred && password_verify_blurred){

           var password_match_error = document.getElementById('passwordMatchError');
	   var password_box = document.getElementById('password');
	   var verify_box = document.getElementById('passwordVerify');
	   
           state = password_match_error.style.display;
	  
	   if (password_box.value != verify_box.value){
	     
	       if (state != 'block'){
	           password_match_error.style.display = 'block';
		   password_match_err = true;
	       }
	   }	   
	   else {
	       if (state != 'none'){
	           password_match_error.style.display = 'none';
		   password_match_err = false;
	       }
	   }        
	              
	   	   
       }      
     
   }


   var email_blurred = false;
   var email_verify_blurred = false;
   var valid_email_pattern = /^(\w|\d)+@(\w|\d)+(\.(\w|\d)+)+/ 

   

   function emailBlurred(){
       if (!email_blurred){
           email_blurred = true;
	   checkEmails();
       }
   }
   

   function emailVerifyBlurred(){
       if (!email_verify_blurred){
           email_verify_blurred = true;
	   checkEmails();
       }
   }      

   function checkEmails() {
      
       if (email_blurred && email_verify_blurred){

           var email_match_error = document.getElementById('emailMatchError');
	   var email_valid_error = document.getElementById('emailValidError');
	   var email_box = document.getElementById('email');
	   var verify_box = document.getElementById('emailVerify');
	   
           match_state = email_match_error.style.display;
	  
	   if (email_box.value != verify_box.value){
	     
	       if (match_state != 'block'){
	           email_match_error.style.display = 'block';
		   email_match_err = true;
	       }
	   }	   
	   else {
	       if (match_state != 'none'){
	           email_match_error.style.display = 'none';
		   email_match_err = false;
	       }


	       valid_state = email_valid_error.style.display;

	       if (!valid_email_pattern.test(email_box.value)){
	           if (valid_state != 'block'){
		       email_valid_error.style.display = 'block';
		       email_valid_err = true;
		   }

	       }
	       else {
	           if (valid_state != 'none'){
	               email_valid_error.style.display = 'none';
		       email_valid_err = false;
		   }


	       }
	   }        
	              
	   	   
       }      
     
   }


 </script>


 </style>

</head>

<body>
<?php
include("titlebar.html");
include("sidebar.html");
?>

<div id="main">
<div id="submitError">
There was a problem with the information you entered. Please see below
for details:
</div>
<form id="registrationForm" 
      method="POST" 
      action="scripts/login.py/register"
      onSubmit="return validateForm()">

    <div class="input">
    <span class="inputLabel">
    User name:
    </span>
    <input type="text" name="username" size="20" maxlength="80"/>*
    </div>
    <br/>

    <div class="input">
    <span class="inputLabel">
    Enter password:
    </span>
       <input id="password" 
              type="password" 
	      name="password" 
	      onBlur="passwordBlurred();"
	      onKeyUp="checkPasswords();"
	      size="20" 
	      maxlength="80"/>*
    </div>

    <div class="input">
    <span class="inputLabel">
    Verify password:
    </span>
       <input id="passwordVerify" 
              type="password"
	      name="password_verify" 
	      onBlur="passwordVerifyBlurred();"
	      onKeyUp="checkPasswords();"
	      size="20" 
	      maxlength="80"/>*
    </div>


    <div id="passwordMatchError">
      
      Passwords don't match!
    </div>
    <script language="JavaScript" type="text/javascript">

   if (document.getElementById('password').value != ''){
      	password_blurred = true;
   }

   var email_verify_blurred = false;
   if (document.getElementById('passwordVerify').value != ''){
       password_verify_blurred = true;
   }

   checkPasswords();
   </script>


    <br/>

    <div class="input">
    <span class="inputLabel">
    Valid e-mail address:
    </span>
       <input id="email" 
              type="text" 
	      name="email" 
	      onBlur="emailBlurred();"
	      onKeyUp="checkEmails();"
	      size="20" 
	      maxlength="80"/>*
    </div>

    <div class="input">
    <span class="inputLabel">
    Re-type email address:
    </span>
       <input id="emailVerify" 
              type="test"
	      name="email_verify" 
	      onBlur="emailVerifyBlurred();"
	      onKeyUp="checkEmails();"
	      size="20" 
	      maxlength="80"/>*
    </div>


    <div id="emailMatchError">
        Addresses don't match!
    </div>
    <div id="emailValidError">
        Not a valid e-mail address!
    </div>

    <script language="JavaScript" type="text/javascript">

    if (document.getElementById('email').value != ''){
      	 email_blurred = true;
    }

    var email_verify_blurred = false;
    if (document.getElementById('emailVerify').value != ''){
        email_verify_blurred = true;
    }

    checkEmails();
    </script>
    <input id="submitButton" type="submit" value="Register"/>
    
</form>
</div>

</body>


</html>
