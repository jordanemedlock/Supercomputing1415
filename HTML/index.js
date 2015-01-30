$(document).ready(function() {
  $("#search").change(function() {
  	var search=$("#search").val()
  	if(search == "doge") {
  		window.open(["http://weknowmemes.com/2013/11/best-of-the-doge-meme-15-pics/"]);
  	}
  	else if(search == "back in the day" || search == "back in nam" || search == "LOL") {
  		window.open(["https://twitter.com/jordanemedlock/status/126382915285291009"]);
  	}
  })
})