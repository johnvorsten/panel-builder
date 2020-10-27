# -*- coding: utf-8 -*-

"""
Created on Wed Jun 17 15:36:15 2020

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
from ProductUpdateDialog import ProductUpdateDialog
from main import AppContext


#%%

context = AppContext()
widget = ProductUpdateDialog(context)

class ProductUpdateTest(unittest.TestCase):

    def setUp(self):

        # Find the correct product database. If the product database does
        # Not exist then raise a message to the user
        path_mdf, path_ldf, database_name = widget.get_product_database_name()

        return None

    def test_get_product_database_name(self):
        # Find the correct product database. If the product database does
        # Not exist then raise a message to the user
        path_mdf, path_ldf, database_name = widget.get_product_database_name()
        test_mdf = r"C:\Program Files\DesignTool\Products\ProductDB.mdf"
        test_ldf = r"C:\Program Files\DesignTool\Products\ProductDB_log.ldf"
        test_name = "ProductDB"
        self.assertEqual(path_mdf, test_mdf)
        self.assertEqual(path_ldf, test_ldf)
        self.assertEqual(database_name, test_name)
        return None

    @patch('__main__.widget')
    def test__check_sop_file_system(self, mockDialog):

        # Check SOP File for correct format
        test_path = r"C:\path\to\fake\file.xlsx"
        QtCore.QTimer.singleShot(500, mockDialog.IOErrMsgBox.accept)
        mockDialog.partFileText.setText(sop_path)
        sop_path = mockDialog._validate_sop_file()

        # A dialog box should open
        # TODO How to assert that a dialog is opened
        print(type(mockDialog.IoErrMsgBox))
        print(isinstance(mockDialog.IOErrMsgBox, QMessageBox))
        print(mockDialog.IOErrMsgBox.called)

        # Assert that sop_path is None
        self.assertEqual(sop_path, None)

        # Test a valid file
        test_path = r"C:\Users\z003vrzk\.spyder-py3\Scripts\Work\panel_builder\data\SOP-2020-7-31.xlsx"
        QtCore.QTimer.singleShot(500, mockDialog.IOErrMsgBox.accept)
        mockDialog.partFileText.setText(test_path)
        sop_path = mockDialog._validate_sop_file()
        self.assertEqual(sop_path, test_path)

        # Test a real file with the wrong extension
        test_path = r"C:\ProgramData"
        QtCore.QTimer.singleShot(500, mockDialog.IOErrMsgBox.accept)
        mockDialog.partFileText.setText(test_path)
        sop_path = mockDialog._validate_sop_file()
        self.assertEqual(sop_path, None)

        return None

    def test__add_parts(self):
        return None

    def test__update_price(self):
        return None

    def test_action_fileselect_excel_SOP(self):

        # Non-existant file
        test_path = r"C:\path\to\fake\file.xlsx"
        widget.action_fileselect_excel_SOP()
        QtCore.QTimer.singleShot(500, widget.fileDialog.)

        # Test a valid file
        test_path = r"C:\Users\z003vrzk\.spyder-py3\Scripts\Work\panel_builder\data\SOP-2020-7-31.xlsx"
        # Test a real file with the wrong extension
        test_path = r"C:\ProgramData"

        # Schedule a timer to select a file


        return None

    def test__read_sop_file_contents(self):
        return None

    def test__add_parts(self):
        return None

    def test__update_price(self):
        return None

    def test_(self):
        return None



if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ProductUpdateTest)
    unittest.TextTestRunner(verbosity=2).run(suite)


#%%

if __name__ == '__main__':
    context = AppContext()
    widget = ProductUpdateDialog(context)

    # Find the correct product database. If the product database does
    # Not exist then raise a message to the user
    path_mdf, path_ldf, database_name = widget.get_product_database_name()

    # Check SOP File for correct format
    sop_path = r"C:\Users\z003vrzk\.spyder-py3\Scripts\Work\panel_builder\data\SOP-2020-7-31.xlsx"
    widget.partFileText.setText(sop_path)
    sop_path = widget._check_sop_file_system()

    # Parse information in excel file and read to memory
    sop_dataframe = widget._read_sop_file_contents(sop_path)

    # Connect to database
    widget.context.init_sql_database_connection(path_mdf, path_ldf, database_name)

    # If parts are not in the product database then add them
    widget._add_parts(sop_dataframe) # TODO

    # If parts exist in database then update the price
    widget._update_price(sop_dataframe) # TODO




#%%