# -*- coding: utf-8 -*-

# Python imports
from pathlib import Path
import json

# Third party imports
from PyQt5.QtWidgets import QDialog

# Local imports
from Ui_MainWindowDialog import Ui_MainWindowDialog

#%%


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