from source.core import getstartup
import time, datetime, math

def pub_uptime(connection, msg, chan, nick):
	startime=getstartup()
	if (startime != ""):
		uptime = math.floor(time.time() - startime) # calculate
		snd = "Protects the channel for: %s" % str(datetime.timedelta(seconds=uptime))
	else:
		snd = "Restart required!"
		
	connection.privmsg(chan, "%s" % snd)
	
