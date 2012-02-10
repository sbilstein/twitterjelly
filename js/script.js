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
				return '<span class="celeb-name">' + arg.item.name + '</span><span class="celeb-screen">&nbsp;@' + arg.item.screen_name +"</span>";
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
			'.show-more@class+' : function(arg){
				if(arg.item.tweets.length < 4){
					return ' visuallyhidden';
				} else {
					return '';
				}
			}
			,
			'div.tweet_entry' : {
				'tweet<-match.tweets' : {
					'+.celeb.tweet' : function(arg) {
						var len = arg.item.word.length;
						var word_match = new RegExp(arg.item.word);
						// workaround in case first word is match.
						var text = arg.item.celeb_tweet.text;
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
						return new_str;
					},
					'@class+' : function(arg) {
						var word_class = ' word-' + arg.item.word;
						if (arg.pos > 2) {
							return ' visuallyhidden ' + word_class;
						}
						return word_class;
					},
					'.user.tweet' : function(arg) {
						var len = arg.item.word.length;
						var word_match = new RegExp(arg.item.word);
						var text = arg.item.user_tweet.text;
						var new_str = '';

						while ((pos = text.toLowerCase().search(word_match)) > -1) {
							new_str += text.slice(0, pos);
							new_str += '<span class="matched-word">'
									+ text.slice(pos, pos + len)
									+ '</span>';
							text = text.slice(pos + len);
						}
						new_str += text;
						return new_str;
					},
					'img.user@src' : 'user.pic_url',
					'img.celeb@src' : 'match.pic_url',
					'.user.tweetbox span a' : function(arg) {
						return '@' + arg.context.user.screen_name;
					},
					'.user.tweetbox span a@href' : function(arg) {
						return 'http://www.twitter.com/'
								+ arg.context.user.screen_name;
					},
					'.user.tweetbox span+' : function(arg) {
						return ' tweeted ';
					},
					'.celeb.tweetbox span a' : function(arg) {
						return '@' + curr_celeb;
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


$(document).ready(function(){
		// if the permalink is empty do nothing, otherwise get a stored result
	if (getParameterByName('permalink'))
	{
		// TODO check in_request and other shit
		$.getJSON('cgi-bin/GetStoredResult.py', {'id':getParameterByName('permalink')}, populateFromStoredResult);
	} else if(getParameterByName('test')) {
		$.get('mock.json', {
			'user' : 'nil'
		}, populateMatchesFromFreshResult);
		console.log('getting json baby');
	}
	// bind the go
	$("#go").click(getMatches);
})

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

	var jqxhr = $.get('cgi-bin/GetCelebMatchesJSON.py', { 'user' : arg },
	populateMatchesFromFreshResult);
	 
	
	console.log('txed request');
	return false;
}

function populateMatchesFromFreshResult(data) {
// console.log('rxed response');
// console.log(data);
	in_request = false;
	if (!validateData(data))
		return;
// console.log("Successful response");
	permalink_url = window.location.origin+window.location.pathname+"?permalink="+data["permalink_id"];
// console.log(permalink_url)
	
	populateMatches(data);
	$("#permalink").attr("href", permalink_url);
	$("#permalink").html(permalink_url);
	
	$("#permalink_container").removeClass('visuallyhidden');

// .append(
// $("<span>share your resultS&nbsp;</span>")
// ).append(
// $("<a>or copy this link</a>").attr("href",permalink_url)
// )
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
					$(this).parent().siblings('.show-more').children('input').val('SHOW MORE');
					$(this).parent().siblings('show-more').removeClass('expanded');
					$(this).parent().siblings('.show-more').children('input').attr('disabled', true);
					$(this).parent().siblings('.show-more').children('input').removeClass('visuallyhidden');
					
					return false;
				}
				// hide all of them
				$(this).parent().siblings('.tweet_entry').addClass(
						'visuallyhidden');

				// show the top entries otherwise
				$(this).parent().siblings('.word-' + this.value).each(
						function(index) {
								$(this).removeClass('visuallyhidden');
						});


				$(this).siblings().removeClass('pressed');
				$(this).addClass('pressed');
				// Instead of hiding, disable button and do showing all tweets
				$(this).parent().siblings('.show-more').children('input').attr('disabled', true);
				$(this).parent().siblings('.show-more').children('input').val('SHOWING ALL TWEETS FOR \'' +this.value.toUpperCase()+ '\'');
			});

	$('.show-more input').click(

			function(arg) {

				if ($(this).hasClass('expanded')) {
					$(this).removeClass('expanded');
					$(this).val('SHOW MORE');

						// hide extra tweets for all
						$(this).parent().siblings('.tweet_entry').each(
								function(index) {
									if (index > 2) {
										$(this).addClass('visuallyhidden');
									}
								});

				} else {
					$(this).addClass('expanded');
					$(this).val('SHOW LESS');

						$(this).parent().siblings('.tweet_entry').removeClass(
								'visuallyhidden');

				}

				return;
			});
	$('.row').removeClass('visuallyhidden');
}

function populateFromStoredResult(data) {
	if (!validateData(data)) {
		return;
	}
	
	$("#usern").val(data['user']['screen_name']);
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
			dispError(data['error']);
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
/**
 * 
 * @param Takes
 *            the name of URL param
 * @returns empty string if no parameter, otherwise return val
 */
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
