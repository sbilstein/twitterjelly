<!doctype html>
<!-- paulirish.com/2008/conditional-stylesheets-vs-css-hacks-answer-neither/ -->
<!--[if lt IE 7]> <html class="no-js ie6 oldie" lang="en"> <![endif]-->
<!--[if IE 7]>    <html class="no-js ie7 oldie" lang="en"> <![endif]-->
<!--[if IE 8]>    <html class="no-js ie8 oldie" lang="en"> <![endif]-->
<!-- Consider adding an manifest.appcache: h5bp.com/d/Offline -->
<!--[if gt IE 8]><!-->
<html class="no-js" lang="en">
<!--<![endif]-->
<head>
<meta charset="utf-8">

<!-- Use the .htaccess and remove these lines to avoid edge case issues.
       More info: h5bp.com/b/378 -->
<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">

<title>TwitterJelly</title>
<meta name="description" content="">
<meta name="author" content="">

<!-- Mobile viewport optimized: j.mp/bplateviewport -->
<meta name="viewport" content="width=device-width,initial-scale=1">

<!-- Place favicon.ico and apple-touch-icon.png in the root directory: mathiasbynens.be/notes/touch-icons -->

<!-- CSS: implied media=all -->
<!-- CSS concatenated and minified via ant build script-->
<link rel="stylesheet" href="css/style.css">
<!-- end CSS-->

<!-- More ideas for your <head> here: h5bp.com/d/head-Tips -->

<!-- All JavaScript at the bottom, except for Modernizr / Respond.
       Modernizr enables HTML5 elements & feature detects; Respond is a polyfill for min/max-width CSS3 Media Queries
       For optimal performance, use a custom Modernizr build: www.modernizr.com/download/ -->
<script src="js/libs/modernizr-2.0.6.min.js"></script>

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

	<?php include("header.html"); ?>
	<div id="container">

		<div id="main" role="main">

			<div id="searchbox">
				<!-- 	<h2>lorem ipsum swag</h2>
		 -->
				<div width="100%" id="lead">
					<h2>
						<span id="lead">LOREM IPSUM DOLOR SIT POS...</span>
					</h2>
					<script src="js/libs/twit.js"></script>
					<a class="twitter-share-button" href="https://twitter.com/share"
						data-lang="en"
						data-text="My celeb twitter match is@ ! Find yours at http://www.twitter.jelly.com"></a>

					<div class="fb-like" data-send="false" data-width="450"
						data-show-faces="false" data-font="arial"></div>

				</div>
				<div id="query">
					<form id="querybox">
						<input type="search" size="30"
							placeholder="Enter your twitter name..." id="usern" /> <input
							type="submit" id="go" value="GO" />

					</form>
				</div>
				<div id="related">SWAGGER SWAGGER SWAGGER</div>
				<div id= "topic">DRUGS CHEESE LOVE</div>
				<!-- 				<div id="selector"></div> -->
				<div id="results">
					<div id="namerow"></div>

				</div>
			</div>
		</div>

		<div id="sidebar" class="hidden">
			<h3>
				PAX ROMANA <em>VELIT</em> URSA MAJOR
			</h3>
			<div id="words"></div>
			<div class="help">
				<a href="#" onclick="toggleinfo(); return false;"> what does jelly
					mean?</a>
			</div>
			<div id="jellyinfo">
				Jelly is a term we use to describe significance or importance. We
				calculate the value of words using something called <a
					href="http://en.wikipedia.org/wiki/Tf%E2%80%93idf">TF-IDF</a>. <br>
				<a href="#" onclick="toggleinfo()">close this box</a>
			</div>
		</div>
	</div>

	</div>

	<footer>
		<div id="debug">
			<input type="checkbox" name="divborder" value="divb" id="borderbox">border</input>
			<input type="checkbox" name="text" value="divj" id="justbox">justify
			</border>
		</div>


	</footer>


	<!-- JavaScript at the bottom for fast page loading -->

	<!-- Grab Google CDN's jQuery, with a protocol relative URL; fall back to local if offline -->
	<script
		src="//ajax.googleapis.com/ajax/libs/jquery/1.6.2/jquery.min.js"></script>
	<script>
		window.jQuery
				|| document
						.write('<script src="js/libs/jquery-1.6.2.min.js"><\/script>')
	</script>


	<!-- scripts concatenated and minified via ant build script-->
	<script defer src="js/plugins.js"></script>
	<script defer src="js/script.js"></script>
	<!-- end scripts-->


	<!-- Change UA-XXXXX-X to be your site's ID -->
	<script>
		window._gaq = [ [ '_setAccount', 'UA-27643392-1' ], [ '_trackPageview' ],
				[ '_trackPageLoadTime' ] ];
		Modernizr.load({
			load : ('https:' == location.protocol ? '//ssl' : '//www')
					+ '.google-analytics.com/ga.js'
		});
	</script>


	<!-- Prompt IE 6 users to install Chrome Frame. Remove this if you want to support IE 6.
       chromium.org/developers/how-tos/chrome-frame-getting-started -->
	<!--[if lt IE 7 ]>
    <script src="//ajax.googleapis.com/ajax/libs/chrome-frame/1.0.3/CFInstall.min.js"></script>
    <script>window.attachEvent('onload',function(){CFInstall.check({mode:'overlay'})})</script>
  <![endif]-->

</body>
</html>
