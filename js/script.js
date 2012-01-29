///* Author: Siegfried Bilstein
//
// */
var data = {
	'screen_name' : 'snoop dogg',
	'pic_url' : 'img/dude.jpg',
	'tweets' : {
		'celeb_tweet' : 'swag city rack city',
		'user_tweet' : 'holler'
	},
	'user' : {
		'screen_name' : 'sbilstein',
		'pic_url' : 'img/gaga.jpg'
	}

}, directive = {
	'span.celeb_name' : 'screen_name',
	'tweet celeb' : 'tweets celeb_tweet',
	'tweet user' : 'tweets user_tweet',
	'.twitprof.celeb img@src' : 'pic_url',
	'.twitprof.user img@src' : 'user pic_url'

}

$("#querybox").submit(function() {
	$('#algo_1').render(data, directive);
	console.log("Mapped!");
	return false;
});
