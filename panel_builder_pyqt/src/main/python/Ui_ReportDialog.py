# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\z003vrzk\.spyder-py3\Scripts\Work\PanelBuilder\panel_builder_pyqt\src\main\ui designer\QDialog Report Group.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ReportDialog(object):
    def setupUi(self, ReportDialog):
        ReportDialog.setObjectName("ReportDialog")
        ReportDialog.resize(400, 300)
        ReportDialog.setMinimumSize(QtCore.QSize(400, 300))
        
        self.verticalLayoutWidget = QtWidgets.QWidget(ReportDialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(310, 10, 77, 81))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.topRightButtonsLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.topRightButtonsLayout.setContentsMargins(0, 0, 0, 0)
        self.topRightButtonsLayout.setObjectName("topRightButtonsLayout")
        self.generateReportButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.generateReportButton.sizePolicy().hasHeightForWidth())
        self.generateReportButton.setSizePolicy(sizePolicy)
        self.generateReportButton.setObjectName("generateReportButton")
        self.topRightButtonsLayout.addWidget(self.generateReportButton)
        self.cancelButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cancelButton.sizePolicy().hasHeightForWidth())
        self.cancelButton.setSizePolicy(sizePolicy)
        self.cancelButton.setObjectName("cancelButton")
        self.topRightButtonsLayout.addWidget(self.cancelButton)
        
        
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(ReportDialog)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(239, 210, 151, 80))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.retroSelectLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.retroSelectLayout.setContentsMargins(0, 0, 0, 0)
        self.retroSelectLayout.setObjectName("retroSelectLayout")
        self.ETRCheckBox = QtWidgets.QCheckBox(self.verticalLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ETRCheckBox.sizePolicy().hasHeightForWidth())
        self.ETRCheckBox.setSizePolicy(sizePolicy)
        self.ETRCheckBox.setObjectName("ETRCheckBox")
        self.retroSelectLayout.addWidget(self.ETRCheckBox)
        self.byothersCheckBox = QtWidgets.QCheckBox(self.verticalLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.byothersCheckBox.sizePolicy().hasHeightForWidth())
        self.byothersCheckBox.setSizePolicy(sizePolicy)
        self.byothersCheckBox.setObjectName("byothersCheckBox")
        self.retroSelectLayout.addWidget(self.byothersCheckBox)
        
        
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(ReportDialog)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(237, 130, 151, 78))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.systemRadioLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.systemRadioLayout.setContentsMargins(0, 0, 0, 0)
        self.systemRadioLayout.setObjectName("systemRadioLayout")
        self.allSystemsButton = QtWidgets.QRadioButton(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.allSystemsButton.sizePolicy().hasHeightForWidth())
        self.allSystemsButton.setSizePolicy(sizePolicy)
        self.allSystemsButton.setObjectName("allSystemsButton")
        self.systemRadioLayout.addWidget(self.allSystemsButton)
        self.selectSystemsButton = QtWidgets.QRadioButton(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.selectSystemsButton.sizePolicy().hasHeightForWidth())
        self.selectSystemsButton.setSizePolicy(sizePolicy)
        self.selectSystemsButton.setObjectName("selectSystemsButton")
        self.systemRadioLayout.addWidget(self.selectSystemsButton)
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(ReportDialog)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(10, 10, 221, 281))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.leftLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.leftLayout.setContentsMargins(0, 0, 0, 0)
        self.leftLayout.setObjectName("leftLayout")
        self.reportSelectLayout = QtWidgets.QHBoxLayout()
        self.reportSelectLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.reportSelectLayout.setSpacing(6)
        self.reportSelectLayout.setObjectName("reportSelectLayout")
        self.reportTypeLabel = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.reportTypeLabel.sizePolicy().hasHeightForWidth())
        self.reportTypeLabel.setSizePolicy(sizePolicy)
        self.reportTypeLabel.setObjectName("reportTypeLabel")
        self.reportSelectLayout.addWidget(self.reportTypeLabel)
        self.reportTypeComboBox = QtWidgets.QComboBox(self.verticalLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.reportTypeComboBox.sizePolicy().hasHeightForWidth())
        self.reportTypeComboBox.setSizePolicy(sizePolicy)
        self.reportTypeComboBox.setCurrentText("")
        self.reportTypeComboBox.setObjectName("reportTypeComboBox")
        self.reportSelectLayout.addWidget(self.reportTypeComboBox)
        self.reportSelectLayout.setStretch(0, 1)
        self.reportSelectLayout.setStretch(1, 1)
        self.leftLayout.addLayout(self.reportSelectLayout)
        
        # GROUP BOX is inside verticalLayoutWidget_4...
        self.systemGroupBox = QtWidgets.QGroupBox(self.verticalLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.systemGroupBox.sizePolicy().hasHeightForWidth())
        self.systemGroupBox.setSizePolicy(sizePolicy)
        self.systemGroupBox.setObjectName("systemGroupBox")
        
        # SCROLL AREA is inside of verticalLayoutWidget_5...
        self.verticalLayoutWidget_5 = QtWidgets.QWidget(self.systemGroupBox)
        # self.verticalLayoutWidget_5.setGeometry(QtCore.QRect(10, 20, 200, 220))
        self.verticalLayoutWidget_5.setObjectName("verticalLayoutWidget_5")
        self.systemLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_5)
        self.systemLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.systemLayout.setContentsMargins(1, 1, 1, 1)
        self.systemLayout.setObjectName("systemLayout")
        
        
        self.scrollArea = QtWidgets.QScrollArea(self.verticalLayoutWidget_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 197, 217))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.systemLayout.addWidget(self.scrollArea)
        self.leftLayout.addWidget(self.systemGroupBox)
        self.leftLayout.setStretch(0, 1)
        self.leftLayout.setStretch(1, 10)
        self.reportTypeLabel.setBuddy(self.reportTypeComboBox)

        self.retranslateUi(ReportDialog)
        QtCore.QMetaObject.connectSlotsByName(ReportDialog)

    def retranslateUi(self, ReportDialog):
        _translate = QtCore.QCoreApplication.translate
        ReportDialog.setWindowTitle(_translate("ReportDialog", "Dialog"))
        self.generateReportButton.setText(_translate("ReportDialog", "Generate"))
        self.cancelButton.setText(_translate("ReportDialog", "Cancel"))
        self.ETRCheckBox.setText(_translate("ReportDialog", "Include ETR (+)"))
        self.byothersCheckBox.setText(_translate("ReportDialog", "Include By Others (*)"))
        self.allSystemsButton.setText(_translate("ReportDialog", "All Systems"))
        self.selectSystemsButton.setText(_translate("ReportDialog", "Select Systems"))
        self.reportTypeLabel.setText(_translate("ReportDialog", "Report Type"))
        self.systemGroupBox.setTitle(_translate("ReportDialog", "All Systems"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ReportDialog = QtWidgets.QDialog()
    ui = Ui_ReportDialog()
    ui.setupUi(ReportDialog)
    ReportDialog.show()
    sys.exit(app.exec_())

