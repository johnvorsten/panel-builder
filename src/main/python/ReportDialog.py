# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 15:35:10 2020

@author: z003vrzk
"""

# Python imports
import logging

# Third party imports
from PyQt5.QtWidgets import (QMainWindow, QApplication, QDialog, QFileDialog,
                             QMessageBox, QLineEdit, QCheckBox,
                             QVBoxLayout)
from PyQt5.QtCore import (pyqtSlot, pyqtSignal)

# Local imports
from BOM_generator import BOMGenerator
from Ui_ReportDialog import Ui_ReportDialog

#%%


class ReportDialogActions:

    def __init__(self):
        return None

    def _close_application(self):
        msgBox = QMessageBox()
        msgBox.setWindowIcon(self.context.alarm_icon)
        msgBox.setText('Exit Application')
        msgBox.setInformativeText('Do you want to exit reports?')
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msgBox.setDefaultButton(QMessageBox.Yes)
        choice = msgBox.exec()

        if choice == QMessageBox.Yes:
            if 'database_connection' in self.context.SQLBase.__dict__:
                self.context.SQLBase.database_connection.close()
            self.close()
        else:
            pass

        return None


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
        # Get a unique list of systems to display on UI
        unique_systems = self.get_unique_systems(self.context.database_name)

        # Layout to display unique systems on
        self.systemCheckLayoutArea = QVBoxLayout(self.scrollAreaWidgetContents)

        # Add all systems to layout
        for str_system in unique_systems:
            systemCheckBox = QCheckBox(str_system)
            systemCheckBox.setObjectName(str_system)
            self.systemCheckLayoutArea.addWidget(systemCheckBox)

        self.systemCheckLayoutArea.addStretch(1)
        self.scrollArea.setWidgetResizable(True)

        # Set the GROUP BOX'S LAYOUT to self.systemLayout!!
        self.systemGroupBox.setLayout(self.systemLayout)

        return None


    # Data processing Logic --- TODO move to separate thread later
    def _get_retro_flags(self):
        """At report generation time get the retro flags for which parts to include
        in the report"""
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
            selected_systems = self.get_unique_systems(self.context.database_name)

        elif self.selectSystemsButton.isChecked():
            selected_systems = []
            for i in range(self.systemCheckLayoutArea.count()):
                widget = self.systemCheckLayoutArea.itemAt(i).widget()
                if isinstance(widget, QCheckBox) and widget.isChecked():
                    selected_systems.append(widget.objectName())

        else:
            msg = ('You must indicate All Systems or Individual systems' +
                   ' before you generate a report. Do you want to default to' +
                   ' All Systems?')
            msgBox = QMessageBox(QMessageBox.Information)
            msgBox.setWindowTitle('Select Systems')
            msgBox.setText(msg)
            msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msgBox.setWindowIcon(self.context.alarm_icon)
            choice = msgBox.exec()

            if choice == QMessageBox.Yes:
                self.allSystemsButton.setChecked(True)
                self.systemGroupBox.setEnabled(False)
                pass
            else:
                pass
            return None

        return selected_systems


    def _get_report_style(self):
        """Get the selected report style from styleTypeComboBox
        see self.styleTypeComboBox"""

        report_style = str(self.styleTypeComboBox.currentText())

        return report_style


    def get_unique_systems(self, database_name):
        """Return a list of unique systems from the database initially
        connected by the instance"""

        sql = """
        SELECT [SYSTEM]
        FROM [{db_name}].[dbo].[DEVICES]
        GROUP BY [SYSTEM]""".format(db_name=database_name)

        df = self.context.SQLBase.pandas_execute_sql(sql)

        return df['SYSTEM'].to_list()


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

        df = self.context.SQLBase.pandas_execute_sql(sql)
        if df.shape[0] == 0:
            return None
        else:
            product_database_name = df.loc[0, 'database_name']

        return product_database_name


    def _generate_report(self):
        """Start to make the BOM report..."""
        try:
            selected_systems = self._get_selected_BOM_systems()
            retro_flags = self._get_retro_flags()
            report_style = self._get_report_style()
            product_db = self.get_product_database_name()

            BomGenerator = BOMGenerator(self.context.path_mdf,
                                        self.context.path_ldf,
                                        self.context.path_j_vars,
                                        self.context.database_name,
                                        self.context.SQLBase)

            msg = ('Your report is being generated and should auto-open when' +
                   ' finished. This may take longer on larger jobs. Select "Ok"' +
                   ' to continue or cancel to change selection')
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setWindowIcon(self.context.help_icon)
            msgBox.setText('Please Wait')
            msgBox.setInformativeText(msg)
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            choice = msgBox.exec()

            if choice == QMessageBox.Ok:
                if report_style == 'OG Larson':
                    BomGenerator.generate_report_larson(retro_flags,
                                                             selected_systems,
                                                             product_db)
                elif report_style == 'Standard':
                    BomGenerator.generate_report_standard(retro_flags,
                                                               selected_systems,
                                                               product_db)
                else:
                    pass
            else:
                pass

        except Exception as e:
            logging.debug(e)
            msg = ('An error occured while generating the report.' +
                   '\nMake sure \n1. A valid job is selected \n2. A product' +
                   ' database is setup \n3. Your job has systems set up')

            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setWindowIcon(self.context.alarm_icon)
            msgBox.setWindowTitle('Report Error')
            msgBox.setText(msg)
            msgBox.setDetailedText(str(e))
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.setDefaultButton(QMessageBox.Ok)
            choice = msgBox.exec()

        return None


class ReportDialog(QDialog, Ui_ReportDialog, ReportDialogActions):

    def __init__(self, context):
        super(ReportDialog, self).__init__()

        # Context manager
        self.context = context

        # Set user interface from Designer
        self.setupUi(self)
        self.setWindowIcon(self.context.report_icon)
        self.setWindowTitle('PB Reports')

        # Connect to specific database with SQLBase
        path_mdf = self.context.path_mdf
        path_ldf = self.context.path_ldf
        database_name = self.context.database_name
        self.context.init_sql_database_connection(path_mdf,
                                                  path_ldf,
                                                  database_name)

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

        # Generate Systems view
        self._init_systems_scroll()

        return None
