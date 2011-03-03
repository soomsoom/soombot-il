#################################
# 	Admin Functions		#
# ----------------------------- #
# Develop by SoomSoom		#
# License: GPLV3		#
#################################

import plugin as plug
import core as cor
import sys, os

pubAdmin = []
privAdmin = []
builtin = ['join','part','plugin','shutdown','restart','rehash']
identifiedAdmins = []

#################################
#	Admin Control Commands	#
#################################

def isAdmin(nick):
	return nick in identifiedAdmins

def insertAdmin(nick):
	if isAdmin(nick) == False:
		identifiedAdmins.append(nick)
		
def removeAdmin(nick):
	if isAdmin(nick) == True:
		identifiedAdmins.remove(nick)

#################################
#	Public Admin Commands	#
#################################

def insertPubAdmin(name):
	if ((name in pubAdmin)==False):
		pubAdmin.append(name)
		
		
def removePubAdmin(name):
	if name in pubAdmin:
		pubAdmin.remove(name)
	
#################################
#	Private Admin Commands	#
#################################
def insertPrvAdmin(name):
	if ((name in privAdmin)==False):
		privAdmin.append(name)
		
		
def removePrvAdmin(name):
	if name in privAdmin:
		privAdmin.remove(name)


#########################################
#	Nessecery Functions	 	#
#########################################

def pluglist():
	ret = ""
	for x in os.listdir("plugins"):
		if os.path.isdir("plugins/%s" %x):
			if (ret):
				ret += ", "
			if x in plug.loadedPlugins:
				ret += "%s*" %x
			else:
				ret += x
	return ret

#########################################
#	Built-in Admin Commands 	#
#########################################

def plugin(act):
	if len(act) > 0:
		if (act[0] == "load"):
			if (act[1] != None):
				return plug.loadPlugin(act[1])
			else:
				return "What to load?"
		elif act[0] == "unload":
			if (act[1] != None):
				return plug.unloadPlugin(act[1])
			else:
				return "What to unload?"
		elif act[0] == "rload":
			if (act[1] != None):
				plug.reloadPlugin(act[1])
				return "Done!"
			else:
				return "What to reload?"
		elif act[0] == "list":
			#send = ", ".join(plug.loadedPlugins)
			send = pluglist()
			return send
		else:
			return "Unkown Command!"
	return "Use %splugin <load [name], unload [name], rload [name], list>" % cor.conf['aprefix']
		
	
def join(chan):
	global server
	cor.server.join(chan)
	return "Done!"
	
def part(chan):
	global server
	cor.server.part(chan)
	return "Done!"


def shutdown(cmd):
	global ircc, server
	cor.server.disconnect("Goodbye!")
	sys.exit()
	
def restart(cmd):
	global ircc, server
	path=sys.path[0]
	cor.server.disconnect("BRB")
	cmd = "python2 "+ path + "/bot.py %s &" % cor.configFile  
	os.system(cmd)
	
def rehash(cmd):
	global configFile
	cor.parseConf(cor.configFile)
	return "Done!"



