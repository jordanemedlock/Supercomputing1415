$(document).ready(function() {
    $("#displayImg").hide().show(1000);
    $("#search").delay(1000).hide().slideDown(1000);
    $("#search").change(function() {
  	var search=$("#search").val();
  	search = $.trim(search);
  	if(search == "doge") {
  		$("#output").prepend('<img src="doge.png" />').hide(100).show(1000);
  	}
  	else if(search == "back in the day" || search == "lel" || search == "LOL") {
  		var random = Math.floor(Math.random()*10);
  		var twitter = [
  		"http://jordanemedlock.com"
  		];
  		window.open([twitter[random]]);
  	}
  	else {
  		$.getJSON("/search/" + encodeURIComponent(search), function(data) {
        console.log(data);
        $("#output").empty();
        for (var i = data.length - 1; i >= 0; i--) {
          console.log(data[i]);
          $("#output").prepend('<img src="' + data[i] + '"/>');
        }
      })
  	}
  })
})