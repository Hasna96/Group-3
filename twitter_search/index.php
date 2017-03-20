<?php 


include "twitteroauth/twitteroauth.php";

$access_token = '787668843804160000-FRN8tT3Mt9sAguMeRUiHUje3QoT0bQN';
$access_token_secret = 'knA0SOFFIGCcU2cLjHAVoA4Vqpe4X3H0VrGahKvBhmP1p';
$consumer_key = 'YfTQLDHt4OYMB4ZYWgoCJVzgl';
$consumer_secret = '0IvxiPbylx5iCQYkoTM5vq0fEYyHpNHgQnQJEzcFeNsMtS4plG';


$twitter = new TwitterOAuth($consumer_key,$consumer_secret,$access_token,$access_token_secret);



?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Twitter API SEARCH</title>
</head>
<body>

<form action="" method="post">
<label>Search : <input type="text" name="keyword"></label><br>

<?php

$con = mysqli_connect("localhost", "root","", "tweets");


if (isset($_POST['keyword'])){
  $tweets = $twitter->get('https://api.twitter.com/1.1/search/tweets.json?q='.$_POST['keyword'].'&result_type=recent&count=50');
  foreach ($tweets as $tweet){
    foreach ($tweet as $t){
      $tweet_text= $t->text;
       echo ($t->text).'<br><br>';
      $text_escaped = mysql_real_escape_string($tweet_text);
      $sql = "INSERT INTO tweets (tweet) VALUES ('$text_escaped')";

      

}

}}
     $con->close();
?>



</body>
</html>