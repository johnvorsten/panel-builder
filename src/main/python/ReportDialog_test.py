# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 11:14:27 2020

@author: z003vrzk
"""
# Python imports
import unittest
from unittest.mock import patch

# Third party imports
from PyQt5.QtWidgets import (QMainWindow, QApplication, QDialog, QFileDialog,
                             QMessageBox, QLineEdit, QCheckBox,
                             QVBoxLayout)
from PyQt5.QtTest import QTest
from PyQt5 import QtCore

# Local imports
from ReportDialog import ReportDialog
from main import AppContext

#%%

def TestReportDialog(unittest.testcase):

    def test_(self):
        return


_close_application
# _init_systems_scroll # Dont test
# _get_retro_flags
# _get_selected_BOM_systems
_get_report_style
# get_unique_systems
# get_product_database_name
_generate_report



if __name__ == '__main__':
    # Initialization
    context = AppContext()
    dialog = QDialog()
    server_name = '.\DT_SQLEXPRESS'
    driver_name = 'SQL Server Native Client 11.0'
    database_name = 'PBJobDB_test'
    product_db = 'ProductDB'
    path_mdf = r"C:\Users\z003vrzk\.spyder-py3\Scripts\Work\panel_builder\SQLTest\JHW\JobDB.mdf"
    path_ldf = r"C:\Users\z003vrzk\.spyder-py3\Scripts\Work\panel_builder\SQLTest\JHW\JobDB_Log.ldf"
    path_j_vars = r"C:\Users\z003vrzk\.spyder-py3\Scripts\Work\panel_builder\SQLTest\JHW\j_vars.ini"
    context.path_mdf = path_mdf
    context.path_ldf = path_ldf
    context.path_j_vars = path_j_vars
    widget = ReportDialog(context)
    # widget.exec() # Show dialog

    # Find the correct product database. If the product database does
    # Not exist then raise a message to the user
    test_name = widget.get_product_database_name()

    # Unique systems
    unique_systems = widget.get_unique_systems(database_name)

    # Initialize UI
    widget._init_systems_scroll()

    # Make sure only the selected systems are represented
    widget.selectSystemsButton.setChecked(True)
    widget.selectSystemsButton.isChecked() # True
    widget.allSystemsButton.isChecked() # False
    checkboxes = []
    checkboxes.append(widget.systemCheckLayoutArea.itemAt(0).widget())
    checkboxes.append(widget.systemCheckLayoutArea.itemAt(2).widget())
    print("Selected {}, {}".format(checkboxes[0].objectName(),
                                   checkboxes[1].objectName()))

    # Check which systems were selected
    res = widget._get_selected_BOM_systems()
    for i in range(len(res)):
        assert(res[i] == checkboxes[i].objectName())

    widget._get_retro_flags
    widget._get_report_style


# Testing...
#%%
# Layout to display unique systems on
widget.systemCheckLayoutArea = QVBoxLayout(widget.scrollAreaWidgetContents)

# Add all systems to layout
for str_system in unique_systems:
    systemCheckBox = QCheckBox(str_system)
    systemCheckBox.setObjectName(str_system)
    widget.systemCheckLayoutArea.addWidget(systemCheckBox)

widget.systemCheckLayoutArea.addStretch(1)
widget.scrollArea.setWidgetResizable(True)

# Set the GROUP BOX'S LAYOUT to self.systemLayout!!
widget.systemGroupBox.setLayout(widget.systemLayout)

#%%

selected_systems = []
a = []
for i in range(widget.systemCheckLayoutArea.count()):
    res = widget.systemCheckLayoutArea.itemAt(i).widget()
    a.append(res)
    if isinstance(res, QCheckBox) and res.isChecked():
        selected_systems.append(res.objectName)


selected_systems = []
a = []
for i in range(widget.scrollAreaWidgetContents.count()):
    res = widget.scrollAreaWidgetContents.itemAt(i)
    a.append(res)
    if isinstance(res, QCheckBox) and res.isChecked():
        selected_systems.append(res.objectName)
