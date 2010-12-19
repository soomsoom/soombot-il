# -*- coding: UTF-8 -*-
import urllib, json, unicodedata, re

def remove_html_tags(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

def searchyoutube(statement):
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
	
def pub_youtube(connection, msg, chan, nick):
	if (len(msg) > 0):
		values = " ".join(msg)
		query = "site:youtube.com %s" % values
		results = searchyoutube(query)
		if (results == None):
			snd = "%s: Not Found" % nick
		else:
			snd = "%s: %s" % (nick, results)
		connection.privmsg(chan,snd)
		
