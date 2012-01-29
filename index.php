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
				<h2>
					<span id="lead">FIND YOUR TOP CELEB TWITTER MATCHES</span>
					<!-- <span id="lead">find your twitter celebrity match</span>-->

				</h2>

			</div>
			<div id="query">
				<form id="querybox">
					<input type="search" size="26"
						placeholder="Enter your twitter username..." id="usern" /> <input
						type="submit" id="go" value="GO" />

				</form>
			</div>

			<div class="results" id="results">
				<div class="row">
					<div class="matchlead">
						SNOOP DOGG <span><em>3.45 JELLYRANK</em> </span>
					</div>
					<div>Y'all match on words like: weed, consecetur, beanbag  <a href="#">Show more tweets</a></div>
					<div class="tweetbox">
						<div class="twitprof">
							<img src="img/dude.jpg" />
						</div>
						<span><a href="">Snoop Dogg</a> tweeted</span>
						<div class="tweet">
							Neque porro quisquam est qui dolorstrong ipsum quia dolor sit
							amet, <strong>consectetur</strong>, adipisci velit..Neque porro
							quisquam est qui dolorstrong ipsum quia dolor
						</div>
					</div>
					<div class="tweetbox">
						<div class="twitprof">
							<img src="img/gaga.jpg" />
						</div>
						<span>You tweeted</span>
						<div class="tweet">
							Neque porro quisquam est qui dolorstrong ipsum quia dolor sit
							amet, <strong>consectetur</strong>, adipisci velit..Neque porro
							quisquam est qui dolorem ipsum quia dolor
						</div>
					</div>

				</div>
				<div class="row" id="social">
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


	<!-- scripts concatenated and minified via ant build script-->
	<script src="js/plugins.js"></script>
	<script src="js/script.js"></script>
	<!-- end concatenated and minified scripts-->


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