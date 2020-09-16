# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 11:45:15 2020

@author: z003vrzk
"""

# Python imports
from pathlib import Path
import os, re

# Third party imports
from PyQt5.QtWidgets import (QMessageBox, QComboBox, QLineEdit, QDialog,
                             QFileDialog)
import pandas as pd

# Local imports
from Ui_ProductUpdateDialog import Ui_ProductUpdateDialog


#%%


class ProductUpdateDialog(QDialog, Ui_ProductUpdateDialog):

    def __init__(self, context):
        super(ProductUpdateDialog, self).__init__()

        # Context manager
        self.context = context

        # Set user interface from Designer
        self.setupUi(self)
        self.setWindowIcon(self.context.options_icon)
        self.setWindowTitle('Database Update')

        # Update ui with dynamic stuff
        self.init_ui()

        # Signals
        self.init_signals()

        return None

    def init_ui(self):
        """Generate the default view"""

        # Initialize user interface and check database settings
        self.database_options = self._check_db_options()

        return None

    def init_signals(self):
        """Connect signals to slots"""

        # Connect cancel button with close UI
        self.buttonBox.accepted.connect(self.close)
        self.buttonBox.rejected.connect(self.close)

        # Connect other buttons
        self.updateDBButton.clicked.connect(self.action_update_product_db)
        self.fileBrowseButton.clicked.connect(self.action_fileselect_excel_SOP)

        return None

    def action_update_product_db(self):
        # Check database configuration options
        self._check_db_options()

        # Check SOP File for correct format
        sop_path = self._check_sop_file_system()

        # Parse information in excel file and read to memory
        sop_dataframe = self._read_sop_file_contents(sop_path)

        # Connect to database

        # If parts are not in the product database then add them

        # If parts exist in database then update the price


        return None

    def _check_db_options(self):
        # Is the product database connected to SQL Server?
        #

        return None

    def action_fileselect_excel_SOP(self):
        """Open QFindDialog to find SQL database file or folder with SQL
        database file"""

        fileDialog = QFileDialog(self,
                                 'Select EXCEL SOP List',
                                 self.context.default_jobs_folder)
        fileDialog.setFileMode(QFileDialog.ExistingFile)
        fileDialog.setNameFilter("Excel Files (*.xlsx *.xls)")
        if fileDialog.exec_():
            file_paths = fileDialog.selectedFiles()
            sop_path = file_paths[0]

        if sop_path in [None, '']:
            # No database file is found in the selected directory
            msg=('The selected file is invalid : {}'.format(sop_path) +
                 '\nPlease choose a valid .xlsx or .xls file')
            self.action_user_message('Invalid File', msg)

        else:
            # Excel SOP file was found
            msg='The selected file is : {}'.format(sop_path.__str__())
            self.action_user_message('File Found', msg)

        # Change the displayed job file name
        self.partFileText.setText(sop_path.__str__())

        return sop_path

    def action_user_message(self, title, msg, detail=None):
        """Create a simple user message box"""
        msgBox = QMessageBox()
        msgBox.setWindowTitle(title)
        msgBox.setText(msg)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowIcon(self.context.alarm_icon)
        if detail:
            msgBox.setDetailedText(detail)
        msgBox.exec()
        return None

    def _read_sop_file_contents(self, sop_path):
        """
        inputs
        -------
        outputs
        -------"""
        # Read the SOP file into memory, into dataframe
        sop_dataframe = pd.read_excel(sop_path,
                                      sheet_name=0,
                                      header=0,
                                      index_co=None)

        # Rename all header column names to lowercase and trimmed
        sop_dataframe.rename(str.lower, axis='columns', inplace=True)
        sop_dataframe.rename(str.strip, axis='columns', inplace=True)

        # File must have the correct header data (cost and all that)
        headers = ['Manufacturer Part Number',
                   'Manufacturer Name',
                   'Material Number',
                   'Material Description',
                   'Siemens Net']
        headers = [header.lower() for header in headers]
        missing_headers = []
        for header in headers:
            # Each header must be present in the dataframe
            res = in_contains(header, sop_dataframe.columns)
            if not res:
                missing_headers.append(header)

        if len(missing_headers) > 0:
            msg=('The following headers were missing in the selected EXCEL' +
            ' file : {}'.format(missing_headers))
            self.action_user_message('Missing Header',msg)

        return sop_dataframe

    def _check_sop_file_system(self, sop_path):
        # File must be valid
        sop_path = Path(self.DBFileText.text)
        if not sop_path.is_file(sop_path):
            msg=('The selected file : {}\nIs invalid. Please select a valid' +
                 ' File System File')
            self.action_user_message('Invalid File', msg)

        # File must be EXCEL File
        root, ext = os.path.splittext(sop_path)
        if not ext in ['.xlsx','.xls']:
            msg=('The selected file {} is not a an EXCEL file with extension' +
                 '.xlsx or .xls\nPlease select a valid EXCEL file')
            self.action_user_message('Invalid file extension',msg)

        return sop_path

    def _update_db(self, product_df):
        """The product database mapping and EXCEL SOP file header mapping
        Format {'SOP EXCEL file header':'SQL Column Header'}"""
        mappings = {'Manufacturer Part Number':'PARTNO',
                    'Manufacturer Name':'MANUFACT',
                    'Siemens Net':'MATER_COST',
                    '':'OBSOLETE', # Don't update, 0
                    '':'ORD_TYPE', # Don't update, Null
                    'Material Description':'PROD_DESC2',
                    'Vendor name':'VENDOR',
                    '':'LAST_MOD', # Date, modify
                    'Material Number':'SBTPARTNO',
                    'Country of Origin':'COO',}
        return None

    def get_product_database_name(self):
        """Return the database name (not physical or logical) of the associated
        products database.
        The product database has the logical_name 'ProductDB'
        in SQL server express"""

        sql = """select t1.[name] as logical_name, t1.physical_name,
                    (select name
                    from [master].[sys].[databases] as t2
                    where t2.database_id = t1.database_id) as [database_name]
                FROM [master].[sys].[master_files] as t1
                where [name] = 'ProductDB'"""

        rows = self.context.SQLBase.execute_sql(sql)
        if len(rows) == 0:
            return None
        else:
            product_database_name = rows[0].database_name

        return product_database_name


def in_contains(check_value, linked_list):
    """Check if 'check_value' is contained in, or matches, at least
    one item in linked_list
    inputs
    -------
    check_value : (str) value to check exists in linked_list
    linked_list : (list) of strings"""

    for item in linked_list:
        if item.__contains__(check_value):
            # check_value is found in linked_list items
            return True
        else:
            continue

    # The check_value was not found in linked_list
    return False