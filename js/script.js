///* Author: Siegfried Bilstein
//
// */


var template = null;
var in_request = false;
var match_success = false;
var directive = {
    'div.row':{
        'match<-celeb_matches':{
            '+.matchlead':function (arg) {
                curr_celeb = arg.item.screen_name;
                var str = '<span class="celeb-name">' + arg.item.name + '</span><span class="celeb-screen">&nbsp;<a alt="See these results" href="?user=' + curr_celeb + '">@' + curr_celeb + "</a></span>";
                return str;
            },
            '.result-share a@href':function (arg) {
                var i;
                var ret_url =  'https://www.twitter.com/intent/tweet?source=celebjelly&text=hey+@' + curr_celeb +
                    '+is+my+celeb+twitter+match!+See+my+results+here+http://www.twitterjelly.com/?user=' + arg.context.user.screen_name;
//                for (var key in arg.item.top_words){
//                    ret_url += key+',+'
//                        i++;
//                    if (i > )
//                }(' + arg.item.name.replace(/ /, '+')+'

                return ret_url;
            },
            'div.words+':function (arg) {
                var str = "";

                for (var key in arg.item.top_words) {
                    str += "<input class=\"word\" title=\"Filter by " + key
                        + " \" type=\"button\" value=\"" + key + "\" >";
                    // str += "test";
                }
                // str += "<input class=\"show-all\" type=\"button\"
                // value=\"+\"/>";

                return str;

            },
            '.show-more@class+':function (arg) {
                if (arg.item.tweets.length < 4) {
                    return ' visuallyhidden';
                } else {
                    return '';
                }
            },
            'div.tweet_entry':{
                'tweet<-match.tweets':{
                    '+.celeb.tweet':function (arg) {
                        var len = arg.item.word.length;
                        var patt = hashRemove(arg.item.word.toLowerCase()) + '\\b';
                        var word_match = new RegExp();
                        word_match.compile(patt);
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
                    '@class+':function (arg) {
                        var word_class = ' word-' + hash2dash(arg.item.word);
                        if (arg.pos > 2) {
                            return ' visuallyhidden ' + word_class;
                        }
                        return word_class;
                    },
                    '.user.tweet':function (arg) {
                        var len = arg.item.word.length;
                        var patt =  hashRemove(arg.item.word.toLowerCase()) + '\\b';
                        var word_match = new RegExp();
                        word_match.compile(patt);
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
                    'img.user@src':'user.pic_url',
                    'img.celeb@src':'match.pic_url',
                    '.user.tweetbox span a':function (arg) {
                        return '@' + arg.context.user.screen_name;
                    },
                    '.user.tweetbox span a@href':function (arg) {
                        return '?user='
                            + arg.context.user.screen_name;
                    },
                    '.user.tweetbox span+':function (arg) {
                        return ' tweeted ';
                    },
                    '.celeb.tweetbox span a':function (arg) {
                        return '@' + curr_celeb;
                    },
                    '.celeb.tweetbox span a@href':function (arg) {
                        return '?user=' + curr_celeb;
                    },
                    '.celeb.tweetbox span+':function (arg) {
                        return ' tweeted ';
                    }

                }
            }

        }
    }
};


$(document).ready(function () {

    if (!console) {
        console = {
            log:function () {
            }
        };
    }
    // if the permalink is empty do nothing, otherwise get a stored result
    if (getParameterByName('permalink')) {
        initMatchLoading();
        $.getJSON('cgi-bin/GetStoredResult.py', {'id':getParameterByName('permalink')}, populateFromStoredResult);
    } else if (getParameterByName('test')) {
        //time_len is in seconds
        var time_len = parseInt(getParameterByName('time'));
        // console.log('time_len: ' + time_len);
        initMatchLoading();
        if(time_len == NaN){
            time_len = 1;
        } else {
            time_len = time_len * 1000;
        }

        var to = setTimeout(
            function(){
            $.get('mock.json', {
                'user':'nil'
            }, populateMatchesFromFreshResult);
                clearTimeout(to);
        }, time_len);

    } else if (getParameterByName('user')) {
        var user_arg = getParameterByName('user');
        $('#usern').val(user_arg);
        initMatchLoading();
        getUserMatch(user_arg);
    } else if(getParameterByName('error'))
    {
        dispError(getParameterByName('error'));
    }
    //bind the go
    $("#go").click(getMatchesFromButton);

});

/**
 *  Call the python to get celeb TFIDF matches
 * @param username
 */

function getUserMatch(username) {
    var jqxhr = $.get('cgi-bin/GetCelebMatchesJSON.py', { 'user':username },
        populateMatchesFromFreshResult);
    in_request = true;
};

/**
 * Does a bunch of cleanup, and setting templates. Must be called before any
 * rendering.
 *
 * @returns whether or not the process should continue
 */
function initMatchLoading() {
    // do not continue if in request
    match_success = false;
    if (in_request == true) {
        return false;
    }
    // store a template
    if (template == null) {
        template = $('#row-template').clone();
    } else {
		//make personality invisible
		$('#pers_section').addClass('visuallyhidden');
        // erase old container add the template so pure.js can render
        $('#row-container').empty();
        $('#row-container').html(template);
    }
    $('#permalink-container').addClass('visuallyhidden');
    $('.error').addClass('visuallyhidden');

    $('.error').empty();
    $("#ajax-load").removeClass('visuallyhidden');
    progress_update();
    return true;
}

function getMatchesFromButton() {
    if (initMatchLoading() == false) {
        return false;
    }
    var arg = $('#usern').val();
    // console.log('arg: ' + arg);
    $('#go').attr('disabled', true);

    getUserMatch(arg);

    return false;
}
/**
 * Set up a result from that isn't accesed via a permalink
 *
 * @param data
 */
function populateMatchesFromFreshResult(data) {
// console.log('rxed response');
// console.log(data);
    in_request = false;
    if (!validateData(data))
        return;
    populateMatches(data);
}
/**
 * Make the call to the rendering function using pure.js.
 * Bind the filters
 * @param data
 */
function populateMatches(data) {
    match_success = true;
    $('#go').attr('disabled', false);
    //check for a index.php specific element.

    if ($('.matchlead').length) {
        renderMatches(data);
        nav_permalink_url = "personality.php?permalink=" +data["permalink_id"];
        $("#nav_link").attr("href",nav_permalink_url);
    }
    else {
        //render personality page
        renderPersonality(data);
    }
    permalink_url = window.location.origin + window.location.pathname + "?permalink=" + data["permalink_id"];

    // console.log(permalink_url)
    //TODO convert the permalink to a bit.ly link
    shortenURLCall(permalink_url);

    $("#ajax-load").addClass('visuallyhidden');
    progress_stop();
}

function shortenURLCall(url) {
    // console.log('shorten url call');
    var jqxhr = $.get('cgi-bin/GetBitlyLink.py', { 'url':url },
        shortenURLResponse);
}

function shortenURLResponse(data) {
    // console.log('url shortened response rxed');
//    $("#nav_link").attr("href",data['url']);

    // console.log(data);
    var url = data['url'];
    $("#permalink").attr("href", url);
    $("#permalink").html(url);

    $("#permalink_container").removeClass('visuallyhidden');
}

function renderMatches(data) {
    //add nav link
    //TODO fix this call

    //render index page
    $('#results').render(data, directive);

    /**
     * Bind all the buttons to the correct event
     */
    $('.word').click(
        function (arg) {

            if (deselectFilter(this)) {
                $(this).parent().siblings('.show-more').children('input').val('SHOW MORE');
                $(this).parent().siblings('show-more').removeClass('expanded');
                $(this).parent().siblings('.show-more').children('input').attr('disabled', false);
                $(this).parent().siblings('.show-more').children('input').removeClass('visuallyhidden');

                return false;
            }
            // hide all of them
            $(this).parent().siblings('.tweet_entry').addClass(
                'visuallyhidden');
            // show the top entries otherwise
            $(this).parent().siblings('.word-' + hash2dash(this.value)).each(
                function (index) {
                    $(this).removeClass('visuallyhidden');
                });
            $(this).siblings().removeClass('pressed');
            $(this).addClass('pressed');
            // Instead of hiding, disable button and do showing all tweets
            $(this).parent().siblings('.show-more').children('input').attr('disabled', true);
            $(this).parent().siblings('.show-more').children('input').val('SHOWING ALL TWEETS FOR \'' + this.value.toUpperCase() + '\'');
        });

    $('.show-more input').click(
        function (arg) {
            if ($(this).hasClass('expanded')) {
                $(this).removeClass('expanded');
                $(this).val('SHOW MORE');
                // hide extra tweets for all
                $(this).parent().siblings('.tweet_entry').each(
                    function (index) {
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
    /**
     * TODO get this image loading working.
     */

//    $('.celeb-name').before(function(arg){
//        var celeb = $(this).html();
//        getImageForCeleb(celeb);
//        return '<img id="' + celeb.replace(/ /, '-') + '" alt="' + celeb + '"></img>';
//    });


}
/**
 * If a string is a hash tag, return a version with the hashtag replaced with a dash.
 * otherwise leave the word untouched.
 */
function hash2dash(str){
    if(str.charAt(0) == '#'){
        return '-' + str.slice(1);
    }
    return str;
}

function dash2hash(str)
{
    if(str.charAt(0) == '-'){
        return '#' + str.slice(1);
    }
    return str;
}

function hashRemove(str){
    if(str.charAt(0) == '#'){
        return str ;
    }
    //'(^|\\s)'
    return  '\\b' + str;
}

function renderPersonality(data) {
    //delete old values
    $('#pers_id').empty();
    $('.pers_dim').addClass('visuallyhidden');
    $("#pers_celebs").empty();

    //add nav link
    nav_permalink_url = "index.php?permalink=" + data["permalink_id"];
    $("#nav_link").attr("href", nav_permalink_url);

    //populate new values
    pers = data["user"]["personality"];
    $('#pers_id').append(pers);
    $('#' + pers[0]).removeClass('visuallyhidden');
    $('#' + pers[1]).removeClass('visuallyhidden');
    $('#' + pers[2]).removeClass('visuallyhidden');
    $('#' + pers[3]).removeClass('visuallyhidden');

    pers_celebs = data["celeb_matches_pers"];
    for (i = 0; i < pers_celebs.length; i = i + 1) {
        celeb_name = pers_celebs[i][0]
        pic_url = pers_celebs[i][1]
        to_append = "<div class='pers_celeb'> <a href='http://twitter.com/" + celeb_name + "'class='pers_celeb_name'>" + celeb_name + "</a><br>" +
            "<a target='_blank' href='http://twitter.com/" + celeb_name + "'><img src='" + pic_url + "'/></a>" +
            "</div>";
        $("#pers_celebs").append(to_append);
    }

    //unhide pers section
    $('#pers_section').removeClass('visuallyhidden');


}

function populateFromStoredResult(data) {
    if (!validateData(data)) {
        return;
    }

    $("#usern").val(data['user']['screen_name']);
    populateMatches(data);
}
/**
 * Ensure json repsonse is usable
 * @param data
 */
function validateData(data) {
    if (data == null) {
        // add pic
        // $('error-pic img').attr
        dispError('null');
        ret_error('data returned is NULL');
        return false;
    } else if (data['status'] == 'error') {
        if ("error" in data) {
            dispError(data['error']);
        }
        else {
            dispError('data');
        }
        ret_error('Data has status = error');
        return false;
    }

    return true;
}

function ret_error(log) {
    // console.log(log);
}
$("body").ajaxError((function (e, jqxhr, settings, exception) {
    if(match_success == false){
        dispError('ajax');
    }
    // console.log(jqxhr);
    // console.log(e);
// console.log("AJAX ERROR");
    // console.log(exception);
}));

$('#usern').keyup(function (e) {
    e.preventDefault();
    if (e.which == 13) {
        getMatchesFromButton();
    }
});
/**
 * Deselect a word-match filter
 * @param selector
 */
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
        $(selector).parent().siblings('.tweet_entry').each(function (index) {
            if (index < 3) {
                $(this).removeClass('visuallyhidden');
            }
        });

        return true;
    }

    return false;
}
function dispError(type) {
    // TODO create images for each error type and switch on error type and inject data

    var error_string;
    $("#ajax-load").addClass('visuallyhidden');
    progress_stop();
    if (type == "protected") {
        error_string = '<div><img src="img/protected.jpg"></img><p>TwitterJelly can\'t access your tweets if they' +
            ' are protected. Try using another twitter account or unprotect your' +
            'tweets if you\'d like.</p></div>';
    }
    else if (type == "no_tweets") {
        error_string = '<div class="no_tweets">'+
            '<p class="errormsg">You don\'t have any tweets!</p>' +
            '<img src="img/no_tweets.png" height="75%" width="75%"/>' +
            '</div>';
    }
    else {
        error_string = '<div class="misc">' +
            '<p class="errormsg">Whoa, something went wrong and we couldn\'t get' +
            ' your matches! We\'re sorry :(</p>' +
            '<img src="img/misc_error.png" />' +
            '</div>';
    }

    $('.error').html(error_string);
    $('.error').removeClass('visuallyhidden');
    // console.log('error should be visible');
}
/**
 *
 * @param Takes the name of URL param
 * @returns empty string if no parameter, otherwise return val
 */
function getParameterByName(name) {
    name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
    var regexS = "[\\?&]" + name + "=([^&#]*)";
    var regex = new RegExp(regexS);
    var results = regex.exec(window.location.search);
    if (results == null)
        return "";
    else
        return decodeURIComponent(results[1].replace(/\+/g, " "));
}

