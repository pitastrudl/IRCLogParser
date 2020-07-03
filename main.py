#!/usr/bin/python
# TODO
# Add date to table and chat messages for better formatting options and to properly wrap messages
# image improvmenet view
import codecs, re, sys
import base64

# for the color nicks
import hashlib
# script file_to_parse outputfile
#full paths!
filename = sys.argv[2]
sourcefile = sys.argv[1]
print(filename,sourcefile)
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

file = open(filename, "w", encoding='utf-8')

nicks = []
auxiliaryList = []
nicksAndColors = []

with codecs.open(sourcefile, encoding='utf-8') as f:
    for line in f:
        # encode greater/lowerthan signs
        line = re.sub(r'<', '&lt;', line)
        line = re.sub(r'>', '&gt;', line)


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
            # color nicks
            for pairs in nicksAndColors:
                line = re.sub("&lt;" + pairs[1] + "&gt;",
                              '<span color="' + pairs[0] + '"><b>&lt;' + pairs[1] + "&gt;</b></span>", line)
        else:  # (?<=\] )<[\S]+ #color if line is not a message?
            linkRegex = r'(?<=\] )&lt[\S]+'
            linkFound = re.search(linkRegex, line)
            if not linkFound:
                line = re.sub(r"((?<=\] )[^&].*)", '<span style="color:#666666">' + r"\1"+ "</span>",line)

        # check if it's an image
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

        line = '<div style="color:#d9d9d9">' + line + '</div>' + "\n"
        #line = line.rstrip() + "</br>" + "\n"

        file.write(line)

f.close()

# prepend styling
file.seek(0, 0)  # Move the cursor to top line
file.write('\n')
file.write(cssline)

file.close()
