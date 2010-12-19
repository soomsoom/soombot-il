import sys, traceback, os, plugins
import source.plugin as plug 
import source.core as core

if __name__ == "__main__":
	if (len(sys.argv) > 1):
		core.launch(sys.argv[1])
	else:
		core.launch("bot.conf")
