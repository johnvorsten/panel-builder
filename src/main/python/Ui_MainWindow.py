# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_MainWindow.ui'
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
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 381, 21))
        self.menubar.setObjectName("menubar")
        self.menuPanelBuilder = QtWidgets.QMenu(self.menubar)
        self.menuPanelBuilder.setObjectName("menuPanelBuilder")
        self.menuReports = QtWidgets.QMenu(self.menubar)
        self.menuReports.setObjectName("menuReports")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionFind_Job = QtWidgets.QAction(MainWindow)
        self.actionFind_Job.setObjectName("actionFind_Job")
        self.actionOptions = QtWidgets.QAction(MainWindow)
        self.actionOptions.setObjectName("actionOptions")
        self.actionBOM = QtWidgets.QAction(MainWindow)
        self.actionBOM.setObjectName("actionBOM")
        self.actionUpdate_Product_DB = QtWidgets.QAction(MainWindow)
        self.actionUpdate_Product_DB.setStatusTip("")
        self.actionUpdate_Product_DB.setWhatsThis("")
        self.actionUpdate_Product_DB.setShortcut("")
        self.actionUpdate_Product_DB.setObjectName("actionUpdate_Product_DB")
        self.actionOpen_Reports = QtWidgets.QAction(MainWindow)
        self.actionOpen_Reports.setObjectName("actionOpen_Reports")
        self.menuPanelBuilder.addAction(self.actionFind_Job)
        self.menuPanelBuilder.addAction(self.actionOptions)
        self.menuPanelBuilder.addAction(self.actionUpdate_Product_DB)
        self.menuReports.addAction(self.actionOpen_Reports)
        self.menuView.addAction(self.actionBOM)
        self.menubar.addAction(self.menuPanelBuilder.menuAction())
        self.menubar.addAction(self.menuReports.menuAction())
        self.menubar.addAction(self.menuView.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuPanelBuilder.setTitle(_translate("MainWindow", "File"))
        self.menuReports.setTitle(_translate("MainWindow", "Reports"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.actionFind_Job.setText(_translate("MainWindow", "Find Job"))
        self.actionOptions.setText(_translate("MainWindow", "Options"))
        self.actionBOM.setText(_translate("MainWindow", "Device Table"))
        self.actionUpdate_Product_DB.setText(_translate("MainWindow", "Update Product DB"))
        self.actionUpdate_Product_DB.setIconText(_translate("MainWindow", "Update Product DB"))
        self.actionUpdate_Product_DB.setToolTip(_translate("MainWindow", "Update Product DB"))
        self.actionOpen_Reports.setText(_translate("MainWindow", "Open Reports"))

