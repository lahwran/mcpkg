#this deals with configuring the repository system
import ConfigParser
import os
import os.path

class Config(object):
	def __init__(self):
		self.c = ConfigParser.ConfigParser()
		self._findConfigPath()
		self._initConfigPath()
		if not os.path.isfile('config.ini'):
			print "Configuration file not found, generating default..."
			self._writeDefaultConfig('config.ini')
		self.c.read('config.ini')
		self.items = self.c.items('mcpkg')
		
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

	def _writeDefaultConfig(self, filename):
		self.c.add_section('mcpkg')
		self.c.set('mcpkg', 'verbose', 'true')
		self.c.set('mcpkg', 'colorize', 'true' if os.name == 'posix' else 'false')
		with open(filename, 'wb') as configfile:
			self.c.write(configfile)
		#TODO: add more configuration directives here
