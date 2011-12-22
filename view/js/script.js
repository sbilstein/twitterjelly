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
var borderon = false;
var texton = false;

function submit() {
	if (serverBusy == true) {
		return false;
	}
	// Empty results pane, word list and selector
	// Insert the loading gif
	
	$("#results").append(createLoading("ajaxloadgif"));
	
	
	serverBusy = true;
	$.get( "submit.php",
	{
		username : $("#usern").val() //submit arguments
	}, 

	// function that is called when server returns a value.
	serverResponseHandler,
	"json");

	return;
}

function serverResponseHandler(data) {

	// do work swag
	$("#ajaxloadgif").remove();
	for (i = 0; i < 5; i++) {
		$("#results").append(
				createDesc(username, twitid, theirtweet, urtweet, picpath,
						score));

	}
	$("#results").before("<div id=\"selector\"></div>");
	$("#selector").append(createImgSelector("img/gaga.jpg", "LADY GAGA", 87));

	// Set flag saying we are ready
	serverBusy = false;
}
//
function createLoading(id) {
	var $loader = $("<div></div>");
	$loader.addClass("ajaxload");
	$loader.attr("id", id);
	$loader.append($("<img/>").attr("src", "img/loader.gif"));
	$loader.attr("align", "center");
	return $loader;
}

