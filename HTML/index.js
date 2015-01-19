$(function() {
  // AJAX - Asynchronous JavaScript And Xml
  // JSON - JavaScript Object Notation
  $("#search").change(function () {
    $("#output").load("http://localhost")
  })

  $("#doge").click(function () {
    alert("DOGE!!!!!!!")
  })

})