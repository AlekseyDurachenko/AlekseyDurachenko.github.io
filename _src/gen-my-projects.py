#!/usr/bin/python2

import markdown
import codecs

# [ 'options as dict', 'formatted html']
def read_file(filename):
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
            if key in ["@TAG", "@LANG"]:
                options[key] = set([x.strip() for x in value.split(",")])
            else:
                options[key] = value
    text = input_file.read()
    html = markdown.markdown(text, extensions=['extra', 'codehilite(css_class=hll)'])
    return [options, html]

print read_file("my-projects/vkDevastator.txt")[0]["@LANG"]
