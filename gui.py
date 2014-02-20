import sys
import PyQt4
from PyQt4 import QtGui 
from gui import mainWindow
import core

def main():
	profile = initCore()

	app = QtGui.QApplication(sys.argv)
	mw = QtGui.QMainWindow()
	ui = mainWindow.Ui_MainWindow()
	ui.setupUi(mw)

	mwHandler = mainWindowHandler(mw, ui, profile)

	mwHandler.initMainWindow()

	mw.show()
	sys.exit(app.exec_())

def initCore():
	profile = core.loadProfile()
	return profile

class mainWindowHandler(object):
	"""docstring for mainWindowHandler"""
	def __init__(self, mainWindow, ui, profile):
		super(mainWindowHandler, self).__init__()
		
		self.mw = mainWindow
		self.ui = ui
		self.profile = profile
		self.databases = profile.databases
		self.liDB = ListInter(ui.listDB)
		self.liTags = ListInter(ui.listTags)
		self.tabResult = TableInter(ui.tableResult, 0, 0)


	def initMainWindow(self):
		# Allow multi selections on selectors
		self.ui.listDB.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
		self.ui.listTags.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)

		# populate DB list
		self.liDB.addItems(self.profile.databases)

		# When DB choices are changed, repopulate tags list
		self.liDB.qtList.itemSelectionChanged.connect(self.liDB.selectionChanged)
		self.liDB.qtList.itemSelectionChanged.connect(self.setTags)

		# Keep track of tags selection to allow tag selection persistence
		self.liTags.qtList.itemClicked.connect(self.liTags.selectionChanged)

		# self.tabResult.qtList.




	def setTags(self):
		#print(self.mw.sender().objectName())
		self.liTags.clear()
		databases = [x.text() for x in self.liDB.qtList.selectedItems()]
		for db in databases:
			self.liTags.addItems(self.databases[db].tags)
			self.liTags.setSelection()

class ListInter(object):
	"""docstring for ListInter"""
	def __init__(self, qtList):
		super(ListInter, self).__init__()
		self.qtList = qtList
		self.items = set()
		self.selected = set()

	def getSelected(self):
		return [x.text() for x in self.qtList.selectedItems()]

	def selectionChanged(self):
		length = self.qtList.count()
		for i in range(0,length):
			item = self.qtList.item(i)
			if item.isSelected():
				self.selected.add(item.text())
			elif item.text() in self.selected:
				self.selected.remove(item.text())

	def setSelection(self):
		length = self.qtList.count()
		for i in range(0,length):
			item = self.qtList.item(i)
			if item.text() in self.selected:
				item.setSelected(True)
			else:
				item.setSelected(False)

	def addItems(self, items):
		for item in items:
			if item not in self.items:
				self.items.add(item)
				self.qtList.addItem(item)

	def removeItems(self, items):
		for item in items:
			if item in self.items:
				self.items.remove(item)
				self.qtList.removeItemWidget(QtGui.QListWidgetItem(item))

	def clear(self):
		# remove all elements from list
		while(True):
			elem = self.qtList.takeItem(0)
			if elem == None:
				break
		# Mirror set with list		
		self.items.clear()


class TableInter(object):
	def __init__(self, qtList, rows, columns):
		super(TableInter, self).__init__()
		self.qtList = qtList

		self.qtList.setRowCount(rows)
		self.qtList.setColumnCount(columns)

		

def addListeners(ui):
	ui.btnEditEntry.clicked.connect(showStatus)

def showStatus():
	window.statusBar().showMessage(window.sender().objectName())

if __name__ == '__main__':
	main()
