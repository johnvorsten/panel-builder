# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\z003vrzk\.spyder-py3\Scripts\Work\PanelBuilder\panel_builder_pyqt\src\main\ui designer\QDialog Main View.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

# from QtCore.Qt import AlignVCenter

class Ui_MainWindowDialog(object):

    def setupUi(self, Dialog):

        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)

        self.horizontalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.CurrentJobLabel = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.CurrentJobLabel.setObjectName("CurrentJobLabel")
        self.horizontalLayout.addWidget(self.CurrentJobLabel)

        self.lineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit.setObjectName("JobPathTextEdit")
        self.horizontalLayout.addWidget(self.lineEdit)

        self.pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)

        # Set the layout and add custom formatting
        self.horizontalLayout.setAlignment(QtCore.Qt.AlignTop)
        Dialog.setLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.CurrentJobLabel.setText(_translate("Dialog", "Current Job"))
        self.pushButton.setText(_translate("Dialog", "Select Job"))

