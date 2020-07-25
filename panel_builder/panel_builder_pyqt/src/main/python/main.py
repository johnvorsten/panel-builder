"""
Created Jan 8, 2020 by John Vorsten
"""

# Python imports
import sys
from pathlib import Path
import logging
import os

# Third party imports
from fbs_runtime.application_context.PyQt5 import (ApplicationContext,
                   cached_property)
from PyQt5.QtWidgets import (QMainWindow, QApplication, QDialog, QFileDialog,
                             QMessageBox, QLineEdit, QCheckBox,
                             QVBoxLayout)

from PyQt5.QtCore import (pyqtSlot, pyqtSignal)
from PyQt5.QtGui import QIcon

# Local imports
from Ui_MainWindowDialog import Ui_MainWindowDialog
from Ui_MainWindow import Ui_MainWindow
from Ui_ReportDialog import Ui_ReportDialog
from BOM_generator import BOMGenerator
from MainWindow_Actions import MainWindowActions
from ReportDialog_Actions import ReportDialogActions
from Ui_DeviceTableDialog import Ui_DeviceTableDialog
from sql_tools import SQLBase

# Instances
logging.basicConfig(filename=os.path.join(os.getcwd(), 'logs', 'sql_logs.log'),
                    level=logging.DEBUG,
                    format='%(asctime)s %(message)s')

#%%


"""# Multiple inheiritance method where we sub-class QDialog and set user interface
# Using __init__() method
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
4)
"""

class MainWindowDialog(QDialog, Ui_MainWindowDialog):

    def __init__(self):
        super(MainWindowDialog, self).__init__()

        # Set user interface from Designer
        self.setupUi(self)

        return None

    def init_signals(self, other):

        # Connect signals and slots
        self.pushButton.released.connect(lambda : other.action_find_job())

        return None

class ReportDialog(QDialog, Ui_ReportDialog, ReportDialogActions):
    path_mdf_Signal = pyqtSignal(str)
    path_ldf_Signal = pyqtSignal(str)
    path_j_vars_Signal = pyqtSignal(str)
    init_system_scrollSignal = pyqtSignal()

    def __init__(self, context):
        super(ReportDialog, self).__init__()

        # Context manager
        self.context = context

        # Set user interface from Designer
        self.setupUi(self)
        self.setWindowIcon(self.context.report_icon)
        self.setWindowTitle('PB Reports')

        # Signasl
        self.init_signals()

        # Update ui with dynamic stuff
        self.init_ui()

        return None

    def init_ui(self):
        """Generate the default report dialog view and add
        signals and slots"""

        # Add a report type to the combo box
        self.reportTypeComboBox.addItem('BOM Report')

        # Add style to combo box
        self.styleTypeComboBox.addItem('OG Larson')
        self.styleTypeComboBox.addItem('Standard')
        self.styleTypeComboBox.setCurrentIndex(1)

        # Connect cancel button with close UI
        self.cancelButton.clicked.connect(self._close_application)

        # Connect other buttons
        self.allSystemsButton.clicked\
            .connect(lambda x : self.systemGroupBox.setEnabled(False))
        self.selectSystemsButton.clicked\
            .connect(lambda x : self.systemGroupBox.setEnabled(True))
        self.generateReportButton.clicked\
            .connect(self._generate_report)

        return None

    def init_signals(self):
        """Connect signals to slots"""

        # Connect path signal to constructor. path_mdf allows BomGenerator
        # To be instantiated. After, the self.systemScrollBox's widgets are
        # Populated. It is important that self.path_mdf is defined before
        # self._init_system_scroll is created...
        self.path_mdf_Signal.connect(self.set_path_mdf)
        self.path_ldf_Signal.connect(self.set_path_ldf)
        self.path_j_vars_Signal.connect(self.set_path_j_vars)
        self.init_system_scrollSignal.connect(self._init_systems_scroll)

        return None


class DeviceTableDialog(QDialog, Ui_DeviceTableDialog):
    # TODO Create and import inheirited files
    def __init__(self, context):
        super(DeviceTableDialog, self).__init__()

        # Context manager
        self.context = context

        # Set user interface from designer
        self.setupUi(self)
        self.setWindowIcon(self.context.report_icon)

        return None

    def get_device_table(self):
        """Retrieve the next cluster of points from documents stored in the
        clustered_points collection. This function handles getting the next
        document that is missing labels, as well as extracting clustered
        points from each of those documents.
        1) Create a data model (Qt is a model-view architecture. The model
        Controls where the data comes from. Right now teh QTableView is only

        inputs
        -------
        None
        outputs
        -------
        dataframe : (pd.DataFrame) a single cluster of points from a document
        in the clustered_ponts collection"""

        # Create a data model (Qt is a model-view architecture. THe model
        # Controls where the data comes from. Right now teh QTableView is only
        # A View on the models data)

        # Instantiate classes if not already
        if not 'dataframe_generator' in self.__dict__.keys():
            self.dataframe_generator = self.mongoQueryHelper.retrieve_points_dataframe(self.current_document)

        try:
            # Generate the next dataframe and set the model in the table view
            self.index, self.current_dataframe = next(self.dataframe_generator)
            tableModel = DataFrameModel(self.current_dataframe)
            self.tableView.setModel(tableModel)

        except StopIteration:
            # The current document is out of clustered points dataframes
            # First, generate a new document to make a new generator over the
            # documents clustered_points objects
            # Finally, get the next dataframe from the generator
            self.current_document = next(self.document_generator)
            self.dataframe_generator = self.mongoQueryHelper.retrieve_points_dataframe(self.current_document)
            self.index, self.current_dataframe = next(self.dataframe_generator)
            tableModel = DataFrameModel(self.current_dataframe)
            self.tableView.setModel(tableModel)

        # Update the documentName Label with the current database name
        database_tag = self.current_document['database_tag']
        documentLabel = self.rightGroupBox.findChild(QLabel, 'databaseTag')
        documentLabel.setText(database_tag)

        # Update the current index
        self.rightGroupBox.findChild(QLabel, 'currentIndex')
        currentIndex = self.rightGroupBox.findChild(QLabel, 'currentIndex')
        currentIndex.setText(str(self.index))

        return None

    def set_device_table(self):

        return None



class MainWindow(QMainWindow, Ui_MainWindow, MainWindowActions):
    # action_find_job_Signal = pyqtSignal()

    def __init__(self, context):
        super(MainWindow, self).__init__()

        # Set user interface from Designer
        self.setupUi(self)

        # FBS Context manager
        self.context = context

        # This will me the main user interface on startup
        self.MyWindowDialog = MainWindowDialog()
        self.MyWindowDialog.init_signals(self)
        self.setCentralWidget(self.MyWindowDialog)
        self.setWindowIcon(self.context.main_icon)
        self.setWindowTitle('Panel Builder')

        # Connect buttons
        self.init_menu()

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
            .connect(self.action_show_options)

        # Show Reports QAction
        self.actionReports.setStatusTip('Show Reports')
        self.actionReports.triggered\
            .connect(lambda state : self.action_show_reports(ReportDialog))

        self.actionBOM.setStatusTip('Show Device Table')
        self.actionBOM.triggered\
            .connect(lambda state : self.action_show_SQL_BOM(DeviceTableDialog))

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

#%%


class AppContext(ApplicationContext):

    def __init__(self, *args, **kwargs):
        super(AppContext, self).__init__(*args, **kwargs)

        self.window = MainWindow(self)

        # TODO Get these dynamically from .ini or options interface
        self.server_name = '.\DT_SQLEXPR2008'
        self.driver_name = 'SQL Server Native Client 10.0'
        self.database_name = 'PBJobDB'

        return None

    def run(self):
        self.window.show()
        return self.app.exec_()

    def init_database_connection(self, path_mdf, path_ldf):
        self.SQLBase = SQLBase()

        pass

    @cached_property
    def main_icon(self):
        return QIcon(self.get_resource('images/PBIcon.ico'))

    @cached_property
    def report_icon(self):
        return QIcon(self.get_resource('images/chrome_reader_mode-24px.ico'))

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
