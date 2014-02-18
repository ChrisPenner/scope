#!/usr/bin/python3
#scope...in python 3.3
import pickle
import core
#import gui_scope.py

# Constants
class CONST(object):
    DISP = '~ ' # Prompt used to display lists
    PROMPT = '> ' # Prompt used for user input
    SEPARATOR = '-------------------------------------'



# Main loop functions
def mainAdd(profile):
    """selects database, then adds a new entry to it"""
    db = selectDatabase(profile)
    entry = createEntry(profile, db)
    db.addEntry(entry)
    return

def mainSearch(profile):
    result = search(profile)
    if result != None:
        (entry, db) = result
        printEntry(entry)
        editEntry(profile, entry, db)
    return

def search(profile):
    while True:
        print("Please enter a search term or tag, 'quit' to exit.")
        query = input(CONST.PROMPT)
        if query == 'quit':
            return None 
        results = profile.querySearch(query)
        
        if len(results) == 0:
            print("Sorry! No results!")
            continue
        # Change set to an indexable list
        resultList = [x for x in results]
        resultList.sort(key=lambda x: x[1].name)

        print("Choose a result by number, 'retry' or 'quit'.")
        # Print out results with number values
        i = 0
        for result in resultList:
            i += 1
            print(CONST.DISP, i, result[1].name, result[0].name,'(', ', '.join(result[0].tags), ')')

        while True: 
            entry = None
            choice = input(CONST.PROMPT)
            if choice == 'retry':
                break
            elif choice == 'quit':
                return None 
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

def mainSave(profile):
    saveToFile(profile, SAVE_LOCATION)
    return

def editEntry(profile, entry, db):
    """Edit or delete database entry"""
    print("'edit', 'delete', 'tags' or 'main'?")
    userChoice = input(CONST.PROMPT).lower()
    if userChoice == 'delete':
        oldName = entry.name
        db.deleteEntry(entry)
        print(oldName, "has been deleted; 'undo' or 'main'.")
    return  

def createEntry(profile, db):
    """Adds one entry to this database"""
    print("Which template would you like to use?")
    while True:
        for t in sorted(db.templates):
            print(CONST.DISP, t)
        templateChoice = input(CONST.PROMPT).lower()
        if templateChoice not in db.templates:
            print("Sorry, don't recognize '%s', try again." %(templateChoice))
            continue
        else:
            break
    print("Please enter the following information: ")
    title = input(CONST.PROMPT + "Title: ")
    entry = db.entryFromTemplate(title,db.templates[templateChoice])
    for field in entry.fields:
        entry.fields[field].content = input(CONST.PROMPT + field + ': ')
    # Get newTags from formatTags as a set
    newTags = core.Utils.formatTags(input("Tags (Comma Separated): ").lower())
    entry.tags = entry.tags.union(newTags)
    return entry

def printEntry(entry):
    print(CONST.SEPARATOR)
    print("Title: ", entry.name)
    for field in entry.fields:
        print (field, ": ", entry.fields[field].content)
    print(CONST.SEPARATOR)
    return

def selectDatabase(profile):
    """Generic selection function, returns a db object for another function to use."""
    print("Which Database would you like to use?")
    potentialDB = None
    while True: #loop until valid input
    # Print all databases
        for name in sorted(profile.databases):
            print(CONST.DISP + name)
        # Collect user input
        workingDB = input(CONST.PROMPT).lower()
        # Check Validity
        if (workingDB  == 'create') and (potentialDB is not None):
            profile.createDB(potentialDB)
            workingDB = potentialDB
            break
        elif workingDB not in profile.databases:
            print(workingDB + " is not a database, type 'create' to create it, or try again")
            # Set name to potentialDB in case it is to be created.
            potentialDB = workingDB 
            continue
        else:
            break
    print("Okay, working on '" + workingDB + "'")
    return profile.databases[workingDB]


def main():
    """Main command loop"""
    
    profile = core.loadProfile()
    commands = {    "add":mainAdd,
                    "search":mainSearch,
                    #"save":mainSave,
                    # "open":profile.openDB,
                    # "close":profile.closeDB,
                    # "template":profile.template,
                }

    while True:
        print("Please choose a command from the list: ")
        for command in commands:
            print(CONST.DISP + command)
        print(CONST.DISP + 'quit')
        userCommand = input(CONST.PROMPT).lower()
        if userCommand == 'quit' or userCommand == 'exit':
            profile.save(core.CONST.SAVE_BACKUP)
            break
        if userCommand in commands:
            commands[userCommand](profile)
            #Save after operations
            profile.save(core.CONST.SAVE_LOCATION)
        else:
            print("Sorry, don't recognize '%s', try again." %(userCommand))
    return

# Run Program if started directly
if __name__ == "__main__":
    main()