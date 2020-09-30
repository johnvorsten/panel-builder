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
from PyQt5.QtCore import pyqtSlot, pyqtSignal
import pandas as pd

# Local imports
from Ui_ProductUpdateDialog import Ui_ProductUpdateDialog


#%%


class ProductUpdateDialog(QDialog, Ui_ProductUpdateDialog):
    # Define signals
    _fileselect_excel_signal = pyqtSignal([]) #
    update_product_db_signal = pyqtSignal([]) #
    _user_message_signal = pyqtSignal([str, str], [str,str,str]) #
    _read_sop_file_signal = pyqtSignal([str]) #
    _validate_sop_file_signal = pyqtSignal([str])#
    get_product_database_name_signal = pyqtSignal([]) #
    _update_price_signal = pyqtSignal([pd.DataFrame]) #
    _add_parts_signal = pyqtSignal([pd.DataFrame]) #

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

        # Initialize user interface with contextual or dynamic stuff
        # Nothing to do for this class

        return None

    def init_signals(self):
        """Connect signals to slots"""

        # Connect cancel button with close UI
        self.buttonBox.accepted.connect(self.close)
        self.buttonBox.rejected.connect(self.close)

        # Connect other buttons
        self.updateDBButton.clicked.connect(self.action_update_product_db)
        self.fileBrowseButton.clicked.connect(self.action_fileselect_excel_SOP)

        # All class signals
        self._fileselect_excel_signal.connect(self._fileselect_excel)
        self.update_product_db_signal.connect(self.update_product_db)
        self._user_message_signal.connect(self._user_message)
        self._read_sop_file_signal.connect(self._read_sop_file)
        self._validate_sop_file_signal.connect(self._validate_sop_file)
        self.get_product_database_name_signal.connect(self.get_product_database_name)
        self._update_price_signal.connect(self._update_price)
        self._add_parts_signal.connect(self._add_parts)

        return None

    @pyqtSlot()
    def update_product_db(self):
        """Update the product database attached to a SQL server instance with
        pricing data uploaded from an EXCEL file

        Steps
        1. Connect to the product database. It is assumed the product database
        has a database_name of ProductDB and that it is already attached. to
        SQL Server
        This class finds the database_name
        with a logical name ProductDB. Then find the assocaited .mdf and .ldf
        file associated with the logical name 'ProductDB'. Then connect to
        this database.

        2. Make sure the selected EXCEL file is a file, and that it is an EXCEL
        file

        3. Check the sop_path EXCEL file for the correct format. It must
        have the correct headers to update the product database
        Make sure the file contains headers 'Manufacturer Part Number',
        'Manufacturer Name', 'Material Number',
        'Material Description', 'Siemens Net'

        4. If the product database does not contain all records in the parsed
        sop-parts file, then add them to the product database

        5. If the product database has records contained in the parsed
        sop-parts file then update the price in the product database

        6. Notify the user the process is finished"""

        # Find the correct product database. If the product database does
        # Not exist then raise a message to the user
        path_mdf, path_ldf, database_name = self.get_product_database_name_signal.emit()

        # Check SOP File for correct format
        sop_path = self.partFileText.text()
        self._validate_sop_file_signal.emit(sop_path)

        # Parse information in excel file and read to memory
        sop_dataframe = self._read_sop_file_signal.emit(sop_path)

        # Connect to database
        self.context.init_sql_database_connection(path_mdf, path_ldf, database_name)

        # If parts are not in the product database then add them
        self._add_parts(sop_dataframe) # TODO

        # If parts exist in database then update the price
        self._update_price(sop_dataframe) # TODO

        return None

    @pyqtSlot(pd.DataFrame)
    def _add_parts(self, sop_dataframe):

        # Find all unique parts in the SOP parts list (sop_dataframe)
        # TODO
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

    @pyqtSlot(pd.DataFrame)
    def _update_price(self, sop_dataframe):

        # Update all common parts in sop_dataframe and the attached product database
        # TODO
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


    @pyqtSlot(result=str)
    def _fileselect_excel(self):
        """Open QFindDialog to find SQL database file or folder with SQL
        database file"""

        self.fileDialog = QFileDialog(self,
                                      'Select EXCEL SOP List',
                                      self.context.default_jobs_folder)
        self.fileDialog.setFileMode(QFileDialog.ExistingFile)
        self.fileDialog.setNameFilter("Excel Files (*.xlsx *.xls)")
        if self.fileDialog.exec_():
            # Dialog accepted
            file_paths = self.fileDialog.selectedFiles()
            sop_path = file_paths[0]
        else:
            # Dialog closed
            sop_path = None

        if sop_path in [None, '']:
            # No database file is found in the selected directory
            pass
        else:
            # Some file or path was selected
            # Change the displayed job file name
            self.partFileText.setText(sop_path.__str__())
            self._validate_sop_file_signal.emit(sop_path)

        return sop_path

    @pyqtSlot(str, str, result=QMessageBox)
    @pyqtSlot(str, str, str, result=QMessageBox)
    def _user_message(self, title, msg, detail=None):
        """Create a simple user message box"""
        msgBox = QMessageBox()
        msgBox.setWindowTitle(title)
        msgBox.setText(msg)
        msgBox.setStandardButtons(QMessageBox.Ok)
        # msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowIcon(self.context.alarm_icon)
        if detail:
            msgBox.setDetailedText(detail)
        return msgBox


    @pyqtSlot(str, result=pd.DataFrame)
    def _read_sop_file(self, sop_path):
        """
        inputs
        -------
        sop_path : (str) path to sop excel file. sop is an acronym that means
        'parts that have an agreed upon price'.
        outputs
        -------
        sop_dataframe : (pd.DataFrame) A dataframe of parsed records from
        the rows in the EXCEL file sop_path

        Make sure the file contains headers 'Manufacturer Part Number',
        'Manufacturer Name', 'Material Number',
        'Material Description', 'Siemens Net'
        """

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
            ' file : {}. The Product Database Update app cannot run' +
            'without these headers'.format(missing_headers))
            self.FileErrMsgBox = self._user_message('Missing Header',msg)
            self.FileErrMsgBox.exec_()

        return sop_dataframe


    @pyqtSlot(str)
    def _validate_sop_file(self, sop_path):

        # File must be EXCEL File
        root, ext = os.path.splitext(sop_path)

        # sop_path must not be None or empty string
        if any((sop_path is None, sop_path == '')):
            msg=('No file has been selected. Please select a file')
            self.IOErrMsgBox = self._user_message('Invalid File', msg)
            self.IOErrMsgBox.exec_()
            sop_path = None

            # No file has been selected - prompt the user to select a file
            self.action_fileselect_excel_SOP()

        # File must be valid
        elif not os.path.isfile(sop_path):
            msg=('The selected file : {} Is invalid.'.format(sop_path) +
                 'Please select a valid File System File')
            self.IOErrMsgBox = self._user_message('Invalid File', msg)
            self.IOErrMsgBox.exec_()
            sop_path = None

        elif not ext in ['.xlsx','.xls']:
            msg=('The selected file {} is not a an EXCEL file with extension' +
                 '.xlsx or .xls\nPlease select a valid EXCEL file')
            self.IOErrMsgBox = self._user_message('Invalid file extension',msg)
            self.IOErrMsgBox.exec_()
            # Reset sop_path
            sop_path = None

        return None


    @pyqtSlot()
    def get_product_database_name(self):
        """Return the database name (not physical or logical) of the associated
        products database.
        The product database has the logical_name 'ProductDB'
        in SQL server
        The logical name CAN be the same as the database_name, but not always

        If no database is found with the logical name 'ProductDB' then raise
        a message to the user"""

        sql = """select t1.[name] as logical_name, t1.physical_name, t1.database_id,
                    (select name
                    from [master].[sys].[databases] as t2
                    where t2.database_id = t1.database_id) as [database_name]
                FROM [master].[sys].[master_files] as t1
                where [name] = 'ProductDB'"""

        rows = self.context.SQLBase.execute_sql_master(sql)
        if len(rows) == 0:
            msg = ('No database with a name "ProductDB" is connected to this' +
                   ' instance of SQL Server. The Product Database may not be' +
                   'connected because it is not configured in Design Tool,'+
                   ' or the Design Tool authors may have changed the default' +
                   'name. The Product Database Update tool app cannot run')
            self.SQLErrMsgBox = self._user_message('Product Database', msg)
            self.SQLErrMsgBox.exec_()
            return None
        else:
            product_database_name = rows[0].database_name
            path_mdf = rows[0].physical_name
            database_id = rows[0].database_id

            # Find the log file name
            sql = """select * from [master].[sys].[master_files]
                     where database_id = {} and type_desc = 'LOG'""".format(database_id)
            rows = self.context.SQLBase.execute_sql_master(sql)
            path_ldf = rows[0].physical_name

        return path_mdf, path_ldf, product_database_name


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