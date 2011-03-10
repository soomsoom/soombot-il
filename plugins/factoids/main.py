#factoids plugin: Allow administrators to add commands that return text strings.
# -*- coding: utf-8 -*-
import os
import ConfigParser
import json as pickle
from source.plugin import add_help, remove_help

conf = {}
factoids = {}

def parseConfig():
    """ Parse the configuration file. Required by the plugin. """
    global conf
    config = ConfigParser.RawConfigParser()
    config.read('plugins/factoids/factoids.conf')
    conf['prefix'] = config.get('factoids','prefix')

def ListFactoids(start=True):
    """ Update the list of the factoids. """
    global factoids, conf
    f = open('plugins/factoids/data/factoids.txt', 'ab+')
    if start:
        factoids = pickle.loads(f.read())
    else:
        os.remove('plugins/factoids/data/factoids.txt')
        f = open('plugins/factoids/data/factoids.txt', 'ab+')
        f.write(pickle.dumps(factoids))
        f.flush()
        f.close()
    for f in factoids:
        add_help(f, "pub")

parseConfig()
ListFactoids()


def factoids_add(connection, msg, chan, nick):
    """ Add a factoid. """
    global factoids
    if len(msg) >= 3:
        factoid = msg[1]
        message = ' '.join(msg[2:])
        if factoid in factoids: # If the command already exists.
            connection.privmsg(nick, 'Factoid {0} already exists! Try @factoids remove {0} .'.format(factoid))
        else:
            factoids[factoid] = message
            ListFactoids(False)
            connection.privmsg(nick, 'Success')
            add_help(factoid, "pub")
    else:
        connection.privmsg(nick, 'Usage: @factoids add <command> <message>')

def factoids_remove(connection, msg, chan, nick):
    """ Remove a factoid. """
    global factoids
    factoid = msg[1]
    if len(msg) != 2:
        connection.privmsg(nick, 'Usage: @factoids remove <command>')
    elif not factoids.has_key(factoid): # If the command does not exist.
        connection.privmsg(nick, 'I\'ve never seen a factoid named {0}, sorry!'.format(factoid))
    else:
        del factoids[factoid]
        connection.privmsg(nick, 'The factoid removed successfully.')
        ListFactoids(False)
        remove_help(factoid, "pub")
        
def factoids_update(connection, msg, chan, nick):
    """ Update the factoids list. """
    global factoids
    ListFactoids(True)

def factoids_list(connection, msg, chan, nick):
    """ Return the factoids list. """
    global factoids
    connection.privmsg(nick, ', '.join(factoids))


def privadmin_factoids(connection, msg, chan, nick):
    darray = {'add': factoids_add, 'remove': factoids_remove, 'update': factoids_update, 'list': factoids_list}

    if len(msg) >= 1 and darray.has_key(msg[0]):
        darray[msg[0]](connection, msg, chan, nick)
    else:
        connection.privmsg(nick,'Usage: @factoids [add/remove/update/list] [<command>] [<message>]')

def pubhandler_factoids(connection, event):
    global conf, factoids
    nick=event.source().split('!')[0]
    msg=event.arguments()
    msg=msg[0].split()
    chan=event.target()
    if len(msg) > 0 and msg[0].startswith(conf['prefix']):
        command=msg[0].lstrip(conf['prefix']) # Receive the command and remove the beginning command char
        if factoids.has_key(command): # If the command is a factoid
            if type(factoids[command]) == unicode:
                connection.privmsg(chan, '{0}'.format(factoids[command].encode('utf-8'))) # Send the factoid data to the channel
            else:
                connection.privmsg(chan, '{0}'.format(unicode(factoids[command], 'utf-8').encode('utf-8'))) # Send the factoid data to the channel
                

# Removing all the helps when unloading the plugin.
def unloader_factoids():
	for factoid in factoids:
		remove_help(factoid, "pub")
		
