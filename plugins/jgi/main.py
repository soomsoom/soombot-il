# -*- coding: UTF-8 -*-

import tinyurl

def make_tiny(msg):
	print msg
	fixed_msg = '+'.join(msg)
	lmgtfy_address = ('http://lmgtfy.com/?q=%s' % fixed_msg)
	lmgtfy_tiny = tinyurl.create_one(lmgtfy_address)

	return lmgtfy_tiny

def pub_jgi(connection, msg, chan, nick):
	if (len(msg) > 0):
		connection.privmsg(chan, make_tiny(msg))
