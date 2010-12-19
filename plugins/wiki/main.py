# -*- coding: UTF-8 -*-
import urllib, json, unicodedata

def gs(statement):
	query = urllib.urlencode({'q': statement})
	url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % query
	search_response = urllib.urlopen(url)
	search_results = search_response.read() # Searching...
	results = json.loads(search_results)['responseData']['results'] # Getting results
	# Checking if there is results
	if (len(results) > 0): # If there is results, so:
		data = results[0]['url']
		data = urllib.unquote(data).encode("utf-8", "replace") # Fixing URL encode, to show correctly on IRC
		data = urllib.unquote_plus(data) # Remove any percents from url 
	else: # If not, return null
		data = None
	return data
	
def pub_wiki(connection, msg, chan, nick):
	if (len(msg) > 0):
		search = " ".join(msg)
		query = "site:wiki.archlinux.org.il -inurl:מיוחד -inurl:שיחה -inurl:קטגוריה -inurl:edit -inurl:printable %s" % search
		results = gs(query)
		if (results == None):
			snd = "%s: Not Found" % nick
		else:
			snd = "%s: %s" % (nick, results)
		connection.privmsg(chan, snd)
	else:
		connection.notice(nick,"What to search?")
	
