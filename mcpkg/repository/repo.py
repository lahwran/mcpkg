#Repo class, represents a repository
from .. import helpers
from .package import Package
from .section import Section
import xml.dom.minidom
class RepositoryException(Exception):
	def __init__(self, msg):
		self.msg = msg
	def __str__(self):
		return repr(self.msg)

class Repo:
	def __init__(self, url):
		self.url = url
		self.sections = []
		self._load()
	def _load(self):
		print "Loading repository from " + self.url
		f = helpers.openAnything(self.url)
		doc = xml.dom.minidom.parse(f)
		f.close()
		root = doc.firstChild #<mcpkg>
		for section in root.childNodes:
			if section.nodeName != "section":
				continue
			if not "name" in section.attributes.keys():
				print 'ERROR: Nameless section detected, skipping'
				continue
			s = Section()
			s.name = section.attributes["name"].value
			for package in section.childNodes:
				if package.nodeName != "package":
					continue
				if not ("name", "author", "version", "mcver" in package.attributes.keys()):
					print 'Invalid <package>: Missing attribute(s), skipping'
					continue
				p = Package()
				p.name = package.attributes["name"].value
				p.author = package.attributes["author"].value
				p.version = package.attributes["version"].value
				p.mcver = package.attributes["mcver"].value
				s.packages.append(p)
			self.sections.append(s)
		print "{0} section(s) in repository".format(len(self.sections))
		for section in self.sections:
			print "Section '{0}' with '{1}' packages".format(section.name, len(section.packages))
			for package in section.packages:
				print package
