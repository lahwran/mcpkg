#Repo class, represents a repository
from .. import helpers
import xml.dom.minidom
class RepositoryException(Exception):
	def __init__(self, msg):
		self.msg = msg
	def __str__(self):
		return repr(self.msg)

class Repo:
	def __init__(self, url):
		self.url = url
		self._load()
	def _load(self):
		print "Loading repository from " + self.url
		f = helpers.openAnything(self.url)
		doc = xml.dom.minidom.parse(f)
		f.close()
		pkgs = doc.getElementsByTagName("package")
		print "{0} packages in repository".format(len(pkgs))
