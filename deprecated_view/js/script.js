/* Author: Siegfried Bilstein

 */
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

function toggle() {
	if (serverBusy == true) {
		return false;
	}

	$("#results").empty();
	$("#selector").empty();
	$("#namerow").empty();
	$("#results").append(createLoading("ajaxload"));
	$("#words").empty();

	if (!submitted) {
		submitted = true;

		$("#sidebar").animate({
			"left" : "+=23%",
			"min-height" : "+=300px"
		}, "slow");

	}
	$("#ajaxload").animate({
		"min-height" : "+=250px"

	}, "slow");
	serverBusy = true;
	$.get(

	"submit.php", // Ajax file

	{
		username : $("#usern").val()
	}, // create an object will all values

	// function that is called when server returns a value.
	serverResponseHandler,
	// How you want the data formated when it is returned from the
	// server.
	"json");

	$("#words").append("Swag<br>");
	$("#words").append("Swag<br>");
	$("#words").append("Swag<br>");
	$("#words").append("Swag<br>");
	$("#selector").removeClass("hidden");

	return;

}

function serverResponseHandler(data) {

	// do work swag
	$("#ajaxload").remove();
	for (i = 0; i < 5; i++) {
		$("#results").append(
				createDesc(username, twitid, theirtweet, urtweet, picpath,
						score));

	}
	$("#results").before("<div id=\"selector\"></div>");
	$("#selector").append(createImgSelector("img/gaga.jpg", "LADY GAGA", 87));
	$("#selector").append(createImgSelector("img/test.jpg", "TEST HOMIE", 79));
	$("#selector").append(createImgSelector("img/dude.jpg", "CAP'N SWAG", 77));
	// $("#namerow").append("JULIUS CEASER <em>85% MATCH</em>");
	// Set flag saying we are ready
	serverBusy = false;
}

function createImgSelector(path, name, score) {

	var img = $("<img/>");
	img.attr("src", path);
	var div = $("<div></div>");

	div.addClass("namerow");
	div.append(img);

	div.append("<div>" + name + "<br><em>" + score + "%</em> MATCH</div>");
	return div;
}
$('#querybox').submit(function() {
	toggle();
	return false;
});

function toggleBorder() {
	if (borderon) {
		$("div").css("border", "");
		borderon = false;
	} else {
		$("div").css("border", "1px solid grey");
		borderon = true;
	}
}

function toggleText() {
	if (texton) {
		$(".tweetbox div").css("text-align", "justify");
		texton = false;
	} else {
		$(".tweetbox div").css("text-align", "left");
		texton = true;
	}

}
$("#borderbox").change(function() {
	toggleBorder();
	return false;
});

$("#justbox").change(function() {
	toggleText();
	return false;
})

function createDesc(username, twitid, theirtweet, urtweet, picpath, score) {
	var $descr = $("<div class=\"descr\"></div>");
	// $descr.append("<div class=\"username\">" + username + " <em>" + score
	// + "% NULLA</em></div>");
	$descr
			.append("<div class=\"tweetbox\"><a href=\"http://www.twitter.com/#!/"
					+ twitid
					+ "\"><em>@"
					+ username
					+ "</em></a> tweeted <div>" + theirtweet + "</div></div>");
	$descr.append("<div class=\"tweetbox\">You tweeted <div>" + urtweet
			+ "</div></div>");

	var $share = $("<div></div>");
	$share.addClass("sharerow");
	$ava = $("<div></div>").addClass("avatar");
	$ava.append("<img src=\"" + picpath + "\" alt=\"" + username + "\"/>");
	$share.append($ava);
	$res = $("<div></div>").addClass("result");
	$res.append($descr);

	$twitter = createTweetIcon(twitid);
	$share.append($twitter);
	// $res.append($share);

	return $res;

}

function createTweetIcon(twitid) {
	$link = $("<a></a>");
	$link.addClass("twitter-share-button");
	$link.attr("href", "https://twitter.com/share");
	$link.attr("data-lang", "en");
	$link.attr("data-text", "My celeb twitter match is @" + twitid
			+ "! Find yours at http://www.twitter.jelly.com");

	$script = $("<script></script>").attr("src", "js/libs/twit.js");
	// console.log($link.after($script));
	return $link.after($script);

}

function createHiddenDesc(name, score) {
	var $newDesc = $("<div class=\"result\"></div>");
	$newDesc.append("<div class=\"nameexpand\">" + name + " <em>" + score
			+ "%</em>" + "</div><div class=\"expand\">"
			+ "<a href=\"#\">Show | Show All</a>" + "</div>");

	return ($newDesc);

}

function createLoading(id) {
	var $loader = $("<div></div>");
	$loader.addClass("load");
	$loader.attr("id", id);
	$loader.append($("<img/>").attr("src", "img/loader.gif"));
	$loader.attr("align", "center");
	return $loader;
}

// Mock data

