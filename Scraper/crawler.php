<?php
include_once('simple_html_dom.php');

ini_set('max_execution_time', 200000);

$dbhost = 'localhost:3306';
$dbuser = 'root';
$dbpass = 'suna';
$conn = new mysqli($dbhost, $dbuser, $dbpass);
$rating_count = 'NULL';$rating = 'NULL';
$db_selected = mysqli_select_db($conn, 'dataset');
if (!$db_selected) {
    die ('Can\'t use the dataset  : ' . mysqli_error($conn));
}   

function scrape($dummy){
	$s = strpos($dummy,">") +1;
	$e = strrpos($dummy,"<") - $s;
	$dum = substr($dummy,$s,$e);
	return $dum;
}

if($conn->connect_error) {
   	die('Could not connect to Server: ' . mysqli_error($conn));
}

$sql = "SELECT * FROM url WHERE id>39006;";
$result = mysqli_query($conn, $sql) or die(mysqli_error($conn));

if (mysqli_num_rows($result) > 0) {
    // output data of each row
    $id = 35803;
    while($row = mysqli_fetch_assoc($result)) {
        echo "Game number : " . $row["id"]."<br>";
        $flag = 0;
		$html = new simple_html_dom();
		$html->load_file($row["game_url"]);
		foreach ($html->find('div[class=id-app-title]') as $val) {
			$title = "NULL";
			$dummmy_1 = scrape($val);
			$title = str_replace( '\'', '', $dummmy_1 );
		}
		$price = $row["price"];
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
			echo $rating;
		}
		foreach ($html->find('div[class=content]') as $value) {
			foreach ($html->find('div[itemprop=datePublished]') as $temp) {
				$date = "NULL";
				$date = scrape($temp);
			}
			foreach ($html->find('div[itemprop=numDownloads]') as $temp1) {
				$temp_downloads= "NULL";
				$temp_downloads= scrape($temp1);
				if(strcmp($temp_downloads, "  100,000,000 - 500,000,000  ") == 0)
					$downloads = "Very High";
				elseif(strcmp($temp_downloads, "  500,000,000 - 1,000,000,000  ") == 0)
					$downloads = "Very High";
				elseif(strcmp($temp_downloads, "  10,000,000 - 50,000,000  ") == 0)
					$downloads = "High";
				elseif(strcmp($temp_downloads, "  50,000,000 - 100,000,000  ") == 0)
					$downloads = "High";
				elseif(strcmp($temp_downloads, "  1,000,000 - 5,000,000  ") == 0)
					$downloads = "Medium";
				elseif(strcmp($temp_downloads, "  5,000,000 - 10,000,000  ") == 0)
					$downloads = "Meduim";
				elseif(strcmp($temp_downloads, "  100,000 - 500,000  ") == 0)
					$downloads = "Low";
				elseif(strcmp($temp_downloads, "  500,000 - 1,000,000  ") == 0)
					$downloads = "Low";
				else
					$downloads = "Very Low";
			}
			foreach ($html->find('div[itemprop=fileSize]') as $temp2) {
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

		$sql = "INSERT INTO games VALUES ('$id', '$title', '$genre', '$rating', '$rating_count', '$date', '$size', '$temp_downloads', '$price')";
		$retval = mysqli_query($conn, $sql );
		if(! $retval ) {
	      	die('Could not enter data into Games by : ' . mysqli_error($conn));
	   	}
	   	echo "Entered data into Games successfully".'<br>';
		
		$sql = "INSERT INTO games_formatted VALUES ('$id', '$title', '$genre', '$rating', '$rating_count', '$date', '$size', '$downloads', '$price')";   
		$retval = mysqli_query($conn, $sql );
		if(! $retval ) {
	      	die('Could not enter data into Games_Formatted : ' . mysqli_error($conn));
	   	}
	   	echo "Entered data into Games_formatted successfully".'<br>';
	   	$id = $id + 1;
    }
} else {
    echo "0 results";
}


/*foreach ($url as $nav) {
	
}*/

//mysql_close($conn);
?>