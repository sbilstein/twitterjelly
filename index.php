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
			<div id="p_nav">
				<a id="nav_link" href="personality.php" >Personality</a>
			</div>
			<div id="lead">
				<h1 class="lead">FIND YOUR TOP CELEB TWITTER MATCHES</h1>

			</div>
			<div class="query-box">
				<!--[if IE]>
					MAKE SURE THIS SHIT SAYS THE RIGHT THING
				<![endif]-->
				<input type="search" size="26"
					placeholder="Enter your twitter username..." id="usern" /> <input
					type="button" id="go" class="submit" value="GO" />

				<div id="permalink_container" class="visuallyhidden">
					share your results with this link: <a id="permalink"></a>
				</div>
			</div>
			<div id="ajax-load" class="visuallyhidden">
				<img src="img/loader.gif"></img>
				<span id="load-text"></span>
			</div>
			<div class="error"></div>
			<div class="results_col" id="results">
				<div id="row-container">
					<div class="row visuallyhidden" id="row-template">
						<div class="matchlead">
							<div class="result-share">
							<img src="img/twitter-icon.gif"></img>
								<a target="_blank">tweet results</a>
							</div>
						</div>
						<div class="words">
							<span class="list-lead">you both tweet about</span>
						</div>
						<div class="tweet_entry top-border">
							<div class="user tweetbox">
								<div class="twitprof">
									<img class="user" src="" /><br /> <a
										class="user twitlink visuallyhidden"></a>
								</div>
								<span><a></a> </span>
								<div class="user tweet"></div>
							</div>
							<div class="celeb tweetbox">
								<div class="twitprof">
									<img class="celeb" src="" /><br /> <a
										class="celeb twitlink visuallyhidden"></a>
								</div>
								<span><a class="leadname"></a> </span>
								<div class="celeb tweet">
									<a class="twitlink"></a>
								</div>
							</div>

						</div>
						<div class="show-more">
							<input type="button" value="SHOW MORE"></input>
						</div>

					</div>
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
	<script src="js/libs/pure_min.js"></script>
	<!-- TODO: Concat and minify -->
	<script src="js/plugins.js"></script>
	<script src="js/script.js"> </script>


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
