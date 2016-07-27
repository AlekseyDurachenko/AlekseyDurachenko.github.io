---
layout: post
title : "Настройка проверки орфографии в kate с помощью пользовательского словаря"
date  : 2015-03-22 18:31:00 UTC
tags  : linux kde kate hunspell myspell
---

<figure>
<img src="/img/posts/2015-03-22-kate-spell-checker-rus-and-eng/kate-without-russian-dict.png">
<figcaption>Kate и проверка орфографии английским словарем.</figcaption>
</figure>


Проверка орфографии вещь несомненно важная и нужная, но в kde в целом
и в kate в частности до сих пор не реализовали возможность 
проверки текста с помощью нескольких словарей.
И это не смотря на то, что [Bug 66516](https://bugs.kde.org/show_bug.cgi?id=66516) 
висит уже более 10 лет.

Что же делать тем, кому надоело это терпеть?

<!--more-->


<figure>
<img src="/img/posts/2015-03-22-kate-spell-checker-rus-and-eng/kate-configure-spellcheck.png">
<figcaption>Настройка проверки орфографии в kate.</figcaption>
</figure>


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


<figure>
<img src="/img/posts/2015-03-22-kate-spell-checker-rus-and-eng/hunspell-merge.png">
<figcaption>Окно программы hunspell-merge.</figcaption>
</figure>


Далее я создал собственный составной словарь из русского и английского словарей.

Внимание! Описанная ниже процедура установки словарей производится на свой страх и риск!
{: .alert .alert-danger}

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

<figure>
<img src="/img/posts/2015-03-22-kate-spell-checker-rus-and-eng/kate-result.png">
<figcaption>Kate и проверка орфографии созданным словарем.</figcaption>
</figure>


### Ссылки ###
* [https://bugs.kde.org/show_bug.cgi?id=66516](https://bugs.kde.org/show_bug.cgi?id=66516) - Bug 66516 - spell checker: automatic language detection

* [http://manpages.ubuntu.com/manpages/dapper/man4/hunspell.4.html](http://manpages.ubuntu.com/manpages/dapper/man4/hunspell.4.html) - format of Hunspell dictionaries and affix files

* [https://github.com/arty-name/hunspell-merge](https://github.com/arty-name/hunspell-merge) - Software for merging several hunspell dictionaries

<hr>
<div class="copyright">
Все материалы данной статьи, если не указано иное, распространяется под лицензией <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>
(c) Алексей Дураченко.
<br>
<br>
<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a>
</div>
