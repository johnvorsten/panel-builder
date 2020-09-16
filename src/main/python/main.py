"""
Created Jan 8, 2020 by John Vorsten
"""

# Python imports
from pathlib import Path
import os, sys, logging
from datetime import datetime

# Third party imports
from fbs_runtime.application_context.PyQt5 import (ApplicationContext,
                   cached_property)
from PyQt5.QtWidgets import (QMainWindow, QApplication, QDialog, QFileDialog,
                             QMessageBox, QLineEdit, QCheckBox,
                             QVBoxLayout, QLabel)

from PyQt5.QtCore import (pyqtSlot, pyqtSignal)
from PyQt5.QtGui import QIcon

# Local imports
from Ui_MainWindow import Ui_MainWindow
from ReportDialog import ReportDialog
from MainWindowDialog import MainWindowDialog
from OptionsDialog import OptionsDialog
from DeviceTableDialog import DeviceTableDialog
from ProductUpdateDialog import ProductUpdateDialog
from sql_tools import SQLBase

# Instances
logging.basicConfig(filename=os.path.join(os.getcwd(), 'logs', 'sql_logs.log'),
                    level=logging.DEBUG,
                    format='%(asctime)s %(message)s')

#%%


"""# Multiple inheiritance method where we sub-class QDialog and set
user interface using __init__() method
It is important to understand how I am subcassing these items.
First, I create a .py file that contains user interface objects with qt designer
and the pyuic tool
1)
Create the .py file from .ui files using the pyuic command line interface like
this : >>pyuic5 -x <path_to_.ui_file> -o <path_and_name_of_output_.py_file>
2)
Once the files are created I can use them by subclassing two items :
    a) the widget that the UI should be displayed in
    b) the output of pyuic5 and designer. The output is an ordinacy python
    class with a .setupUi() method which is used to 'inject' the ui widgets
    into the widget which it inheirits from.  This was tricky for me to understand
    at first
3) Finally, I can add functionality to each dialog or window because I already
    subclassed the Ui_ files and python classes.  I have to access objects by name
    or by class attribute
"""


class MainWindow(QMainWindow, Ui_MainWindow):
    # action_find_job_Signal = pyqtSignal()

    def __init__(self, context):
        super(MainWindow, self).__init__()

        # Set user interface from Designer
        self.setupUi(self)

        # FBS Context manager
        self.context = context

        # This will be the main user interface on startup
        self.MyWindowDialog = MainWindowDialog()
        self.MyWindowDialog.init_signals(self)
        self.setCentralWidget(self.MyWindowDialog)
        self.setWindowIcon(self.context.main_icon)
        self.setWindowTitle('Panel Builder')

        # Connect buttons
        self.init_menu()

        # Initialize database connection
        self.context.init_application_options()
        self.context.init_sql_master_connection()

        return None

    def init_menu(self):
        """Define all signals and slots for this widget, including the menu bar
        """
        # Find_Job QAction
        self.actionFind_Job.setStatusTip('Find SQL Database')
        self.actionFind_Job.triggered\
            .connect(lambda state : self.action_find_job())

        # Options QAction
        self.actionOptions.setStatusTip('Change application settings & Options')
        self.actionOptions.triggered\
            .connect(lambda : self.action_show_options(OptionsDialog))

        # Show Reports QAction
        self.actionOpen_Reports.setStatusTip('Show Reports')
        self.actionOpen_Reports.triggered\
            .connect(lambda state : self.action_show_reports(ReportDialog))

        self.actionBOM.setStatusTip('Show Device Table')
        self.actionBOM.triggered\
            .connect(lambda state : self.action_show_SQL_BOM(DeviceTableDialog))

        # Show update Product DB Dialog
        self.actionUpdate_Product_DB.setStatusTip('Update product DB from EXCEL SOP')
        self.actionUpdate_Product_DB.triggered\
            .connect(lambda state : self.action_show_update_products(ProductUpdateDialog))

        return None


    def closeEvent(self, event):
        msgBox = QMessageBox(QMessageBox.Information,
                             'Exit application',
                             'Do you want to exit?',
                             QMessageBox.Yes | QMessageBox.No)
        msgBox.setWindowIcon(self.context.alarm_icon)
        choice = msgBox.exec()
        if choice == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
            pass
        return None

    @staticmethod
    def find_mdf(directory):
        """Input a user-defined directory on their file system.  Output a
        full path to a .mdf SQL database file in a sub directory of the user
        specified path.  This function handles (2) cases :
        Look for the .mdf file in the given directory (yield all matching files
        in the given directory matching a pattern *.mdf)
        Look for the .mdf file in the given directory up to 2 sub folders down
        (yield all matching files in the given driectory and its direct child
        directories - do not search recursively)
        Inputs
        directory : (pathlib.Path) Path object
        """
        if isinstance(directory, Path):
            pass
        else:
            # Try to handle strings
            try:
                directory = Path(directory)
            except TypeError:
                msg = ('An incorrect directory argument was passed of ' +
                       'type {} '.format(type(directory)) +
                       'please pass type pathlib.Path')

        # Search the top level directory
        mdf_match_list = list(directory.glob('*.mdf'))
        ldf_match_list = list(directory.glob('*.ldf'))

        if mdf_match_list.__len__() >= 1 and ldf_match_list.__len__() >= 1:
            path_mdf = mdf_match_list[0]
            path_ldf = ldf_match_list[0]
            msg = 'Database found at {}'.format(path_mdf)
            return path_mdf, path_ldf, msg

        # No files are found in root directory
        if mdf_match_list.__len__() < 1:
            # Search child directories
            child_dirs = [x for x in directory.iterdir() if x.is_dir()]

            for child in child_dirs:
                mdf_match_list_sub = list(child.glob('*.mdf'))
                ldf_match_list_sub = list(child.glob('*.ldf'))

                if mdf_match_list_sub.__len__() >= 1 and ldf_match_list_sub.__len__() >= 1:
                    path_mdf = mdf_match_list_sub[0]
                    path_ldf = ldf_match_list_sub[0]
                    msg = 'Database found at {}'.format(path_mdf)
                    return path_mdf, path_ldf, msg

                # No files are found
                else:
                    path_mdf = None
                    path_ldf = None
                    msg = ('No SQL database with a .mdf extension .mdf was found in ' +
                           'the selected directory : {}.'.format(directory) +
                           ' Please select a new directory')


        return path_mdf, path_ldf, msg

    @staticmethod
    def find_j_vars(directory):
        """Input a user-defined directory on their file system.  Output a
        full path to a .mdf SQL database file in a sub directory of the user
        specified path.  This function handles (2) cases :
        Look for the .mdf file in the given directory (yield all matching files
        in the given directory matching a pattern *.mdf)
        Look for the .mdf file in the given directory up to 2 sub folders down
        (yield all matching files in the given driectory and its direct child
        directories - do not search recursively)
        Inputs
        directory : (pathlib.Path) Path object
        """
        if isinstance(directory, Path):
            pass
        else:
            # Try to handle strings
            try:
                directory = Path(directory)
            except TypeError:
                msg = ('An incorrect directory argument was passed of ' +
                       'type {} '.format(type(directory)) +
                       'please pass type pathlib.Path')

        # Search the top level directory
        match_list = list(directory.glob('j_vars.ini'))

        if match_list.__len__() >= 1:
            file_path = match_list[0]
            msg = 'jvars found at {}'.format(file_path)
            return file_path, msg

        # No files are found in root directory
        if match_list.__len__() < 1:
            # Search child directories
            child_dirs = [x for x in directory.iterdir() if x.is_dir()]

            for child in child_dirs:
                match_list_sub = list(child.glob('j_vars.ini'))

                if match_list_sub.__len__() >= 1:
                    file_path = match_list_sub[0]
                    msg = 'j_vars found at {}'.format(file_path)
                    break

                # No files are found
                else:
                    file_path = None
                    msg = ('No j_vars was found in ' +
                           'the selected directory : {}.'.format(directory) +
                           ' Please select a new directory')

        return file_path, msg


    def action_find_job(self):
        """Open QFindDialog to find SQL database file or folder with SQL
        database file"""

        fileDialog = QFileDialog(self)
        fileDialog.setFileMode(QFileDialog.Directory)
        str_directory = QFileDialog.getExistingDirectory(self,
                                                'Select Job Directory',
                                                self.context.default_jobs_folder,
                                                options=QFileDialog.ShowDirsOnly)

        directory = Path(str_directory)

        path_mdf, path_ldf, msg = self.find_mdf(directory)
        j_vars_path, j_vars_msg = self.find_j_vars(directory)

        if path_mdf is None:
            # No database file is found in the selected directory
            msgBox = QMessageBox()
            msgBox.setWindowTitle('Database Search')
            msgBox.setText(msg)
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setWindowIcon(self.context.alarm_icon)
            msgBox.exec()
            return None

        elif j_vars_path is None:
            # No job variables found in directory
            msgBox = QMessageBox()
            msgBox.setWindowTitle('Job Variables Search')
            msgBox.setText(j_vars_msg)
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setWindowIcon(self.context.alarm_icon)
            msgBox.exec()
            return None

        elif path_ldf is None:
            # No database Log file is found in the selected directory
            msgBox = QMessageBox()
            msgBox.setWindowTitle('Database Search')
            msgBox.setText(msg)
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setWindowIcon(self.context.alarm_icon)
            msgBox.exec()
            return None

        else:
            # Database file, Log file, and j_vars file are all found
            msgBox = QMessageBox()
            msgBox.setWindowTitle('Database Search')
            msgBox.setText(msg)
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.setWindowIcon(self.context.alarm_icon)
            msgBox.exec()

        # Change the displayed job file name
        self.context.path_mdf = path_mdf.__str__()
        self.context.path_ldf = path_ldf.__str__()
        self.context.path_j_vars = j_vars_path.__str__()


        self.MyWindowDialog.findChild(QLineEdit, 'JobPathTextEdit')\
            .setText(self.context.path_mdf)

        return None

    def action_show_options(self, OptionsDialog):
        # TODO
        """create a customs window dialog with helpful user info including
        SQL Server, Parts database name/location"""

        self.OptionsDialog = OptionsDialog(self.context)
        self.OptionsDialog.exec()

        return None

    def action_show_reports(self, ReportDialog):
        """Show the report dialog and
        set any data in the class that will be needed for job processing,
        including the selected job path"""

        if 'path_mdf' not in self.context.__dict__:
            self.action_show_select_job_message()

        elif self.context.path_mdf is None:
            self.action_show_select_job_message()

        elif not Path(self.context.path_mdf).is_file():
            self.action_show_select_job_message()

        else:
            try:
                self.ReportDialog = ReportDialog(self.context)
                self.ReportDialog.exec()
            except Exception as e:
                logging.debug(e)
                msg = ('An error occured while opening Reports.' +
                       '\nMake sure \n1. A valid job is selected \n2. A product' +
                       ' database is setup \n3. Your job has systems set up')

                msgBox = QMessageBox()
                msgBox.setWindowIcon(self.context.alarm_icon)
                msgBox.setWindowTitle('Report Error')
                msgBox.setText(msg)
                msgBox.setDetailedText(str(e))
                msgBox.setStandardButtons(QMessageBox.Ok)
                msgBox.setDefaultButton(QMessageBox.Ok)
                choice = msgBox.exec()

        return None

    def action_show_select_job_message(self):

        msg = ('No job has been selected yet. Please select a job' +
                ' using File-> Find Job')
        msgBox = QMessageBox(self)
        msgBox.setWindowIcon(self.context.help_icon)
        msgBox.setWindowTitle('BOM Select')
        msgBox.setText(msg)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.setDefaultButton(QMessageBox.Ok)
        choice = msgBox.exec()

        return choice

    def action_show_SQL_BOM(self, DeviceTableDialog):

        """Show the Device Table Dialog if the job is already set"""

        if 'path_mdf' not in self.__dict__:
            self.action_show_select_job_message()

        elif self.path_mdf is None:
            self.action_show_select_job_message()

        elif not Path(self.path_mdf).is_file():
            self.action_show_select_job_message()

        else:
            self.DeviceTableDialog = DeviceTableDialog(self.context)
            self.DeviceTableDialog.exec()

        return None

    def action_show_update_products(self, ProductUpdateDialog):
        """Show the dialog to update product database from an SOP Excel file"""
        ProductUpdateDialog = ProductUpdateDialog(self.context)
        ProductUpdateDialog.exec()
        return None



#%%


class AppContext(ApplicationContext):

    def __init__(self, *args, **kwargs):
        super(AppContext, self).__init__(*args, **kwargs)

        self.window = MainWindow(self)

        return None

    def run(self):
        self.window.show()
        return self.app.exec_()


    def init_sql_master_connection(self):
        """Create a database connection for other apps to use"""
        # Read configuration options for database connection
        if '_DEFAULT_FILE_PATH' not in self.__dict__:
            self.init_application_options()
        options = OptionsDialog(self)._action_read_json_options(self._OPTIONS_FILE_PATH)
        self.sql_server = options['sql_server']
        self.sql_driver = options['sql_driver']
        self.default_jobs_folder = options['default_jobs_folder']

        # Initialize database connection to master database
        self.SQLBase = SQLBase(self.sql_server, self.sql_driver)

        return None


    def init_sql_database_connection(self, path_mdf, path_ldf, database_name):
        """
        If a database is already attached then file_used_bool will be True.
        If name_used_bool is True then the logical database name is in use.
        existing_database_name is a string if file_used_bool is True"""

        (file_used_bool,
         name_used_bool,
         existing_database_name) = self.SQLBase\
            .check_existing_database(path_mdf, database_name)

        if file_used_bool:
            # The SQL Database file is in use by other program
            # Dont try and attach the database
            self.database_name = existing_database_name
            self.SQLBase.init_database_connection(self.database_name)

        elif name_used_bool and not file_used_bool:
            # The current database name is in use, and the current .mdf file
            # Cannot be attached under that name
            # Try to attach the database with a new name
            now = datetime.now()
            database_name = database_name + now.strftime('%m%d%H%M%S')
            self.database_name = database_name
            self.SQLBase.attach_database(path_mdf,
                                         database_name=database_name,
                                         path_ldf=path_ldf)
            self.SQLBase.init_database_connection(self.database_name)

        else:
            # The name and database file are not in use - Try to attach
            self.SQLBase.attach_database(path_mdf,
                                         path_ldf=path_ldf,
                                         database_name=database_name)
            self.SQLBase.init_database_connection(self.database_name)

        return None

    def init_application_options(self):
        self._OPTIONS_FILE_PATH = r'./pb_options.json'
        self._DEFAULT_OPTIONS = {'sql_server':'.\DT_SQLEXPRESS',
                            'products_db':'C:\Program Files\DesignTool\Products',
                            'sql_driver':'SQL Server Native Client 11.0',
                            'default_jobs_folder': r'C:\\',
                            }
        self.database_name = 'PBJobDB'

        return None

    @cached_property
    def main_icon(self):
        return QIcon(self.get_resource('images/PBIcon.ico'))

    @cached_property
    def report_icon(self):
        return QIcon(self.get_resource('images/chrome_reader_mode-24px.ico'))

    @cached_property
    def options_icon(self):
        return QIcon(self.get_resource('images/settings_applications-24px.svg'))

    @cached_property
    def help_icon(self):
        return QIcon(self.get_resource('images/help-24px.svg'))

    @cached_property
    def alarm_icon(self):
        return QIcon(self.get_resource('images/alarm-24px.svg'))


if __name__ == '__main__':
    appctxt = AppContext()
    exit_code = appctxt.run()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)
