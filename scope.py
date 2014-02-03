#!python3
#scope...in python 3.3
import pickle

# Constants
DISP = '~ ' # Prompt used to display lists
PROMPT = '> ' # Prompt used for user input
SEPARATOR = '-------------------------------------'
SAVE_LOCATION = 'save.pkl'
SAVE_BACKUP = 'save.pkl.bak'

#Global Functions

def saveToFile(obj, dest):
	f = open(dest, 'wb')
	pickle.dump(obj, f)
	f.close()
	return

def loadFromFile(dest):
	f = open(dest, 'rb')
	obj = pickle.load(f)
	f.close()
	return obj

class Profile(object):
    """High-level object containing all program data for a specific user"""
    def __init__(self):
        # templates is a library containing all defined templates by name
        self.templates = 	{
        						'basic':Template('basic',{'note':Field('note', Field.TYPE_TEXT)}, set())
        					}
        # databases contains all DBs for this user, init with Home and Work DBs
        self.databases = 	{
        						'home':Database('home', self.templates), 
        						'work':Database('work', self.templates),
        					}
        # openDatabases is a set containing all DBs open for searching
        self.openDatabases = set(self.databases.values())
        return

    # High Level Functions:
    def createDB(self,name):
    	"""Creates a new db with 'name'"""
    	db = Database(name, self.templates)
    	self.databases[name] = db
    	self.openDatabases.add(db)
    	return

    def selectDatabase(self, command):
    	"""Generic selection function, 'command' is simply what's displayed, returns a db object for another function to use."""
    	print("Which Database would you like to " + command + " an entry?")
    	potentialDB = None
    	while True: #loop until valid input
    	# Print all databases
	    	for name in sorted(self.databases):
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

	def formatTags(tagString):
		"""Formats 'tagString' into a set of individual tags"""
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
		# Entries keyed by name
		self.entries = {}
		#templates is a REFERENCE to the 'profile' templates library
		self.templates = templates
		return

	def addEntry(self):
		"""Adds one entry to this database"""
		print("Which template would you like to use?")
		while True:
			for t in sorted(self.templates):
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

	def editEntry(self, entry):
		"""Edit or delete database entry"""
		print("'edit', 'delete', 'tags' or 'main'?")
		userChoice = input(PROMPT).lower()
		if userChoice == 'delete':
			self.deleteEntry(entry)
			print(entry.name, "has been deleted; 'undo' or 'main'.")
		return		

	def deleteEntry(self, entry):
		for tag in entry.tags:
			self.tags[tag].remove(entry.name)
		self.entries.pop(entry.name)
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
		"""Creates an entry instance from a given entry 'template' object"""
		entry = Entry(name, template.templateName)
		entry.fields = template.fields.copy() #TODO: will probably need to Deep copy this
		entry.tags = template.tags.copy()
		return entry

class Entry(object):
	"""Basic DB-entry class, typically based on a Template"""
	def __init__(self, name, entryType):
		self.name = name
		self.fields = {}
		self.entryType = entryType
		self.tags = set()
		return

	def printSelf(self):
		print(SEPARATOR)
		print("Title: ", self.name)
		for field in self.fields:
			print (field, ": ", self.fields[field].content)
		print(SEPARATOR)
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
		self.fields = fields.copy() #Lib obj TODO: will probably need to Deep copy this
		self.tags = tags.copy() #Set obj
		return


# Main loop functions
def mainAdd(profile):
	"""selects database, then adds a new entry to it"""
	db = profile.selectDatabase("add")
	db.addEntry()
	return

def mainSearch(profile):
	(entry, db) = querySearch(profile)
	if entry is not None:
		entry.printSelf()
		db.editEntry(entry)
	else:
		return

def mainSave(profile):
	saveToFile(profile, SAVE_LOCATION)
	return


def querySearch(profile):
	while True:
		print("Please enter a search term or tag, 'quit' to exit.")
		query = input(PROMPT)
		if query == 'quit':
			return (None,None)

		# split query into word list by spaces
		queries = query.lstrip(' ').rstrip(' ').split(' ')
		# iterate through entries in all databases and search titles adding matches to a set
		results = set()
		for db in profile.openDatabases:
			for entryName in db.entries:
				for word in queries:
					if word in entryName or entryName in word:
						# Add entry in a tuple with db (db, entry)
						results.add((db.entries[entryName], db))
			for tag in db.tags:
				if word in tag or tag in word:
					for entryName in db.tags[tag]:
						results.add((db.entries[entryName], db))
		# Change set to an indexable list
		resultList = [x for x in results]
		resultList.sort(key=lambda x: x[1].name)
		if len(resultList) == 0:
			print("Sorry! No results!")
			continue
		print("Choose a result by number, 'retry' or 'quit'.")
		# Print out results with number values
		i = 0
		for result in resultList:
			i += 1
			print(DISP, i, result[1].name, result[0].name,'(', ', '.join(result[0].tags), ')')

		while True:	
			entry = None
			choice = input(PROMPT)
			if choice == 'retry':
				break
			elif choice == 'quit':
				return (None, None)
			elif choice.isdigit() == True and 0 < int(choice) <= i:
				entry = resultList[i-1][0]
				db = resultList[i-1][1]
				break
			else:
				print("Sorry, that's not a valid option, try again")
				continue
		if entry is None:
			continue
		else:
			return (entry, db)

def main():
	"""Main command loop"""

	# Initialize: Attempt to load file, if none exists make a new one
	try:
		profile = loadFromFile(SAVE_LOCATION)
	except FileNotFoundError:
		try:
			profile = loadFromFile(SAVE_BACKUP)
			print("DB profile not found, loaded last backup.")
		except FileNotFoundError:
			print('No existing file found, creating new one')
			profile = Profile()
	saveToFile(profile, SAVE_BACKUP)

	commands = { 	"add":mainAdd,
					"search":mainSearch,
					#"save":mainSave,
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
			#Save after operations
			saveToFile(profile, SAVE_LOCATION)
		else:
			print("Sorry, don't recognize '%s', try again." %(userCommand))
	return

# # populate home db with some entries for testing
# basicTemplate = profile.templates['basic']
# testEntry1 = profile.databases['home'].entryFromTemplate('shopping list', basicTemplate)
# field = Field('note',Field.TYPE_TEXT)
# field.content = 'Buy milk, eggs, and bacon!'
# testEntry1.fields['note'] = field
# testEntry1.tags.add('shopping')
# testEntry1.tags.add('tuesday')
# testEntry1.tags.add('city')

# profile.databases['home'].entries['shopping list'] = testEntry1


main()
