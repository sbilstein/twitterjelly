/* Author: Siegfried Bilstein

 */
var username = "Snoop Dogg";
var twitid = "snoopdogg";
var theirtweet = "puffin blunts at work lol"
		+ "w/ @BUNBTRILLOG Sailor Swag all the way cuzzin. "
		+ "Also mad respect for my favorite lag football team"
		+ " the raiders!<3";
var urtweet = "I got bitches in the living room gettin\' it on "
		+ "And, they ain't leavin' 'til six in the mornin\'"
		+ "So what you wanna do? Shit, I got a pocket";
var picpath = "img/snoop.jpg";
var score = 98;
var submitted = false;
var serverBusy = false;

function toggle() {
	if (serverBusy == true) {
		return false;
	}

	$("#results").empty();
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
	// Set flag saying we are ready
	serverBusy = false;
}

$('#querybox').submit(function() {
	toggle();
	return false;
});

function createDesc(username, twitid, theirtweet, urtweet, picpath, score) {
	var $descr = $("<div class=\"descr\"></div>");
	$descr.append("<div class=\"username\">" + username + " <em>" + score
			+ "% MATCH</em></div>");
	$descr
			.append("<div class=\"tweetbox\"><a href=\"http://www.twitter.com/#!/"
					+ twitid
					+ "\"><em>@SnoopDogg</em></a> tweeted <div>"
					+ theirtweet + "</div></div>");
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
	$res.append($share);

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
	$loader.addClass("result");
	$loader.attr("id", id);
	$loader.append($("<img/>").attr("src", "img/loader.gif"));
	$loader.attr("align", "center");
	return $loader;
}

// Mock data

