#!python3
#scope...in python 3.3

DISP = '~ '
PROMPT = '> '

class Profile(object):
    """High-level object containing all program data for a specific user"""
    def __init__(self):
        # templates is a library containing all defined templates by name
        self.templates = 	{
        						'basic':Template('basic',{'note':Field('note', Field.TYPE_TEXT)}, set())
        					}
        # databases contains all DBs for this user, init with Home and Work DBs
        self.databases = {'home':Database('home', self.templates), 'work':Database('work',self.templates)}
        # openDatabases is a set containing all DBs open for searching
        self.openDatabases = set()
        return

    # High Level Functions:
    def createDB(self,name):
    	"""Creates a new db with 'name'"""
    	db = Database(name)
    	self.databases[name] = db
    	return

    def selectDatabase(self, command):
    	"""Generic selection function, 'command' is simply what's displayed, returns a db object for another function to use."""
    	print("From which Database would you like to " + command + " an entry?")
    	potentialDB = None
    	while True: #loop until valid input
    	# Print all databases
	    	for name in self.databases:
	    		print(DISP + name)
	    	# Collect user input
	    	workingDB = input(PROMPT).lower()
	    	# Check Validity
	    	if (workingDB  == 'create') and (potentialDB is not None):
	    		self.createDB(potentialDB)
	    		workingDB = potentialDB
	    		break
	    	elif workingDB not in self.databases:
    			print(workingDB + " is not a database, type 'create' to create it, or try again")
    			# Set name to potentialDB in case it is to be created.
    			potentialDB = workingDB 
    			continue
    		else:
    			break
    	print("Okay, working on '" + workingDB + "'")
    	return self.databases[workingDB]

class Utils(object):
	"""Utility class containing handy functions"""
	def __init__(self):
		pass
		return

	def formatTags(tagString):
		if tagString == '':
			return set()

		# Split by comma separator
		tagList = tagString.split(',')
		# drop leading and trailing whitespace
		tagList = [tag.lstrip(' ').rstrip(' ') for tag in tagList]
		# kill any null tags that slipped through
		while '' in tagList:
			tagList.remove('')	
		tags = set()
		for tag in tagList:
			tags.add(tag)
		return tags

class Database(object):
	"""High-level object containing one complete database"""
	def __init__(self, name, templates):
		self.name = name
		# tags is a library of tagnames keyed to sets containing entry titles with those tags
		self.tags = {}
		self.entries = {}
		#templates is a REFERENCE to the 'profile' templates library
		self.templates = templates
		return

	def addEntry(self):
		"""Adds one entry to this database"""
		print("Which template would you like to use?")
		while True:
			for t in self.templates:
				print(DISP, t)
			templateChoice = input(PROMPT).lower()
			if templateChoice not in self.templates:
				print("Sorry, don't recognize '%s', try again." %(templateChoice))
				continue
			else:
				break
		print("Please enter the following information: ")
		title = input(PROMPT + "Title: ")
		entry = self.entryFromTemplate(title,self.templates[templateChoice])
		for field in entry.fields:
			entry.fields[field].content = input(PROMPT + field + ': ')
		# Get newTags from formatTags as a set
		newTags = Utils.formatTags(input("Tags (Comma Separated): ").lower())
		entry.tags = entry.tags.union(newTags)
		self.crossRefTags(entry)
		self.entries[entry.name] = entry
		return

	def crossRefTags(self,entry):
		"""Adds cross Reference to Entry in DB tag bank (for easy searching)"""
		# Check if each tag exists, if it does, add an entry, otherwise key it to a set.
		for tag in entry.tags:
			if tag in self.tags:
				self.tags[tag].add(entry.name)
			else:
				self.tags[tag] = set([entry.name])
		return		

	def entryFromTemplate(self, name, template):
		entry = Entry(name)
		entry.fields = template.fields.copy() #ATTN: will probably need to Deep copy this
		entry.tags = template.tags.copy()
		return entry

class Entry(object):
	"""Basic DB-entry class, typically based on a Template"""
	def __init__(self, name):
		self.name = name
		self.fields = {}
		self.tags = set()
		return

class Field(object):
	"""Basic field class with a given field type"""
	TYPE_TEXT = "text"
	TYPE_IMAGE = "image"
	def __init__(self, name, fieldType):
		self.name = name
		self.fieldType = fieldType
		self.content = ''
		return

class Template(object):
	"""Consists of a list of fields and tags that are associated with a given template"""
	def __init__(self,templateName,fields,tags):
		self.templateName = templateName
		self.fields = fields.copy() #Lib obj ATTN: will probably need to Deep copy this
		self.tags = tags.copy() #Set obj
		return


# Main loop functions
def mainAdd(profile):
	db = profile.selectDatabase("add")
	db.addEntry()
	return

# Initialize: Eventually replace this with loading a saved profile...
profile = Profile()

def main():
	commands = { 	"add":mainAdd,
					# "lookup":profile.lookupEntry,
					# "open":profile.openDB,
					# "close":profile.closeDB,
					# "template":profile.template,
				}

	while True:
		print("Please choose a command from the list: ")
		for command in commands:
			print(DISP + command)
		print(DISP + 'quit')
		userCommand = input(PROMPT).lower()
		if userCommand == 'quit' or userCommand == 'exit':
			break
		if userCommand in commands:
			commands[userCommand](profile)
		else:
			print("Sorry, don't recognize '%s', try again." %(userCommand))
	return

main()
