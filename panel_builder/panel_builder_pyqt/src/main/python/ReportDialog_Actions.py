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
            self.close()
        else:
            pass
        return None

    @pyqtSlot(str)
    def set_path_mdf(self, path_mdf):
        """Set the database path chosen by the user"""
        # self.path_mdf = path_mdf
        return None

    @pyqtSlot(str)
    def set_path_ldf(self, path_ldf):
        """Set the database log file path chosen by the user"""
        # self.path_ldf = path_ldf
        return None

    @pyqtSlot(str)
    def set_path_j_vars(self, path_j_vars):
        """Set the job variable ini path chosen by the user"""
        # self.path_j_vars = path_j_vars
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

    def _init_BOM_generator(self):
        """Instantiate a BOM generator class for generating reports and filling
        the UI"""
        path_mdf = self.context.path_mdf
        path_ldf = self.context.path_ldf
        path_j_vars = self.context.path_j_vars
        server_name = self.context.server_name
        driver_name = self.context.driver_name
        database_name = self.context.database_name

        self.BomGenerator = BOMGenerator(path_mdf=path_mdf,
                                         path_ldf=path_ldf,
                                         path_j_vars=path_j_vars,
                                         server_name=server_name,
                                         driver_name=driver_name,
                                         database_name=database_name)
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
            report_style = self._get_report_style()

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
                    self.BomGenerator.generate_report_larson(retro_flags,
                                                            selected_systems)
                elif report_style == 'Standard':
                    self.BomGenerator.generate_report_standard(retro_flags,
                                                            selected_systems)
                else:
                    event.ignore()
            else:
                event.ignore()

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
