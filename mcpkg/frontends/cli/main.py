#main CLI handler
import argparse

class Main(object):
	def __call__(self):
		#application entrypoint
		print "Hello world!"

if __name__ == "__main__":
	Main()()
