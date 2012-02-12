///* Author: Siegfried Bilstein
//
// */

if (!console) {
    console = {
        log:function () {
        }
    };
}
var tweet_text = '...';
var cur_celeb;
var template = null;
var in_request = false;
var directive = {
    'div.row':{
        'match<-celeb_matches':{
            '+.matchlead':function (arg) {
                curr_celeb = arg.item.screen_name;
                // return "you and " + arg.item.name.toUpperCase() + ' <span>98%
                // MATCH</span>';
                // return 'you and <span class="celeb-name">'
                // + arg.item.name + '</span> tweet about';

                var str = '<span class="celeb-name">' + arg.item.name + '</span><span class="celeb-screen">&nbsp;@' + curr_celeb + "</span>";
                return str;
            },
            '.result-share a@href':function (arg) {

                return 'https://www.twitter.com/intent/tweet?source=celebjelly&text=TWATTER+CELEB+MATCH+IS+@' + curr_celeb + '.+WE+BOTH+USE+DA+WORDS.+CHECK+MY+RESULTS!';
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
                    '@class+':function (arg) {
                        var word_class = ' word-' + hash2dash(arg.item.word);
                        if (arg.pos > 2) {
                            return ' visuallyhidden ' + word_class;
                        }
                        return word_class;
                    },
                    '.user.tweet':function (arg) {
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
                    'img.user@src':'user.pic_url',
                    'img.celeb@src':'match.pic_url',
                    '.user.tweetbox span a':function (arg) {
                        return '@' + arg.context.user.screen_name;
                    },
                    '.user.tweetbox span a@href':function (arg) {
                        return 'http://www.twitter.com/'
                            + arg.context.user.screen_name;
                    },
                    '.user.tweetbox span+':function (arg) {
                        return ' tweeted ';
                    },
                    '.celeb.tweetbox span a':function (arg) {
                        return '@' + curr_celeb;
                    },
                    '.celeb.tweetbox span a@href':function (arg) {
                        return 'http://www.twitter.com/' + curr_celeb;
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
    // if the permalink is empty do nothing, otherwise get a stored result
    if (getParameterByName('permalink')) {
        initMatchLoading();
        $.getJSON('cgi-bin/GetStoredResult.py', {'id':getParameterByName('permalink')}, populateFromStoredResult);
    } else if (getParameterByName('test')) {
        initMatchLoading();
        $.get('mock.json', {
            'user':'nil'
        }, populateMatchesFromFreshResult);
        console.log('getting json baby');
    } else if (getParameterByName('user')) {
        initMatchLoading();
        var user_arg = getParameterByName('user');
        getUserMatch(user_arg);
    }
    //bind the go
    $("#go").click(getMatchesFromButton);

})

/**
 * Call the python to get celeb TFIDF matches
 * @param username
 */
function getUserMatch(username) {
    var jqxhr = $.get('cgi-bin/GetCelebMatchesJSON.py', { 'user':username },
        populateMatchesFromFreshResult);
    in_request = true;
}
;
/**
 * Does a bunch of cleanup, and setting templates. Must be called before any
 * rendering.
 *
 * @returns whether or not the process should continue
 */
function initMatchLoading() {
    // do not continue if in request
    if (in_request == true) {
        return false;
    }
    // store a template
    if (template == null) {
        template = $('#row-template').clone();
    } else {
        // erase old container add the template so pure.js can render
        $('#row-container').empty();
        $('#row-container').html(template);
    }
    $('.error').addClass('visuallyhidden');
    $('.error').children().addClass('visuallyhidden');
    $("#ajax-load").removeClass('visuallyhidden');
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

    console.log(permalink_url)
    //TODO convert the permalink to a bit.ly link
    shortenURLCall(permalink_url);

    $("#ajax-load").addClass('visuallyhidden');
}

function shortenURLCall(url) {
       console.log('shorten url call');
    var jqxhr = $.get('cgi-bin/GetBitlyLink.py', { 'url':url },
        shortenURLResponse);

}

function shortenURLResponse(data) {
    console.log('url shortened response rxed');
//    $("#nav_link").attr("href",data['url']);

    console.log(data);
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
                $(this).parent().siblings('.show-more').children('input').attr('disabled', true);
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
            "<a href='http://twitter.com/" + celeb_name + "'><img src='" + pic_url + "'/></a>" +
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
    console.log(log);
}
$("body").ajaxError((function (e, jqxhr, settings, exception) {

    dispError('ajax');
    console.log("AJAX ERROR");
    console.log(exception);
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
    $("#ajax-load").addClass('visuallyhidden');
    if (type == "protected") {
        $('.protected').removeClass('visuallyhidden');
    }
    else if (type == "no_tweets") {
        $('.no_tweets').removeClass('visuallyhidden');
    }
    else {
        $('.misc').removeClass('visuallyhidden');
    }
    $('.error').removeClass('visuallyhidden');
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
