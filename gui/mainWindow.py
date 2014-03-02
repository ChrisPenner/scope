# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './gui/mainWindow.ui'
#
# Created: Sun Mar  2 14:46:58 2014
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(857, 610)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.widget_2 = QtGui.QWidget(self.centralwidget)
        self.widget_2.setEnabled(True)
        self.widget_2.setMaximumSize(QtCore.QSize(300, 16777215))
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.label_2 = QtGui.QLabel(self.widget_2)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_3.addWidget(self.label_2)
        self.listDB = QtGui.QListWidget(self.widget_2)
        self.listDB.setObjectName(_fromUtf8("listDB"))
        self.verticalLayout_3.addWidget(self.listDB)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label_3 = QtGui.QLabel(self.widget_2)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_2.addWidget(self.label_3)
        self.listTags = QtGui.QListWidget(self.widget_2)
        self.listTags.setObjectName(_fromUtf8("listTags"))
        self.verticalLayout_2.addWidget(self.listTags)
        self.label = QtGui.QLabel(self.widget_2)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setIndent(0)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_2.addWidget(self.label)
        self.textTagSelector = QtGui.QLineEdit(self.widget_2)
        self.textTagSelector.setObjectName(_fromUtf8("textTagSelector"))
        self.verticalLayout_2.addWidget(self.textTagSelector)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_3.addWidget(self.widget_2)
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.tableResult = QtGui.QTableWidget(self.centralwidget)
        self.tableResult.setObjectName(_fromUtf8("tableResult"))
        self.tableResult.setColumnCount(0)
        self.tableResult.setRowCount(0)
        self.verticalLayout_5.addWidget(self.tableResult)
        self.btnEditEntry = QtGui.QPushButton(self.centralwidget)
        self.btnEditEntry.setObjectName(_fromUtf8("btnEditEntry"))
        self.verticalLayout_5.addWidget(self.btnEditEntry)
        self.horizontalLayout_3.addLayout(self.verticalLayout_5)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 857, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label_2.setText(_translate("MainWindow", "Select Databases", None))
        self.label_3.setText(_translate("MainWindow", "Choose Tags", None))
        self.label.setText(_translate("MainWindow", "Search for Tags:", None))
        self.btnEditEntry.setText(_translate("MainWindow", "Edit Entry", None))

