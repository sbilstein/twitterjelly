/*** PROGRESS BAR FUNCTIONS ***/
var progressEnd = 15; // set to number of progress <span>'s.
var progressColor = '#A63F00'; // set to progress bar color

var messages = [
    "Hold tight.. we gotta get your tweets",
    "Processing tweets, interesting...",
    "Calculating LaGrange Multiplier Sequence ",
    "Processing Einstein summation convention",
    "Okay, now we are finding similar celebs",
    "Inverting database, computing edit distance, whoah nelly",
    "Almost done, finding matches!"
]

var progressAt = progressEnd;
var progressTimer;

var step = progressEnd / messages.length;
function progress_clear() {
	for (var i = 1; i <= progressEnd; i++) 
		document.getElementById('progress'+i).style.backgroundColor = 'transparent';
	progressAt = 0;
}
function progress_update() {
    $('#ajax-load').removeClass('visuallyhidden');
	progressAt++;
	if (progressAt > progressEnd)
		progress_clear();
	else {
        if((progressAt/2) > (messages.length -1)){
            cur_text = messages[messages.length - 1];
        } else {
		    cur_text= messages[Math.floor(progressAt / 2)];
        }
        console.log(progressAt);
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
	$('#ajax-load').addClass('visuallyhidden');
}