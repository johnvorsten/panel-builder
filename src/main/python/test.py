# -*- coding: utf-8 -*-
"""
Created on Sat Jan 11 17:59:46 2020

@author: z003vrzk
"""

from PyQt5.QtWidgets import (QApplication, QWidget, QGroupBox, QSizePolicy, 
                             QVBoxLayout, QHBoxLayout, QLayout, QComboBox,
                             QCheckBox, QLabel, QScrollArea, QDialog)

from PyQt5.QtCore import QRect

# Local imports
from Ui_ReportDialog import Ui_ReportDialog

unique_systems = ['check1','check2','check3','check4','check5','check6','check7',
                  'check8','check9','check10']

class Window(QDialog, Ui_ReportDialog):
    """Left Layout
        reportSelectLayout
            Label
            ComboBox
            
        scroll
            QWidget
                VLayout
                    GroupBox
                        CheckBox..."""
    
    def __init__(self):
        super(Window, self).__init__()

        
        # Set user interface from Designer
        self.setupUi(self)
        
        # Change UI
        self._init_ui()
        
        
    def _init_ui(self):
        
        self.systemCheckLayoutArea = QVBoxLayout(self.scrollAreaWidgetContents)
        
        for str_system in unique_systems:
            systemCheckBox = QCheckBox(str_system)
            self.systemCheckLayoutArea.addWidget(systemCheckBox)
        
        self.systemCheckLayoutArea.addStretch(1)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.sizeHint()
        # self.scrollArea
        
        # self.systemLayout.addStretch(1)
        self.systemLayout.setStretch(0, 1)
        self.systemLayout.setStretch(1, 1)
        
        
        pass
        
            


if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    window = Window()
    # window.setGeometry(500, 300, 300, 400)
    window.show()
    sys.exit(app.exec_())