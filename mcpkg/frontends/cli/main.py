#main CLI handler
import argparse
from config import Config
from mcpkg.repository.repomanager import RepoManager
import glob
import os
import os.path

class Main(object):
        def __init__(self):
                self.parsers = {}
                self.conf = Config()
        def __call__(self):
                #application entrypoint
                self._createParser()
                self.args = self.parser.parse_args()
                self.args.func(self.args)
        def _createParser(self):
                p = argparse.ArgumentParser(description="mcpkg command-line interface.")
                sub = p.add_subparsers()
                a = sub.add_parser('update', help='Update all repositories')
                a.set_defaults(func=self._update)
                a.add_argument("-v", action="store_true", help="Be more verbose")
                a.add_argument("--add-repo", action="append", nargs=1, help="Adds a repository to the cache.")
                b = sub.add_parser('maint', help='Maintain local mcpkg data')
                b.add_argument('--reset-all', action='store_true', help='Reset mcpkg to newly-installed state (WARNING: this deletes the .mcpkg directory)')
                b.set_defaults(func=self._maint)
                self.parser = p
                self.subparser = sub
                self.parsers['update'] = a
                self.parsers['maint'] = b
        def _update(self, args):
                if args.add_repo :
                        repoarg = args.add_repo[0][0]
                        if repoarg :
                                if os.path.exists(self.conf.get("index-name")) :
                                        fileobj = open(self.conf.get("index-name"), "rb")
                                        lines = fileobj.read().replace("\r", "").split("\n")
                                        fileobj.close()
                                        for line in lines :
                                                if line != "" :
                                                        if line == repoarg :
                                                                print "URL already in index"
                                                                return
                                else : open(self.conf.get("index-name"), "w").close()
                                if args.v : verbose = 1
                                if not args.v : verbose = 0
                                r = RepoManager(self.conf.get('cache-name'))
                                r.load(repoarg, verbose)
                                r.writeCache()
                                print "Added %(url)s to cache" % dict(url=repoarg)
                                fileobj = open(self.conf.get("index-name"), "a")
                                if os.name == "nt" :
                                    lineending = "\r\n"
                                else : lineending = "\n"
                                fileobj.write(repoarg + lineending)
                                fileobj.close()
                        

                        return
                if not os.path.exists(self.conf.get("index-name")) :
                    open(self.conf.get("index-name"), "w").close()
                r = RepoManager(self.conf.get('cache-name'))
                #clear out the cache
                r.cache = {}
                try:
                    f = open(self.conf.get('index-name'), 'rb')
                except IOError as e:
                    print "Failed to open %(iname)s: %(reason)s" % dict(iname=self.conf.get('index-name'), reason=str(e))
                    print "Abort"
                    return
                for line in f:
                    if os.name == "nt" : line = line[:-2]
                    else : line = line[:-1]
                    print 'Processing %(url)s ...' % dict(url=line)
                    r.load(line)
                f.close()
                r.writeCache()
        def _maint(self, args):
                if args.reset_all:
                        print "Performing full reset..."
                        #delete config file     
                        for f in glob.glob('*'):
                                print "Deleting %s" % (f)
                                os.remove(f)
                        return
                self.parsers['maint'].print_help()
if __name__ == "__main__":
        Main()()
