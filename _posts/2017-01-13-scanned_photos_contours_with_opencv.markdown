---
layout: post
comments: true
uid: 2017-01-13-scanned_photos_contours_with_opencv
title: "Определение контуров отсканированных фотографий при помощи OpenCV"
date: 2017-01-13 12:00:00
last_modified_at: 2017-01-13 12:00:00
categories: programming
tags: bash linux python opencv imagemagick
permalink: /2017/01/13/scanned_photos_contours_with_opencv.html
---

После долгого и муторного сканирования семейного фотоархива образовалась 
огромная куча "цифрового полуфабриката". 

Для ускорения процесса в сканер помещалась не одна, а сразу несколько
фотографий, что потребовало их разделение при обработке.
Процесс этот рутинный, не интересный и, ко всему прочему, достаточно легко 
автоматизируется.

Ниже пойдет речь о том, как это можно сделать при помощи [Python][python] 
и [OpenCV][opencv].

В качестве примеров исходных данных для демонстрации были взяты 2 скана, 
на которых реальные семейные фотографии заменены на нейтральные.

<div class="post-image-container">
<a href="/img/posts/2017-01-13-scanned_photos_contours_with_opencv/img1_src.jpg">
<img class="post-image-img" src="/img/posts/2017-01-13-scanned_photos_contours_with_opencv/img1_src.jpg">
</a>
<div class="post-image-caption">Рис.1: Пример А - разворот страницы фотоальбома</div>
</div>

<!--more-->

<div class="post-image-container">
<a href="/img/posts/2017-01-13-scanned_photos_contours_with_opencv/img2_src.jpg">
<img class="post-image-img" src="/img/posts/2017-01-13-scanned_photos_contours_with_opencv/img2_src.jpg">
</a>
<div class="post-image-caption">Рис.2: Пример Б - просто несколько фотографий</div>
</div>

<div class="post-image-container">
<a href="/img/posts/2017-01-13-scanned_photos_contours_with_opencv/img1_conts.jpg">
<img class="post-image-img" src="/img/posts/2017-01-13-scanned_photos_contours_with_opencv/img1_conts.jpg">
</a>
<div class="post-image-caption">Рис.3: Пример А - контуры найденные при помощи OpenCV</div>
</div>

<div class="post-image-container">
<a href="/img/posts/2017-01-13-scanned_photos_contours_with_opencv/img2_conts.jpg">
<img class="post-image-img" src="/img/posts/2017-01-13-scanned_photos_contours_with_opencv/img2_conts.jpg">
</a>
<div class="post-image-caption">Рис.4: Пример Б - контуры найденные при помощи OpenCV</div>
</div>

<div class="post-image-container">
<a href="/img/posts/2017-01-13-scanned_photos_contours_with_opencv/img1_rects.jpg">
<img class="post-image-img" src="/img/posts/2017-01-13-scanned_photos_contours_with_opencv/img1_rects.jpg">
</a>
<div class="post-image-caption">Рис.5: Пример А - итоговые контуры фотографий</div>
</div>

<div class="post-image-container">
<a href="/img/posts/2017-01-13-scanned_photos_contours_with_opencv/img2_rects.jpg">
<img class="post-image-img" src="/img/posts/2017-01-13-scanned_photos_contours_with_opencv/img2_rects.jpg">
</a>
<div class="post-image-caption">Рис.6: Пример Б - итоговые контуры фотографий</div>
</div>


Скрипт с подробным описанием работы алгоритма:
{% highlight python %}
#!/usr/bin/python2
# -*- coding: utf-8 -*-
#
# Copyright 2017, Durachenko Aleksey V. <durachenko.aleksey@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import numpy as np
import argparse
import cv2
import os


# исходное изображение очень большое: приблизительно 10x14 тысяч пикселей.
# во-первых, выделение контуров на таком большом изображении займет много
# времени, а во-вторых на нем будет слишком много избыточной информации. 
# необходимы же только контуры больших фигур - фотографий, поэтому изображение
# можно смело уменьшать.
image_scale_factor = 0.1        # 1.0 - 100% изображения

# на рис.3 видно, что OpenCV решил выделить контур альбомного листа, что
# в нашем случае совершенно неприемлемо. для исключения таких ситуаций
# вводится ограничение на максимальный размер ширины и высоты контура фотографии.
contour_maximum_width_factor = 0.8      # 1.0 - 100% изображения
contour_maximum_height_factor = 0.8     # 1.0 - 100% изображения

# после работы алгоритма слияния контуров(о нем пойдет речь ниже)
# могут появиться области, которые ошибочно приняты за контуры фотографий.
# на рис.5 хорошо видно такие области. чтобы их исключить вводится
# правило, по которому контур фотографии не может быть меньше определенного 
# размера
contour_minimum_width_factor = 0.1      # 1.0 - 100% изображения
contour_minimum_height_factor = 0.1     # 1.0 - 100% изображения

# найденные контуры фотографий будет расширены на указанное кол-во пикселей
# во все стороны
contour_additional_pixels = 50

# цвет контуров на диагностических изображениях
contour_color = (0, 255, 0,)
# ширина линий контуров на диагностических изображениях
contour_width = 2

# параметры фильтрации и детектора контуров (примера А)
#gaussian_blur_size = (7, 7)
#canny_threshold_1 = 15
#canny_threshold_2 = 140

# параметры фильтрации и детектора контуров (примера Б)
gaussian_blur_size = (3, 3) 
canny_threshold_1 = 5
canny_threshold_2 = 100


# прямоугольник, описывающий контур фотографии
class MyRect:
    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0

    def __init__(self, x1=0, y1=0, x2=0, y2=0):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def __str__(self):
        return "((%d, %d), (%d, %d))" % (self.x1, self.y1, self.x2, self.y2,)

    def __repr__(self):
        return self.__str__()

    # проверка пересечения двух прямоугольников
    def overlaps(self, rect):
        if rect.x1 <= self.x2 and rect.x2 >= self.x1 and rect.y1 <= self.y2 and rect.y2 >= self.y1:
            return True
        return False

    # слияние двух прямоугольников. итоговый прямоугольник будет полностью
    # вписывать два исходных
    def join(self, rect):
        result = MyRect()
        result.x1 = min(rect.x1, self.x1)
        result.y1 = min(rect.y1, self.y1)
        result.x2 = max(rect.x2, self.x2)
        result.y2 = max(rect.y2, self.y2)
        return result


# алгоритм слияния контуров найденных OpenCV в итоговые контуры фотографий.
# его суть заключается в том, что для каждого контура строится прямоугольник
# полностью вписывающий его, а также слияние всех пересекающихся прямоугольников. 
# в итоге должны получиться прямоугольники, описывающие контуры фотографий.
# так же алгоритм учитывает особый случай: слишком большие контуры
# (вероятно, контуры листа альбома) игнорируются
# примеры слияния: 
# контуры рис.3 в прямоугольники рис.5, 
# контуры рис.4 в прямоугольники рис.6
def merge_contours(contours):
    rectangles = []
    for contour in contours:
        if len(contour) > 2:
            x1 = x2 = contour.tolist()[0][0][0]
            y1 = y2 = contour.tolist()[0][0][1]
            for item in contour.tolist():
                x = item[0][0]
                y = item[0][1]
                x1 = min(x, x1)
                y1 = min(y, y1)
                x2 = max(x, x2)
                y2 = max(y, y2)
                        
            if ((x2 - x1) / image_scale_factor > image_width * contour_maximum_width_factor 
                or (y2 - y1) / image_scale_factor > image_height * contour_maximum_height_factor):
                continue;
            
            # add rect to rectangles and compact them
            rect = MyRect(x1, y1, x2, y2)
            while True:
                new_rect_arr = []
                found = False
                for tmp_rect in rectangles:
                    if rect.overlaps(tmp_rect):
                        rect = rect.join(tmp_rect)
                        found = True
                    else:
                        new_rect_arr.append(tmp_rect)
                rectangles = new_rect_arr
                if not found:
                    break
            rectangles.append(rect)            
    return rectangles


# сохранение изображения с выделенными прямоугольниками фотографий
def write_image_with_rects(filename, image, rectangles):
    contours = []
    for rect in rectangles:
        contours.append(np.array([[rect.x1, rect.y1], [rect.x1, rect.y2], [rect.x2, rect.y2], [rect.x2, rect.y1]]))
    cv2.drawContours(image, contours, -1, contour_color, contour_width)
    cv2.imwrite(filename, image)


# сохранение изображений с выделенными контурами OpenCV
def write_image_with_conts(filename, image, contours):
    cv2.drawContours(image, contours, -1, contour_color, contour_width)
    cv2.imwrite(filename, image)


# чтение аргументов командной строки
appargs = argparse.ArgumentParser()
appargs.add_argument("-i", "--image", required=True, help="path to the image")
args = vars(appargs.parse_args())
# имя исходного файла
image_filename = args["image"]
# базовое имя файла без расширения
image_basefilename = os.path.splitext(os.path.basename(image_filename))[0]
# имя файла с отмеченными итоговыми контурами фотографий
image_rects_filename = image_basefilename + "_rects.tiff"
# имя файла с отмеченными контурами найденными OpenCV
image_conts_filename = image_basefilename + "_conts.tiff"
# чтение исходного изображения с диска
image = cv2.imread(image_filename)
# геометрия исходного изображения
image_height, image_width, image_channels = image.shape
# изменение размера изображения
image = cv2.resize(image, (0, 0), fx=image_scale_factor, fy=image_scale_factor)
# перевод изображения в Ч\Б
image_prepared = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# размывание, чтобы скрыть мелкие детали (иначе они будут ошибочно приняты за конутры)
image_prepared = cv2.GaussianBlur(image_prepared, gaussian_blur_size, 0)
# поиск контуров на изображении
image_prepared = cv2.Canny(image_prepared, canny_threshold_1, canny_threshold_2)
(contours, _) = cv2.findContours(image_prepared, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# слияние найденных контуров в итоговые контуры фотографий
rectangles = merge_contours(contours)
# печать кол-ва найденных контуров фотографий на экран (включая ложные)
print("# %s has %s images" % (image_filename, len(rectangles),))
# запись диагностических изображений с контурами на диск
write_image_with_conts(image_conts_filename, image.copy(), contours)
write_image_with_rects(image_rects_filename, image.copy(), rectangles)
# вывод на экран команд для вырезания фотографий по координатам их контуров
n = 1
for rect in rectangles:
    x1 = rect.x1 / image_scale_factor
    x2 = rect.x2 / image_scale_factor
    y1 = rect.y1 / image_scale_factor
    y2 = rect.y2 / image_scale_factor
    # слишком маленькие контуры фотографий игнорируются (считаются ложными)
    if (x2 - x1 >= image_width * contour_minimum_width_factor
        and y2 - y1 >= image_height * contour_minimum_height_factor):
        x1 -= contour_additional_pixels
        x2 += contour_additional_pixels
        y1 -= contour_additional_pixels
        y2 += contour_additional_pixels
        if x1 < 0:
            x1 = 0
        if y1 < 0:
            y1 = 0
        if x2 >= image_width:
            x2 = image_width - 1
        if y2 >= image_width:
            y2 = image_height - 1
        w = x2 - x1
        h = y2 - y1
        print("convert %s -crop %dx%d+%d+%d %s_%d.%s" % (image_filename, w, h, x1, y1, image_basefilename, n, "ppm",))
        n += 1
{% endhighlight %}

В результате работы скрипта получаются диагностические файлы с контурами,
а также команды, необходимые для получения итоговых фотографий. 
{% highlight bash %}
# img1.pnm has 6 images
convert img1.pnm -crop 4650x7410+5350+6620 img1_1.pnm
convert img1.pnm -crop 4590x7440+650+6590 img1_2.pnm
convert img1.pnm -crop 4220x5580+870+460 img1_3.pnm
convert img1.pnm -crop 4440x5890+5590+430 img1_4.pnm
# img2.pnm has 13 images
convert img2.pnm -crop 4740x6330+180+7700 img2_1.pnm
convert img2.pnm -crop 4490x6350+5030+7680 img2_2.pnm
convert img2.pnm -crop 4540x5870+5120+1470 img2_3.pnm
convert img2.pnm -crop 4450x5980+340+1350 img2_4.pnm
{% endhighlight %}

Конечно, для каждого набора файлов нужно подбирать свои параметры
определения контуров. Но в целом, это намного быстрее чем ручная работа.


### Ссылки ###

- [Python][python] - высокоуровневый язык программирования общего назначения
- [OpenCV][opencv] - библиотека компьютерного зрения с открытым исходным кодом
- [ImageMagick][imagemagick] - набор программ (консольных утилит) для чтения и 
редактирования файлов множества графических форматов
- [Исходный код скрипта для определения контуров отсканированных фотографий](https://gist.github.com/AlekseyDurachenko/a3194313f145321e03ada9b1c510dfcd)


[imagemagick]: http://www.imagemagick.org/script/index.php
[opencv]: http://opencv.org/
[python]: https://www.python.org/