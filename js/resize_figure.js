$().ready(function() {
  $.each($('div.post-image'), function(i, val) {
    var img = $(val).find('img');
    img.imagesLoaded(function() {
      $(val).find('div.post-image-caption').css("maxWidth", img.get(0).naturalWidth);
    });
  });
});
