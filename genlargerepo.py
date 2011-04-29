#generate a large repository for testing
import random
print "<?xml version=\"1.0\"?>"
print "<mcpkg>"
print "<section name=\"Spam\">"
templ = '<package name="%(name)s" author="%(author)s" version="1.0" mcver="1.5_01">\
<description>Spam</description>\
</package>'
def randstr(length):
    s = ""
    for i in range(1,length):
        s += str(random.randint(33,126))
    return s
for i in range(0,10000):
    author = randstr(5)
    name = randstr(5)
    print templ % dict(author = author, name = name)
print "</section>"
print "</mcpkg>"
