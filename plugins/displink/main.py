# -*- coding: UTF-8 -*-
# Display information about link
# Built by soomsoom and ddorda


import os, re, urllib2
from BeautifulSoup import BeautifulSoup

def pubhandler_displink(connection, event):
	nick=event.source().split('!')[0]
	msg=event.arguments()
	msg=msg[0].split()
	chan=event.target()
	txt = " ".join(msg)
	URL_re = re.compile(ur'[a-z]{3,4}://[a-zA-Z0-9.-]+\.[a-zA-Z]+(/[a-z%A-Z0-9&-]+)*', re.U)
	if (URL_re.search(txt)):
		for url in msg:
			if url.startswith('http') or url.startswith('https://'):
				response = urllib2.urlopen(url)
				content = BeautifulSoup(response.read())
				title=str(content.html.head.title).replace("<title>","").replace("</title>","")
				res = "%s @ %s" % (title, url.split("/")[2])
				connection.privmsg(chan, res)
				break
