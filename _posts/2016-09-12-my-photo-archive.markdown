---
layout: post
title: Организация архива фотографий
date: 2016-09-12 15:08:00
last_modified_at: 2016-09-12 15:08:00
categories: photo
tags: darktable digiKam photo
permalink: /2016/09/12/my-photo-archive.html
---

В данной статье я постараюсь описать методы каталогизации, обработки и резервного копирования
моего фотоархива.

Я не являются профессиональным фотографом, поэтому вопросы хранения и обработки коммерческой фотографии
не затрагиваю.

В статье есть технические моменты, которые подразумевают владение навыками программирования.
Но в общем, материал должен быть понятен всем. Возможно, вы почерпнете для себя что-то полезное.

<!--more-->

- [Структура каталогов для хранения архива фотографий](#file_structure)
  - [Иерархия каталогов верхнего уровня](#file_structure_top_level)
  - [Содержание каталога "**-for-sort-**"](#file_structure_for_sort)
  - [Содержание каталога "**-id-**"](#file_structure_id)
  - [Содержание каталога "**-notes-**"](#file_structure_notes)
  - [Содержание каталога "**-tests-**"](#file_structure_tests)
  - [Содержание каталога "**Groups**"](#file_structure_groups)
  - [Содержание каталога "**Dates**"](#file_structure_dates)
  - [Каталог с фотографиями](#file_structure_kf)
  - [Указание авторства фотографий](#file_structure_kf_authors)
  - [Содержимое каталога с фотографиями](#file_structure_kf_content)
- [Каталогизация фотографий](#catalogization)
- [Обработка фотографий](#processing)
- [Резервное копирование](#backup)
- [Программное обеспечение используемое для обработки и каталогизации фотографий](#software)
- [Исходные коды вспомогательных скриптов и файлов](#appendix)
  - [Скрипт make_all_photos.sh](#make_all_photos.sh)
  - [Скрипт make_photos_for_vk.sh](#make_photos_for_vk.sh)
  - [Скрипт make_photos_for_flickr.sh](#make_photos_for_flickr.sh)
  - [Скрипт backup.sh](#mbackup.sh)
  - [Файл .gitignore](#gitignore)

<span id="file_structure"></span>

## Структура каталогов для хранения архива фотографий

<span id="file_structure_top_level"></span>

### Иерархия каталогов верхнего уровня
<pre>
[D] <b>MyPhotos</b>
    [D] <b>-for-sort-</b>
    [D] <b>-id-</b>
    [D] <b>-notes-</b>
    [D] <b>-tests-</b>
    [D] <b>Groups</b>
    [D] <b>Dates</b>
</pre>

- **-for-sort-** - временный каталог для хранения неотсортированных фотографий;
- **-id-** - информация об авторах;
- **-notes-** - различные фото-заметки;
- **-tests-** - тестовые фотографии для технических нужд;
- **Groups**  - фотографии объединенные в группы;
- **Dates** - остальные фотографии.

<span id="file_structure_for_sort"></span>

### Содержание каталога "**-for-sort-**"

Сюда сгружаются фотографии с различных устройств для последующей сортировки. Для каждого устройства
создается отдельный каталог, который совпадает с его моделью.

<pre>
[D] <b>Canon350D</b>
    [F] <b>IMG_1001.JPG</b>
    [F] <b>IMG_1001.CR2</b>
[D] <b>Canon450D</b>
    [F] <b>IMG_2001.JPG</b>
    [F] <b>IMG_2001.CR2</b>
</pre>

<span id="file_structure_id"></span>

### Содержание каталога "**-id-**"
Для каждого автора, чьи фотографии присутствуют в архиве, создается отдельный каталог с информацией о нем.
Имя этого каталога является уникальным идентификатором автора - **AuthorId**.

<pre>
[D] <b>IvanPetrov</b>
    [F] <b>readme.txt</b>
[D] <b>PetrIvanov</b>
    [F] <b>photo.jpg</b>
    [F] <b>links.txt</b>
</pre>

<span id="file_structure_notes"></span>

### Содержание каталога "**-notes-**"
Каталог с различными фото-заметками, например: объявления, расписания автобусов и т.п.

<pre>
[F] <b>Расписание_Трамвая_13.jpg</b>
[F] <b>Выходные_Дни_Август_2016.jpg</b>
[D] <b>Цены_На_Радиодетали</b>
    [F] <b>IMG_0001.JPG</b>
    [F] <b>IMG_0002.JPG</b>
</pre>

<span id="file_structure_tests"></span>

### Содержание каталога "**-tests-**"
Тестовые фотографии для технических нужд, например: фотографии с закрытой крышкой для
определения горячих пикселей, фотографии белого фона с зажатой диафрагмой
для определения местоположения пыли и т.д.

Для каждого устройства создается отдельный каталог, который совпадает с его моделью.

Пример оформления тестов:
<pre>
[D] <b>Canon600D</b>
    [D] <b>2016.05.02-Canon600D.DustTest</b>
        [F] <b>IMG_0123.CR2</b>
    [D] <b>2016.07.01-Canon600D.HotPixelTest</b>
        [F] <b>IMG_0456.CR2</b>
</pre>

<span id="file_structure_groups"></span>

### Содержание каталога "**Groups**"
Каждая группа фотографий имеет свой отдельный каталог.

<pre>
[D] <b>Birthday</b>
    [D] <b>2011.09.23-Birthday.IvanIvanov</b>
[D] <b>Family</b>
    [D] <b>0000.00.00-Family.Archive</b>
    [D] <b>2002.03.10-Family.School</b>
[D] <b>Dance</b>
    [D] <b>2015.07.18-Dance.OpenAir</b>
[D] <b>IT</b>
    [D] <b>2014.03.15-HardwareFreedomDay.Novosibirsk</b>
    [D] <b>2016.05.14-LugNsk.Picnic</b>
</pre>

<span id="file_structure_dates"></span>

### Содержание каталога "**Dates**"
Фотографии, которые остались без группы, сортируются по дате.

<pre>
[D] <b>0000</b>
    [D] <b>0000.00.00-Animals</b>
[D] <b>2012</b>
    [D] <b>2012.03.17-Walk.Novosibirsk</b>
    [D] <b>2012.09.22-Stuff.Fruits</b>
[D] <b>2016</b>
    [D] <b>2016.02.27-Selfie</b>
    [D] <b>2016.07.25-NightSky</b>
</pre>

<span id="file_structure_kf"></span>

### Каталог с фотографиями
Каталог с фотографиями (сокращенно КФ) содержит набор файлов(не обязательно фотографий), которые объеденны
общей тематикой. Как правило, в один и тот же день у меня может быть несколько КФ.

Для примера:

- 2010.04.10-Marriage.IvanPetrov
- 2011.09.24-Picnic
- 2016.04.14-Walk.Akademgorodok
- 2014.09.21-SoftwareFreedomDay.Novosibirsk.NSU
- 2014.09.21-SoftwareFreedomDay.Novosibirsk.Afterparty

В целом, формат имени КФ свободный. Но я стараюсь записывать ключевые слова через точку и более
значимые помещать левее. В дальнейшем это облегчает поиск.

<span id="file_structure_kf_authors"></span>

### Указание авторства фотографий
В моем архиве находятся не только мои фотографии, но и фотографии других людей.
Для того, чтобы как-то их различать в каждом КФ я создаю отдельный каталог
с именем автора (**AuthorId**).

Но есть пара исключений:

- В каталоге **Dates** в основном хранятся мои фотографии. Поэтому,  в случае  отсутствия других авторов, я не создаю отдельный каталог.
- В каталоге **Groups** могут присутствовать КФ в которых авторы фотографий неизвестны. В этом случае, если нет других авторов, отдельный каталог так же не создается.

Пример:
<pre>
[D] <b>**Dates**</b>
    [D] <b>2012</b>
        [D] <b>2012.03.17-Walk.Novosibirsk</b>   # Мои фотографии
            [F] <b>IMG_0001.JPG</b>     
        [D] <b>2012.05.17-Walk.Tomsk</b>
            [D] <b>AlekseyDurachenko</b>         # Мои фотографии
                [F] <b>IMG_0002.JPG</b>
            [D] <b>IvanPetrov</b>                # Автор "Иван Петров"
                [F] <b>IMG_0003.JPG</b>
            [D] <b>Unknow</b>                    # Автор фотографий неизвестен
                [F] <b>IMG_0004.JPG</b>
[D] <b>**Groups**</b>
    [D] <b>Birthday</b>
        [D] <b>2001.01.11-Birthday.PetrIvanov</b>       # Автор фотографий неизвестен
            [F] <b>IMG_0005.JPG</b>                     
        [D] <b>2011.09.23-Birthday.IvanPetrov</b>
            [D] <b>AlekseyDurachenko</b>                # Мои фотографии
                [F] <b>IMG_0006.JPG</b>
            [D] <b>IvanPetrov</b>                       # Автор "Иван Петров"
                [F] <b>IMG_0007.JPG</b>
            [D] <b>Unknow</b>                           # Автор фотографий неизвестен
                [F] <b>IMG_0008.JPG</b>                     
</pre>

<span id="file_structure_kf_content"></span>

### Содержимое каталога с фотографиями
<pre>
[D] <b>audio</b>
    [F] <b>REC_0001.WAV</b>
[D] <b>raw</b>
    [D] <b>.git</b>
    [D] <b>processed</b>
    [D] <b>uploaded</b>
        [D] <b>vk</b>
        [D] <b>flickr</b>
    [F] <b>.gitignore</b>
    [F] <b>IMG_0001.CR2</b>
    [F] <b>IMG_0001.CR2.xmp</b>
    [F] <b>IMG_0002.CR2</b>
    [F] <b>IMG_0003.CR2</b>
    [D] <b>make_all_photos.sh</b>
    [D] <b>make_photos_for_vk.sh</b>
    [D] <b>make_photos_for_flickr.sh</b>
    [D] <b>uploaded.txt</b>
[D] <b>video</b>
    [F] <b>VID_0001.MP4</b>
[F] <b>IMG_0001.JPG</b>
[F] <b>IMG_0002.JPG</b>
[F] <b>IMG_0003.JPG</b>
[F] <b>track.gpx</b>
</pre>

- **audio** - каталог для аудиофайлов
- **raw** - каталог для фотографий в формате RAW
  - **.git** - локальный [git][git] репозиторий
  - [**.gitignore**][gitignore] - списком файлов, которые не будут добавляться в гит репозиторий
  - **procesed** - каталог для обработанных фотографий в максимальном качестве
  - **uploaded** - каталог для обработанных фотографий предназначенных для загрузки на интернет сайты
    - **vk** - фотографии предназначенные для [ВКонтакте][vk]
    - **flickr** - фотографии предназначенные для [Flickr][flickr]
  - **\*.xmp** - [сопроводительные файлы][sidecarfiles] [darktable][darktable]
  - [**make_all_photos.sh**][make_all_photos.sh] - скрипт для создания обработанных фотографий в максимальном качестве
  - [**make_photos_for_vk.sh**][make_photos_for_vk.sh] - скрипт для создания обработанных фотографий для [ВКонтакте][vk]
  - [**make_photos_for_flickr.sh**][make_photos_for_flickr.sh] - скрипт для создания обработанных фотографий для [Flickr][flickr]
  - **uploaded.txt** - адреса интернет страницу, куда были выложены фотографии
- **video** - каталог для видеофайлов
- **track.gpx** - файл с GPS координатами трека

<span id="catalogization"></span>

## Каталогизация фотографий
После того, как фотографии разложены по каталогам необходимо отредактировать их метаданные.
Для этой цели я использую [digikam][digiKam]. Он позволяет записать метаданные прямо в файлы изображений.
Да и просто является удобным менеджером фотографий.

Обычно, я добавляю следующую информацию:

- GPS координаты места съемки
- Заголовок и описание фотографии
- Информацию об авторе
- Различные теги, включая информацию о людях на фотографии
- Удачные/понравившиеся фотографии помечаю зеленым флажком
- Желтым флажком помечаю JPEG фотографии, RAW которых подлежит обработке в [darktable][darktable]
- Обработанные фотографии помечаются зеленым флажком автоматически(при помощи скриптов)

GPS координаты можно добавить используя либо визуальные инструменты [digiKam][digiKam], либо воспользовавшись
лайфхаком: записать GPS трек на телефон и затем применить его к фотографиям при помощи [exiftool][exiftool]:

```bash
exiftool -overwrite_original -geosync=+07:00:00 -geotag=track.gpx *.JPG
```

Примечание: я редактирую метаданные исходных JPEG файлов, RAW файлы не трогаю.

<span id="processing"></span>

## Обработка фотографий
Обработкой фотографий я занялся совсем недавно, поэтому процедуры еще не совсем устоявшиеся
и в дальнейшем будут усовершенствоваться.

Первым делом я просматриваю фотографии в формате JPEG и отмечаю в [digiKam][digikam] желтыми флажками те,
чьи RAW будут обработаны в [darktable][darktable].

После того, как я завершил обработку RAW файла я помечаю его пятью звездами в [darktable][darktable].
Эта информация нужна для того, чтобы скрипт [make_all_photos.sh][make_all_photos.sh],
понял, что данный файл является завершенным и из него можно создавать JPEG файл максимального качества.
JPEG файл максимального качества автоматически помечается зеленым флажком.

Фотографии, которые предназначены для [Вконтакте][vk] прописываются вручную в скрипте
[make_photos_for_flickr.sh][make_photos_for_flickr.sh]. А для [Flickr][flickr] в
[make_photos_for_flickr.sh][make_photos_for_flickr.sh].

Чтобы сохранить историю изменений файлов я создаю в каталоге <b>raw</b> локальный
[git][git] репозиторий.

<span id="backup"></span>

## Резервное копирование
В качестве носителя для резервных копий я использую внешний жесткий диск с файловой системой ext4.

Перед созданием резервной копии я рассчитываю контрольные суммы всех файлов
и сохраняю их в <b>checksum.md5</b>.

```bash
find . -type f -print0 | xargs -0 md5sum > ./checksum.md5
```

<pre>
[D] <b>MyPhotos</b>
    [D] -for-sort-
    [D] -id-
    [D] -notes-
    [D] -tests-
    [D] Groups
    [D] Dates
    [F] <b>checksum.md5</b>
</pre>

Затем подключаю внешний жесткий диск и запускаю скрипт [backup.sh][backup.sh].

После каждого запуска [backup.sh][backup.sh] создается полная копия содержимого <b>MyPhotos</b>.
Благодаря тому, что файловая система позволяет создавать жесткие ссылки будут скопированы только
измененные файлы. Это позволяет сэкономить место на внешнем жестком диске(и, как следствие,
увеличить число снапшотов) а так же ускорить время создания резервной копии.

<span id="software"></span>

## Программное обеспечение используемое для обработки и каталогизации фотографий
- [digiKam][digikam] - программа для управления коллекцией фотографий
- [Darktable][darktable] - программа для недеструктивной обработки фотографий в формате RAW
- [gimp][gimp] - редактор растровых изображений
- [exiftool][exiftool] - позволяет совершать манипуляции с метаданными фотографий из командной строки
- [imagemagick][imagemagick] - позволяет совершать манипуляции с фотографиями из командной строки

<span id="appendix"></span>

## Исходные коды вспомогательных скриптов и файлов

<span id="make_all_photos.sh"></span>

### Скрипт make_all_photos.sh
Скрипт создает финальные JPEG обработанных RAW в максимальном качестве,
помечает их зеленым флажком, а так же копирует метаданные из исходных JPEG файлов.

```bash
#!/bin/bash

DST_PATH=`pwd`/processed

mkdir -p ${DST_PATH}

function export_photo {
    echo "Processing $1"
    # export raw file to jpeg file
    darktable-cli $1 $1.xmp ${DST_PATH}/${1%%.*}.jpg
    # remove rating from the jpeg file, because the darktable-cli create it, but i don't need it!
    exiftool -overwrite_original -rating=0 -IFD0:Rating=0 -xmp:Rating=0 -IFD0:RatingPercent=0 -xmp:RatingPercent=0 ${DST_PATH}/${1%%.*}.jpg
    exiftool -overwrite_original -rating= -IFD0:Rating= -xmp:Rating= -IFD0:RatingPercent= -xmp:RatingPercent= ${DST_PATH}/${1%%.*}.jpg
    # copy metadata from the original jpeg file
    if [ -f ../${1%%.*}.JPG ];
    then
      exiftool -overwrite_original -TagsFromFile ../${1%%.*}.JPG  "-all:all>all:all" ${DST_PATH}/${1%%.*}.jpg
    else
      exiftool -overwrite_original -TagsFromFile ../${1%%.*}.jpg  "-all:all>all:all" ${DST_PATH}/${1%%.*}.jpg
    fi
    # mark photo as PickLabel=3 (green flag)
    exiftool -overwrite_original -orientation= -xmp:PickLabel=3 ${DST_PATH}/${1%%.*}.jpg
}


# export all photos with .xmp files and rating "5"
for i in *.xmp; do
  RATING=`exiftool -xmp:Rating -s -s -s $i`
  ACCEPT="5"
  if [ "$RATING" == "$ACCEPT" ]
  then
      export_photo ${i%.*}
  fi;
done;
```
<span id="make_photos_for_vk.sh"></span>

### Скрипт make_photos_for_vk.sh  
Скрипт создает JPEG файлы предназначенные для [ВКонтакте][vk]. Разрешение изображений
уменьшается до 1280х1024, а все метаданные удаляются.

```bash
#!/bin/bash

MAX_WIDTH=1280
MAX_HEIGHT=1024
DST_PATH=`pwd`/uploaded/vk

mkdir -p ${DST_PATH}

function export_photo {
    echo "Processing $1"
    darktable-cli $1 $1.xmp ${DST_PATH}/${1%%.*}.jpg --width ${MAX_WIDTH} --height ${MAX_HEIGHT}
    exiftool -overwrite_original -all= ${DST_PATH}/${1%%.*}.jpg
}

# list of the photos
export_photo P9086662.ORF
export_photo P9086669.ORF
export_photo P9086675.ORF
export_photo P9086682.ORF
export_photo P9086690.ORF
export_photo P9086697.ORF
```

<span id="make_photos_for_flickr.sh"></span>

### Скрипт make_photos_for_flickr.sh  
Скрипт создает JPEG файлы предназначенные для [Flickr][flickr].

```bash
# Скрипт еще не написан
```

<span id="backup.sh"></span>

### Скрипт backup.sh  
Скрипт для создания резервной копии фотоархива.

```bash
#!/bin/bash
set -e
set -x

SUBDIR=MyPhotos
SRC_PATH=/home/user/$SUBDIR/
DATE=`date "+%Y%m%d_%H%M%S"`
CUR_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

FILE=`find $CUR_DIR/$SUBDIR -mindepth 1 -maxdepth 1 -type 'd'  | sort -r | head -1`
if [ "$FILE" ]; then
  cp -al $FILE $CUR_DIR/$SUBDIR/$DATE
else
  mkdir -p $CUR_DIR/$SUBDIR/$DATE
fi

rsync -a --delete --numeric-ids --no-relative --delete-excluded $SRC_PATH $CUR_DIR/$SUBDIR/$DATE/.
```

<span id="gitignore"></span>

### Файл .gitignore

```
*.ORF
*.orf
*.CR2
*.cr2
*.DNG
*.dng
*.JPG
*.jpg
.sha1.sum
.par2
processed
uploaded
```

[imagemagick]: http://www.imagemagick.org/script/index.php
[gimp]: https://www.gimp.org/
[exiftool]: http://www.sno.phy.queensu.ca/~phil/exiftool/ "exiftool"
[digikam]: https://www.digikam.org/ "digiKam"
[darktable]: http://www.darktable.org/ "Darktable"
[sidecarfiles]: https://www.darktable.org/usermanual/ch02s02s07.html.php "Sidecar files"
[git]: https://git-scm.com/ "Git"
[vk]: https://vk.com/ "Вконтакте"
[flickr]: https://flickr.com/ "Flickr"
[make_all_photos.sh]: #make_all_photos.sh
[make_photos_for_vk.sh]: #make_photos_for_vk.sh
[make_photos_for_flickr.sh]: #make_photos_for_flickr.sh
[backup.sh]: #backup.sh
[gitignore]: #gitignore
