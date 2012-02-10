<!doctype html>

<!--[if lt IE 7 ]> <html lang="en" class="no-js ie6"> <![endif]-->
<!--[if IE 7 ]>    <html lang="en" class="no-js ie7"> <![endif]-->
<!--[if IE 8 ]>    <html lang="en" class="no-js ie8"> <![endif]-->
<!--[if IE 9 ]>    <html lang="en" class="no-js ie9"> <![endif]-->
<!--[if (gt IE 9)|!(IE)]><!-->
<html lang="en" class="no-js">
<!--<![endif]-->
<head>
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">

<title>TwitterJelly</title>
<meta name="description" content="">
<meta name="author" content="">

<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="shortcut icon" href="/favicon.ico">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">

<link rel="stylesheet" href="css/style.css?v=2">
<link rel="stylesheet" href="css/custom.css">
<link rel="stylesheet" href="css/persStyle.css?v=2">
<script src="js/libs/modernizr-1.6.min.js"></script>

</head>

<body>
	<div id="fb-root"></div>
	<script>
		(function(d, s, id) {
			var js, fjs = d.getElementsByTagName(s)[0];
			if (d.getElementById(id))
				return;
			js = d.createElement(s);
			js.id = id;
			js.src = "//connect.facebook.net/en_US/all.js#xfbml=1&appId=137222446375584";
			fjs.parentNode.insertBefore(js, fjs);
		}(document, 'script', 'facebook-jssdk'));
	</script>

	<div id="container" class="container_16">

	<?php include("header.html"); ?>

		<div class="grid_2 spacer"></div>
		<div id="main" class="grid_12 main centercol">
			<div class="vert-spacer"></div>
			<div id="lead">
				<h1 class="lead">
					FIND YOUR TWITTER PERSONALITY
				</h1>
			</div>
			<div class="query-box">

				<input type="search" size="26"
					placeholder="Enter your twitter username..." id="usern" /> <input
					type="button" id="go" class="submit" value="GO" />

			</div>
			<div id="ajax-load" class="visuallyhidden">
				<img src="img/loader.gif"></img>
			</div>
			<div class="error-pic visuallyhidden">
				<img src="img/protected.jpg "></img>
				<div>
					<h3>TwitterJelly can't access your tweets if they are protected.
						Try using another twitter account or unprotect your tweets if
						you'd like.</h3>
				</div>
			</div>

			<div class="results_col" id="results">

				<div class="row">
				
					<div class = "visuallyhidden" id="pers_section">
						<p id="test_ro"></p>
						<div class="pers_id">Twitter Personality: <span id="pers_id"></span></div>
						
						<div id="E" class ="pers_dim visuallyhidden">
						<img src="img/E.png" />
							<h3>Usage Purpose</h3>							
							<p>Entertainment: You tweet in your free time for fun. Twitter is probably the best thing to happen to you since the day you discovered reddit.</p>
						</div>
						<div id="A" class ="pers_dim visuallyhidden">
						<img src="img/A.png" />
							<h3>Usage Purpose</h3>							
							<p>Amusement: You tweet when you need a distraction. Try to enjoy dinner with your grandma instead of tweeting about the toothless geriatrics at the early bird special.</p>
						</div>
						<div id="S" class ="pers_dim visuallyhidden">
						<img src="img/C.png" />
							<h3>Information Use</h3>
							<p>Sharer: You're an Info Sharer. For good or for bad, you post tons of links to share with the twitter world.</p>
						</div>
						<div id="C" class ="pers_dim visuallyhidden">
						<img src="img/C.png" />
							<h3>Information Use</h3>
							<p>Consumer: You're an info consumer. You use Twitter to filter the internet down to the things that interest you most.</p>
						</div>
						<div id="T" class ="pers_dim visuallyhidden">
						<img src="img/T.png" />
							<h3>Social Circle Density</h3>
							<p>Tight: You have a tight twitter network, and are not gung ho on interacting with randoms on the Internet.</p>
						</div>
						<div id="W"class ="pers_dim visuallyhidden">
						<img  src="img/W.png" />
							<h3>Social Circle Density</h3>
							<p>Wide: You interact with a wide and varied group of twitter users. Strangers are just friends you haven't met yet, right?</p>
						</div>
						<div id="J" class ="pers_dim visuallyhidden">
						<img src="img/J.png" />
							<h3>Twitter Role</h3>
							<p>Joiner: If twitter were a party, you would be the host. You naturally connect people and topics.</p>
						</div>
						<div id="E" class ="pers_dim visuallyhidden">
						<img src="img/M.png" />
							<h3>Twitter Role</h3>
							<p>Maverick: You are a lone wolf. You make twitter interesting. Do you have thousands of followers?</p>
						</div>
						
						<div class="pers_id">Celebrities With Same Personality</div>
						<div id="pers_celebs"> </div>
						


					</div>
					

				</div>
				
				<!--
				<div id="social">
					<div id="facebook">
						<div class="fb-like" data-href="http://www.twitterjelly.com"
							data-send="false" data-width="250" data-show-faces="false"></div>
					</div>
					<div id="twitter">
						<script src="js/libs/twit.js"></script>
						<a class="twitter-share-button" href="https://twitter.com/share"
							data-lang="en"
							data-text="My celeb twitter match is@ ! Find yours at http://www.twitter.jelly.com"></a>

				</div>
					<a href="#">How do we compute jellyrank?</a>
				</div>
				-->
			</div>
		</div>


	</div>
	<!-- end of #container -->

	<!--  		
	<footer> </footer>

	-->


	<script src="//ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.js"></script>
	<script>
		!window.jQuery
				&& document
						.write(unescape('%3Cscript src="js/libs/jquery-1.4.2.js"%3E%3C/script%3E'))
	</script>
	<script src="js/libs/pure_min.js"></script>
	<!-- TODO: Concat and minify -->
	<script src="js/plugins.js"></script>
	<script src="js/scriptP.js"></script>


	<!--[if lt IE 7 ]>
<script src="js/libs/dd_belatedpng.js"></script>
<script> DD_belatedPNG.fix('img, .png_bg'); </script>
<![endif]-->

	<!-- yui profiler and profileviewer - remove for production -->
	<script src="js/profiling/yahoo-profiling.min.js"></script>
	<script src="js/profiling/config.js"></script>
	<!-- end profiling code -->



	<!-- change the UA-XXXXX-X to be your site's ID -->
	<script>
		var _gaq = [ [ '_setAccount', 'UA-XXXXX-X' ], [ '_trackPageview' ] ];
		(function(d, t) {
			var g = d.createElement(t), s = d.getElementsByTagName(t)[0];
			g.async = true;
			g.src = ('https:' == location.protocol ? 'https://ssl'
					: 'http://www')
					+ '.google-analytics.com/ga.js';
			s.parentNode.insertBefore(g, s);
		})(document, 'script');
	</script>

</body>
</html>
