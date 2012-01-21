<?php

require('LoremIpsum.class.php');
$generator = new LoremIpsumGenerator;

//echo $generator->getContent(100);


//Get post variables
header('Access-Control-Allow-Origin: *');

if (isset($_GET['username'])){
    $value = $_GET['username'];
}else{
    $value = "";
    //return an error message
}

//TODO encode some fake json objects using the lorem ipsum gen

sleep(1);
echo json_encode(array("returnValue"=>"This is from PHP : ".$value));

?>
