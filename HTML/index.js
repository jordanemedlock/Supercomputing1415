// Authors: Samuel J. Gervais and Thomas R. Curtin
// School: Saint Pius X High School
// Email: samgervais512@gmail.com
// Discription: Program for the main functions of the search bar which sends search to server, and displays the results.
$(document).ready(function() {
    $("#displayImg").hide().show(1000);
    $("#search").delay(1000).hide().slideDown(1000);
    $("#search").change(function() {
  	var search=$("#search").val();
  	search = $.trim(search);
  	if(search == "doge") {
      $("#output").empty()
  		$("#output").prepend('<img src="doge.png" />').hide(100).show(1000);
  	}
  	else if(search == "acknowledge") {
  		var random = Math.floor(Math.random()*10);
      console.log(random)
  		var acknowl = [
  		"http://jordanemedlock.com",
      "http://www.cgpgrey.com"
  		];
      if(random % 2 == 0) {
        window.open([acknowl[0]]);
      }
      else {
        window.open([acknowl[1]]);
      }
  	}
  	else {
  		$.getJSON("/search/" + encodeURIComponent(search), function(data) {
        console.log(data);
        $(output).empty()
        for (var i = data.length - 1; i >= 0; i--) {
          console.log(data[i]);
          $("#output").prepend('<img src="' + data[i] + '"/>');
        }
      })
  	}
  })
})