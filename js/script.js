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
				// str += "<input class=\"show-all\" type=\"button\"
				// value=\"+\"/>";

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
							return ' visuallyhidden ' + word_class;
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

// DOING STUFF (should probably be $(document).ready()) ===================================================================

$("#go").click(getMatches);

if (getParameterByName('permalink'))
{
	// TODO check in_request and other shit
	$.getJSON('cgi-bin/GetStoredResult.py', {'id':getParameterByName('permalink')}, populateFromStoredResult);
}

// END OF DOING STUFF =====================================================================================================

function getMatches() {
	// TODO validate arg first
	// Erase previous data
	// do not continue if in request
	if (in_request == true) {
		return false;
	}
	if (template == null) {
		template = $('#row-template').clone();
	} else {
		console.log('removing container');
		$('#row-container').empty();
		$('#row-container').html(template);
	}
	// TODO check for error flag
	$('.error').addClass('visuallyhidden');
	$("#ajax-load").removeClass('visuallyhidden');
	var arg = $('#usern').val();
	// console.log('arg: ' + arg);
	$('#go').attr('disabled', true);
	in_request = true;
	/*
	 var jqxhr = $.get('cgi-bin/GetCelebMatchesJSON.py', { 'user' : arg },
	 populateMatchesFromFreshResult);
	  */
	 
	var jqxhr = $.get('mock.json', {
		'user' : arg
	}, populateMatchesFromFreshResult);
	
	console.log('txed request');
	return false;
}

function populateMatchesFromFreshResult(data) {
	console.log('rxed response');
	console.log(data);
	in_request = false;
	if (!validateData(data))
		return;
	console.log("Successful response");
	permalink_url = window.location.origin+window.location.pathname+"?permalink="+data["permalink"]
	console.log(permalink_url)
	
	populateMatches(data);
	
	$("#permalink_container").append(
			$("<span>Got your results!&nbsp;</span>")
		).append(
			$("<a>Share this link with your friends to make them jelly!</span>").attr("href",permalink_url)
		)
}

function populateMatches(data) {
	$('#go').attr('disabled', false);
	
	$('#results').render(data, directive);
	$("#ajax-load").addClass('visuallyhidden');
	/**
	 * Bind all the buttons to the correct event
	 */
	$('.word').click(
			function(arg) {

				if (deselectFilter(this)) {
					return false;
				}
				// hide all of them
				$(this).parent().siblings('.tweet_entry').addClass(
						'visuallyhidden');

				// show the top entries otherwise
				$(this).parent().siblings('.word-' + this.value).each(
						function(index) {
							if (index < 3) {
								$(this).removeClass('visuallyhidden');
							}
						});
				$(this).parent().siblings('.show-more').children('input').val(
						'SHOW MORE');

				$(this).siblings().removeClass('pressed');
				$(this).addClass('pressed');

			});

	$('.show-more input').click(

			function(arg) {
				// check for pressed filter
				var button_node;
				var button_pressed = false;
				if ((button_node = $(this).parent().siblings('.words')
						.children('.pressed')).length == 1) {
					console.log("filter " + button_node.val() + " selected");
					button_pressed = true;
				}

				if ($(this).hasClass('expanded')) {
					$(this).removeClass('expanded');
					$(this).val('SHOW MORE');
					if (button_pressed) {
						// hide extra tweets for button
						$(button_pressed).removeClass('expanded');
						$(this).parent().siblings('.word-' + button_node.val())
								.each(function(index) {
									if (index > 2) {
										$(this).addClass('visuallyhidden');
									}
								});

					} else {
						// hide extra tweets for all
						$(this).parent().siblings('.tweet_entry').each(
								function(index) {
									if (index > 2) {
										$(this).addClass('visuallyhidden');
									}
								});

					}

				} else {
					$(this).addClass('expanded');
					$(this).val('SHOW LESS');
					if (button_pressed) {
						// show extra tweets for word
						$(this).parent().siblings('.word-' + button_node.val())
								.removeClass('visuallyhidden');

					} else {
						// show extra tweets for all
						$(this).parent().siblings('.tweet_entry').removeClass(
								'visuallyhidden');
					}

				}

				return;
			});
	$('.row').removeClass('visuallyhidden');
}

function populateFromStoredResult(data) {
	if (!validateData(data)) {
		return;
	}
	
	$("#usern").val(data['user']['screen_name'])
	populateMatches(data);
}

function validateData(data) {
	if (data == null) {
		// add pic
		// $('error-pic img').attr
		dispError('null');
		ret_error('data returned is NULL');
		return false;
	} else if (data['status'] == 'error') {
		if ("error" in data)
		{
			dispError(data['error'])
		}
		else
		{
			dispError('data');
		}
		ret_error('Data has status = error');
		return false;
	}
	
	return true;
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
	if (e.which == 13) {
		getMatches();
	}
});

function deselectFilter(selector) {
	// .word class
	if ($(selector).hasClass('pressed')) {

		// deselect filter
		// give indicator
		$(this).parent().siblings('.show-more').children('input').val(
				"SHOW MORE");

		$(selector).removeClass('pressed');
		// hide all tweets again
		$(selector).parent().siblings('.tweet_entry')
				.addClass('visuallyhidden');

		// show three tweets
		$(selector).parent().siblings('.tweet_entry').each(function(index) {
			if (index < 3) {
				$(this).removeClass('visuallyhidden');
			}
		});

		return true;
	}

	return false;
}
function dispError(type) {
	// TODO create images for each error type
	// switch on error type and inject data
	$("#ajax-load").addClass('visuallyhidden');
	if (type == "protected")
	{
		$('.protected').removeClass('visuallyhidden');
	}
	else if (type == "no_tweets")
	{
		$('.no_tweets').removeClass('visuallyhidden');
	} 
	else 
	{
		$('.null').removeClass('visuallyhidden');
	}
}

function getParameterByName(name)
{
  name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
  var regexS = "[\\?&]" + name + "=([^&#]*)";
  var regex = new RegExp(regexS);
  var results = regex.exec(window.location.search);
  if(results == null)
    return "";
  else
    return decodeURIComponent(results[1].replace(/\+/g, " "));
}