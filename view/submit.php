<?php
//Get post variables
header('Access-Control-Allow-Origin: *');

if (isset($_GET['username'])){
    $value = $_GET['username'];
}else{
    $value = "";
    //return an error message
}

//

sleep(1);
echo json_encode(array("returnValue"=>"This is from PHP : ".$value));

?>
