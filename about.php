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
				<a id="nav_link" href="personality.php">PERSONALITY</a>
			</div>
			<div id="lead">
				<h1 class="lead">ABOUT US</h1>
			</div>

			<div class="content">
			<div align="center">
			<iframe width="420" height="315" src="http://www.youtube.com/embed/AfpyoGFJNNE" frameborder="0" allowfullscreen></iframe>
			</div>
			<div>
			<h2>Meet the TwitterJelly team</h2>
			<p>
			Hi! We're a group of software engineers based out of Seattle, WA.
			We love machine learning, web design, and working on fun projects. Our other hobbies
			include listening to Ween, hanging out with our favorite cats Lorie and Gus, and skiing down the streets during the snowpocalypse.
			</p>

			<h2>How does TwitterJelly work?</h2><p>
			Our matches are based on an algorithm called <a href="http://en.wikipedia.org/wiki/Tfidf">TFIDF</a> that is used to identify meaningful words in a document.
			We've processed the tweets of hundreds of celebrities to identify their most important terms. Once you enter your username, we run the same algorithm on a recent
			selection of tweets. With your list of key terms, we compare your key terms to those of celebrities and then find your best matches along with tweets
			that showcase your use of those words.
			</p>
			<div>
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
	<script src="js/animation.js"></script>
	<script src="js/images.js"></script>
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
		var _gaq = [ [ '_setAccount', 'UA-26514236-2' ], [ '_trackPageview' ] ];
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
