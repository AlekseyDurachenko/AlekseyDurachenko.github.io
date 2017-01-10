---
layout: post
title: "Автоматическая синхронизация flash памяти MP3 плеера с локальным каталогом"
date: 2015-03-14 22:09:00
last_modified_at: 2015-03-14 22:09:00
categories: linux
tags: bash rsync linux udev dbus sync
permalink: /2015/03/14/mp3-player-mp840-sync.html
---


<div class="post-image-container">
<img class="post-image-img" src="/img/posts/2015-03-14-mp3-player-mp840-sync/mp840-photo.png">
<div class="post-image-caption">Transcend MP840.</div>
</div>


Наконец-то дошли руки, чтобы сделать автоматическую синхронизацию flash памяти MP3 плеера
с локальным каталогом.


<!--more-->


Описанная ниже реализация тестировалась на дистрибутиве
[GNU/Linux Kubuntu 14.04](http://www.kubuntu.org/news/kubuntu-14.04),
но, в принципе, ничего не мешает использовать её на любом другом дистрибутиве с udev.

Принцип работы синхронизации следующий: после подключения MP3 плеера (определяется
с помощью правила udev) запускается скрипт, выполняющий зеркалирование при помощи rsync.
Монтирование и размонтирование выполняется скриптом
автоматически. О начале и окончании синхронизации посылается уведомление
на рабочий стол.

Идентификацию flash накопителя MP3 плеера будем производить при помощи UUID.
В нашем случае это: `2408-0200`

Для начала создадим перманентную точку монтирования:
{% highlight bash %}
sudo mkdir /media/MP840
{% endhighlight %}

и пропишем правило в `/etc/fstab`:
{% highlight bash %}
UUID=2408-0200 /media/MP840 vfat noauto,async,rw,user,dmask=000,fmask=111,utf8,codepage=866 0 0
{% endhighlight bash %}

Предположим, что мы храним мастер копию файлов для плеера в
`/home/username/MySync/TranscendMP840/sdcard/`,
а полное имя скрипта `/home/username/MySync/TranscendMP840/sdcard/sync-to-player.sh`.

Создадим правило для udev `/etc/udev/rules.d/99-usb-player-mp840.rules`:
{% highlight bash %}
KERNEL=="sd?1", ENV{ID_FS_UUID}=="2408-0200", RUN+="/bin/su username -c '/home/username/MySync/TranscendMP840/sdcard/sync-to-player.sh'"
{% endhighlight %}

Содержимое скрипта синхронизации:
{% highlight bash %}
#!/bin/bash
set -e  # abort if any command failed

# MP3 player must be attached to the USB
if [ ! -b /dev/disk/by-uuid/2408-0200 ]
then
    echo "MP840 is not attached"
    exit 1
fi

# /etc/fstab:
#    UUID=2408-0200 /media/MP840 vfat noauto,async,rw,user,dmask=000,fmask=111,utf8,codepage=866 0 0
mount /media/MP840

# the flag file must be created on the device root
if [ ! -f /media/MP840/rsync-accept.flag ]
then
    echo "The flag file on the MP840 is missing"
    umount -l /media/MP840
    exit 1
fi

# detect the dbus session of the current user
USERNAME=`whoami`
export DBUS_SESSION_BUS_ADDRESS=`ps -u $USERNAME e | grep -Eo 'dbus-daemon.*address=unix:abstract=/tmp/dbus-[A-Za-z0-9]{10}' | tail -c35`

# notification of the beginning of the synchronization
if [ ! -z "$DBUS_SESSION_BUS_ADDRESS" ]
then
    notify-send "MP3 Player MP840" "Synchronization is beginning..."
fi

# synchronization: mirror
# rsync -va --delete /home/username/MySync/TranscendMP840/sdcard/ /media/MP840/sdcard/
# compare only by size
rsync -vr --delete --size-only /home/username/MySync/TranscendMP840/sdcard/ /media/MP840/sdcard/

# operation may take a long time, due to `async` in the /etc/fstab
umount -l /media/MP840

# notification of the completion of synchronization
if [ ! -z "$DBUS_SESSION_BUS_ADDRESS" ]
then
    notify-send "MP3 Player MP840" "Synchronization is complete!"
fi

# all is well
exit 0
{% endhighlight %}

Для того чтобы началась синхронизация в корне файловой системы
плеера необходимо создать пустой файл `rsync-accept.flag`. Это необходимо, во-первых,
для того, чтобы исключить затирание носителя информации со случайно совпавшим UUID,
во-вторых, может случиться так, что на плеер будут записаны файлы в обход
мастер копии. В последнем случае следует не забыть удалить данный файл,
чтобы избежать потери данных.

### Ссылки ###

* [http://reactivated.net/writing_udev_rules.html](http://reactivated.net/writing_udev_rules.html) - writing udev rules by Daniel Drake (dsd)

* [https://gist.github.com/AlekseyDurachenko/335e3ca333a70d16a101](https://gist.github.com/AlekseyDurachenko/335e3ca333a70d16a101) - скрипт синхронизации
