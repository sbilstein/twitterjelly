<?  
	include('sanitize.php'); 
	include('db.php');

	if (!isset($_POST['terms']) || empty($_POST['terms']))
	{
	    echo json_encode(Array("idfs"=>Array()));
	}

	$terms = implode('","',explode(",",$_POST['terms']));

	//$sql = "SELECT COUNT(DISTINCT tweets.from_user) FROM tweets";
	$sql = "SELECT COUNT(*) FROM (SELECT DISTINCT from_user FROM tweets) as t";
	$results = mysql_query($sql);
	$num_users = 0;
	while($row = mysql_fetch_array($results))
	{
		$num_users = intval($row[0]);
	}
	
	$sql = "SELECT * FROM doc_freqs WHERE token IN (\"$terms\" ) AND token IS NOT null";

	$results = mysql_query($sql);
	$idfs = Array();
	while($row = mysql_fetch_array($results))
	{
		$idfs[$row['token']] = uft8_encode(log((1+$num_users)/(1+intval($row['c']))));
	}
	
	echo json_encode(Array("idfs"=>$idfs));
	
?>
