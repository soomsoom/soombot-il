# clogger plugin: A channel HTML logging plugin.
# -*- coding: utf-8 -*-
from ConfigParser import SafeConfigParser
from plugins.clogger.advancedlogging.htmllogger import HTMLLogger
import sys
import trackback

# Get the logging path and the autostart boolean from the configuration file
confparser = SafeConfigParser()
confparser.read('plugins/clogger/logger.conf')
path = confparser.get('logger', 'path')
autostart = confparser.getboolean('logger', 'autostart')

# Initialize the logger
logger = HTMLLogger(path, autostart)

def privadmin_clogger(connection, msg, chan, nick):
    """ @clogger - Start or stop the logger. """
    global autostart
    global logger
    if len(msg) >= 1:
        if msg[0] == "start":
            if not logger.logging:
                logger.logging = True
            else:
                connection.privmsg(nick, 'The logger already started!')
        else:
            if logger.logging:
                logger.logging = False
            else:
                connection.privmsg(nick, 'The logger already stopped!')
    else:
        connection.privmsg(nick, 'Usage: @clogger [start/stop]')

def pubhandler_clogger(connection, event):
    """ Call the logger if the logging started in any case of message in the channel. """
    global logger
    global autostart
    try:
        nick=event.source().split('!')[0]
        msg=event.arguments()[0]
        chan=event.target()
        logger.LogMessage(nick, msg)
    except UnicodeDecodeError:
        connection.privmsg(nick, 'We only support UTF-8, so please change your client\'s encoding in order to allow reading of your messages.') # Alert users who are not using UTF-8 encoding
    except Exception:
       exc_type, exc_value, exc_traceback = sys.exc_info()
       traceback.print_exception(exc_type, exc_value,exc_traceback, file=sys.stdout) # Avoid bot crashes in any other cases of exceptions
