<?php
include_once('simple_html_dom.php');

$base_url = 'https://play.google.com';
$target_url = 'https://play.google.com/store/apps/category/GAME_ACTION?hl=en';

ini_set('max_execution_time', 300);

$html = new simple_html_dom();
$html->load_file($target_url);

$url = []; $i=0;

$dbhost = 'localhost:3310';
$dbuser = 'root';
$dbpass = 'suna';
$conn = new mysqli($dbhost, $dbuser, $dbpass);
   
function scrape($dummy){
	$s = strpos($dummy,">") +1;
	$e = strrpos($dummy,"<") - $s;
	$dum = substr($dummy,$s,$e);
	return $dum;
}

if($conn->connect_error) {
   	die('Could not connect: ' . mysql_error());
}

foreach($html->find('a[class=title]') as $link){
	$value = $base_url.$link->href;
	array_push($url, $value);
}
foreach ($url as $nav) {
	$html = new simple_html_dom();
	$html->load_file($nav);		
	foreach ($html->find('div[class=id-app-title]') as $val) {
		echo '<b>'.$val.'</b>'.'<br>';
		$title = scrape($val);
	}
	foreach ($html->find('span[class=reviews-num]') as $val1) {
		//echo "Rating Count : ".$val1.'<br>';
		$rating_count = scrape($val1);
	}
	foreach ($html->find('span[itemprop=genre]') as $val2) {
		//echo "Genre : ".$val2.'<br>';	
		$genre = scrape($val2);
	}
	foreach ($html->find('div[class=score]') as $val3) {
		//echo "Rating : ".$val3.'<br>';	
		$rating = scrape($val3);
	}
	foreach ($html->find('div[class=content]') as $value) {
		$size = "UNAVAILABLE";
		$price = "Free";
		echo $value.'<br>';
		foreach ($html->find('div[itemprop=datePublished]') as $temp) {
			$date = scrape($temp);
		}
		foreach ($html->find('div[itemprop=numDownloads]') as $temp1) {
			$downloads = scrape($temp1);
		}
		foreach ($html->find('div[itemprop=fileSize]') as $temp2) {
			$size = scrape($temp2);
		}
	}

	$sql = "INSERT INTO games (game_name,genre, rating, review_count, date_Published, size, downloads, price) VALUES ('$title', '$genre', '$rating', '$rating_count', '$date', '$size', '$downloads', '$price')";
	mysqli_select_db($conn,'dataset');

   	$retval = mysqli_query($conn, $sql );
	   
   	if(! $retval ) {
      	die('Could not enter data: ' . mysqli_error($conn));
   	}
   	echo "Entered data into Database successfully\n";
}

mysql_close($conn);
?>