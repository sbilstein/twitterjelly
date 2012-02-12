/*** PROGRESS BAR FUNCTIONS ***/
var progressEnd = 15; // set to number of progress <span>'s.
var progressColor = '#A63F00'; // set to progress bar color

var progressAt = progressEnd;
var progressTimer;
function progress_clear() {
	for (var i = 1; i <= progressEnd; i++) 
		document.getElementById('progress'+i).style.backgroundColor = 'transparent';
	progressAt = 0;
}
function progress_update() {
	document.getElementById('showbar').style.visibility = 'visible';
	progressAt++;
	if (progressAt > progressEnd) 
		progress_clear();
	else {
		cur_text=""
		switch(progressAt)
			{
			case 1:
			  cur_text="Hold tight.. we gotta get your tweets"
			  break;
			case 2:
			  cur_text="Hold tight.. we gotta get your tweets"
			  break;
			case 3:
			  cur_text="Processing tweets, interesting..."
			  break;
			case 4:
			  cur_text="Calculating LaGrange Multiplier Sequence "
			  break;
			case 5:
			  cur_text="Processing Einstein summation convention"
			  break;
			case 6:
			  cur_text="You said what??"
			  break;
			case 7:
			  cur_text="Okay, now we are finding similar celebs"
			  break;
			case 8:
			  cur_text="Okay, now we are finding similar celebs"
			  break;
			case 9:
			  cur_text="Inverting database, computing edit distance, whoah nelly"
			  break;
			case 10:
			  cur_text="Almost done, finding matches!"
			  break;
			case 11:
			  cur_text="Just a bit more..."
			  break;
			case 12:
				cur_text="Just a bit more..."
				break;
			case 13:
				cur_text="really, very, close..."
				break;
			case 14:
				cur_text="really, very, close..."
				break;
			case 15:
				cur_text="okay, we got em!"
				break;
			default:
				break;
			}
		
		$('#current_progress_step').empty();
		$('#current_progress_step').append(cur_text);
		
		document.getElementById('progress'+progressAt).style.backgroundColor = progressColor;
		}
		
	if (progressAt <= 9){
		progressInterval = 500;
	}
	else if (progressAt > 9 && progressAt < 13){
		progressInterval = progressInterval +1000;
	}
	else {
		progressInterval = progressInterval +2000;
	}
	progressTimer = setTimeout('progress_update()',progressInterval);
}
function progress_stop() {
	clearTimeout(progressTimer);
	progress_clear();
	document.getElementById('showbar').style.visibility = 'hidden';
}