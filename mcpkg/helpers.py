#This file contains helper functions that don't really belong anywhere else


def openAnything(source):
    """Opens a URI, filename, or string as a stream
    Just call .close when you are done with returned object
    """
    if hasattr(source, "read"):  # it's likely a stream already
        return source
    if source == '-':  # stdin
        import sys
        return sys.stdin
    # try to open it with urllib
    import urllib2
    try:
        return urllib2.urlopen(source)
    except (IOError, OSError):
        pass
    # try to use native open function (source is pathname)
    try:
        return open(source)
    except (IOError, OSError):
        pass
    # treat it as a string
    import StringIO
    return StringIO.StringIO(str(source))
