# -*- coding: UTF-8 -*-
def privadmin_say(connection, msg, chan, nick):
	if (len(msg) > 1):
		ms = " ".join(msg[1:])
		#ms = unicode(ms)
		connection.privmsg(msg[0], ms)
	else:
		connection.privmsg(nick,"usage: @say <#chan> <text>")
	
