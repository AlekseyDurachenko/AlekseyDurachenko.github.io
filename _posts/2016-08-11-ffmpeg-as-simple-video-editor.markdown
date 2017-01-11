---
layout: post
comments: true
uid: 2016-08-11-ffmpeg-as-simple-video-editor
title: "Магия ffmpeg: деинтерлейсинг, стабилизация видео, коррекция аудиодорожки"
date: 2016-08-11 23:16:00
last_modified_at: 2016-08-11 23:16:00
categories: video
tags: linux ffmpeg audacity video
permalink: /2016/08/11/ffmpeg-as-simple-video-editor.html
---

<div class="post-image-container">
<a href="/img/posts/2016-08-11-ffmpeg-as-simple-video-editor/1.png">
<img class="post-image-img" src="/img/posts/2016-08-11-ffmpeg-as-simple-video-editor/1.png">
</a>
<div class="post-image-caption">ffmpeg</div>
</div>

Недавно мне потребовалось обработать несколько видеороликов применяя
к ним приблизительно одинаковую последовательность действий.

На первый взгляд кажется логичным использование полноценного редактора видео, но в этом случае
потребуется выполнять однотипные действия для каждого проекта, что очень долго и лениво.

Другой путь: автоматизировать процесс обработки при помощи [ffmpeg](https://ffmpeg.org/). Именно о нем и пойдет речь.

<!--more-->

Исходный файл input.mts имеет частоту кадров равную 50 с чересстрочной разверткой.

Для начала удалим чересстрочную развертку понизив частоту кадров до 25, а видео переведем в формат rawvideo,
чтобы дальнейшая обработка не сказалась на качестве видеоматериала.
Если резать видео не нужно, то убираем ключи `-ss`(время первого кадра видео) и `-t`(продолжительность).

```bash
$ ffmpeg -threads 0 -i input.mts -filter:v yadif -r 25 -acodec copy -vcodec rawvideo -ss 00:00:00 -t 00:02:34 -y deinterlece.avi
```

Устранить тряску камеры можно при помощи фильтра [vidstabdetect](https://ffmpeg.org/ffmpeg-filters.html#vidstabdetect-1), но
имейте ввиду, что для этого требуется относительно свежая версия [ffmpeg](https://ffmpeg.org/). Её можно
скачать [отсюда](https://ffmpeg.org/download.html).

```bash
$ ffmpeg -threads 0 -i deinterlece.avi -vf vidstabdetect=stepsize=6:shakiness=10:accuracy=15 -acodec copy -vcodec rawvideo -y stab_vidstabdetect.avi
$ ffmpeg -threads 0 -i deinterlece.avi -vf vidstabtransform -acodec copy -vcodec rawvideo -y stabilized.avi
```

Извлекаем оригинальную аудиодорожку в файл `input.wav`.

```bash
$ ffmpeg -i stabilized.avi input.wav
```

Корректируем полученный аудиофайл в [audacity](http://www.audacityteam.org/) и сохраняем результат в файл `output.wav`.
Важно, чтобы файлы `input.wav` и `output.wav` были одинаковой длины.

Заменяем аудиодорожку на `output.wav`, накладываем фильтр `unsharp=5:5:0.8:3:3:0.4`,
а так же в начале и конце создаем плавное проявление и затемнение продолжительностью
по 5 секунд (100 кадров) `fade=in:0:100,fade=out:N:100`, где N - это кол-во кадров в видео минус 100.

```bash
$ ffmpeg -threads 0 -i stabilized.avi -i output.wav -filter_complex "[0:v]unsharp=5:5:0.8:3:3:0.4,fade=in:0:100,fade=out:1394:100" -acodec copy -vcodec rawvideo -map 1:a -map 0:v -y result.avi
```

Сжимаем видео.

```bash
$ ffmpeg -threads 0 -i result.avi -c:v libx264 -preset slow -crf 22 -c:a aac -b:a 256k result.mp4
```

Удаляем временные файлы.

```bash
$ rm deinterlece.avi input.wav result.avi stab_vidstabdetect.avi stabilized.avi transforms.trf
```

Готовый скрипт.

```bash
#!/bin/bash
set -e
# Работа со скриптом проходит в три этапа.
# * Первый запуск скрипта. В случае успеха будет создан файл $AUDIO_EXPORT
# * Ручное создание файла $AUDIO_IMPORT
# * Второй запуск скрипта. В случае успеха будет создан файл $VIDEO_RESULT


# Входной файл с чересстрочной разверткой
VIDEO_IN="input.mts"
# Целевая частота кадров равная половине от частоты кадров $VIDEO_IN.
# Например, если $VIDEO_IN имеет частоту кадров 50, то нужно вписать 25
VIDEO_DEINTERLECE_FPS="25"
# Выходной файл в формате mp4 (libx264)
VIDEO_RESULT="result.mp4"
# В этот файл будет экспортирована аудиодорожка из $VIDEO_IN
AUDIO_EXPORT="original.wav"
# Аудиодорожка, которая будет использована в $VIDEO_RESULT
AUDIO_IMPORT="result.wav"


# Если необходимо обрезать кусок видео, то впишите "true", в противном случае "false"
TRIM_VIDEO="true"
# Время первого кадра
TRIM_ARG_SS="00:01:00"
# Продолжительность
TRIM_ARG_T="00:00:20"

# Кол-во кадров для эффекта fade in в начале видео
FADE_IN_FRAMES="100"
# Кол-во кадров для эффекта fade out в конце видео
FADE_OUT_FRAMES="100"

# Конфигурация фильтра стабилизации видео
VIDSTABDETECT_OPTIONS="stepsize=6:shakiness=10:accuracy=15"
# Конфигурация фильтра unsharp (применяется после стабилизации видео)
UNSHARP_OPTIONS="5:5:0.8:3:3:0.4"


# Если входного файла нет, то прекращаем работу скрипта
if [ ! -f "$VIDEO_IN" ];
then
  echo "Error: $VIDEO_IN not exits"
  exit -1
fi


# Производим деинтерлейсинг и, если нужно, вырезаем кусок видео
if [ ! -f "deinterlece.avi" ];
then
  if [ "$TRIM_VIDEO" = "true" ]
  then
    # Деинтерлейсинг и вырезание куска видео
    ffmpeg -threads 0 -i "$VIDEO_IN" -filter:v yadif -r $VIDEO_DEINTERLECE_FPS -acodec copy -vcodec rawvideo -ss $TRIM_ARG_SS -t $TRIM_ARG_T -y deinterlece.avi
  else
    # Просто деинтерлейсинг
    ffmpeg -threads 0 -i "$VIDEO_IN" -filter:v yadif -r $VIDEO_DEINTERLECE_FPS -acodec copy -vcodec rawvideo -y deinterlece.avi
  fi
fi


# Расчет таблицы для стабилизации видео
if [ ! -f "stab_vidstabdetect.avi" ];
then
  ffmpeg -threads 0 -i deinterlece.avi -vf vidstabdetect=$VIDSTABDETECT_OPTIONS -acodec copy -vcodec rawvideo -y stab_vidstabdetect.avi
fi


# Стабилизация видео
if [ ! -f "stabilized.avi" ];
then
  ffmpeg -threads 0 -i deinterlece.avi -vf vidstabtransform -acodec copy -vcodec rawvideo -y stabilized.avi
fi


# Извлечение аудиодорожки из исходного видео
if [ ! -f "$AUDIO_EXPORT" ];
then
  ffmpeg -i stabilized.avi "$AUDIO_EXPORT"
fi


# Если аудиодорожка для замены не создана, то завершаем работу скрипта
if [ ! -f "$AUDIO_IMPORT" ];
then
  echo "Error: $AUDIO_IMPORT not exits";
  exit -1
fi


# Создаем итоговое видео
if [ ! -f "result.avi" ];
then
  # Узнаем кол-во кадров в видеофайле
  TOTAL_FRAMES=`exiftool stabilized.avi | grep "Total Frame Count" | grep -oE "[^:]+$" | tr -d '[[:space:]]'`
  # Вычитаем длину эффекта fade out
  TOTAL_FRAMES=`expr $TOTAL_FRAMES - $FADE_OUT_FRAMES`
  # Создаем итоговое видео
  ffmpeg -threads 0 -i stabilized.avi -i "$AUDIO_IMPORT" -filter_complex "[0:v]unsharp=$UNSHARP_OPTIONS,fade=in:0:$FADE_IN_FRAMES,fade=out:$TOTAL_FRAMES:$FADE_OUT_FRAMES" -acodec copy -vcodec rawvideo -map 1:a -map 0:v -y result.avi
fi


# Конвертируем из rawvideo в libx264
if [ ! -f "$VIDEO_RESULT" ];
then
  ffmpeg -threads 0 -i result.avi -c:v libx264 -preset slow -crf 22 -c:a aac -b:a 256k "$VIDEO_RESULT"
fi


# Удаляем временные файлы
rm deinterlece.avi "$AUDIO_EXPORT" result.avi stab_vidstabdetect.avi stabilized.avi transforms.trf
```
