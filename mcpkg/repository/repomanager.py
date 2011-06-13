#Repository manager - stuff outside this package should use this
from . import *
import cPickle
import gzip
import time
import os.path


class RepoManager(object):

    def __init__(self, cachefile, loadnow=True):
        self.cache = {}  # dict of uri:repo
        self.cachefile = cachefile
        if loadnow:
            self._loadCache()

    def _loadCache(self):  # internal
        print "Loading cache...",
        if not os.path.isfile(self.cachefile):
            print "Not found, creating..."
            self._writeCache()
        try:
            f = gzip.open(self.cachefile, 'rb')
            p = cPickle.Unpickler(f)
            o = p.load()
            f.close()
            for rep in o.values():
                if rep.expireat != 0 and rep.expireat < time.time():
                    del o[rep.url]
            self.cache = o
            print "Done"
        except (IOError) as e:
            print "Failed"
            raise repo.RepositoryException("Failed to load cache: " + str(e))
        except EOFError:
            print "Failed"
            raise repo.RepositoryException("Failed to load cache: Invalid cache file (EOF)")

    def _writeCache(self):  # internal
        print "Writing cache...",
        try:
            f = gzip.open(self.cachefile, 'wb')
            p = cPickle.Pickler(f)
            p.dump(self.cache)
            f.close()
            print "Done"
        except (IOError) as e:
            print "Failed"
            raise repo.RepositoryException("Failed to write cache: " + str(e))

    def loadCache(self):
        self._loadCache()

    def writeCache(self):
        self._writeCache()

    def load(self, uri, verbose=0):
        "Load a repository from a given URI. If it's cached, it will be loaded from the cache"
        if uri in self.cache.keys():
            return self.cache[uri]
        r = repo.Repo(uri, verbosity=verbose)
        self.cache[uri] = r
        return r
