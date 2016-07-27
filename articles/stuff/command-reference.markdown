---
layout: post
title : Справочник команд
date  : 2016-07-27 12:00:00
tags  : []
---

<h3 style="text-indent: 0">Работа с растровыми изображениями</h3>

<div class="panel panel-primary" style="text-indent: 0">
  <div class="panel-heading">
    Привязка фотографий к географическим координатам
  </div>
  <div class="panel-body">
{% highlight bash %}
exiftool -overwrite_original -geosync=+07:00:00 -geotag=track.gpx *.JPG
{% endhighlight %}   
    <ul>
      <li><b>overwrite_original</b> - перезапись исходных файлов;</li>
      <li><b>geosync=+07:00:00</b> - коррекция времени.</li>
    </ul>
  </div>
</div>


<hr>
<div class="copyright">
Все материалы данной статьи, если не указано иное, распространяется под лицензией <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>
(c) Алексей Дураченко.
<br>
<br>
<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a>
</div>
