$().ready(function() {
  $.each($('div.post-image-container'), function(i, val) {
    var img = $(val).find('img.post-image-img');
    img.imagesLoaded(function() {
      $(val).find('div.post-image-caption').css("maxWidth", img.get(0).naturalWidth);
    });
  });
});
