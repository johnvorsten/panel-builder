# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 15:36:15 2020

@author: z003vrzk
"""


# Python imports
from pathlib import Path

# Third party imports
from PyQt5.QtWidgets import (QMainWindow, QApplication, QDialog, QFileDialog,
                             QMessageBox, QLineEdit, QCheckBox,
                             QVBoxLayout)

# Local imports
from MainWindow_Actions import MainWindowActions

#%%

if __name__ == '__main__':
    directory = r"C:\Users\z003vrzk\.spyder-py3\Scripts\Work\PanelBuilder\panel-builder\SQLTest\JHW"
    directory2 = r"C:\Users\z003vrzk\.spyder-py3\Scripts\Work\PanelBuilder\panel-builder\SQLTest"
    directory3 = r"C:\Users\z003vrzk\.spyder-py3\Scripts\Work\PanelBuilder\panel-builder"

    file_path, msg = MainWindowActions.find_mdf(directory)
    print("File Path : {} | Message : {}\n".format(file_path, msg))
    file_path, msg = MainWindowActions.find_j_vars(directory)
    print("File Path : {} | Message : {}\n\n".format(file_path, msg))

    file_path, msg = MainWindowActions.find_mdf(directory2)
    print("File Path : {} | Message : {}\n".format(file_path, msg))
    file_path, msg = MainWindowActions.find_j_vars(directory)
    print("File Path : {} | Message : {}\n\n".format(file_path, msg))

    file_path, msg = MainWindowActions.find_mdf(directory3)
    print("File Path : {} | Message : {}\n".format(file_path, msg))
    file_path, msg = MainWindowActions.find_j_vars(directory3)
    print("File Path : {} | Message : {}\n\n".format(file_path, msg))