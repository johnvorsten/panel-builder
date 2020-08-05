# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 10:55:38 2020

@author: z003vrzk

Clickable actions for the main dialog class MainWindow.  Pair with the dialog
Ui_MainWindow

See main.py for usage

"""

# Python imports
from pathlib import Path
import json

# Third party imports
from PyQt5.QtWidgets import QMessageBox, QComboBox, QLineEdit, QDialog

# Local imports
from Ui_OptionsDialog import Ui_OptionsDialog

#%%


class OptionsDialogActions():

    def __init__(self):
        pass


    def _action_read_json_options(self, json_path):
        """Read the application json options file, and create the file with
        default values if the file does not exist
        inputs
        -------
        json_path : (str) directory path to json file
        """
        if isinstance(json_path, Path):
            pass
        else:
            # Try to handle strings
            try:
                json_path = Path(json_path)
            except TypeError:
                msg = ('An incorrect directory argument was passed of ' +
                       'type {} '.format(type(json_path)) +
                       'please pass type pathlib.Path')

        # Check if the ini_path is actually a file, if not raise exception
        if json_path.is_file():
            try:
                with open(json_path, 'r') as fp:
                    options = json.load(fp)
            except json.JSONDecodeError:
                msg=('There was a problem reading your JSON Options. Options'+
                    ' were reset to default')
                self._show_configuration_message(msg)
                self._action_save_options(self.context._DEFAULT_OPTIONS)
        else:
            # No JSON file found, create file with default values
            self._action_save_options(self.context._DEFAULT_OPTIONS)
            options = self.context._DEFAULT_OPTIONS

        return options


    def _action_read_ui_options(self):
        """Read inputs from the user interface"""

        # Set options in visible dialog box
        sql_server = self.SQLHostText.text()
        products_db = self.ProductDBText.text()
        sql_driver = self.sqlDriverComboBox.currentText()
        default_jobs_folder = self.JobFolderText.text()

        options = {'sql_server':sql_server,
                    'products_db':products_db,
                    'sql_driver':sql_driver,
                    'default_jobs_folder':default_jobs_folder,
                    }

        return options

    def _action_set_context_options(self, options):
        """Set the options shown in the options dialog if a json configuration
        file exists"""

        # Set options in the context manager
        self.context.sql_server = options['sql_server']
        self.context.default_jobs_folder = options['default_jobs_folder']
        self.context.products_db = options['products_db']
        self.context.sql_driver = options['sql_driver']

        return None


    def _action_set_ui_options(self, options):
        """Set the options shown in the options dialog if a json configuration
        file exists"""

        # Set options in visible dialog box
        self.findChild(QLineEdit, 'SQLHostText')\
            .setText(self.context.sql_server)
        self.findChild(QLineEdit, 'ProductDBText')\
            .setText(self.context.products_db)
        self.findChild(QComboBox, 'sqlDriverComboBox')\
            .setLineEdit(QLineEdit(self.context.sql_driver))
        self.findChild(QLineEdit, 'JobFolderText')\
            .setText(self.context.default_jobs_folder)

        return None


    def _action_save_options(self, options):
        """Save configuration options after the user is finished setting them
        inputs
        -------
        options : (dict) to be saved as json file"""

        # Check options before saving
        self._action_check_options(options)

        # Save a json file
        with open(self.context_OPTIONS_FILE_PATH, 'wt') as fp:
            json.dump(options, fp)
        return None


    def _action_save_changes(self):
        """Check to see if the user made changes to the current options
        If the use made changes notify them of the changes, and ask to overwrite
        If no changes were made then simply close the dialog"""

        # Read currently configured options
        new_options = self._action_read_ui_options()

        # If options have changed
        if not json.dumps(new_options) == json.dumps(self.options):
            # Dialog
            msg=('It looks like configuration options were changed.' +
                 ' Do you want to save Changes?')
            msgBox = QMessageBox()
            msgBox.setWindowTitle('Options Message')
            msgBox.setText(msg)
            msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msgBox.setWindowIcon(self.context.alarm_icon)
            choice = msgBox.exec()

            if choice == QMessageBox.Yes:
                # Save
                self._action_save_options(new_options)
            else:
                # Cancel
                self.close

        else:
            # Close
            self.close

        return None


    def _action_check_options(self, options):
        """Check the options configuration if they are appropriate"""

        # Unpack options
        default_jobs_folder = options['default_jobs_folder']
        sql_driver = options['sql_driver']
        sql_server = options['sql_server']
        products_db = options['products_db']

        jobs_folder_exists = True
        if not jobs_folder_exists:
            # If the default jobs folder is not a directory
            base=('The selected default jobs folder is not a directory' +
            ' Please enter a valid jobs directory, like "C:\", got {}')
            msg = base.format(default_jobs_folder)

        sql_driver_correct = True
        if not sql_driver_correct:
            # Incorrect SQL Driver
            correct_sql_drivers=['SQL Server Native Client 10.0',
                                 'SQL Server Native Client 11.0']
            base = ('Incorrect SQL Driver configuration option, got {}' +
                ' Try one of {}')
            msg=base.format(sql_driver, correct_sql_drivers)
            self._show_configuration_message(msg)
            pass

        sql_server_exists = True
        if not sql_server_exists:
            # SQL Server does not exist
            base = ('Incorrect SQL Server Name configuration option, got {}')
            msg=base.format(sql_server)
            self._show_configuration_message(msg)
            pass

        products_db_is_dir = True
        if not products_db_is_dir:
            # products folder is not directory
            base = ('Incorrect Products database folder configuration' +
                    ' option, got {}')
            msg=base.format(products_db)
            self._show_configuration_message(msg)
            pass

        return None


    def _show_configuration_message(self, msg):
        """Show configuration errors with the options dialog"""

        msgBox = QMessageBox()
        msgBox.setWindowTitle('Options Message')
        msgBox.setText(msg)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.setWindowIcon(self.context.alarm_icon)
        msgBox.exec()

        return None


class OptionsDialog(QDialog, Ui_OptionsDialog, OptionsDialogActions):

    def __init__(self, context):
        super(OptionsDialog, self).__init__()

        # Context manager
        self.context = context

        # Set user interface from Designer
        self.setupUi(self)
        self.setWindowIcon(self.context.options_icon)
        self.setWindowTitle('PB Options')

        # Update ui with dynamic stuff
        self.init_ui()

        # Signals
        self.init_signals()

        return None

    def init_ui(self):
        """Generate the default view"""

        # Initialize user interface and read options file
        self.options = self._action_read_json_options(self.context._OPTIONS_FILE_PATH)
        self._action_check_options(self.options)
        self._action_set_context_options(self.options)

        # Set items based on read options
        self._action_set_ui_options(self.options)

        return None

    def init_signals(self):
        """Connect signals to slots"""

        # Connect cancel button with close UI
        self.buttonBox.accepted.connect(lambda : self._action_save_changes())
        self.buttonBox.rejected.connect(self.close)

        # Connect other buttons

        return None