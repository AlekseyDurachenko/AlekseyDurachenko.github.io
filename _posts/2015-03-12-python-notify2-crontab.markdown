---
layout: post
comments: true
uid: 2015-03-12-python-notify2-crontab
title: "Заставляем работать связку: python, notify2, crontab"
date: 2015-03-12 22:30:00
last_modified_at: 2015-03-12 22:30:00
categories: linux
tags: python linux crontab x11 dbus
permalink: /2015/03/12/python-notify2-crontab.html
---

При реализации [скрипта](https://github.com/AlekseyDurachenko/podfmdog)
автоматической загрузки новых подкастов с сайта [podfm.ru](http://podfm.ru)
возникла необходимость внедрения уведомлений на рабочем столе о появлении новых файлов.
Для решения этой задачи была выбрана библиотека notify2. И все работало хорошо, до тех пор,
пока не потребовалось запускать скрипт по расписанию в crontab...

<!--more-->

Ниже приведен код скрипта, который позволяет вывести уведомление на рабочий стол:
{% highlight python %}
#!/usr/bin/python3
# -*- coding: utf-8 -*-
import notify2

notify2.init("podfmdog")
notify = notify2.Notification("Title", "Message")
notify.show()                  
{% endhighlight %}

<div class="post-image-container">
<a href="/img/posts/2015-03-12-python-notify2-crontab/screenshot-notify2.png">
<img class="post-image-img" src="/img/posts/2015-03-12-python-notify2-crontab/screenshot-notify2.png">
</a>
<div class="post-image-caption">Результат работы скрипта.</div>
</div>


При попытке запустить этот скрипт в crontab появляется сообщении об ошибке:
{% highlight bash %}
Traceback (most recent call last):
  File "<PATH>/my1.py", line 5, in <module>
    notify2.init("podfmdog")
  File "/usr/lib/python3/dist-packages/notify2.py", line 93, in init
    bus = dbus.SessionBus(mainloop=mainloop)
  File "/usr/lib/python3/dist-packages/dbus/_dbus.py", line 211, in __new__
    mainloop=mainloop)
  File "/usr/lib/python3/dist-packages/dbus/_dbus.py", line 100, in __new__
    bus = BusConnection.__new__(subclass, bus_type, mainloop=mainloop)
  File "/usr/lib/python3/dist-packages/dbus/bus.py", line 122, in __new__
    bus = cls._new_for_bus(address_or_type, mainloop=mainloop)
dbus.exceptions.DBusException: org.freedesktop.DBus.Error.NotSupported: Unable to autolaunch a dbus-daemon without a $DISPLAY for X11
{% endhighlight %}

Проблема заключается в том, что notify2 необходимо знать адрес пользовательской
шины dbus. Для этого перед запуском скрипта нам необходимо экспортировать
переменную окружения `DBUS_SESSION_BUS_ADDRESS`. Сделать это можно следующим образом:
{% highlight bash %}
...
USERNAME=`whoami`
...
export DBUS_SESSION_BUS_ADDRESS=`ps -u $USERNAME e | grep -Eo 'dbus-daemon.*address=unix:abstract=/tmp/dbus-[A-Za-z0-9]{10}' | tail -c35`
...
{% endhighlight %}
Полный код скрипта можно взять [здесь](https://gist.github.com/AlekseyDurachenko/2027114608e4863eb038).
Следует отметить, что скрипт должен вызываться из crontab от имени пользователя с активной
сессией x11.
