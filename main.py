#!/usr/bin/python
# TODO
# Add date to table and chat messages for better formatting options and to properly wrap messages
# image improvmenet view
import codecs, re, random
import base64

# for the color nicks
import hashlib

import numpy as np
import matplotlib.pyplot as plt
import matplotlib

filename = "testfile.html"
sourcefile = "/home/arun/file.txt"
cssline = " \
<style> \
.responsive { \
    width: 100%; \
    max-width: 1000px; \
    height: auto;  \
} \
img { \
    margin: 20px \
} \
body{ \
    background-color: black; \
    color: #ccc; \
} \
a { \
    color: cornflowerblue\
}\
</style>"

# def line_prepender(filename, line):
#     with open(filename, 'r+') as f:
#         content = f.read()
#         f.seek(0, 0)
#         f.write(line.rstrip('\r\n') + '\n' + content)


file = open(filename, "w", encoding='utf-8')

nicks = []
auxiliaryList = []
nicksAndColors = []

with codecs.open(sourcefile, encoding='utf-8') as f:
    for line in f:
        line = re.sub(r'<', '&lt;', line)
        line = re.sub(r'>', '&gt;', line)
        line = line.rstrip() + "</br>" + "\n"

        # Find the nick
        m = re.search('&lt;(.+?)&gt;', line)
        if m:
            found = m.group(1)
            nicks.append(found)
            for word in nicks:
                if word not in auxiliaryList:
                    result = hashlib.sha256(word.encode())
                    hexcolor = result.hexdigest()[:6]
                    hexhtml = "#" + hexcolor
                    auxiliaryList.append(word)
                    nicksAndColors.append([hexhtml, word])
        else:  # (?<=\] )<[\S]+ #make links hyperlinks
            linkRegex = r'(?<=\] )<[\S]+'
            linkFound = re.search(linkRegex, line)
            if not linkFound:
                line = '<div style="color:gray">' + line + '</div>'

        # color nicks
        for pairs in nicksAndColors:
            line = re.sub("&lt;" + pairs[1] + "&gt;",
                          '<font color="' + pairs[0] + '"><b>&lt;' + pairs[1] + "&gt;</b></font>", line)

        # what if two links?
        regex = r'https?://(?:[a-z0-9\-]+\.)+[a-z]{2,6}(?:/[^/#?]+)+\.(?:jpg|gif|png)'
        mss = re.search(regex, line)
        if mss:
            founds = mss.group(0)
            line = re.sub(regex, '</br><img class="responsive" src="' + founds + '">', line)
        else:  # if it's not an image, check for a normal link
            linkRegex = r'http(s)?://([\w+?\.\w+])+([a-zA-Z0-9\~\!\@\#\$\%\^\&amp;\*\(\)_\-\=\+\\\/\?\.\:\;\'\,]*)?'
            linkFound = re.search(linkRegex, line)
            if linkFound:
                fooundl = linkFound.group(0)
                line = re.sub(linkRegex, '<a href="' + fooundl + '">' + fooundl + '</a>', line)

        file.write(line)

f.close()

# prepend styling
file.seek(0, 0)  # Move the cursor to top line
file.write('\n')
# file.seek(0, 0)# Add a new blank line
file.write(cssline)

file.close()
