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
builtin = ['join','part','load','unload','rload','bot']
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
#	Built-in Admin Commands 	#
#########################################

def load(name):
	return plug.loadPlugin(name)
	
def unload(name):
	return plug.unloadPlugin(name)
	
def rload(name):
	plug.reloadPlugin(name)
	return "Done!"

	
def join(chan):
	global server
	cor.server.join(chan)
	return "Done!"
	
def part(chan):
	global server
	cor.server.part(chan)
	return "Done!"
	
	
def bot(command):
	global ircc,configFile
	if (len(command) > 0):
		if command == "shutdown":
			cor.server.disconnect("Goodbye!")
			sys.exit()
		elif command == "restart":
			path=sys.path[0]
			cor.server.disconnect("BRB")
			cmd = "python2.7 "+ path + "/bot.py %s &" % cor.configFile  
			os.system(cmd)
		elif command == "plugins":
			send = ", ".join(plug.loadedPlugins)
			return send
		elif command == "rehash":
			cor.parseConf(cor.configFile)
			return "Done!"
		return "Unkown Command!"
	return "Use %sbot <command>" % cor.conf['acommand']


