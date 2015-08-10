$(document).ready(function() {
  var anchor = window.location.hash;  
  $("#tag-" + anchor.replace("#", "")).addClass('in');
});
