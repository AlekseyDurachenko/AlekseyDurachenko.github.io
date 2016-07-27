$().ready(function() {
  $.each($('figure'), function(i, val) {
    var img = $(val).find('img');
    img.imagesLoaded(function() {
      $(val).find('figcaption').css("maxWidth", img.get(0).naturalWidth);
    });
  });
});
