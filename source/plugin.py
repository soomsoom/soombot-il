#################################
# 	Plugin Manager 		#
# ----------------------------- #
# Develop by SoomSoom		#
# License: GPLV3		#
#################################

import sys,os, traceback
import commandhandler as coha
from core import ircc
import admin as ad
# List to save all loadedPlugins
loadedPlugins=[]
#LOG_FILENAME = 'logs/plugin.log'
#logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

# Loading a plugin to the system.
# Getting name of the plugin to load.
def loadPlugin(name):
	global ircc
	package="plugins.%s.main" % name
	if (name in loadedPlugins):
		return "This plugin is already loaded!"
	elif os.path.exists("plugins/%s/main.py" % name):
		try:
			__import__(package) # Loading to the memory the requested plugin
			
			loadedPlugins.append(name)
			if (hasattr(sys.modules[package],"priv_%s" % name)):
				coha.priv_insert(name)
			if (hasattr(sys.modules[package],"pub_%s" % name)):
				coha.pub_insert(name)
			if (hasattr(sys.modules[package],"pubhandler_%s" % name)):
				func=getattr(sys.modules[package],"pubhandler_%s" % name)
				coha.pubhandler_insert(func)
			if (hasattr(sys.modules[package],"privhandler_%s" % name)):
				funcp=getattr(sys.modules[package],"privhandler_%s" % name)
				coha.pubhandler_insert(funcp)
			if (hasattr(sys.modules[package],"joinhandler_%s" % name)):
				funcj=getattr(sys.modules[package],"joinhandler_%s" % name)
				ircc.add_global_handler ('join',  funcj)
			if (hasattr(sys.modules[package],"pubadmin_%s" % name)):
				ad.insertPubAdmin(name)
			if (hasattr(sys.modules[package],"privadmin_%s" % name)):
				ad.insertPrvAdmin(name)
			return "Done!"
		except Exception: # Catching exceptions to avoid crashes...
			exc_type, exc_value, exc_traceback = sys.exc_info()
			traceback.print_exception(exc_type, exc_value,exc_traceback, file=sys.stdout) # printing the exceptions without exit the program
	else:
		return "Cant find this plugin"


		
# Unloading a plugin from the system.
# Getting name of the plugin to unload.
def unloadPlugin(name):
	global ircc
	package="plugins.%s.main" % name
	plugname="plugins.%s" % name
	if ((name in loadedPlugins) == False):
		return "%s is not loaded" % name
	else:
		try:
			if (hasattr(sys.modules[package],"priv_%s" % name)):
				coha.priv_remove(name)
			if (hasattr(sys.modules[package],"pub_%s" % name)):
				coha.pub_remove(name)
			if (hasattr(sys.modules[package],"pubhandler_%s" % name)):
				func=getattr(sys.modules[package],"pubhandler_%s" % name)
				coha.pubhandler_remove(func)
			if (hasattr(sys.modules[package],"pubadmin_%s" % name)):
				ad.removePubAdmin(name)
			if (hasattr(sys.modules[package],"privadmin_%s" % name)):
				ad.removePrvAdmin(name)
			if (hasattr(sys.modules[package],"privhandler_%s" % name)):
				func=getattr(sys.modules[package],"privhandler_%s" % name)
				coha.privhandler_remove(func)
			if (hasattr(sys.modules[package],"joinhandler_%s" % name)):
				funcj=getattr(sys.modules[package],"joinhandler_%s" % name)
				ircc.remove_global_handler ('join',  funcj)
			loadedPlugins.remove(name)
			for n in sys.modules.keys():
     				if (n.startswith(plugname) == True):
            				del(sys.modules[n])
			return "Done!"
		except Exception: # Catching exceptions to avoid crashes...
			exc_type, exc_value, exc_traceback = sys.exc_info()
			traceback.print_exception(exc_type, exc_value,exc_traceback, file=sys.stdout) # printing the exceptions without exit the program
			
			
			
# Reloading a plugin from the system.
# Getting name of plugin. 
# unload it and load it
def reloadPlugin(name):
	unloadPlugin(name)
	loadPlugin(name)
	return "Done!"
	
def getPluginPackage(name):
	package="plugins.%s.main" % name
	return package

def add_help(cmd,wh):
	if (wh == "pm"):
		coha.priv_insert(cmd)
	if (wh == "pub"):
		coha.pub_insert(cmd)
		
def remove_help(cmd,wh):
	if (wh == "pm"):
		coha.priv_remove(cmd)
	if (wh == "pub"):
		coha.pub_remove(cmd)
