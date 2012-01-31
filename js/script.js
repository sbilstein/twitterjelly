///* Author: Siegfried Bilstein
//
// */
var tweet_text = '...';
var cur_celeb;
var directive = {
	'div.row' : {
		'match<-celeb_matches' : {
			'.matchlead' : function(arg) {
				curr_celeb = arg.item.screen_name;
				// return "you and " + arg.item.name.toUpperCase() + ' <span>98%
				// MATCH</span>';
				return '<span class="celeb-name">'
						+ arg.item.name + '</span> match on';

			},
			'div.words' : {
				"word<-match.top_words" : {
					'input.word@value' : 'word.pos'
				}
			// function(arg) {
			// var str = "matched on ";
			//
			// for ( var key in arg.item.top_words) {
			// str += " " + key.toUpperCase() + " |";
			// }
			// return str.slice(0, str.length - 2);

			},
			'div.tweet_entry' : {
				'tweet<-match.tweets' : {
					'+.celeb.tweet' : function(arg) {
						var len = arg.item.word.length;
						var word_match = new RegExp(arg.item.word);
						// workaround in case first word is match.
						var text = " " + arg.item.celeb_tweet.text;
						var new_str = '';

						while ((pos = text.toLowerCase().search(word_match)) > -1) {
							new_str += text.slice(0, pos);
							// console.log('Found match');
							// check for spaces on either side
							new_str += '<span class="matched-word">'
									+ text.slice(pos, pos + len) + '</span>';
							text = text.slice(pos + len);
						}
						new_str += text;
						// Trim out first additional space.
						return new_str.slice(1);
					},
					'a.celeb.twitlink@href' : 'tweet.celeb_tweet.url',
					'a.celeb.twitlink' : function(arg) {
						return tweet_text;
					},
					'+.user.tweet' : function(arg) {
						var word = arg.item.word;
						var text = arg.item.user_tweet.text;
						var new_str = '';

						while ((pos = text.toLowerCase().search(word)) > -1) {
							new_str += text.slice(0, pos);
							new_str += '<span class="matched-word">'
									+ text.slice(pos, pos + word.length)
									+ '</span>';
							text = text.slice(pos + word.length);
						}
						new_str += text;
						return new_str;
					}

					,

					'a.user.twitlink@href' : 'tweet.user_tweet.url',
					'a.user.twitlink' : function(arg) {
						return tweet_text;
					},
					'img.user@src' : 'user.pic_url',
					'img.celeb@src' : 'match.pic_url',
					'.user.tweetbox span a' : function(arg) {
						return arg.context.user.screen_name;
					},
					'.user.tweetbox span a@href' : function(arg) {
						return 'http://www.twitter.com/'
								+ arg.context.user.screen_name;
					},
					'.user.tweetbox span+' : function(arg) {
						return ' tweeted ';
					},
					'.celeb.tweetbox span a' : function(arg) {
						return curr_celeb;
					},
					'.celeb.tweetbox span a@href' : function(arg) {
						return 'http://www.twitter.com/' + curr_celeb;
					},
					'.celeb.tweetbox span+' : function(arg) {
						return ' tweeted ';
					}

				}
			}

		}
	}
};

$("#go").click(function() {
	// TODO validate arg first
	var arg = $('#usern').val();
	console.log('arg: ' + arg);

	// var jqxhr = $.get('cgi-bin/GetCelebMatchesJSON.py', {
	// 'user' : arg
	// }, ajax_ret);
	var jqxhr = $.get('mock.json', {
		'user' : arg
	}, ajax_ret);
	console.log('txed request');
	return false;
});

function ajax_ret(data) {
	console.log('rxed response');
	console.log(data);
	if (data == null) {
		ret_error('data returned is NULL');
		return;
	} else if (data['status'] == 'error') {
		ret_error('Data has status = error');
		return;
	}
	console.log("Successful response");
	$('#results').render(data, directive);
}

function ret_error(log) {
	console.log(log);
}
$("body").ajaxError((function(e, jqxhr, settings, exception) {
	console.log("AJAX ERROR");
}));
