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
					<span id="lead">LOREM IPSUM DOLOR SIT POS...</span>
				</h2>
				<div class="social">
					<script src="js/libs/twit.js"></script>
					<a class="twitter-share-button" href="https://twitter.com/share"
						data-lang="en"
						data-text="My celeb twitter match is@ ! Find yours at http://www.twitter.jelly.com"></a>

					<div class="fb-like" data-send="false" data-width="450"
						data-show-faces="false" data-font="arial"></div>
				</div>
			</div>
			<div id="query">
				<form id="querybox">
					<input type="search" size="30"
						placeholder="Enter your twitter name..." id="usern" /> <input
						type="submit" id="go" value="GO" />

				</form>
			</div>
			<!-- Append stuff right here -->
			<!-- 		<div id="ajaxload">
				<img src="img/loader.gif" />
			</div> -->
			<div class="clear"></div>
			<div class="results grid_8" id="results">
				<div class="result_row">
					<div class="tweetbox">
						Snoop Dogg tweeted:
						<div class="tweet">sdfsfsmsfs gdfgdfg dfgdg dfgdfgdfg
							dfgdfgdfgdgf ipsum swag lorem</div>
					</div>

					<div class="tweetbox">
						Shwayze tweeted:
						<div class="tweet">lorem ipsum swag lorem ipsum swag lorem
							lorem ipsum swag loresdfsfsmsfs gdfgdfg dfgdg dfgdfgdfg
							dfgdfgdfgdgf ipsum swag lorem</div>
					</div>
				</div>
			</div>
			<!--  			<div class="spacer grid_1"></div> -->
			<div id="selector" class="grid_3">
				<div class="namerow">
					<img src="img/dude.jpg" />
					<div>
						cap'n swag<br> <em>98% MATCH</em>
					</div>
				</div>

			</div>
		</div>


	</div>

	<div class="clear"></div>
	<div class="grid_2 spacer"></div>
	<div class="grid_12 centercol bottom"></div>
	<div class="grid_2 spacer"></div>

	<footer> </footer>
	</div>
	<!-- end of #container -->


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
