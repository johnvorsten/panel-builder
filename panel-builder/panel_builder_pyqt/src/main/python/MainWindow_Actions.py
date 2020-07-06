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
import os

# Third party imports
from PyQt5.QtWidgets import (QMainWindow, QApplication, QDialog, QFileDialog,
                             QMessageBox, QLineEdit, QCheckBox,
                             QVBoxLayout)

#%%


class MainWindowActions():

    def __init__(self):
        pass

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
                                                'C:\\', # TODO Default
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
        self.path_mdf = path_mdf.__str__()
        self.path_ldf = path_ldf.__str__()
        self.path_j_vars = j_vars_path.__str__()
        self.MyWindowDialog.findChild(QLineEdit, 'JobPathTextEdit')\
            .setText(self.path_mdf)

        return None

    def action_show_options(self):
        # TODO
        """create a customs window dialog with helpful user info including
        SQL Server, Parts database name/location"""

        msg = ('The options dialog is still under-way. Please stand-by while' +
                ' it is being developed')
        msgBox = QMessageBox(self)
        msgBox.setWindowTitle('Application Options')
        msgBox.setText(msg)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.setDefaultButton(QMessageBox.Ok)
        msgBox.setWindowIcon(self.context.alarm_icon)
        msgBox.exec()

        return None

    def action_show_reports(self, ReportDialog):
        """Show the report dialog and
        set any data in the class that will be needed for job processing,
        including the selected job path"""

        if 'path_mdf' not in self.__dict__:
            self.action_show_select_job_message()

        elif self.path_mdf is None:
            self.action_show_select_job_message()

        elif not Path(self.path_mdf).is_file():
            self.action_show_select_job_message()

        else:
            self.MyReportDialog = ReportDialog(self.context)
            self.MyReportDialog.path_mdf_Signal.emit(self.path_mdf)
            self.MyReportDialog.path_ldf_Signal.emit(self.path_ldf)
            self.MyReportDialog.path_j_vars_Signal.emit(self.path_j_vars)
            self.MyReportDialog.init_system_scrollSignal.emit()
            self.MyReportDialog.exec()

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

        # msg = ('The SQL dialog is still under-way. Please stand-by while' +
        #         ' it is being developed')
        # msgBox = QMessageBox()
        # msgBox.setWindowIcon(self.context.help_icon)
        # msgBox.setWindowTitle('BOM View')
        # msgBox.setText(msg)
        # msgBox.setStandardButtons(QMessageBox.Ok)
        # msgBox.setDefaultButton(QMessageBox.Ok)
        # choice = msgBox.exec()

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



