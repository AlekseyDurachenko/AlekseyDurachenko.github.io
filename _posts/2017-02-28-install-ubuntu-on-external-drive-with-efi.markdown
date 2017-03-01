---
layout: post
comments: true
uid: 2017-02-28-install-ubuntu-on-external-drive-with-efi
title: "Установка Ubuntu на внешний носитель (флешку или жесткий диск) в режиме EFI"
date: 2017-02-28 05:00:00
last_modified_at: 2017-02-28 05:00:00
categories: linux
tags: linux ubuntu efi install
permalink: /2017/02/28/install-ubuntu-on-external-drive-with-efi.html
---

Ежегодного после [Software Freedom Day][sfd2017] проходит уже ставший традиционным
Linux Install Fest, где все желающие могут получить помощь в установке
дистрибутива GNU/Linux на свои ноутбуки.

Вообще говоря, процедура установки современного дистрибутива GNU/Linux
вроде Ubuntu не представляет никаких сложностей, даже в том случае, если
его необходимо установить рядом с Windows 8/10 в режиме [UEFI][efi] и
включенным [Secure Boot][secureboot].

Но что делать, если требуется поставить GNU/Linux в режиме [UEFI][efi] на
внешний жесткий диск, флешку или карту памяти?

Казалось бы, вставляешь внешний носитель, и устанавливаешь
GNU/Linux стандартным образом.

Но, к сожалению, все не так просто. Если вы начнете устанавливать
GNU/Linux в таком режиме, то после перезагрузки вы уже не сможете
загрузиться с внутреннего жесткого диска при отключенном внешнем носителе.

Проблема заключается в том, что при вызове `update-grub` обновляется содержимое
NVRAM [UEFI][efi]. Туда прописывается адрес EFI файла который находится
на внешнем носителе, а информация о том, как грузиться
со встроенного жесткого диска удаляется. Более подробно о процессе загрузке
можно почитать здесь: [http://www.rodsbooks.com/efi-bootloaders/installation.html](http://www.rodsbooks.com/efi-bootloaders/installation.html)


Зачем вообще ставить GNU/Linux на внешний носитель? Причины могут быть различны.
Например, я столкнулся с проблемой, что на встроенном диске недостаточно
места для установки двух ОС. Серьезно, в ноутбуке был установлен SSD
объемом 32ГиБ, чего с трудом хватало даже для работы голой Windows 8.1.

Так же многие новички боятся ставить незнакомую ОС на свой компьютер,
или не уверены, нужна ли она им вообще, а попробовать хочется.
В этом случае флешка с полноценным GNU/Linux идеальный вариант.
(Не просто LiveUSB, а полноценно установленная ОС, как если бы она
была установлена на жесткий диск, чтобы оценить все её достоинства).

<div class="post-image-container">
<a href="/img/posts/2017-02-28-install-ubuntu-on-external-drive-with-efi/vb-no-bootable-device.png">
<img class="post-image-img" src="/img/posts/2017-02-28-install-ubuntu-on-external-drive-with-efi/vb-no-bootable-device.png">
</a>
<div class="post-image-caption">В VirtualBox отсутсвует загрузочный диск</div>
</div>

<p class="alert alert-danger">
Все, что описано ниже, рассчитано на опытного пользователя GNU/Linux.
Все, что вы делаете - Вы делаете на свой страх и риск. Автор не несет
никакой ответственности за Ваши действия или бездействия, которые повлекли
за собой порчу или полную потерю Ваших данных.
</p>

<!--more-->

В качестве примера будем ставить на внешний диск Ubuntu 16.04.

В качестве хост-системы используется Kubuntu 16.04.

Потребуется следующий набор ПО:
- [VirtualBox][virtualbox]
- [dd][dd]
- [GParted][gparted]
- [axel][axel]

Для начала скачаем образ Ubuntu 16.04:

```bash
# подготовка
mkdir -p /home/`whoami`/temp/LinuxLiveDrive/
# скачивание
axel -n 10 http://releases.ubuntu.com/16.04/ubuntu-16.04.2-desktop-amd64.iso --output=/home/`whoami`/temp/LinuxLiveDrive/ubuntu-16.04.2-desktop-amd64.iso
```

Затем создадим пустой файл, который будет использоваться в качестве виртуального
жесткого диска. (Инсталлятор Ubuntu 16.04 требует как минимум 9ГиБ
свободного места на диске, но мы возьмем чуть больше - 10ГиБ)

```bash
# создаем пустой файл
dd if=/dev/zero of=/home/`whoami`/temp/LinuxLiveDrive/LinuxLiveDrive.dd bs=1G count=10
```

Создадим [vmdk][vmdk], чтобы этот "диск" можно было подключить в [VirtualBox][virtualbox]:

```bash
VBoxManage internalcommands createrawvmdk -filename /home/`whoami`/temp/LinuxLiveDrive/LinuxLiveDrive.vmdk -rawdisk /home/`whoami`/temp/LinuxLiveDrive/LinuxLiveDrive.dd
```

Теперь приступим к созданию виртуальной машины со следующими характеристиками:
- тип ОС GNU/Linux
- в качестве жесткого диска указать созданный выше виртуальный диск
- включить загрузку через EFI

<div class="post-image-container">
<a href="/img/posts/2017-02-28-install-ubuntu-on-external-drive-with-efi/vb-os.png">
<img class="post-image-img" src="/img/posts/2017-02-28-install-ubuntu-on-external-drive-with-efi/vb-os.png">
</a>
<div class="post-image-caption">VirtualBox: выбор OS</div>
</div>

<div class="post-image-container">
<a href="/img/posts/2017-02-28-install-ubuntu-on-external-drive-with-efi/vb-hdd.png">
<img class="post-image-img" src="/img/posts/2017-02-28-install-ubuntu-on-external-drive-with-efi/vb-hdd.png">
</a>
<div class="post-image-caption">VirtualBox: выбор жесткого диска</div>
</div>

<div class="post-image-container">
<a href="/img/posts/2017-02-28-install-ubuntu-on-external-drive-with-efi/vb-efi-enabled.png">
<img class="post-image-img" src="/img/posts/2017-02-28-install-ubuntu-on-external-drive-with-efi/vb-efi-enabled.png">
</a>
<div class="post-image-caption">VirtualBox: включение загрузки через EFI</div>
</div>

Теперь запускаем виртуальную машину, выбираем загрузочный диск,
устанавливаем и настраиваем систему.

Из ньюансов: я рекомендую сделать разбивку жесткого диска следующим образом:
- первый раздел EFI, размер 500МиБ
- второй раздел ext4, точка монтирования '/', все оставшееся место
- раздел swap создавать не нужно, т.к. во первых скорее всего на медленной
флешке он будет очень сильно фризить систему, во вторых это увеличит
размер установочного образа, что потребует больше времени на заливку
его на целевую флешку(или жесткий диск). В конце концов, swap раздел можно
создать потом, или же вообще обойтись swap файлом, чего более чем достаточно.

<div class="post-image-container">
<a href="/img/posts/2017-02-28-install-ubuntu-on-external-drive-with-efi/vb-partitions.png">
<img class="post-image-img" src="/img/posts/2017-02-28-install-ubuntu-on-external-drive-with-efi/vb-partitions.png">
</a>
<div class="post-image-caption">Пример разбивки диска</div>
</div>

<p class="alert alert-warning">
Почему-то после установки Ubuntu VirtualBox отказался грузить установленную систему.
При повторной установке проблем не возникло. Странно. Потом нужно будет
разобраться.
</p>

После установки необходимо немного порпавить конфигурационные файлы [grub][grub].

Для того, чтобы [grub][grub] не трогал память NVRAM [UEFI][efi] необходимо
отредактировать файл `/etc/grub.d/30_uefi-firmware` следующим образом:
добавить `exit 0` сразу после `#!/bin/sh`:

```bash
#! /bin/sh
set -e
exit 0    # добавить эту строку

# grub-mkconfig helper script.
...
```

Но это еще не все, по умолчанию [UEFI][efi] ищет загрузочные образы
не в том месте, куда их кладет [grub][grub], поэтому нам нужно создать
еще один скрипт `/etc/grub.d/42_custom` со следующим содержанием:

```bash
#!/bin/sh

set -x

mkdir -p /boot/efi/EFI/boot/
cp /boot/efi/EFI/ubuntu/shimx64.efi /boot/efi/EFI/boot/bootx64.efi
cp /boot/efi/EFI/ubuntu/grubx64.efi /boot/efi/EFI/boot/grubx64.efi
cp /boot/efi/EFI/ubuntu/grub.cfg /boot/efi/EFI/boot/grub.cfg
```

и сделать его исполняемым

```bash
chmod +x /etc/grub.d/42_custom
```

Вот и все! Теперь осталось обновить загрузчик и можно приступать
к копированию образа на реальный диск:
```bash
update-grub
```

<p class="alert alert-danger">
Далее вам следует быть предельно острожным, и не перепутать буквы
диска. Будьте внимательны. Так же Вам необходимо выполнять все нижеописанные
команды от имени суперпользователя.
</p>

Для эксперимента возьмем внешний жесткий диск и зальем на него
созданный образ:

```bash
dd if=/home/`whoami`/temp/LinuxLiveDrive/LinuxLiveDrive.dd of=/dev/sdX bs=4M
```

теперь запустим [GParted][gparted] и выставим нужный размер разделов
(При запуске [GParted][gparted] скорее всего ругнется, что геометрия диска
`/dev/sdX` не совпадает с таблицей разделов. Смело жмем "Fix")

<div class="post-image-container">
<a href="/img/posts/2017-02-28-install-ubuntu-on-external-drive-with-efi/gparted-before.png">
<img class="post-image-img" src="/img/posts/2017-02-28-install-ubuntu-on-external-drive-with-efi/gparted-before.png">
</a>
<div class="post-image-caption">Таблица разделов: было</div>
</div>

<div class="post-image-container">
<a href="/img/posts/2017-02-28-install-ubuntu-on-external-drive-with-efi/gparted-after.png">
<img class="post-image-img" src="/img/posts/2017-02-28-install-ubuntu-on-external-drive-with-efi/gparted-after.png">
</a>
<div class="post-image-caption">Таблица разделов: стало</div>
</div>

Теперь можно подключать жесткий диск к ноутбуку смело загружаться в GNU/Linux!

В случае, если потребуется добавить своп, то можно воспользоваться следующим
рецептом:

Создаем своп файл (от имени суперпользователя):
```bash
dd if=/dev/zero of=/swap.swp bs=1G count=16
mkswap /swap.swp
```

И добавляем в конец `/etc/fstab` следующую строку:

```
/swap.swp    none    swap    sw    0   0
```

На этом, пожалуй, все. Всем добра и пингвинов!


### Ссылки ###
- [Managing EFI Boot Loaders for Linux: EFI Boot Loader Installation](http://www.rodsbooks.com/efi-bootloaders/installation.html)

[sfd2017]: https://lugnsk.org/lugnskru/2016/09/sfd2016.html
[efi]: https://en.wikipedia.org/wiki/Unified_Extensible_Firmware_Interface
[secureboot]: https://en.wikipedia.org/wiki/Unified_Extensible_Firmware_Interface#Secure_boot_2
[virtualbox]: https://en.wikipedia.org/wiki/VirtualBox
[dd]: https://en.wikipedia.org/wiki/Dd_(Unix_software)
[gparted]: https://en.wikipedia.org/wiki/GParted
[axel]: https://axel.alioth.debian.org/
[vmdk]: https://en.wikipedia.org/wiki/VMDK
[grub]: https://en.wikipedia.org/wiki/GNU_GRUB
