<?php
include_once('simple_html_dom.php');

$base_url = 'https://play.google.com';
$target_url = 'https://play.google.com/store/apps/category/GAME_STRATEGY';

ini_set('max_execution_time', 300);

$html = new simple_html_dom();
$html->load_file($target_url);

$url = []; $price_array =[]; $title_array = [];

$dbhost = 'localhost:3306';
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
	$temp_title = $link->title;
	$temp_title = str_replace( '\'', '', $temp_title );
	array_push($title_array, $temp_title);
}

foreach($html->find('div[class=subtitle-container]') as $link1){
	foreach($link1->find('span[class=display-price]') as $span){
		$temp_price = scrape($span);
		if(strcmp($temp_price, "Free") == 0){
			$temp_price = 0;
		}
		else{
			$temp_dum = (str_replace( 'Rs.', '', $temp_price ));
			$temp_price = (float)(substr($temp_dum, 2));
		}
		array_push($price_array, $temp_price);
	}
}

foreach ($url as $nav) {
	$flag = 0;
	$html = new simple_html_dom();
	$html->load_file($nav);
	foreach ($html->find('div[class=id-app-title]') as $val) {
		$title = "NULL";
		$dummmy_1 = scrape($val);
		$title = str_replace( '\'', '', $dummmy_1 );
		for ($i=0; $i <count($title_array) ; $i++) { 
			if(strcmp($title_array[$i], $title) == 0){
				$price = $price_array[$i];
			}
		}
	}
	foreach ($html->find('span[class=reviews-num]') as $val1) {
		$rating_count = NULL;
		$dummy = scrape($val1);
		$rating_count = (int)(str_replace( ',', '', $dummy ));
	}
	foreach ($html->find('span[itemprop=genre]') as $val2) {
		$genre = "NULL";
		$dum = scrape($val2);
		$genre = str_replace( 'amp;', '', $dum );
	}
	foreach ($html->find('div[class=score]') as $val3) {
		$rating = NULL;
		$rating = (float)scrape($val3);
	}
	foreach ($html->find('div[class=content]') as $value) {
		$size = "NULL";
		//echo $value.'<br>';
		foreach ($html->find('div[itemprop=datePublished]') as $temp) {
			$date = "NULL";
			$date = scrape($temp);
		}
		foreach ($html->find('div[itemprop=numDownloads]') as $temp1) {
			$t = "NULL";
			$t = scrape($temp1);
			if(strcmp($t, " 100,000,000 - 500,000,000 ") == 0)
				$downloads = "Very High";
			elseif(strcmp($t, " 500,000,000 - 1,000,000,000 ") == 0)
				$downloads = "Very High";
			elseif(strcmp($t, " 10,000,000 - 50,000,000 ") == 0)
				$downloads = "High";
			elseif(strcmp($t, " 50,000,000 - 100,000,000 ") == 0)
				$downloads = "High";
			elseif(strcmp($t, " 1,000,000 - 5,000,000 ") == 0)
				$downloads = "Medium";
			elseif(strcmp($t, " 5,000,000 - 10,000,000 ") == 0)
				$downloads = "Meduim";
			elseif(strcmp($t, " 100,000 - 500,000 ") == 0)
				$downloads = "Low";
			elseif(strcmp($t, " 500,000 - 1,000,000 ") == 0)
				$downloads = "Low";
			else
				$downloads = "Very Low";
		}
		foreach ($html->find('div[itemprop=fileSize]') as $temp2) {
			//$size = "NULL";
			$temp_size = scrape($temp2);
			if(strpos($temp_size, 'M') !== FALSE){
				$size = (float)(str_replace( 'M', '', $temp_size ));
			}
			elseif(strpos($temp_size, 'G') !== FALSE){
				$size = (float)(str_replace( 'G', '000', $temp_size ));
			}
			else{
				$flag = 1;
				break;
			}
		}
		if($flag){
			break;
		}
	}
	if($flag)
		continue;

	$sql = "INSERT INTO games (game_name,genre, rating, review_count, date_Published, size, downloads, price) VALUES ('$title', '$genre', '$rating', '$rating_count', '$date', '$size', '$downloads', '$price')";
	mysqli_select_db($conn,'dataset');

   	$retval = mysqli_query($conn, $sql );
	   
   	if(! $retval ) {
      	die('Could not enter data: ' . mysqli_error($conn));
   	}
   	echo "Entered data into Database successfully".'<br>';
}

//mysql_close($conn);
?>