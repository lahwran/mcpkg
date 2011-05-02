#Repo class, represents a repository
from .. import helpers
from .package import Package
from .section import Section
import xml.dom.minidom
import time
class RepositoryException(Exception):
	def __init__(self, msg):
		self.msg = msg
	def __str__(self):
		return str(self.msg)

class Repo(object):
	def __init__(self, url, loadnow=True, verbosity=0):
		self.url = url
		self.sections = []
		self.expireat = 0
		if verbosity == 0  :
                        self.silent = True
                else :
                        self.silent = False
		if loadnow:
			self._load()
	def load(self):
		self._load()
	"""Internal method. Do not call from outside this class!"""
	def _load(self):
		if not self.silent: print "Loading repository from " + self.url
		f = helpers.openAnything(self.url)
		doc = False #this could be anything
		try:
			doc = xml.dom.minidom.parse(f)
		except xml.parsers.expat.ExpatError as e:
			raise RepositoryException("Failed to load repository: {0}".format(e))
		finally:
			f.close()
		root = doc.firstChild #<mcpkg>
		if "autorefresh" in root.attributes.keys():
			refresh = root.attributes["autorefresh"].value
			self.expireat = time.time() + refresh
		for section in root.childNodes:
			if section.nodeName != "section":
				continue
			if not "name" in section.attributes.keys():
				if not self.silent : print 'ERROR: Nameless section detected, skipping'
				continue
			s = Section()
			s.name = section.attributes["name"].value
			for package in section.childNodes:
				if package.nodeName != "package":
					continue
				if not all(a in package.attributes.keys() for a in ("name", "author", "version", "mcver")):
					if not self.silent : print 'Invalid <package>: Missing attribute(s), skipping'
					continue
				p = Package()
				p.name = package.attributes["name"].value
				p.author = package.attributes["author"].value
				p.version = package.attributes["version"].value
				p.mcver = package.attributes["mcver"].value
				for pkginfo in package.childNodes:
					if pkginfo.nodeName == "description":
						p.description = pkginfo.firstChild.nodeValue #why is this a child node?
				s.packages.append(p)
			self.sections.append(s)
                if not self.silent :
                        pkgtotal = 0
                        for section in self.sections:
                                pkgtotal += len(section.packages)
                        print "{0} section(s) in repository, totalling {1} packages".format(len(self.sections), pkgtotal)
                        for section in self.sections:
                                print "Section '%(name)s' with '%(numpackages)s' packages" % dict(name=section.name, numpackages=len(section.packages))
                                for package in section.packages:
                                        print package
                                        if package.description :
                                                print "Description:"
                                                print package.description


