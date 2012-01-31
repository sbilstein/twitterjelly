///* Author: Siegfried Bilstein
//
// */
var tweet_text = '...';
var cur_celeb;
var data_sample = {
	"status" : "ok",
	"celeb_matches" : [
			{
				"screen_name" : "craigferguson",
				"match_score" : 0.4274964368380887,
				"top_words" : {
					"fucking" : 0.607759
				},
				"tweets" : [ {
					"user_tweet" : {
						"url" : "http://twitter.com/tjfaust/status/162970911442608128",
						"text" : "It is a fucking amateur hour free-for-all at SFO. Guy in front of me tried to weigh his kid on the checked baggage scale."
					},
					"word" : "fucking",
					"celeb_tweet" : {
						"url" : "http://twitter.com/craigferguson/status/57470002",
						"text" : "At work, slurping an americano, fucking with data, missing my couch."
					}
				} ],
				"pic_url" : "http://a1.twimg.com/sticky/default_profile_images/default_profile_6_normal.png",
				"name" : "Craig Ferguson"
			},
			{
				"screen_name" : "youngbuck",
				"match_score" : 0.367200970865024,
				"top_words" : {
					"buck" : 0.144339
				},
				"tweets" : [
						{
							"user_tweet" : {
								"url" : "http://twitter.com/tjfaust/status/158979880032284672",
								"text" : "Joe Buck remains LAPD's single least successful suicide threat negotiator. Everyone has jumped."
							},
							"word" : "buck",
							"celeb_tweet" : {
								"url" : "http://twitter.com/youngbuck/status/154963040545157120",
								"text" : "RT @redda2150: @youngbuck just ordered my t, can't wait to rep young buck out here in Australia !!!! young buck is for the people!!"
							}
						},
						{
							"user_tweet" : {
								"url" : "http://twitter.com/tjfaust/status/158913934399774721",
								"text" : "I have been thinking about Joe Buck for nearly eight hours in a row now. Can this cause brain cancer or something?"
							},
							"word" : "buck",
							"celeb_tweet" : {
								"url" : "http://twitter.com/youngbuck/status/152235404081369089",
								"text" : "\u00e2\u0080\u009c@lmallory29: @youngbuck What does that mean Mr. Buck? :-)\u00e2\u0080\u009d&lt;&lt;&lt;&lt;&lt;#1000ADAY Lol!!"
							}
						},
						{
							"user_tweet" : {
								"url" : "http://twitter.com/tjfaust/status/158913493234487298",
								"text" : "The next Godspeed You! Black Emperor album is just a 90min recording of Joe Buck describing different ways of building sandcastles to a dog."
							},
							"word" : "buck",
							"celeb_tweet" : {
								"url" : "http://twitter.com/youngbuck/status/151857374800523264",
								"text" : "RT @LTL_dunndunn: @youngbuck Need that new Buck #LiveLoyalDieRich"
							}
						},
						{
							"user_tweet" : {
								"url" : "http://twitter.com/tjfaust/status/158825814304100353",
								"text" : "\"Joe Buck: telling bedtime stories on Sundays at 1 from September to January\" -- @MapsRubin"
							},
							"word" : "buck",
							"celeb_tweet" : {
								"url" : "http://twitter.com/youngbuck/status/152097519705399296",
								"text" : "\u00e2\u0080\u009c@ManOfSteel88: @youngbuck Changed the avi....get em Buck!\u00e2\u0080\u009d#1000ADAY"
							}
						},
						{
							"user_tweet" : {
								"url" : "http://twitter.com/tjfaust/status/158823959272497152",
								"text" : "A drunk driver plows into the side of the building. Joe Buck looks up from his meal. \"That is not where cars go,\" he stammers."
							},
							"word" : "buck",
							"celeb_tweet" : {
								"url" : "http://twitter.com/youngbuck/status/151857244521246720",
								"text" : "RT @JinMing0622: @youngbuck Young Buck is very underrated. He's not a saleout"
							}
						},
						{
							"user_tweet" : {
								"url" : "http://twitter.com/tjfaust/status/158822730249146369",
								"text" : "Joe Buck was giving a tour of a sports-themed wax museum. When he reached his own statue, he forgot which one of them was the real Joe Buck."
							},
							"word" : "buck",
							"celeb_tweet" : {
								"url" : "http://twitter.com/youngbuck/status/151863639513628673",
								"text" : "RT @Wildlife_Foe: Buck shakin my TL he #LilBoTuff #GoLoco! @youngbuck"
							}
						},
						{
							"user_tweet" : {
								"url" : "http://twitter.com/tjfaust/status/158822730249146369",
								"text" : "Joe Buck was giving a tour of a sports-themed wax museum. When he reached his own statue, he forgot which one of them was the real Joe Buck."
							},
							"word" : "buck",
							"celeb_tweet" : {
								"url" : "http://twitter.com/youngbuck/status/151863221005979649",
								"text" : "RT @Jayvit0: @youngbuck hood need that Buck music Fu*k the distraction"
							}
						},
						{
							"user_tweet" : {
								"url" : "http://twitter.com/tjfaust/status/158821763235581952",
								"text" : "The Joe Buck recipe book spends most of its time describing ways to cut onions. There are fourteen illustrations in the \"diced\" section."
							},
							"word" : "buck",
							"celeb_tweet" : {
								"url" : "http://twitter.com/youngbuck/status/151863000037466113",
								"text" : "RT @ITsJord_: @youngbuck Everybody is on the Young Buck hype tonight"
							}
						},
						{
							"user_tweet" : {
								"url" : "http://twitter.com/tjfaust/status/158819171227013120",
								"text" : "Joe Buck slideshows are legally defined as torture and are not allowed in Guantanamo. The iron glove of oppression uses PowerPoint."
							},
							"word" : "buck",
							"celeb_tweet" : {
								"url" : "http://twitter.com/youngbuck/status/154222416195883010",
								"text" : "\u00e2\u0080\u009c@Takebreadcheif: @youngbuck how much a verse a hit me foe buck.\u00e2\u0080\u009d/bookingbuck@gmail.com"
							}
						},
						{
							"user_tweet" : {
								"url" : "http://twitter.com/tjfaust/status/158818729944285185",
								"text" : "Joe Buck gives you a slideshow of his trip to SF. \"This is me on Market Street. It is one of the biggest streets in San Francisco.\""
							},
							"word" : "buck",
							"celeb_tweet" : {
								"url" : "http://twitter.com/youngbuck/status/152080239663644673",
								"text" : "\u00e2\u0080\u009c@marc_BwS_UK: @youngbuck check my avi buck support from the uk!\u00e2\u0080\u009d/#1000ADAY"
							}
						},
						{
							"user_tweet" : {
								"url" : "http://twitter.com/tjfaust/status/158817906191380480",
								"text" : "\"There are many kinds of coffee,\" explains Joe Buck to the Blue Bottle barista. \"Sometimes the beans are roasted for a long time.\""
							},
							"word" : "buck",
							"celeb_tweet" : {
								"url" : "http://twitter.com/youngbuck/status/152090495730987011",
								"text" : "RT @Chineseyez: @Youngbuck changed that avi.u already follow but ill always support..so get buck bitch!!!"
							}
						},
						{
							"user_tweet" : {
								"url" : "http://twitter.com/tjfaust/status/158817223014760448",
								"text" : "The NextMuni sign blinks \"2 min\" for five minutes. \"The bus is not here,\" says Joe Buck, \"it's not.\" He shifts his weight from foot to foot."
							},
							"word" : "buck",
							"celeb_tweet" : {
								"url" : "http://twitter.com/youngbuck/status/154975951988600833",
								"text" : "\u00e2\u0080\u009c@Neika2012: @youngbuck buck I'm getting that shirt I'm order it asap\u00e2\u0080\u009d/#SALUTE"
							}
						},
						{
							"user_tweet" : {
								"url" : "http://twitter.com/tjfaust/status/158816763050606592",
								"text" : "Joe Buck stands on the Golden Gate Bridge looking out onto the sunset. \"The sun is setting,\" he explains to nobody in particular"
							},
							"word" : "buck",
							"celeb_tweet" : {
								"url" : "http://twitter.com/youngbuck/status/152173150526902272",
								"text" : "\u00e2\u0080\u009c@Stulittle: @TheDJIceberg @youngbuck let's work Buck the homie!!!\u00e2\u0080\u009d/#1000ADAY Let's Go!!"
							}
						},
						{
							"user_tweet" : {
								"url" : "http://twitter.com/tjfaust/status/158816688706560000",
								"text" : "Joe Buck tries to buy skunk weed from some street kids in the Haight. He texts Troy Aikman to \"do the talking for him\""
							},
							"word" : "buck",
							"celeb_tweet" : {
								"url" : "http://twitter.com/youngbuck/status/152466709561868288",
								"text" : "RT @Elitenashville: With @youngbuck and @PEARLLION got that #LiveLoyalDieRich bumping. Wow is all I can say. BUCK the truth"
							}
						},
						{
							"user_tweet" : {
								"url" : "http://twitter.com/tjfaust/status/158816654485237760",
								"text" : "Joe Buck is jumped by the Bush Guy in the Wharf. \"Oh,\" he says, sweating."
							},
							"word" : "buck",
							"celeb_tweet" : {
								"url" : "http://twitter.com/youngbuck/status/152078956349239296",
								"text" : "\u00e2\u0080\u009c@DBuss270: On my Buck shit! Check da avi Ca$hville Ten-A-Key! @youngbuck\u00e2\u0080\u009d/#1000ADAY"
							}
						} ],
				"pic_url" : "http://a3.twimg.com/profile_images/1734443926/LLDRSHIRT_normal.jpg",
				"name" : "The Real Young Buck"
			},
			{
				"screen_name" : "trohman",
				"match_score" : 0.14322638690619308,
				"top_words" : {
					"discern" : 0.213115
				},
				"tweets" : [ {
					"user_tweet" : {
						"url" : "http://twitter.com/tjfaust/status/161654214894956546",
						"text" : "I'm losing my ability to discern GOP debate talking points from @timheidecker parody speeches."
					},
					"word" : "discern",
					"celeb_tweet" : {
						"url" : "http://twitter.com/trohman/status/156378474318270464",
						"text" : "Didn't he really say...RT @MatthewRubano: RT As far as we can discern, the sole purpose of human existence is to buy a Kindle.-Carl Jung"
					}
				} ],
				"pic_url" : "http://a2.twimg.com/profile_images/574920906/DSC_0058_2_normal.jpg",
				"name" : "Joseph Trohman"
			},
			{
				"screen_name" : "anamariecox",
				"match_score" : 0.09539650718580628,
				"top_words" : {
					"newt" : 0.152777
				},
				"tweets" : [ {
					"user_tweet" : {
						"url" : "http://twitter.com/tjfaust/status/162701714313576449",
						"text" : "If there is a God and He is Good, then He'll let Newt win the GOP nomination."
					},
					"word" : "newt",
					"celeb_tweet" : {
						"url" : "http://twitter.com/anamariecox/status/157547056918036481",
						"text" : "RT @BashirLive: 3 pm cont Top Lines @anamariecox @capehartj #gop #2012 #SC #newt / @RepBarbaraLee #incomegap #palin / @Isikoff_Files #superpacs @msnbctv"
					}
				} ],
				"pic_url" : "http://a3.twimg.com/profile_images/1632642063/tumblr_lubgglxDWo1r5gmoeo1_500_normal.jpg",
				"name" : "Ana Marie Cox"
			},
			{
				"screen_name" : "joerogan",
				"match_score" : 0.08242091330374955,
				"top_words" : {
					"fucking" : 0.0192272,
					"joe" : 0.0318905,
					"newt" : 0.007801
				},
				"tweets" : [
						{
							"user_tweet" : {
								"url" : "http://twitter.com/tjfaust/status/158979880032284672",
								"text" : "Joe Buck remains LAPD's single least successful suicide threat negotiator. Everyone has jumped."
							},
							"word" : "joe",
							"celeb_tweet" : {
								"url" : "http://twitter.com/joerogan/status/154819964363214849",
								"text" : "RT @Cloud_ax: @joerogan Newt needs to realize you can't fool us like that now in the internet age. We'll find out the truth."
							}
						},
						{
							"user_tweet" : {
								"url" : "http://twitter.com/tjfaust/status/158978821670965248",
								"text" : "Joe Buck's first audition was the bad guy in a Cookie Crisp spot. \"Cookies aren't for breakfast,\" he whispered into the mic. \"Not cookies.\""
							},
							"word" : "joe",
							"celeb_tweet" : {
								"url" : "http://twitter.com/joerogan/status/154825113462767616",
								"text" : "RT @jScottDay: @joerogan Newt, Marijuana goes back to the Pyramids of Egypt punk! Check it! #SeshatCannabisGod http://t.co/JAkxuHDQ"
							}
						},
						{
							"user_tweet" : {
								"url" : "http://twitter.com/tjfaust/status/158970328847097856",
								"text" : "You're not allowed to call Joe Buck's dog a 'good boy.' \"He is not a boy,\" Joe begins to explain. \"He is a dog. They are very different.\""
							},
							"word" : "joe",
							"celeb_tweet" : {
								"url" : "http://twitter.com/joerogan/status/147249739648339968",
								"text" : "Thanks to @joelmchale for having me on @The Soup tonight!  Fucking hilarious show!  I had a great time!"
							}
						},
						{
							"user_tweet" : {
								"url" : "http://twitter.com/tjfaust/status/158970328847097856",
								"text" : "You're not allowed to call Joe Buck's dog a 'good boy.' \"He is not a boy,\" Joe begins to explain. \"He is a dog. They are very different.\""
							},
							"word" : "joe",
							"celeb_tweet" : {
								"url" : "http://twitter.com/joerogan/status/158092613583503360",
								"text" : "RT @onefivebbeastin: @joerogan http://t.co/R5WQOCnN We are living in the fucking future. Smart window."
							}
						},
						{
							"user_tweet" : {
								"url" : "http://twitter.com/tjfaust/status/158913934399774721",
								"text" : "I have been thinking about Joe Buck for nearly eight hours in a row now. Can this cause brain cancer or something?"
							},
							"word" : "joe",
							"celeb_tweet" : {
								"url" : "http://twitter.com/joerogan/status/154770148190990338",
								"text" : "RT @GlothrDraven: @joerogan http://t.co/EAScYVde and to think, at any time he could go apeshit and massacre that family. People are fucking CRAZY son."
							}
						},
						{
							"user_tweet" : {
								"url" : "http://twitter.com/tjfaust/status/158913493234487298",
								"text" : "The next Godspeed You! Black Emperor album is just a 90min recording of Joe Buck describing different ways of building sandcastles to a dog."
							},
							"word" : "joe",
							"celeb_tweet" : {
								"url" : "http://twitter.com/joerogan/status/151458854989856768",
								"text" : "RT @OMGitsJayRay: @joerogan , the media fucking with Ron Paul AGAIN! CNN's edited footage http://t.co/GXv3evlm Raw Footage - http://t.co/Sj9PxnjT"
							}
						},
						{
							"user_tweet" : {
								"url" : "http://twitter.com/tjfaust/status/162970911442608128",
								"text" : "It is a fucking amateur hour free-for-all at SFO. Guy in front of me tried to weigh his kid on the checked baggage scale."
							},
							"word" : "fucking",
							"celeb_tweet" : {
								"url" : "http://twitter.com/joerogan/status/157677850521112577",
								"text" : "@KidSagan that's a fucking amazing quote. I fucking love Carl Sagan"
							}
						},
						{
							"user_tweet" : {
								"url" : "http://twitter.com/tjfaust/status/162819777117691904",
								"text" : "\"I enjoy a mutually satisfying and loving relationship with my cat.\" -- fucking nobody"
							},
							"word" : "fucking",
							"celeb_tweet" : {
								"url" : "http://twitter.com/joerogan/status/158279601028743168",
								"text" : "@KitCope yeah, it's a pretty fucking trippy path of research! That was one wild fucking culture, that's for sure."
							}
						},
						{
							"user_tweet" : {
								"url" : "http://twitter.com/tjfaust/status/161289619512631296",
								"text" : "@KHil NO BUT A PUNT RETURN WAS FUCKING DROPPED AND THE FUCKING GIANTS RECOVERED IN FIELD GOAL RANGE"
							},
							"word" : "fucking",
							"celeb_tweet" : {
								"url" : "http://twitter.com/joerogan/status/155518843652030464",
								"text" : "Stole it or not, god damn they knocked that song out of the fucking park.\nThat's a fucking powerful piece of musical art."
							}
						},
						{
							"user_tweet" : {
								"url" : "http://twitter.com/tjfaust/status/161289619512631296",
								"text" : "@KHil NO BUT A PUNT RETURN WAS FUCKING DROPPED AND THE FUCKING GIANTS RECOVERED IN FIELD GOAL RANGE"
							},
							"word" : "fucking",
							"celeb_tweet" : {
								"url" : "http://twitter.com/joerogan/status/155523539892584448",
								"text" : "@J_Walt_ Yup.  I'm a total hypocrite.  I fucking hate that they stole it but fucking love the way it sounds. They've got to deal with grief"
							}
						},
						{
							"user_tweet" : {
								"url" : "http://twitter.com/tjfaust/status/158979250974752769",
								"text" : ".@KathleenAlcott Q. How do you know when you've met someone who runs a zine? A. They fucking tell you."
							},
							"word" : "fucking",
							"celeb_tweet" : {
								"url" : "http://twitter.com/joerogan/status/145583812674469888",
								"text" : "@OpieRadio Wow.  That's fucking ridiculous."
							}
						},
						{
							"user_tweet" : {
								"url" : "http://twitter.com/tjfaust/status/158642819223912449",
								"text" : "Going to say this once just to get it over with: SPORTS! AAAAAH! SPORTS! AAAAAH! GO PACKERS. GO. FUCKING. PACK. GO. SPORTS!"
							},
							"word" : "fucking",
							"celeb_tweet" : {
								"url" : "http://twitter.com/joerogan/status/149079971535654912",
								"text" : "@ConorHeun is it really? What a fucking awesome choice!!"
							}
						},
						{
							"user_tweet" : {
								"url" : "http://twitter.com/tjfaust/status/158355946572226560",
								"text" : "What. A. Fucking. Catch. What a fucking quarter! Vernon Davis is not human."
							},
							"word" : "fucking",
							"celeb_tweet" : {
								"url" : "http://twitter.com/joerogan/status/152887521779527680",
								"text" : "@KudzuGorilla That was pretty fucking sweet."
							}
						},
						{
							"user_tweet" : {
								"url" : "http://twitter.com/tjfaust/status/158355946572226560",
								"text" : "What. A. Fucking. Catch. What a fucking quarter! Vernon Davis is not human."
							},
							"word" : "fucking",
							"celeb_tweet" : {
								"url" : "http://twitter.com/joerogan/status/144664153964036096",
								"text" : "@reidshikuma Jesus.  That's a lot of fucking pressure.  Congrats on the kid!"
							}
						} ],
				"pic_url" : "http://a1.twimg.com/profile_images/1743185056/Joe_Rogan_trippy_peace2_normal.jpg",
				"name" : "Joe Rogan"
			},
			{
				"screen_name" : "davidgregory",
				"match_score" : 0.07762113586177871,
				"top_words" : {
					"joe" : 0.00671168,
					"newt" : 0.10273
				},
				"tweets" : [
						{
							"user_tweet" : {
								"url" : "http://twitter.com/tjfaust/status/158979880032284672",
								"text" : "Joe Buck remains LAPD's single least successful suicide threat negotiator. Everyone has jumped."
							},
							"word" : "joe",
							"celeb_tweet" : {
								"url" : "http://twitter.com/davidgregory/status/160909277261873152",
								"text" : "RT @murphymike: Tune in #MTP tmmrw for full SC analysis from @chucktodd, @joenbc, @kattykaybbc and yours truly. Plus Newt and Christie. Politics galore!"
							}
						},
						{
							"user_tweet" : {
								"url" : "http://twitter.com/tjfaust/status/158978821670965248",
								"text" : "Joe Buck's first audition was the bad guy in a Cookie Crisp spot. \"Cookies aren't for breakfast,\" he whispered into the mic. \"Not cookies.\""
							},
							"word" : "joe",
							"celeb_tweet" : {
								"url" : "http://twitter.com/davidgregory/status/160898452065222657",
								"text" : "RT @JoeNBC: No. But a Newt Florida win would be the first step. RT @jmillstead @joenbc does #sc results get us closer to brokered convention?"
							}
						} ],
				"pic_url" : "http://a2.twimg.com/profile_images/1683416665/Gregory__David_09_copy_normal.jpg",
				"name" : "David Gregory"
			},
			{
				"screen_name" : "TroyAikman",
				"match_score" : 0.06886189602600759,
				"top_words" : {
					"buck" : 0.0200246,
					"joe" : 0.00892527
				},
				"tweets" : [ {
					"user_tweet" : {
						"url" : "http://twitter.com/tjfaust/status/158979880032284672",
						"text" : "Joe Buck remains LAPD's single least successful suicide threat negotiator. Everyone has jumped."
					},
					"word" : "buck",
					"celeb_tweet" : {
						"url" : "http://twitter.com/TroyAikman/status/161298021643063297",
						"text" : "Thanks Maria...congrats to your Pats...Super Bowl XLVI will be fun! RT @mariamenounos: @troyaikman and @buck -nice job today."
					}
				} ],
				"pic_url" : "http://a2.twimg.com/profile_images/1635653038/309008_2364595525867_1579760544_2236938_139416037_n_normal.jpg",
				"name" : "Troy Aikman"
			} ],
	"celeb_matches_pers" : [ "ErictheActor", "KeikoAgena", "AlexAlbrecht",
			"lobosworth" ],
	"user" : {
		"personality" : "ECTM",
		"pic_url" : "http://a2.twimg.com/profile_images/1677605390/AIbEiAIAAABDCPOt9e-bvZujYyILdmNhcmRfcGhvdG8qKDZiYjFhMjVhOWYyNzBmYzVlYmJmZWVkY2I0NzQ2ZDI3MWQ2YjZhNjEwAfsKqekI3TRVb8LD6QVADLgVwY25_normal.jpg",
		"screen_name" : "tjfaust",
		"name" : "Timothy Faust"
	}
}
var directive = {
	'div.row' : {
		'match<-celeb_matches' : {
			'.matchlead' : function(arg) {
				curr_celeb = arg.item.screen_name;
				// return "you and " + arg.item.name.toUpperCase() + ' <em>98%
				// MATCH</em>';
				return "<span><em>" + arg.item.name.toUpperCase()
						+ '</em></span>';

			},
			'.words' : function(arg) {
				var str = "matched on ";

				for ( var key in arg.item.top_words) {
					str += " " + key.toUpperCase() + " |";
				}
				return str.slice(0, str.length - 2);

			}

			,
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
							console.log("Found match");
							// check for spaces on either side
							new_str += '<strong>' + text.slice(pos, pos + len)
									+ '</strong>';
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
							new_str += '<strong>'
									+ text.slice(pos, pos + word.length)
									+ '</strong>';
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

$("#querybox").submit(function() {
	// TODO validate arg first
	var arg = $('#usern').val();
	console.log('arg: ' + arg);
	$.get('cgi-bin/GetCelebMatchesJSON.py', arg, ajax_ret);
	console.log('txed request');
	return false;
});

function ajax_ret(data) {
	console.log('rxed response');
	$('#results').render(data, directive);
}
