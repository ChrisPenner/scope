#!/usr/bin/python3
import pickle
from copy import deepcopy


# Constants --------------
class CONST(object):
    SAVE_LOCATION = 'save.pkl'
    SAVE_BACKUP = 'save.pkl.bak'


class Profile(object):
    """High-level object containing all program data for a specific user"""
    def __init__(self):
        # templates is a library containing all defined templates by name
        self.templates = {
            'basic': Template(
                'basic', {'note': Field('note', Field.TYPE_TEXT)}, set())}
        # databases contains all DBs for this user, init with Home and Work DBs
        self.databases = {
            'home': Database('home', self.templates),
            'work': Database('work', self.templates),
            }
        # openDatabases is a set containing all DBs open for searching
        self.openDatabases = set(self.databases.values())
        return

    # High Level Functions:
    def createDB(self, name):
        """Creates a new db with 'name'"""
        db = Database(name, self.templates)
        self.databases[name] = db
        self.openDatabases.add(db)
        return

    def getDatabases(self):
        return self.databases

    def getMatchingEntries(self, matchDBs, matchTags):
        entries = set()
        for db in matchDBs:
            if db in self.databases:
                db = self.databases[db]
                for tag in matchTags:
                    if tag in db.tags:
                        for entry in db.tags[tag]:
                            entries.add(db.entries[entry])
        return entries

    def querySearch(self, query):
        # split query into word list by spaces
        queries = query.lstrip(' ').rstrip(' ').split(' ')
        # iterate through entries in all databases and search titles
        # adding matches to a set
        results = set()
        for db in self.openDatabases:
            if len(db.entries) > 0:
                for entryName in db.entries:
                    for word in queries:
                        if word in entryName or entryName in word:
                            # Add entry in a tuple with db (db, entry)
                            results.add((db.entries[entryName], db))
                for tag in db.tags:
                    if word in tag or tag in word:
                        for entryName in db.tags[tag]:
                            results.add((db.entries[entryName], db))
        return results

    def save(self, dest):
        f = open(dest, 'wb')
        pickle.dump(self, f)
        f.close()
        return


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
        # tags is a library of tagnames keyed to sets
        # containing entry titles with those tags
        self.tags = {}
        # Entries keyed by name
        self.entries = {}
        #templates is a REFERENCE to the 'profile' templates library
        self.templates = templates
        return

    def addEntry(self, entry):
        self.crossRefTags(entry)
        self.entries[entry.name] = entry

    def deleteEntry(self, entry):
        for tag in entry.tags:
            self.tags[tag].remove(entry.name)
        self.entries.pop(entry.name)
        return

    def crossRefTags(self, entry):
        """Adds cross Reference to Entry in DB tag bank (for easy searching)"""
        # Check if each tag exists, if it does,
        # add an entry, otherwise key it to a set.
        for tag in entry.tags:
            if tag in self.tags:
                self.tags[tag].add(entry.name)
            else:
                self.tags[tag] = set([entry.name])
        return

    def entryFromTemplate(self, name, template):
        """Creates an entry instance from a given entry 'template' object"""
        entry = Entry(name, template.templateName)
        # Deepcopy template attributes as new objects
        entry.fields = deepcopy(template.fields)
        entry.tags = deepcopy(template.tags)
        return entry


class Entry(object):
    """Basic DB-entry class, typically based on a Template"""
    def __init__(self, name, entryType):
        self.name = name
        self.fields = {}
        self.entryType = entryType
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
    """
    Consists of a list of fields and tags that
    are associated with a given template
    """

    def __init__(self, templateName, fields, tags):
        self.templateName = templateName
        # Deepcopy from input fields
        self.fields = deepcopy(fields.copy())
        self.tags = deepcopy(tags.copy())
        return


def loadProfile():
# Attempt to load profile, if none exists make a new one
    try:
        profile = load(CONST.SAVE_LOCATION)
    except IOError:
        try:
            profile = load(CONST.SAVE_BACKUP)
            print("DB profile not found, loaded last backup.")
        except IOError:
            print('No existing file found, creating new one')
            profile = Profile()
    return profile


def load(dest):
    f = open(dest, 'rb')
    obj = pickle.load(f)
    f.close()
    return obj
