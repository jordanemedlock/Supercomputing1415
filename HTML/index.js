$(document).ready(function() {
  $("#search").change(function() {
  	var search=$("#search").val()
  	if(search == "doge") {
  		window.open(["http://weknowmemes.com/2013/11/best-of-the-doge-meme-15-pics/"])
  	}
  	else if(search == "back in the day" || search == "lel" || search == "LOL") {
  		var random = parseInt(Math.random()*10)
  		var twitter = [
  		"https://twitter.com/jordanemedlock/status/126382915285291009",
  		"https://twitter.com/jordanemedlock/status/230350738839187458",
  		"https://twitter.com/jordanemedlock/status/137402194256338946",
  		"https://twitter.com/jordanemedlock/status/88816149214658560",
  		"https://twitter.com/jordanemedlock/status/112760542271242240",
  		"https://twitter.com/jordanemedlock/status/115611206563270656",
  		"https://twitter.com/jordanemedlock/status/110931996750004226",
		"https://twitter.com/jordanemedlock/status/114081908358512640",
		"https://twitter.com/jordanemedlock/status/92490374521683968",
  		"http://jordanemedlock.com"
  		]
  		window.open([twitter[random]])
  	}
  })
})