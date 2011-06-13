#This is just a data holding class


class Package(object):
    def __init__(self):
        self.name = ""
        self.author = ""
        self.version = ""
        self.mcver = ""
        self.description = ""

    def __str__(self):
        return "Package '%s' by '%s' version '%s' for Minecraft %s" % (self.name, self.author, self.version, self.mcver)
