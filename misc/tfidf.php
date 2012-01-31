<?
	include('sanitize.php'); 
	include('db.php');

	$user = $_GET['user'];
	$sql = "SELECT tfidf_scores.* FROM tokens,";
    $sql .= "(SELECT tfidf.token, tfidf.tf, tfidf.df, log(tfidf.tf/tfidf.df) as score FROM";
    $sql .=   " (SELECT token,";
    $sql .=     " COUNT(*) AS df,";
    $sql .=      " SUM(CASE WHEN user='$user' THEN 1 ELSE 0 END) AS tf";
    $sql .=   " FROM token_user_mapping";
    $sql .=  " GROUP BY token";
    $sql .=  " ORDER BY tf DESC) as tfidf";
    $sql .= " ORDER BY score DESC) as tfidf_scores";
    $sql .= " WHERE tokens.token = tfidf_scores.token AND tokens.type = 'word' AND tfidf_scores.score != 0";

	
	$results = mysql_query($sql);
	$tokens = array();
	
	while($row = mysql_fetch_array($results))	
	{
		unset($row["0"]);
		unset($row["1"]);
		unset($row["2"]);
		unset($row["3"]);
		array_push($tokens,$row);
	}
	
	echo json_encode($tokens);
	
?>