#################################
# 	BOT Core 		#
# ----------------------------- #
# Develop by SoomSoom		#
# License: GPLV3		#
#################################

from irclib import SimpleIRCClient
from irclib import nm_to_n, irc_lower, all_events
from irclib import parse_channel_modes, is_channel
from irclib import ServerConnectionError
import ConfigParser, os, sys, datetime, time, irclib, traceback
import plugin as plug
import admin as ad
import commandhandler as coha
import logging
__version__= "2.0.1"
ircc=irclib.IRC() # Creating the Bot object.
server = ircc.server() # Creating server object
conf={}
configFile=""
startime=""
LOG_FILENAME = 'logs/errors.log'
status = 0 # 0 - not connected, 1 - connected!
FORMAT="%(asctime)s - Error\n"
logging.basicConfig(filename=LOG_FILENAME,level=logging.NOTSET,format=FORMAT)

def getstartup():
	return startime

#Parsing config parameters
def parseConf(path):
	global config, conf
	config = ConfigParser.RawConfigParser()
	config.read(path)
	conf['me'] = config.get('bot','nick')
	conf['nspassword'] = config.get('nickserv','password')
	conf['password'] = config.get('bot','password')
	conf['admins'] = config.get('bot','admins').split(', ')
	conf['server'] = config.get('bot','server')
	conf['port'] = int(config.get('bot', 'port'))
	conf['chan'] = config.get('bot', 'channel')
	plugins = config.get('bot','plugins').split(',')
	for x in plugins:
		plug.loadPlugin(x.replace(' ',''))
	conf['prefix'] = config.get('bot','prefix')
	conf['aprefix'] = config.get('bot','aprefix')
	if (config.has_option('bot','vhost') == True):
		conf['vhost'] = config.get('bot','vhost')
	else:
		conf['vhost'] = ""

# Handle incoming msgs on the channel 
def handlePubmsg(connection, event):
	nick=event.source().split('!')[0]
	msg=event.arguments()
	msg=msg[0].split(" ")
	chan=event.target()
	if (len(msg) > 0 and msg[0].startswith(conf['prefix'])):
		command=msg[0].split(conf['prefix'])[1]
	if (len(msg) > 0 and msg[0].startswith(conf['aprefix'])):
		acommand=msg[0].split(conf['aprefix'])[1]
	if ('acommand' in locals() and ad.isAdmin(nick)):
		if (acommand == "cmds"):
			x = ", ".join(ad.pubAdmin)
			connection.notice(nick, x)
		elif (ad.isAdmin(nick) and acommand in ad.pubAdmin):
				try:
					package=plug.getPluginPackage(acommand)
					func=getattr(sys.modules[package],"pubadmin_%s" % acommand)
					func(connection, msg[1:], chan, nick)
				except Exception:
					exc_type, exc_value, exc_traceback = sys.exc_info()
					traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stdout)
	if ('command' in locals()):
		if (command == "cmds"):
			x = ", ".join(coha.pubcmds)
			connection.notice(nick, x)
		if (command in plug.loadedPlugins):
			try:
				package=plug.getPluginPackage(command)
				func=getattr(sys.modules[package],"pub_%s" % command)
				func(connection, msg[1:], chan, nick)
			except Exception:
				exc_type, exc_value, exc_traceback = sys.exc_info()
				logging.exception(traceback.extract_stack())
				
# Handle incoming msgs for channel - for pubhandler functions
def handlePubmsgh(connection, event):
	for x in coha.pubfuncs:
		try:
			x(connection, event)
		except Exception:
			exc_type, exc_value, exc_traceback = sys.exc_info()
			traceback.print_exception(exc_type, exc_value, exc_traceback,  file=sys.stdout)
			
# Handle incoming private msgs
def handlePrvmsg(connection, event):
	nick=event.source().split('!')[0]
	msg=event.arguments()
	msg=msg[0].split(" ")
	if (len(msg) > 0 and msg[0].startswith(conf['prefix'])):
		command=msg[0].split(conf['prefix'])[1]
	if (len(msg) > 0 and msg[0].startswith(conf['aprefix'])):
		acommand=msg[0].split(conf['aprefix'])[1]
	chan=nick
	if ('acommand' in locals()):
		if (nick in conf['admins']):
			
			if (acommand == "login" and len(msg) > 1 and ad.isAdmin(nick) == False):
				if (conf['password'] == msg[1]):
					ad.insertAdmin(nick)
					connection.privmsg(nick, "Logged in!")
				else:
					connection.privmsg(nick, "Incorrect Password!")
			elif (acommand == "login" and len(msg) > 1 and ad.isAdmin(nick) == True):
				connection.privmsg(nick,"You are already logged in!")
			elif (ad.isAdmin(nick) and acommand in ad.builtin and len(msg) > 0):
				func=getattr(ad,acommand)
				connection.privmsg(chan,func(msg[1:]))
			elif (ad.isAdmin(nick) and acommand == "cmds"):
				x=""
				if (len(ad.privAdmin) > 0):
					x = ", " + ", ".join(ad.privAdmin)
				connection.privmsg(nick, "%s%s" % (", ".join(ad.builtin),x))
			elif (ad.isAdmin(nick) and acommand in ad.privAdmin):
				try:
					package=plug.getPluginPackage(acommand)
					func=getattr(sys.modules[package],"privadmin_%s" % acommand)
					func(connection, msg[1:], chan, nick)
				except Exception:
					exc_type, exc_value, exc_traceback = sys.exc_info()
					logging.exception(traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stdout))
	if ('command' in locals() and command in plug.loadedPlugins):
		try:
			package=plug.getPluginPackage(command)
			func=getattr(sys.modules[package],"priv_%s" % command)
			func(connection, msg[1:], chan, nick)
		except Exception:
			exc_type, exc_value, exc_traceback = sys.exc_info()
			logging.exception(traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stdout))

# Handle incoming private msgs - for privhandler functions
def handlePrvmsgh(connection, event):
	for x in coha.privfucs:
		try:
			x(connection, event)
		except Exception:
			exc_type, exc_value, exc_traceback = sys.exc_info()
			logging.exception(traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stdout))
	
def handleJoin(connection, event):
	nick=event.source().split('!')[0]
	global startime
	if (nick == conf['me'] and event.target() == conf['chan']):
		startime = time.time()


# Handle Welcome message
def handleWelcome(connection, event):		
	global status, conf, server
	status = 1
	server.join(conf['chan'])  # Channel to join
	print "Connected!"
	MoveToBackground()
	
	
# Handle ctcp requerst
def HandleCtcp(connection, event):
	nick=event.source().split('!')[0]
	msg=event.arguments()[0].split(" ")
	if (msg[0].upper() == "VERSION"):
		connection.ctcp_reply(nick, "Soombot version: %s" % __version__)
	
#Handle incoming private notices
def handlePrvNotice(connection, event):
	global status
	nick=event.source().split('!')[0]
	msg=event.arguments()
	if (status == 0):
		print msg[0]
	#Seeing if we need to identify to NickServ
	if ("identify" in msg[0] and nick == "NickServ"):
		cmd="identify " + conf['nspassword']
		connection.privmsg("nickserv", cmd)
		
		
# If admin is left the channel or change a nick or disconnected,
# Remove him from Admin list.
# -------------------------------
# When admin changes his nick
def handleNick(connection, event):
	nick=event.source().split('!')[0]
	if (ad.isAdmin(nick) and event.target() == conf['chan']):
		ad.removeAdmin(nick)
		
# When admin left the channel
def handlePart(connection, event):
	nick=event.source().split('!')[0]
	if (ad.isAdmin(nick) and event.target() == conf['chan']):
		ad.removeAdmin(nick)
		
# When admin disconnected
def handleQuit(connection, event):
	nick=event.source().split('!')[0]
	if (ad.isAdmin(nick)):
		ad.removeAdmin(nick)

# Moving the proccess to background, that we need no more the '&' on launching or to use Screen
def MoveToBackground():
	UMASK = 0
	WORKDIR = os.getcwd()
	try:
		 pid = os.fork()
	except OSError, e:
      		raise Exception, "%s [%d]" % (e.strerror, e.errno)
      	
      	if (pid == 0):
		os.setsid()
		
		try:
			  pid = os.fork()	# Fork a second child.
	     	except OSError, e:
		 	raise Exception, "%s [%d]" % (e.strerror, e.errno)
		if (pid == 0):	
			os.chdir(WORKDIR)
			os.umask(UMASK)
		else:
			os._exit(0)
	else:
		os._exit(0)
		
	
		
def launch(confFile):
	parseConf(confFile)
	global ircc, server, configFile
	configFile = confFile
	ircc.add_global_handler ('ctcp', HandleCtcp) # Handle Ctcp Reuqests.
	ircc.add_global_handler ('welcome', handleWelcome) # Handle Welcome
	ircc.add_global_handler ('pubmsg', handlePubmsg ) # Handle messges on channel.
	ircc.add_global_handler ('privmsg', handlePrvmsg) # Handles private messages.
	ircc.add_global_handler ('pubmsg', handlePubmsgh ) # Handle messges on channel - for pubhandler fucntions.
	ircc.add_global_handler ('privmsg', handlePrvmsgh ) # Handles private messages - for privhandler functions.
	ircc.add_global_handler ('privnotice', handlePrvNotice) # Handles private notices
	ircc.add_global_handler ('nick', handleNick ) # handle nick changes
	ircc.add_global_handler ('part', handlePart ) # handle part
	ircc.add_global_handler ('quit', handleQuit ) # handle quit
	ircc.add_global_handler ('join', handleJoin )
	print "Connecting..."
	server.connect(conf['server'], conf['port'], conf['me'],None,None,"soombot",conf['vhost'])
	ircc.process_forever() 
