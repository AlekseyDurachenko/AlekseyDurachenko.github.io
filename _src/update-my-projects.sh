#!/bin/bash

git rm ../content/my-projects/tag/*
rm ../content/my-projects/tag/*
mkdir -p ../content/my-projects/tag
./gen-my-projects.py
git add ../content
git add ../my-projects.html
