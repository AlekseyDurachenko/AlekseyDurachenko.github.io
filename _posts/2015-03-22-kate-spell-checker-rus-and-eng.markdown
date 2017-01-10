---
layout: post
title: "Настройка проверки орфографии в kate с помощью пользовательского словаря"
date: 2015-03-22 18:31:00
last_modified_at: 2015-03-22 18:31:00
category: linux
tags: linux kde kate hunspell myspell
---

<div class="post-image-container">
<img class="post-image-img" src="/img/posts/2015-03-22-kate-spell-checker-rus-and-eng/kate-without-russian-dict.png">
<div class="post-image-caption">Kate и проверка орфографии английским словарем.</div>
</div>


Проверка орфографии вещь несомненно важная и нужная, но в kde в целом
и в kate в частности до сих пор не реализовали возможность
проверки текста с помощью нескольких словарей.
И это не смотря на то, что [Bug 66516](https://bugs.kde.org/show_bug.cgi?id=66516)
висит уже более 10 лет.

Что же делать тем, кому надоело это терпеть?

<!--more-->


<div class="post-image-container">
<img class="post-image-img" src="/img/posts/2015-03-22-kate-spell-checker-rus-and-eng/kate-configure-spellcheck.png">
<div class="post-image-caption">Настройка проверки орфографии в kate.</div>
</div>


Единственный вариант решения проблемы, который пришел мне в голову -
это склеить несколько словарей в один.

Но нельзя просто взять и склеить 2 словаря, с помощью `cat`.
Это связано с тем, что формат словарей не так прост, как может
показаться на первый взгляд. Кому интересно могут посмотреть
описание формата hunspell
[здесь](http://manpages.ubuntu.com/manpages/dapper/man4/hunspell.4.html).

Изобретать очередной велосипед мне очень не хотелось, поэтому после
недолгого гугления удалось найти готовое решение:
[https://github.com/arty-name/hunspell-merge](https://github.com/arty-name/hunspell-merge)


<div class="post-image-container">
<img class="post-image-img" src="/img/posts/2015-03-22-kate-spell-checker-rus-and-eng/hunspell-merge.png">
<div class="post-image-caption">Окно программы hunspell-merge.</div>
</div>


Далее я создал собственный составной словарь из русского и английского словарей.

<p class="alert alert-danger">
Внимание! Описанная ниже процедура установки словарей производится на свой страх и риск!
</p>

<div class="alert alert-warning">
<p>К сожалению, я не нашел способа устанавливать словари в домашний каталог,
и решил оставить этот вопрос на потом, а пока записать файлы на место
словаря `hunspell-ru`, предварительно удалив его из системы.</p>
<p style="margin-top: 1.0em">
{% highlight bash %}
sudo apt-get remove hunspell-ru
sudo cp ru_RU.* /usr/share/hunspell/
{% endhighlight %}
</p>
</div>

Теперь при выборе языка проверки орфографии `Russian (Russia)`
используется созданный мной составной словарь.

<div class="post-image-container">
<img class="post-image-img" src="/img/posts/2015-03-22-kate-spell-checker-rus-and-eng/kate-result.png">
<div class="post-image-caption">Kate и проверка орфографии созданным словарем.</div>
</div>


### Ссылки ###
* [https://bugs.kde.org/show_bug.cgi?id=66516](https://bugs.kde.org/show_bug.cgi?id=66516) - Bug 66516 - spell checker: automatic language detection

* [http://manpages.ubuntu.com/manpages/dapper/man4/hunspell.4.html](http://manpages.ubuntu.com/manpages/dapper/man4/hunspell.4.html) - format of Hunspell dictionaries and affix files

* [https://github.com/arty-name/hunspell-merge](https://github.com/arty-name/hunspell-merge) - Software for merging several hunspell dictionaries
