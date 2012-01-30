///* Author: Siegfried Bilstein
//
// */

var data = {
	'celeb_matches' : [
			{
				'match_score' : 2.414154506384151,
				'name' : '',
				'pic_url' : 'https://twimg0-a.akamaihd.net/profile_images/1644506238/image003_normal.jpg',
				'screen_name' : 'souljaboy',
				'top_words' : {
					'soulja' : 4.20653
				},
				'tweets' : [
						{
							'celeb_tweet' : {
								'text' : 'RT @DrueLucas: "@souljaboy: Soulja Boy - Purp n Beans\' http://t.co/Od2z2Z0K" � soulja boy just made my day lol',
								'url' : 'http://twitter.com/souljaboy'
							},
							'user_tweet' : {
								'text' : 'lil b and soulja boy are doing what dre was doing back in 88 except less coherent and more tattoos?',
								'url' : 'http://twitter.com/sbilstein/status/105523907804659712'
							},
							'word' : 'soulja'
						},
						{
							'celeb_tweet' : {
								'text' : 'RT @HoesLocal: RT @souljaboy Soulja Boy - 50/13 (Music Video) [HD] @souljaboy: http://t.co/7voszCrO via @youtube!!!!!!!!!!!!!!!!!!!!!!!!!!!  &gt;&gt; soulja dope',
								'url' : 'http://twitter.com/souljaboy'
							},
							'user_tweet' : {
								'text' : 'trying really hard to understand how lil b and soulja boy',
								'url' : 'http://twitter.com/sbilstein/status/105523193317572608'
							},
							'word' : 'soulja'
						} ]
			},
			{
				'match_score' : 0.27696052346921524,
				'name' : '',
				'pic_url' : 'https://twimg0-a.akamaihd.net/profile_images/1644506238/image003_normal.jpg',
				'screen_name' : 'chrisbosh',
				'top_words' : {
					'floridians' : 0.44357,
					'seattle' : 0.00642854
				},
				'tweets' : [ {
					'celeb_tweet' : {
						'text' : 'Thanks to FIU and south floridians. Had a great time at the game. The environment was INCREDIBLE! #imissbasketball',
						'url' : 'http://twitter.com/chrisbosh'
					},
					'user_tweet' : {
						'text' : "Lol at texans thinking they're good at hurricanes. When Ike hit us floridians living in  houston thought it was a breeze",
						'url' : 'http://twitter.com/sbilstein/status/107173980280066048'
					},
					'word' : 'floridians'
				} ]
			},
			{
				'match_score' : 0.1405331468496224,
				'name' : '',
				'pic_url' : 'https://twimg0-a.akamaihd.net/profile_images/1644506238/image003_normal.jpg',
				'screen_name' : 'Ludacris',
				'top_words' : {
					'luda' : 0.264545
				},
				'tweets' : [
						{
							'celeb_tweet' : {
								'text' : 'RT @AguaAzulMorena: Luda!! Sofia!! RT @SofiaVergara: @ludacris in the house! http://t.co/U4kL1j74',
								'url' : 'http://twitter.com/Ludacris'
							},
							'user_tweet' : {
								'text' : 'fuck, whatever. luda http://t.co/jum2gJGl',
								'url' : 'http://twitter.com/sbilstein/status/142169376622252033'
							},
							'word' : 'luda'
						},
						{
							'celeb_tweet' : {
								'text' : "RT @Swaggin_Gio: @Ludacris mixtape is dope can't wait till your new album Ludaversal 2012 shit bout to be fire! Keep it up luda!",
								'url' : 'http://twitter.com/Ludacris'
							},
							'user_tweet' : {
								'text' : 'well Seattle, if i have to be the only person who drives with the windows down blasting luda at all times, so be it.',
								'url' : 'http://twitter.com/sbilstein/status/105835787492405248'
							},
							'word' : 'luda'
						} ]
			},
			{
				'match_score' : 0.058748165884048284,
				'name' : '',
				'pic_url' : 'https://twimg0-a.akamaihd.net/profile_images/1644506238/image003_normal.jpg',
				'screen_name' : 'DougBenson',
				'top_words' : {
					'icehouse' : 0.0927043,
					'miami' : 0.00521462
				},
				'tweets' : [ {
					'celeb_tweet' : {
						'text' : 'RT @surrenderedflow: @DougBenson this is EXACTLY what you said would happen during an icehouse podcast - #potheadsaresmart http://t.co/hD5ZGU2N',
						'url' : 'http://twitter.com/DougBenson'
					},
					'user_tweet' : {
						'text' : '@RocktheBurch real talk. Twitter friends: come to icehouse tonight for tacos and my last night in Houston till like beer bike',
						'url' : 'http://twitter.com/sbilstein/status/81467376872341504'
					},
					'word' : 'icehouse'
				} ]
			} ],
	'celeb_matches_pers' : [ 'TedNugent', 'andy_murray', 'lisalampanelli',
			'missravensymone' ],
	'user' : {
		'name' : 'Siegfried Bilstein',
		'personality' : 'ECTJ',
		'pic_url' : 'http://a2.twimg.com/profile_images/1029382216/prof_normal.jpg',
		'screen_name' : 'sbilstein'
	}
};

var directive = {
	'div.row' : {
		'match<-celeb_matches' : {
			'.matchlead' : function(arg) {
				return arg.item.screen_name.toUpperCase();

			},
			'.words span' : {
				'word<-match.top_words' : {
					'.' : 'word.pos'
				}
			},
			'div.tweet_entry' : {
				'tweet<-match.tweets' : {
					'+.celeb.tweet' : 'tweet.celeb_tweet.text',
					'a.celeb.twitlink@href' : 'tweet.celeb_tweet.url',
					'a.user.twitlink' : function(arg) {
						return 'link';
					},
					'+.user.tweet' : 'tweet.user_tweet.text',
					'a.user.twitlink@href' : 'tweet.user_tweet.url',
					'a.user.twitlink' : function(arg) {
						return 'link';
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
						return arg.context.user.screen_name;
					},
					'.celeb.tweetbox span a@href' : function(arg) {
						return 'http://www.twitter.com/'
								+ arg.context.user.screen_name;
					},
					'.celeb.tweetbox span+' : function(arg) {
						return ' tweeted ';
					}

				}
			}

		}
	}
};

$("#querybox").submit(function() {
	$('#results').render(data, directive);
	console.log("Mapped!");
	return false;
});
