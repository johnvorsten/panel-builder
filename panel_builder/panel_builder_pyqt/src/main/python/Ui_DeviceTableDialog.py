# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\z003vrzk\.spyder-py3\Scripts\Work\PanelBuilder\panel-builder\panel_builder_pyqt\src\main\ui designer\QDialog Device Table.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DeviceTableDialog(object):
    def setupUi(self, DeviceTableDialog):
        DeviceTableDialog.setObjectName("DeviceTableDialog")
        DeviceTableDialog.resize(413, 431)
        DeviceTableDialog.setMinimumSize(QtCore.QSize(250, 250))
        DeviceTableDialog.setSizeGripEnabled(True)
        DeviceTableDialog.setModal(True)
        self.gridLayout_2 = QtWidgets.QGridLayout(DeviceTableDialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.DeviceTableGroupBox = QtWidgets.QGroupBox(DeviceTableDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.DeviceTableGroupBox.sizePolicy().hasHeightForWidth())
        self.DeviceTableGroupBox.setSizePolicy(sizePolicy)
        self.DeviceTableGroupBox.setToolTip("")
        self.DeviceTableGroupBox.setObjectName("DeviceTableGroupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.DeviceTableGroupBox)
        self.gridLayout.setVerticalSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.DeviceTableView = QtWidgets.QTableView(self.DeviceTableGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.DeviceTableView.sizePolicy().hasHeightForWidth())
        self.DeviceTableView.setSizePolicy(sizePolicy)
        self.DeviceTableView.setMinimumSize(QtCore.QSize(250, 250))
        self.DeviceTableView.setObjectName("DeviceTableView")
        self.gridLayout.addWidget(self.DeviceTableView, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.DeviceTableGroupBox, 0, 0, 1, 1)

        self.retranslateUi(DeviceTableDialog)
        QtCore.QMetaObject.connectSlotsByName(DeviceTableDialog)

    def retranslateUi(self, DeviceTableDialog):
        _translate = QtCore.QCoreApplication.translate
        DeviceTableDialog.setWindowTitle(_translate("DeviceTableDialog", "Device Table"))
        self.DeviceTableGroupBox.setTitle(_translate("DeviceTableDialog", "Device Table"))

