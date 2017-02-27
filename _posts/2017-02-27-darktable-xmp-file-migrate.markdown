---
layout: post
comments: true
uid: 2017-02-27-darktable-xmp-file-migrate
title: "Сказ о том, как я проекты darktable с версии 2.0.X на 2.2.3 переводил"
date: 2017-02-27 05:00:00
last_modified_at: 2017-02-27 05:00:00
categories: photo
tags: darktable photo python
permalink: /2017/02/27/darktable-xmp-file-migrate.html
---

<div class="post-image-container">
<a href="/img/posts/2017-02-27-darktable-xmp-file-migrate/levels-after.png">
<img class="post-image-img" src="/img/posts/2017-02-27-darktable-xmp-file-migrate/levels-after.png">
</a>
<div class="post-image-caption">darktable: корректно выставленные уровни (levels)</div>
</div>

После перехода с Kubuntu 14.04 на 16.04 появилась возможность обновить
[darktable][darktable] с версии 2.0.X до 2.2.3, но внезапно выяснилось, что
старые проекты, в которых использовалась коррекция уровней ([levels][darktable_levels]),
отныне открываются некорректно.

<!--more-->

При попытке открытия проекта в глаза бросаются неверно выставленные уровни.

<div class="post-image-container">
<a href="/img/posts/2017-02-27-darktable-xmp-file-migrate/levels-before.png">
<img class="post-image-img" src="/img/posts/2017-02-27-darktable-xmp-file-migrate/levels-before.png">
</a>
<div class="post-image-caption">darktable: некорректно выставленные уровни (levels)</div>
</div>

Ползунки уровней белого/черного/серого отображаются "зеркально":

<div class="post-image-container">
<a href="/img/posts/2017-02-27-darktable-xmp-file-migrate/levels-before-and-after.png">
<img class="post-image-img" src="/img/posts/2017-02-27-darktable-xmp-file-migrate/levels-before-and-after.png">
</a>
<div class="post-image-caption">Слева - корректные, справа - некорректные уровни</div>
</div>

На официальном IRC канале `#darktable` сказали следующее:

```
<LebedevRI> that is a really bad thing, and unfortunately, there isn't any real way to fix this. it was not intentional change
<LebedevRI> the problem is, levels module happened to swap places with tonecurve module. twice. before 2.0 it was like you see with 2.2
<LebedevRI> so to fix this locally, you can just swap these two numbers https://github.com/darktable-org/darktable/blob/master/src/iop/tonecurve.c#L626 https://github.com/darktable-org/darktable/blob/master/src/iop/levels.c#L511
```

Жаль, но что поделаешь? Бывает.

Пересобирать darktable ради открытия старых проектов ни малейшего желания
у меня не возникло, поэтому я выбрал другой путь: изменить значения
уровней прямо в файлах проекта.

Секция с конфигурацией плагина levels в файле `*.xmp` выглядит следующим образом:

```xml
<rdf:li
 darktable:operation="levels"
 darktable:enabled="1"
 darktable:modversion="2"
 darktable:params="0000000000000000000048420000c842d9ce373da19bc43eb41e393f"
 darktable:multi_name=""
 darktable:multi_priority="0"
 darktable:blendop_version="7"
 darktable:blendop_params="gz12eJxjYGBgkGAAgRNODESDBnsIHll8ANNSGQM="/>
</rdf:Seq>
```

где в `darktable:params` хранится [структура](https://github.com/darktable-org/darktable/blob/master/src/iop/levels.c#L65-L70) с настройками плагина в шестнадцатиричном представлении:

```c
typedef enum dt_iop_levels_mode_t
{
  LEVELS_MODE_MANUAL,
  LEVELS_MODE_AUTOMATIC
} dt_iop_levels_mode_t;

typedef struct dt_iop_levels_params_t
{
  dt_iop_levels_mode_t mode;
  float percentiles[3];
  float levels[3];
} dt_iop_levels_params_t;
```

фактически, чтобы вернуть уровни на место достаточно изменить значения
`float levels[3]` следующим образом:

```c
levels[0] = 1.0 - levels[2]
levels[1] = 1.0 - levels[1]
levels[2] = 1.0 - levels[0]
```

после чего уровни должны занять свое прежнее положение.

Чтобы автоматизировать процесс преобразования `*.xmp` файлов пришлось
закостылять скрипт на [python][python]:

```python
#!/usr/bin/python3
import struct
import binascii
import sys


if len(sys.argv) != 2:
    print("Usage:")
    print("    darktable_xmp_migrate_from_2_0_X_to_2_2_3.py filename")
    print("")
    print("Please note the file will be rewritten. Be sure you created a backup")
    sys.exit(1)


out = []
stage = 0
stage_lines = [
        "<rdf:li",
        "darktable:operation=\"levels\"",
        "darktable:enabled",
        "darktable:modversion",
        "darktable:params"
    ]


fin = open(sys.argv[1])
while True:
    line = fin.readline()
    if line == "":
        break
    linestrip = line.strip()
    lineseg = linestrip.split("=")

    if stage == 0 and linestrip == stage_lines[0]:
        stage = 1
        out.append(line)
        continue

    if stage == 1 and linestrip == stage_lines[1]:
        stage = 2
        out.append(line)
        continue

    if stage == 2 and lineseg[0] == stage_lines[2]:
        stage = 3
        out.append(line)
        continue

    if stage == 3 and lineseg[0] == stage_lines[3]:
        stage = 4
        out.append(line)
        continue

    if stage == 4 and lineseg[0] == stage_lines[4]:
        stage = 0
        paramhex_pre = lineseg[1][1:33]
        paramhex = lineseg[1][-25:-1]
        infloathex1 = paramhex[0:8]
        infloathex2 = paramhex[8:16]
        infloathex3 = paramhex[16:24]
        infloat1 = struct.unpack('<f', bytes.fromhex(infloathex1))[0]
        infloat2 = struct.unpack('<f', bytes.fromhex(infloathex2))[0]
        infloat3 = struct.unpack('<f', bytes.fromhex(infloathex3))[0]
        outfloat1 = 1.0 - infloat3
        outfloat2 = 1.0 - infloat2
        outfloat3 = 1.0 - infloat1
        outfloathex1 = hex(struct.unpack('>I', struct.pack('<f', outfloat1))[0])[2:].rjust(8, '0')
        outfloathex2 = hex(struct.unpack('>I', struct.pack('<f', outfloat2))[0])[2:].rjust(8, '0')
        outfloathex3 = hex(struct.unpack('>I', struct.pack('<f', outfloat3))[0])[2:].rjust(8, '0')
        out.append("      %s=\"%s%s%s%s\"\n" % (lineseg[0], paramhex_pre, outfloathex1, outfloathex2, outfloathex3,))
        continue

    stage = 0
    out.append(line)
fin.close()


fout = open(sys.argv[1], "w")
for line in out:
    fout.write(line)
fout.close()
```

От же на github gist: [https://gist.github.com/AlekseyDurachenko/5f831d6051dad70a0356685a0e815f17](https://gist.github.com/AlekseyDurachenko/5f831d6051dad70a0356685a0e815f17)

<p class="alert alert-danger">
Скрипт перезаписывает существующие файлы. Перед использованием убедитесь,
что сделали резервную копию данных.
</p>

### Результат ###

<div class="post-image-container">
<a href="/img/posts/2017-02-27-darktable-xmp-file-migrate/bw_result_dt20X_left_dt223_right.jpg">
<img class="post-image-img" src="/img/posts/2017-02-27-darktable-xmp-file-migrate/bw_result_dt20X_left_dt223_right.jpg">
</a>
<div class="post-image-caption">Ч/Б фотография(перефотографированный негатив): слевая - darktable 2.0.X, справа - darktable 2.2.3 после коррекции уровней</div>
</div>

Файл получился в точности таким же, каким и был.

Так что если вы тоже столкнулись с этой проблемой, то можете
воспользоваться данным рецептом.

Удачи!

### Ссылки ###

- [darktable][darktable] - бесплатная и свободная компьютерная программа с открытым исходным кодом, предназначенная для обработки и каталогизации цифровых изображений.

[darktable]: http://www.darktable.org/
[darktable_levels]: https://www.darktable.org/usermanual/ch03s04s02.html.php
[python]: https://www.python.org/
