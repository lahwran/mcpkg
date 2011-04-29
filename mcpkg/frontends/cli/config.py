#this deals with configuring the repository system
import ConfigParser
import os
import os.path
class MisconfigurationException(Exception):
	def __init__(self, msg):
		self.msg = msg
	def __str__(self):
		return str(self.msg)
class Config(object):
	def __init__(self):
		self.c = ConfigParser.ConfigParser()
		self._findConfigPath()
		self._initConfigPath()
		if not os.path.isfile('config.ini'):
			print "Configuration file not found, generating default..."
			self._writeDefaultConfig('config.ini')
		self.c.read('config.ini')
		self.items = {}
		for (name, value) in self.c.items('mcpkg'):
			self.items[name] = value
		
	def _initConfigPath(self):
		if not os.path.exists(self.confpath):
			print "Configuration directory '%(dir)s' doesn't exist, creating..." % dict(dir=self.confpath)
			os.mkdir(self.confpath)
		os.chdir(self.confpath)
			
	def _findConfigPath(self):
		if not any(k == os.name for k in ['posix', 'nt']):
			print "Abort: Invalid OS"
			os.exit(1)
		p = os.path.join(os.path.expanduser("~"), ".mcpkg")
		self.confpath = p

	def get(self, key, default = None):
		if not key in self.items:
			print self.items
			if default == None:
				raise MisconfigurationException('Configuration directive "%(item)s" not defined' % dict(item=key))
			return default
		return self.items[key]

	def _writeDefaultConfig(self, filename):
		self.c.add_section('mcpkg')
		self.c.set('mcpkg', 'verbose', 'true')
		self.c.set('mcpkg', 'colorize', 'true' if os.name == 'posix' else 'false')
		self.c.set('mcpkg', 'cache-name', 'cache.db.gz')
		self.c.set('mcpkg', 'index-name', 'index.lst')
		with open(filename, 'wb') as configfile:
			self.c.write(configfile)
		#TODO: add more configuration directives here
