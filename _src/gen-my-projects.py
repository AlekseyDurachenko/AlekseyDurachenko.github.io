#!/usr/bin/python2
# -*- coding: utf-8 -*-

import markdown
import os
import codecs
import pytils
from trans import trans

def u8(string):
  return unicode(string,'utf-8')

def eu8(string):
  return string.encode('utf-8')

def ful_trans(string):
  #return eu8(u8(string.replace(' ','-')).encode('trans').lower())
  return string.replace(' ','-').encode('trans').lower()

def create_ul_list_from_dict(data):
    html = "<ul>\n"
    for d in data:        
        html += '<li><a href=/content/my-projects/tag/%s.html>%s (%d)</a></li>\n' % (ful_trans(d), d, len(data[d]))
    html += "</ul>\n"
    return html

# [ 'options as dict', 'formatted html']
def read_project_file(filename):
    #input_file = open(filename, mode="r")
    input_file = codecs.open(filename, mode="r", encoding="utf-8")
    options = {}
    while True:
        line = input_file.readline()
        if not line:
            break
        line = line.strip()
        if line == "@!":
            break;
        if line[0] == "@":
            [key, value] = [x.strip() for x in line.split(":", 1)]
            if key in ["@TAGS"]:
                options[key] = set([x.strip() for x in value.split(",")])
            else:
                options[key] = value
    text = input_file.read()
    html = markdown.markdown(text, extensions=['extra', 'codehilite(css_class=hll)'])
    return [options, html]

def create_html_menu(tags):
    return u"""
<div class="nav-content">
<p><b>Ярлыки</b></p>
%s
</div>
""" % (create_ul_list_from_dict(tags))

def create_html_content(data):
    a = []
    for tag in data[0]["@TAGS"]:
        a.append("<a href=\"/content/my-projects/tag/%s.html\">%s</a>" % (ful_trans(tag), tag))

    return u"""
<div class="content-project">
<h2>%s</h2>
%s
<p><small>Ярлыки: %s</small></p>
<p><a href="%s"><b>Перейти на страницу проекта: %s</b></a></p>
</div>
    """ % (data[0]["@TITLE"], data[1], ", ".join(a), data[0]["@LINK"], data[0]["@LINK"])

data = {}
tags = {}

for filename in os.listdir("my-projects"):    
    [options, html] = read_project_file("my-projects/" + filename)
    data[options["@ID"]] = [options, html]
    
    for tag in options["@TAGS"]:
        if tag not in tags:
            tags[tag] = []
        tags[tag].append([options, html])

html_menu = create_html_menu(tags)

def write_my_projects():
    html_content = u""
    for d in data:
        html_content += create_html_content(data[d])

    template_file = codecs.open("template.html", mode="r", encoding="utf-8")
    html = template_file.read()
    html = html.replace(u"{%TITLE%}", u"Мои проекты")
    html = html.replace(u"{%MENU%}", html_menu)
    html = html.replace(u"{%CONTENT%}", html_content)
    template_file.close()

    output_file = codecs.open("../my-projects.html", mode="w", encoding="utf-8")
    output_file.write(html)
    output_file.close()

def write_my_project_tags():       
    for tag in tags:
        html_content = u""
        eng_tag = ful_trans(tag)
        for data in tags[tag]:
            html_content += create_html_content(data)

            template_file = codecs.open("template.html", mode="r", encoding="utf-8")
            html = template_file.read()
            html = html.replace(u"{%TITLE%}", u"Мои проекты")
            html = html.replace(u"{%MENU%}", html_menu)
            html = html.replace(u"{%CONTENT%}", html_content)
            template_file.close()
    
            output_file = codecs.open("../content/my-projects/tag/%s.html" % (eng_tag), mode="w", encoding="utf-8")
            output_file.write(html)
            output_file.close()

write_my_projects()
write_my_project_tags()
