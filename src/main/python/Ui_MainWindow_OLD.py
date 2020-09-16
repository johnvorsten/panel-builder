# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\z003vrzk\.spyder-py3\Scripts\Work\PanelBuilder\panel_builder_pyqt\src\main\ui designer\QMainWindow Main Window.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    
    def setupUi(self, MainWindow):
        
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(381, 325)
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        
        # This creates the menubar, and I can add menu's to this bar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 381, 21))
        self.menubar.setObjectName("menubar")
        
        # Create a menu
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        
        # Create a menu
        self.menuReports = QtWidgets.QMenu(self.menubar)
        self.menuReports.setObjectName("menuReports")
        
        # Create a menu
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        
        # This sets the menubar of the inheirited object
        MainWindow.setMenuBar(self.menubar)
        
        # I dont know what status bar is 
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        self.actionFind_Job = QtWidgets.QAction(MainWindow)
        self.actionFind_Job.setObjectName("actionFind_Job")
        
        self.actionOptions = QtWidgets.QAction(MainWindow)
        self.actionOptions.setObjectName("actionOptions")
        
        self.actionBOM = QtWidgets.QAction(MainWindow)
        self.actionBOM.setObjectName("actionBOM")
        
        self.actionReports = QtWidgets.QAction(MainWindow)
        self.actionReports.setObjectName("actionReports")
        
        self.menuFile.addAction(self.actionFind_Job)
        self.menuFile.addAction(self.actionOptions)
        self.menuReports.addAction(self.actionReports)
        self.menuView.addAction(self.actionBOM)
        
        # These add actions to the clickable button menus...
        # To add signal/slot I can 
        # a) get the associated action object by referencing self.actionFind_Job
        # b) add a signal with self.actionFind_Job.triggered.connect(lambda state, arg2 : self.class_method_slot(arg2)))
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuReports.menuAction())
        self.menubar.addAction(self.menuView.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuReports.setTitle(_translate("MainWindow", "Reports"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.actionFind_Job.setText(_translate("MainWindow", "Find Job"))
        self.actionOptions.setText(_translate("MainWindow", "Options"))
        self.actionBOM.setText(_translate("MainWindow", "Device Table"))
        self.actionReports.setText(_translate("MainWindow", "Open Reports"))

