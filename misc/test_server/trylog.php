<HTML>
<H1>Checking...</H1>
<BR>
<?php
	$username = $_POST['username']; 
	$password = $_POST['password'];
	if($username === 'admin' && $password === '998'){
		echo "Success!";
	}
	else {
	echo "Error: Incorrect login or password.";
	}
?>
