///* Author: Siegfried Bilstein
//
// */

if (!console) {
	console = {
		log : function() {
		}
	};
}
var tweet_text = '...';
var cur_celeb;
var template = null;
var in_request = false;
var directive = {
	'div.row' : {
		'match<-celeb_matches' : {
			'.matchlead' : function(arg) {
				curr_celeb = arg.item.screen_name;
				// return "you and " + arg.item.name.toUpperCase() + ' <span>98%
				// MATCH</span>';
				// return 'you and <span class="celeb-name">'
				// + arg.item.name + '</span> tweet about';
				return '<span class="celeb-name">' + arg.item.name + '</span>';
			},
			'div.words+' : function(arg) {
				var str = "";

				for ( var key in arg.item.top_words) {
					str += "<input class=\"word\" title=\"Filter by " + key
							+ " \" type=\"button\" value=\"" + key + "\" >";
					// str += "test";
				}
				str += "<input class=\"show-all\" type=\"button\" value=\"...\"/>";

				return str;

			},
			'div.tweet_entry' : {
				'tweet<-match.tweets' : {
					'+.celeb.tweet' : function(arg) {
						var len = arg.item.word.length;
						var word_match = new RegExp(arg.item.word);
						// workaround in case first word is match.
						var text = "" + arg.item.celeb_tweet.text;
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
					'@class+' : function(arg) {
						var word_class = ' word-' + arg.item.word;
						if (arg.pos > 2) {
							return ' visuallyhidden' + word_class;
						}
						return word_class;
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

$("#go").click(getMatches);

function getMatches() {
	// TODO validate arg first
	// Erase previous data
	// do not continue if in request
	if (in_request == true) {
		return false;
	}
	if (template == null) {
		template = $('#row-template').clone();
		console.log(template);
	} else {
		console.log('removing container');
		$('#row-container').empty();
		$('#row-container').html(template);
	}
	// TODO check for error flag
	$('.error-pic').addClass('visuallyhidden');
	$("#ajax-load").removeClass('visuallyhidden');
	var arg = $('#usern').val();
	// console.log('arg: ' + arg);
	$('#go').attr('disabled', true);
	in_request = true;
	/**
	 * var jqxhr = $.get('cgi-bin/GetCelebMatchesJSON.py', { 'user' : arg },
	 * ajax_ret);
	 * 
	 */
	var jqxhr = $.get('mock.json', {
		'user' : arg
	}, ajax_ret);

	console.log('txed request');
	return false;
}

function ajax_ret(data) {
	console.log('rxed response');
	console.log(data);
	$('#go').attr('disabled', false);
	in_request = false;
	if (data == null) {
		// add pic
		// $('error-pic img').attr
		dispError('null');
		ret_error('data returned is NULL');
		return;
	} else if (data['status'] == 'error') {
		dispError('data');
		ret_error('Data has status = error');
		return;
	}
	console.log("Successful response");
	$('#results').render(data, directive);
	$("#ajax-load").addClass('visually hidden');
	/**
	 * Bind all the buttons to the correct event
	 */
	$('.word').click(
			function(arg) {
				$(this).parent().siblings('.tweet_entry').addClass(
						'visuallyhidden');
				$(this).parent().siblings('.word-' + this.value).removeClass(
						'visuallyhidden');
				$(this).siblings().removeClass('pressed');
				$(this).addClass('pressed');

			});

	$('.show-all').click(
			function(arg) {
				$(this).parent().siblings('.tweet_entry').removeClass(
						'visuallyhidden');
				$(this).siblings('.word').removeClass('pressed');
				$(this).addClass('pressed');
				return;
			});
	$('.row').removeClass('visuallyhidden');
}

function ret_error(log) {
	console.log(log);
}
$("body").ajaxError((function(e, jqxhr, settings, exception) {

	dispError('ajax');
	console.log("AJAX ERROR");
}));

$('#usern').keyup(function(e) {
	e.preventDefault();
	console.log("pressed a key");
	if (e.which == 13) {
		getMatches();
	}
});

function dispError(type) {
	// TODO create images for each error type
	// switch on error type and inject data
	$("#ajax-load").addClass('visuallyhidden');
	$('.error-pic').removeClass('visuallyhidden');
}
