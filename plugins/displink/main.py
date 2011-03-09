# -*- coding: UTF-8 -*-
# Display information about link
# Build by soomsoom and ddorda

import os, re, unicodedata, lxml.html 

def pubhandler_displink(connection, event):
	nick=event.source().split('!')[0]
	msg=event.arguments()
	msg=msg[0].split()
	chan=event.target()
	txt = " ".join(msg)
	URL_re = re.compile(ur'[a-z]{3,4}://[a-zA-Z0-9.-]+\.[a-zA-Z]+(/[a-z%A-Z0-9&-]+)*', re.U)
	if (URL_re.search(txt)):
		for url in msg:
			if url.startswith('http'):
				content = lxml.html.parse(url)
				title = content.find(".//title").text
				res = "%s @ %s" % (title.encode("utf-8"), url.split("/")[2])
				connection.privmsg(chan, res)
				break
