---
layout: post
hide_updates: true
comments: true
uid: 2017-01-11-command-reference
title: "Справочник команд"
date: 2017-01-11 12:00:00
last_modified_at: 2017-06-06 12:00:00
categories: linux
tags: bash linux
permalink: /2017/01/11/command-reference.html
---

Справочник полезных команд. Будет постепенно пополняться.

<!--more-->

### Git

Удаление локальной и удаленной ветки

```bash
# local branch
git branch -d some_feature
# remote branch
git push origin :some_feature
```

Удаление локальной и удаленной метки

```bash
# local tag
git tag --delete tagname
# remote tag
git push origin :tagname
```

Создание новой пустой ветки

```bash
git checkout --orphan some_feature
git reset --hard
```

### ffmpeg

Замена аудиодорожки в видеофайле mp4

```bash
ffmpeg -i INPUT_VIDEO.mp4 -i INPUT_AUDIO.wav -map 0:0 -map 1:0 -c:v copy -c:a aac -b:a 256k RESULT.mp4
```
