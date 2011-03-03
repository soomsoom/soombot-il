#################################
#      BOT Command handler 	#
# ----------------------------- #
# Develop by SoomSoom		#
# License: GPLV3		#
#################################

pubcmds=[] # for Public Commands.
privcmds=[] # for PM Commands.
pubfuncs=[] # For pubhandler functions
privfucs=[] # For privhandler functions

# ------------------ #
# Priv		     #
# ------------------ #


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

# Insert a function to privfucs array.
def privhandler_insert(func):
	if ((func in privfucs) == False):
		privfucs.append(func)
		
# Remove funcrion from the privfucs array		
def privhandler_remove(func):
	privfucs.remove(func)

# Checking if function is in privfucs.
# True - The function is exists
# False - the function is not exists.	
def privhandler_exists(func):
	return (func in privfucs)
	
	
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

# Insert a function to pubfuncs array.
def pubhandler_insert(func):
	if ((func in pubfuncs) == False):
		pubfuncs.append(func)
		
# Remove funcrion from the pubfuncs array		
def pubhandler_remove(func):
	pubfuncs.remove(func)

# Checking if function is in pubfuncs.
# True - The function is exists
# False - the function is not exists.	
def pubhandler_exists(func):
	return (func in pubfuncs)



