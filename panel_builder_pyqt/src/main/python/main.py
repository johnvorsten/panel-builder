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

    
class ReportDialog(QDialog, Ui_ReportDialog):
    pathSignal = pyqtSignal(str)
    init_system_scrollSignal = pyqtSignal()
    
    def __init__(self, context):
        super(ReportDialog, self).__init__()
        
        # Context manager
        self.context = context
        
        # Set user interface from Designer
        self.setupUi(self)
        self.setWindowIcon(self.context.report_icon)
        self.setWindowTitle('PB Reports')
        
        # Connect path signal to constructor. path_mdf allows BomGenerator
        # To be instantiated. After, the self.systemScrollBox's widgets are
        # Populated. It is important that self.path_mdf is defined before
        # self._init_system_scroll is created...
        self.pathSignal.connect(self.set_path_mdf)
        self.init_system_scrollSignal.connect(self._init_systems_scroll)
        
        # Update ui with dynamic stuff
        self.init_ui()
        
    def init_ui(self):
        """Some things need to be changed in the UI
        Add a list of systems
        Change select systems buttons to 'all systems' or 'select individuals'
        add options to 'include ETR (+) parts', 'include by others (*) parts'"""
        
        # Add a report type to the combo box
        self.reportTypeComboBox.addItem('BOM Report')
        
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
    
    def _close_application(self):
        msgBox = QMessageBox(QMessageBox.Information, 
                             'Exit application',
                             'Do you want to exit reports?',
                             QMessageBox.Yes | QMessageBox.No)
        msgBox.setWindowIcon(self.context.alarm_icon)
        choice = msgBox.exec()
        if choice == QMessageBox.Yes:
            self.close()
        else:
            pass
        return None
    
    @pyqtSlot(str)
    def set_path_mdf(self, path):
        """Set the database path chosen by the user"""
        self.path_mdf = path
        return None
    
    @pyqtSlot()
    def _init_systems_scroll(self):
        """Show a list of systems under the scroll box
        The tree shows widget and layout nesting, but inheiritance is not 
        exactly right...
        
        self.leftLayout (QVBoxLayout)
            self.systemGroupBox (QGroupBox, self.verticalLayoutWidget_4)
                self.systemLayout (QVboxLayout, self.verticalLayoutWidget_5)
                    self.scrollArea (QScrollArea, self.verticalLayoutWidget_5)
                        
                        self.scrollAreaWidgetContents (QWidget)
                        ↑
                        systemCheckLayoutArea (QVBoxLayout, self.scrollAreaWidgetContents)
                            QCheckBox
                
        """
        unique_systems = self._get_database_BOM_systems()
        
        self.systemCheckLayoutArea = QVBoxLayout(self.scrollAreaWidgetContents)
        
        for str_system in unique_systems:
            systemCheckBox = QCheckBox(str_system)
            systemCheckBox.setObjectName(str_system)
            self.systemCheckLayoutArea.addWidget(systemCheckBox)
        
        self.systemCheckLayoutArea.addStretch(1)
        self.scrollArea.setWidgetResizable(True)
        
        # Set the GROUP BOX'S LAYOUT to self.systemLayout!!
        self.systemGroupBox.setLayout(self.systemLayout)
        
        return None
    
    # Data processing Logic ------------- move to separate thread later
    def _get_retro_flags(self):
        """At report generation time get the retro flags for which parts to include
        in the report. See BOM_generator.py at BOMGenerator.generate_fancy_report"""
        retro_list = ['IS NULL']
                
        if self.ETRCheckBox.isChecked():
            retro_list.append("= '+'")
        if self.byothersCheckBox.isChecked():
            retro_list.append("= '*'")
            
        return retro_list
    
    def _get_selected_BOM_systems(self):
        """Get a list of unique systems from the left layout group
        see self.systemGroupBox and self.systemScrollBox"""
        
        if self.allSystemsButton.isChecked():
            # Return every system in the job database
            selected_systems = self._get_database_BOM_systems()
        elif self.selectSystemsButton.isChecked():
            selected_systems = []
            for i in range(self.systemCheckLayoutArea.count()):
                checkbox = self.systemCheckLayoutArea.itemAt(i)
                if isinstance(checkbox, QCheckBox):
                    selected_systems.append(checkbox.objectName)
                    print(checkbox.objectName)
                    print(type(checkbox.objectName))
        else:
            msg = ('You must indicate All Systems or Individual systems' + 
                   ' before you generate a report. Do you want to default to' +
                   ' All Systems?')
            msgBox = QMessageBox(QMessageBox.Information, 
                                'Select Systems',
                                  msg,
                                  QMessageBox.Yes | QMessageBox.No)
            msgBox.setWindowIcon(self.context.alarm_icon)
            coice = msgBox.exec()
            if choice == QMessageBox.Yes:
                self.allSystemsButton.setChecked(True)
                self.systemGroupBox.setEnabled(False)
                pass
            else:
                pass
            return None
        
        return selected_systems
    
    def _init_BOM_generator(self):
        """Instantiate a BOM generator class for generating reports and filling
        the UI"""
        self.BomGenerator = BOMGenerator(self.path_mdf, 
                                         database_name='PBJobDB')
        return None
    
    def _get_database_BOM_systems(self):
        """Read a SQL job database for a list of unique BOM systems. Use this
        to generate a list of systems for the BOM reporting screen"""
        
        if 'BomGenerator' not in self.__dict__:
            self._init_BOM_generator()
            
        unique_systems = self.BomGenerator.get_unique_systems()
        
        return unique_systems
    
    def _generate_report(self):
        """Start to make the BOM report..."""
        try:
            selected_systems = self._get_selected_BOM_systems()
            retro_flags = self._get_retro_flags()
            
            msg = ('Your report is being generated and should auto-open when' + 
                   ' finished. This may take longer on larger jobs. Select "Ok"' +
                   ' to continue or cancel to change selection')
            msgBox = QMessageBox(QMessageBox.Information, 
                                'Please wait',
                                  msg,
                                 QMessageBox.Ok | QMessageBox.Cancel)
            msgBox.setWindowIcon(self.context.help_icon)
            choice = msgBox.exec()
            if choice == QMessageBox.Ok:
                self.BomGenerator.generate_fancy_report(retro_flags,
                                                        selected_systems)
            else:
                event.ignore()
                pass
            
        except Exception as e:
            logging.debug(e)
            msg = ('An error occured while generating the report : {}'.format(e) + 
                   '\nMake sure \n1. A valid job is selected \n2. A product' + 
                   ' database is setup \n3. Your job has systems set up')
            msgBox = QMessageBox(QMessageBox.Information,
                                 'Database Search',
                                 msg,
                                 QMessageBox.Ok)
            msgBox.setWindowIcon(self.context.alarm_icon)
            choice = msgBox.exec()
        
        return None
    

class MainWindow(QMainWindow, Ui_MainWindow):
    
    def __init__(self, context):
        super(MainWindow, self).__init__()
        
        # Set user interface from Designer
        self.setupUi(self)
        
        # FBS Context manager
        self.context = context
        
        # This will me the main user interface on startup
        self.MyWindowDialog = MainWindowDialog()
        self.setCentralWidget(self.MyWindowDialog)
        self.setWindowIcon(self.context.main_icon)
        self.setWindowTitle('Panel Builder')
        
        # Connect buttons
        self.init_menu()
        
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
            .connect(self.action_show_reports)
            
        self.actionBOM.setStatusTip('Show Device Table')
        self.actionBOM.triggered\
            .connect(self.action_show_SQL_BOM)

    def action_find_job(self):
        """Open QFindDialog to find SQL database file or folder with SQL 
        database file"""
        
        fileDialog = QFileDialog(self)
        fileDialog.setFileMode(QFileDialog.Directory)
        str_directory = QFileDialog.getExistingDirectory(self, 
                                                'Select Job Directory', 
                                                'C:\\',
                                                options=QFileDialog.ShowDirsOnly)
        
        directory = Path(str_directory)
        try:
            file_path = list(directory.glob('*/*.mdf'))[0]
        
        except IndexError:
            msg = ('No SQL database with a .mdf extension .mdf was found in ' +
                   'the selected directory : {}.'.format(str_directory) + 
                   ' Please select a new directory')
            msgBox = QMessageBox(QMessageBox.Information,
                                 'Database Search',
                                  msg,
                                QMessageBox.Ok)
            msgBox.setWindowIcon(self.context.alarm_icon)
            choice = msgBox.exec()
            file_path = None
        
        # Change the displayed job file name
        self.path_mdf = file_path.__str__()
        self.MyWindowDialog.findChild(QLineEdit, 'JobPathTextEdit')\
            .setText(self.path_mdf)
        
        return None

    def action_show_options(self):
        # TODO 
        """create a customs window dialog with helpful user info including
        SQL Server, Parts database name/location"""
        
        msg = ('The options dialog is still under-way. Please stand-by while' +
                ' it is being developed')
                    
        messageBox = QMessageBox(QMessageBox.Information,
                                 'Application Options',
                                 msg,
                                 QMessageBox.Ok)
        messageBox.setWindowIcon(self.context.alarm_icon)
        choice = messageBox.exec()
        pass
    
    def action_show_reports(self):
        """Show the report dialog and set any data in the class that will be needed
        for job processing, including the selected job path"""
            
        def show_select_job_message():
            msg = ('No job has been selected yet. Please select a job' +
                    ' using File-> Find Job')
            messageBox = QMessageBox(QMessageBox.Information,
                                     'BOM Select',
                                     msg,
                                     QMessageBox.Ok)
            messageBox.setWindowIcon(self.context.help_icon)
            choice = messageBox.exec()
            return None
            
        if 'path_mdf' not in self.__dict__:
            show_select_job_message()
            
        elif self.path_mdf is None:
            show_select_job_message()
            
        else:
            self.MyReportDialog = ReportDialog(self.context)
            self.MyReportDialog.pathSignal.emit(self.path_mdf)
            self.MyReportDialog.init_system_scrollSignal.emit()
            self.MyReportDialog.exec()
            
        return None
        
    def action_show_SQL_BOM(self):
        
        msg = ('The SQL dialog is still under-way. Please stand-by while' +
                ' it is being developed')
                    
        messageBox = QMessageBox(QMessageBox.Information,
                                 'BOM View',
                                 msg,
                                 QMessageBox.Ok)
        messageBox.setWindowIcon(self.context.help_icon)
        choice = messageBox.exec()
        pass
    
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

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())

class AppContext(ApplicationContext):

    def __init__(self, *args, **kwargs):
        super(AppContext, self).__init__(*args, **kwargs)

        self.window = MainWindow(self)

    def run(self):
        self.window.show()
        return self.app.exec_()
    
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
