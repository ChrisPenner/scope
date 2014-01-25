#scope...
class Profile(object):
    """High-level object containing all program data for a specific user"""
    def __init__(self):
        # databases contains all DBs for this user, init with Home and Work DBs
        self.databases = {Database('Home'), Database('Work')}
        # openDatabases is a set containing all DBs open for searching
        self.openDatabases = set()
        # templates is a library containing all defined templates by name
        self.templates = {}

class Database(object):
	"""High-level object containing one complete database"""
	def __init__(self, name):
		self.name = name
		self.tags = {}
		self.entries = set()

class Entry(object):
	"""Basic DB-entry class, typically based on a Template"""
	def __init__(self, name):
		self.name = name
		self.fields = {}
		self.tags = set()

class Field(object):
	"""Basic field class with a given field type"""
	def __init__(self, name, fieldType):
		self.name = name
		self.fieldType = fieldType
