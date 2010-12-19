from logger import log
import sys, ConfigParser, source.core as cor

commands	=	['start','stop','subject','mute','unmute', 'meeting','keywords','vote','push']
logstart	=	False

keys		=	None

logob	= 	None
logchan	=	None
logdir	=	None
site	=	None

activeVote	=	None
votes		=	None
voteSubject	=	None
varSubject	=	None

def Fetchconfig():
	global logchan, logdir, site
	config = ConfigParser.RawConfigParser()
	config.read(cor.configFile)
	logchan = config.get("meeting","channel")
	logdir = config.get("meeting","directory")
	site = config.get("meeting", "site")
	
def privadmin_meeting(connection, msg, chan, nick):
	if (len(msg) > 0):
		if (msg[0] in commands):
			func=getattr(sys.modules[__name__],msg[0])
			func(connection, msg[1:], chan, nick)
	else:
		temp = ", ".join(commands)
		connection.notice(nick,"Visible commands: %s" % temp)

def start(connection, msg, chan, nick):
	global logstart,logob,logdir, logchan
	if (logstart == True):
		connection.privmsg("There is already started meeting")
	else:
		Fetchconfig()
		logob = log(logdir)
		connection.mode(logchan,"+m")
		connection.notice(logchan, "Attention! %s started meeting" % nick)
		connection.mode(logchan, "+v %s" %nick)
		logstart=True
		connection.notice(logchan,"Attention! log has been started!")
		logob.setOper(nick)
		connection.mode(logchan,"-m")
		connection.privmsg(nick, "Done!")

def subject(connection, msg, chan, nick):
	global logstart, logob, logdir, logchan, varSubject, activeVote
	if (logstart == False):
		connection.notice(nick, "No Log started")
	if (activeVote):
		connection.notice(nick, "You can't do this untill the vote will be off")
	else:
		if (len(msg) > 0):
			varSubject = " ".join(msg)
			connection.mode(logchan, "+m")
			logob.addTopic(varSubject)
			connection.notice(logchan,"The channel is on mute")
			connection.privmsg(logchan,"The subject is: %s" % varSubject)
			connection.privmsg(nick, "Done!")
		else:
			connection.privmsg(nick,"What is the subject?")

def stop(connection, msg, chan, nick):
	global logstart,logob,logdir, logchan, activeVote, varSubject
	if (activeVote):
		connection.privmsg(nick, "Can't do this when a vote is active")
	elif (logstart == False):
		connection.privmsg(nick, "No meeting has started!")
	else:
		logstart=False
		connection.mode(logchan, "+m")
		connection.notice(logchan, "%s stopped the meeting!" % nick)
		connection.notice(logchan, "Attention! log has been stopped!")
		connection.mode(logchan, "-m")
		connection.mode(logchan, "-v %s" %nick)
		connection.privmsg(nick,"Done!")
		subject = "n0ne"
def countVotes():
	results={'agree':0, 'decline':0, 'avoid':0}
	global votes
	for v in votes.itervalues():
		if (v == 1):
			results['agree'] += 1
		elif (v == -1):
			results['decline'] += 1
		elif (v == 0):
			results['avoid'] += 1
	return results

def vote(connection, msg, chan, nick):
	global logob, logchan, activeVote, varSubject, votes, voteSubject
	if (msg[0] == "start"):
		if (varSubject == None):
			connection.privmsg(nick, "There is no subject")
		elif (activeVote):
			connection.privmsg(nick, "There is already active vote")
		else:
			if (len(msg) > 1):
				voteSubject = " ".join(msg[1:])
				connection.mode(logchan,"+m")
				connection.notice(logchan,"Attention! a vote has been started")
				connection.privmsg(logchan,"Vote question: %s" % voteSubject)
				connection.privmsg(logchan,"Vote options: '-1' - for Declined, '0'  - for avoid, '+1' - for agree")
				connection.privmsg(logchan,"For stats type: !stats")
				activeVote=True
				votes = {}
				connection.mode(logchan,"-m")
				connection.privmsg(nick,"Done!")
			else:
				connection.privmsg(nick,"What is the question for the poll?")
	elif (msg[0] == "stop"):
		if (activeVote == False):
			connection.privmsg(nick,"There is no vote active")
		else:
			connection.mode(logchan,"+m")
			activeVote=False
			res=countVotes()
			logob.addVote(voteSubject,res)
			connection.notice(logchan,"Attention! vote stopped")
			results="Agree: " + str(res['agree']) + ", Declined: " + str(res['decline']) + ", Avoided: " + str(res['avoid'])
			connection.privmsg(logchan,"Vote results:")
			connection.privmsg(logchan,results)
			voteSubject = None
			votes = None
			varSubject = None
			connection.mode(logchan,"-m")
			connection.privmsg(nick,"Done!")
			
def keywords(connection, msg, chan, nick):
	global keys, logob
	if (len(msg) > 1):
		keys=", ".join(msg)
		logob.setKeywords(keys)
		connection.privmsg(nick,"Done!")
	else:
		connection.privmsg("What are the keywords?")

def unmute(connection, msg, chan, nick):
	global logchan
	connection.mode(logchan,"-m")
	connection.notice(logchan,"The channel is unmuted!")
	connection.privmsg(nick,"Done!")

def mute(connection, msg, chan, nick):
	global logchan
	connection.mode(logchan,"+m")
	connection.notice(logchan,"The channel is on mute")
	connection.privmsg(nick,"Done!")

def pubhandler_meeting(connection, event):
	nick=event.source().split('!')[0]
	msg=event.arguments()
	msg=msg[0].split(" ")
	chan=event.target()
	global logstart,logob, logchan, votes, activeVote
	if (logstart==True and chan == logchan):
		if ((msg[0] == "+1" or msg[0] == "0" or msg[0] == "-1") and activeVote == True):
			votes[nick]=int(msg[0])
		if (msg[0] == "!stats" and activeVote == True):
			res=countVotes()
			results="Agree: " + str(res['agree']) + ", Declined: " + str(res['decline']) + ", Avoided: " + str(res['avoid'])
			connection.privmsg(logchan,results)
		allmsg = " ".join(msg)
		logob.addLog(nick, allmsg)
	
def push(connection, msg, chan, nick):
	global logob, logstart, keys, logob, logchan, logdir, activeVote, votes, votesSubject, varSubject, keys, site
	if (keys == None):
		
		connection.privmsg(nick, "There is no keywords")
	else:
		logob.done()
		connection.privmsg(logchan, "Log meeting have pushed to %s" % site)
		connection.privmsg(logchan, "By: %s" % nick)
		connection.privmsg(logchan, "Have a nice day!")
		connection.privmsg(nick,"Done!")
	logstart	=	False
	keys		=	None
	logob	= 	None
	logchan	=	None
	logdir	=	None
	site	=	None
	activeVote	=	None
	votes		=	None
	voteSubject	=	None
	varSubject	=	None

