<?php  	
	header('content-type:application:json;charset=utf8');  
	header('Access-Control-Allow-Origin:*');  
	header('Access-Control-Allow-Methods:POST');  
	header('Access-Control-Allow-Headers:x-requested-with,content-type');
    $year = $_POST["year"];
    $month = $_POST["month"];
    $day = $_POST["day"];
	$date=$year.$month.$day;
    $file='data/'.strval($date).'.json';
    $json = file_get_contents($file); 
    echo $json;
?>
