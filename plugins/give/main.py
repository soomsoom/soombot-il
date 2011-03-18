# Plugin made by Soomsoom

import sys
import source.plugin as plug


def pub_give(connection, msg, chan, nick):
	if (len(msg) > 2):
		if (msg[1] != None):
			module = msg[1]
			mod = plug.getPluginPackage(module)
			if (hasattr(sys.modules[mod], "pub_%s" % module)):
				func = getattr(sys.modules[mod], "pub_%s" % module)
				func(connection, msg[2:], chan, msg[0])
			else:
				connection.notice(nick, "Command not found")
	else:
		connection.notice(nick,"Usage: give <nick> <command> <values>")
	

