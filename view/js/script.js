///* Author: Siegfried Bilstein
//
// */
var username = "Julius Ceaser";
var twitid = "juliusceaser";
var theirtweet = "Lorem ipsum dolor sit amet, <em><b>consectetur</b></em> adipiscing elit. "
		+ "Duis hendrerit justo ac augue viverra sed aliquam nulla gravida."
		+ " Phasellus posuere.";
var urtweet = "Lorem ipsum dolor sit amet, <em><b>consectetur</b></em> adipiscing elit."
		+ "In ac bibendum turpis. Curabitur non mi eros. Ut feugiat mauris"
		+ " et massa varius id.";
var picpath = "img/test.jpg";
var score = 98;
var submitted = false;
var serverBusy = false;

var debug_flag = true

function debug(string){
	if(debug_flag){
		console.log(string);
	}
}


function submitRequest() {
	debug("Submitting request");
	if (serverBusy == true) {
		return false;
	}
	// Empty results pane, word list and selector
	// Insert the loading gif

// $("#results").append(createLoading("ajaxload"));
//
// serverBusy = true;
 $.get("../test.py", {
 username : "test"
 // submit arguments
 },

 // function that is called when server returns a value.
 serverResponseHandler, "json");
	inflate();
	return;
}
function inflate(){
	$("#selector").append(createNamerow("dickhead", "img/test.jpg", 95));
	$("#results").append(createTweetrow("swag", "swag", "swag", "swag"));

}

function serverResponseHandler(data) {

	// do work swag
	console.log(data);
	// Set flag saying we are ready
	serverBusy = false;
}
// Initialize query box
$("#querybox").submit(function() {
	submitRequest();
	return false;
});

function createNamerow(name, picpath, score){
// <div class="namerow">
// <img src="img/dude.jpg" />
// <div>
// CAP'N SWAG<br> <em>98% MATCH</em>
// </div>
// </div>
  	var $row = $("<div></div>");
  	$row.addClass("namerow");
  	$row.append("<img src=\"" + picpath +"\"/><div>" + name+"<br><em>" + score +"% MATCH</em></div>");
  	return $row;
}

function createTweetrow(user_a, user_b, tweet_a, tweet_b){
	
// <div class="result_row">
// <div class="tweetbox">
// Snoop Dogg tweeted:
// <div class="tweet">sdfsfsmsfs gdfgdfg
// dfgdg dfgdfgdfg dfgdfgdfgdgf ipsum swag lorem</div>
// </div>
//
// <div class="tweetbox">
// Shwayze tweeted:
// <div class="tweet">lorem ipsum swag lorem ipsum swag lorem
// lorem ipsum swag loresdfsfsmsfs gdfgdfg dfgdg dfgdfgdfg
// dfgdfgdfgdgf ipsum swag lorem</div>
// </div>
// </div>
	$row = createResultrow();
	$d1 = $("<div></div>").addClass("tweetbox");
	$d1.append(user_a + " tweeted:");
	$d1.append($("<div></div>").addClass("tweet").append(tweet_a));

	$d2 = $("<div></div>").addClass("tweetbox");
	$d2.append(user_a + " tweeted:");
	$d2.append($("<div></div>").addClass("tweet").append(tweet_b));
	$row.append($d1);
	$row.append($d2);
	return $row;
	console.log("Swag city");
}


function createResultrow(){
	var $row = $("<div></div>");
	$row.addClass("result_row");
	return $row;
}