# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_ProductUpdateDialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ProductUpdateDialog(object):
    def setupUi(self, ProductUpdateDialog):
        ProductUpdateDialog.setObjectName("ProductUpdateDialog")
        ProductUpdateDialog.setEnabled(True)
        ProductUpdateDialog.resize(400, 200)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ProductUpdateDialog.sizePolicy().hasHeightForWidth())
        ProductUpdateDialog.setSizePolicy(sizePolicy)
        ProductUpdateDialog.setMinimumSize(QtCore.QSize(400, 200))
        ProductUpdateDialog.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        ProductUpdateDialog.setSizeGripEnabled(False)
        self.verticalLayout = QtWidgets.QVBoxLayout(ProductUpdateDialog)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout.setObjectName("formLayout")
        self.DBNameLabel = QtWidgets.QLabel(ProductUpdateDialog)
        self.DBNameLabel.setObjectName("DBNameLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.DBNameLabel)
        self.DBFileText = QtWidgets.QLineEdit(ProductUpdateDialog)
        self.DBFileText.setObjectName("DBFileText")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.DBFileText)
        self.partFileLabel = QtWidgets.QLabel(ProductUpdateDialog)
        self.partFileLabel.setObjectName("partFileLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.partFileLabel)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.partFileText = QtWidgets.QLineEdit(ProductUpdateDialog)
        self.partFileText.setEnabled(False)
        self.partFileText.setObjectName("partFileText")
        self.horizontalLayout_2.addWidget(self.partFileText)
        self.fileBrowseButton = QtWidgets.QToolButton(ProductUpdateDialog)
        self.fileBrowseButton.setObjectName("fileBrowseButton")
        self.horizontalLayout_2.addWidget(self.fileBrowseButton)
        self.formLayout.setLayout(1, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.verticalLayout.addLayout(self.formLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.updateDBButton = QtWidgets.QPushButton(ProductUpdateDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.updateDBButton.sizePolicy().hasHeightForWidth())
        self.updateDBButton.setSizePolicy(sizePolicy)
        self.updateDBButton.setObjectName("updateDBButton")
        self.horizontalLayout.addWidget(self.updateDBButton, 0, QtCore.Qt.AlignRight)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(ProductUpdateDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(ProductUpdateDialog)
        self.buttonBox.accepted.connect(ProductUpdateDialog.accept)
        self.buttonBox.rejected.connect(ProductUpdateDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ProductUpdateDialog)

    def retranslateUi(self, ProductUpdateDialog):
        _translate = QtCore.QCoreApplication.translate
        ProductUpdateDialog.setWindowTitle(_translate("ProductUpdateDialog", "Options"))
        self.DBNameLabel.setText(_translate("ProductUpdateDialog", "Products Database File"))
        self.DBFileText.setText(_translate("ProductUpdateDialog", "ProductDB.mdf"))
        self.partFileLabel.setText(_translate("ProductUpdateDialog", "SOP Parts EXCEL File"))
        self.fileBrowseButton.setText(_translate("ProductUpdateDialog", "..."))
        self.updateDBButton.setText(_translate("ProductUpdateDialog", "Update Database"))

