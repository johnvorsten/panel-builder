# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 12:03:00 2020

@author: z003vrzk
"""

# Python imports
import sys

# Third party imports
from fbs_runtime.application_context.PyQt5 import (ApplicationContext,
                   cached_property)
from PyQt5.QtWidgets import (QMainWindow, QApplication, QDialog, QFileDialog,
                             QMessageBox, QLineEdit, QCheckBox,
                             QVBoxLayout)
from PyQt5.QtGui import QIcon

# Local imports
from Ui_OptionsDialog import Ui_OptionsDialog



#%%

class OptionsDialog(QDialog, Ui_OptionsDialog):
    # TODO Create and import inheirited files
    def __init__(self, context):
        super(OptionsDialog, self).__init__()

        # Context manager
        self.context = context

        # Set user interface from designer
        self.setupUi(self)
        self.setWindowIcon(self.context.report_icon)

        return None


#%%

class AppContext(ApplicationContext):

    def __init__(self, *args, **kwargs):
        super(AppContext, self).__init__(*args, **kwargs)

        self.dialog = OptionsDialog(self)

    def run(self):
        self.dialog.show()
        return self.app.exec_()

    @cached_property
    def main_icon(self):
        return QIcon(self.get_resource('images/PBIcon.ico'))

    @cached_property
    def report_icon(self):
        return QIcon(self.get_resource('images/chrome_reader_mode-24px.ico'))



if __name__ == '__main__':
    appctxt = AppContext()
    exit_code = appctxt.run()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)