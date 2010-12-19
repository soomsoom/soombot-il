#################################
#      BOT Command handler 	#
# ----------------------------- #
# Develop by SoomSoom		#
# License: GPLV3		#
#################################

pubcmds=[] # for Public Commands.
privcmds=[] # for PM Commands.

# Insert a command to privcmds array.
def priv_insert(cmd):
	if ((cmd in privcmds) == False):
		privcmds.append(cmd)
# Remove command from the privcmds array
def priv_remove(cmd):
	privcmds.remove(cmd)
	
# Checking if command is in privcmds.
# True - The command is exists
# False - the command is not exists.
def priv_exists(cmd):
	return (cmd in privcmds)


# ------------------ #
# Pub		     #
# ------------------ #


# Insert a command to pubcmds array.
def pub_insert(cmd):
	if ((cmd in pubcmds) == False):
		pubcmds.append(cmd)
# Remove command from the pubcmds array
def pub_remove(cmd):
	pubcmds.remove(cmd)
	
# Checking if command is in pubcmds.
# True - The command is exists
# False - the command is not exists.
def pub_exists(cmd):
	return (cmd in pubcmds)


