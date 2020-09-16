from PyQt5 import QtCore, QtGui, QtWidgets

import pandas as pd

from PandasTableModel import DataFrameModel


class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent=None)
        vLayout = QtWidgets.QVBoxLayout(self)
        hLayout = QtWidgets.QHBoxLayout()
        
        self.pathLE = QtWidgets.QLineEdit(self)
        hLayout.addWidget(self.pathLE)
        
        self.loadBtn = QtWidgets.QPushButton("Select File", self)
        hLayout.addWidget(self.loadBtn)
        vLayout.addLayout(hLayout)
        
        self.pandasTv = QtWidgets.QTableView(self)
        vLayout.addWidget(self.pandasTv)
        self.loadBtn.clicked.connect(self.loadFile)
        self.pandasTv.setSortingEnabled(True)

    def loadFile(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "", "CSV Files (*.csv)");
        self.pathLE.setText(fileName)
        df = pd.read_csv(fileName)
        model = DataFrameModel(df)
        self.pandasTv.setModel(model)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())



#%% Testing tableview methods

# Third party imports
from pymongo import MongoClient
import sys

from PyQt5.QtWidgets import (QApplication, QDialog, QStyleFactory,
                             QGroupBox, QGridLayout, QTableView, QVBoxLayout,
                             QPushButton, QCheckBox, QWidget, QMainWindow,
                             QAction, qApp, QMessageBox, QLabel
                             )


# Local imports
from PandasTableModel import DataFrameModel
from mongo_query import MongoQuery


client = MongoClient('localhost', 27017)
db = client['master_points']
test_collection = db['test']

# Testing retrieve documents
myQueryClass = MongoQuery(test_collection)
my_generator = myQueryClass.retrieve_document_missing_labels()
document = next(my_generator)

# Testing retrieving dataframe
dataframe_generator = myQueryClass.retrieve_points_dataframe(document)
index, dataframe = next(dataframe_generator)

# Getting the selected rows of a table
tableView = QTableView()
tableView.setColumnHidden(0, True)
model = DataFrameModel(dataframe)
tableView.setModel(model)
tableView.show()

rows = tableView.selectedIndexes() # Row objects , QtCore.QModelIndex
item = rows[0]
col = item.column()

#%% Testing key bindings
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QApplication, QDialog, QStyleFactory,
                             QGroupBox, QGridLayout, QTableView, QVBoxLayout,
                             QPushButton, QCheckBox, QWidget, QMainWindow,
                             QAction, qApp, QMessageBox, QLabel
                             )

#%% 


dialog = QDialog()

rightGroupBox = QGroupBox('Label Options')

# This button will set the current table view and update the model data
nextButton = QPushButton('Next Cluster')
nextButton.clicked.connect(lambda state, msg='Test Next Button' : print(msg))

# Label options
label1 = QCheckBox('ahu')
label1.setObjectName('ahu')
label2 = QCheckBox('exhaust_fan')
label2.setObjectName('exhaust_fan')
label3 = QCheckBox('misc')
label3.setObjectName('misc')


# Labels layout
labelsLayout = QVBoxLayout()
labelsLayout.setObjectName('labelsLayout')
labelsLayout.setContentsMargins(3,3,3,3)
labelsLayout.addWidget(label1)
labelsLayout.addWidget(label2)
labelsLayout.addWidget(label3)


parentLayout = QVBoxLayout()
parentLayout.setContentsMargins(2,2,2,2)
parentLayout.addWidget(nextButton)
parentLayout.addLayout(labelsLayout)
parentLayout.addStretch(1)

dialog.setLayout(parentLayout)

# Testing key press signal
def on_key(event):
    if event.key() == QtCore.Qt.Key_1:
        dialog.findChild(QCheckBox, 'ahu').setChecked()
    if event.key() == QtCore.Qt.Key_2:
        dialog.findChild(QCheckBox, 'exhaust_fan').setChecked()
    if event.key() == QtCore.Qt.Key_3:
        dialog.findChild(QCheckBox, 'misc').setChecked()
        
keyPressed = QtCore.pyqtSignal(int, name='keyPressed')
keyPressed.connect(on_key)


    
    
dialog.show()

#%% 

from PyQt5.QtWidgets import QTextEdit

class myDialog(QDialog):
    keyPressed = QtCore.pyqtSignal(QtCore.QEvent)
    
    def __init__(self, parent=None):
        super(myDialog, self).__init__(parent)
        self.keyPressed.connect(self.on_key)
        
        self.create_left_group()
        self.create_right_group()
        # Create the main layout
        mainLayout = QGridLayout()
        mainLayout.addWidget(self.leftGroupBox)
        mainLayout.addWidget(self.rightGroupBox)
        self.setLayout(mainLayout)
        
    def create_left_group(self):
        self.leftGroupBox = QGroupBox('Unlabeled Points')
        
        text = QTextEdit('Enter some text')
        layout = QVBoxLayout()
        layout.addWidget(text)
        self.leftGroupBox.setLayout(layout)
        
    
    def create_right_group(self):
        self.rightGroupBox = QGroupBox('Label Options')
        
        # Label options
        label1 = QCheckBox('ahu')
        label1.setObjectName('ahu')
        parentLayout = QVBoxLayout()
        parentLayout.addWidget(label1)
        self.rightGroupBox.setLayout(parentLayout)
        
    def keyPressEvent(self, event):
        print('pressed : ', event.key())
        
    def on_key(self, event):
        print('event received')
        if event.key() == QtCore.Qt.Key_0:
            print(0)

class Example(QMainWindow):
    keyPressed = QtCore.pyqtSignal(QtCore.QEvent)
    
    def __init__(self):
        super(Example, self).__init__()
        self.setGeometry(300, 300, 250, 150)
        self.show()
        self.keyPressed.connect(self.on_key)
        self.setCentralWidget(myDialog())
#        self.setCentralWidget(QPushButton())
        self.show()

    def keyPressEvent(self, event):
#        super(Example, self).keyPressEvent(event)
        self.keyPressed.emit(event)
        print('pressed : ', event.key())

    def on_key(self, event):
        print('event received')
        if event.key() == QtCore.Qt.Key_Enter and self.ui.continueButton.isEnabled():
            self.proceed()  # this is called whenever the continue button is pressed
        elif event.key() == QtCore.Qt.Key_Q:
            print("Killing")
        elif event.key() == QtCore.Qt.Key_0:
            print(0)

if __name__ == '__main__':
    ex = Example()



