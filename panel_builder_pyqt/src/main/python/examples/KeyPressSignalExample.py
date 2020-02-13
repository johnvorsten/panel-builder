# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 17:19:26 2019

@author: z003vrzk
"""
from PyQt5 import QtCore, QtWidgets


#%% 
"""Take a look at this first example : 
The key press signal is added in QMainWindow AND myDialog
QMainWindow has the central widget myDialog
The signal will not be received by on_key in the QMainWindow, but WILL be received
at myDialog.
Contrast this to the case where keyPressEvent is only overridden in MainWindow
and NOT in myDialog (below)"""

class myDialog(QtWidgets.QDialog):
    keyPressed = QtCore.pyqtSignal(QtCore.QEvent)
    
    def __init__(self, parent=None):
        super(myDialog, self).__init__(parent)
        self.keyPressed.connect(self.on_key)
        
        leftGroupBox = QtWidgets.QGroupBox('A Group Label')
        text = QtWidgets.QTextEdit('Enter some text')
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(text)
        leftGroupBox.setLayout(layout)
        
        rightGroupBox = QtWidgets.QGroupBox('Label Options')
        label1 = QtWidgets.QCheckBox('ahu')
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(label1)
        rightGroupBox.setLayout(layout)
        
        # Create the main layout
        mainLayout = QtWidgets.QGridLayout()
        mainLayout.addWidget(leftGroupBox)
        mainLayout.addWidget(rightGroupBox)
        self.setLayout(mainLayout)
        
    def keyPressEvent(self, event):
        # A keyPressEvent is overridden in the child
        print('pressed from myDialog: ', event.key())
        # Comment out the .emit to highlight that MainWindow's keyPressEvent
        # Does NOT receive the signal
#        self.keyPressed.emit(event)
        
    def on_key(self, event):
        print('event received @ myDialog')
        if event.key() == QtCore.Qt.Key_0:
            print(0)

class MainWindow(QtWidgets.QMainWindow):
    keyPressed = QtCore.pyqtSignal(QtCore.QEvent)
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.keyPressed.connect(self.on_key)
        self.setCentralWidget(myDialog())
        self.show()

    def keyPressEvent(self, event):
        super(MainWindow, self).keyPressEvent(event)
        print('pressed from MainWindow: ', event.key())
        self.keyPressed.emit(event)
        

    def on_key(self, event):
        print('event received @ MainWindow')
        if event.key() == QtCore.Qt.Key_0:
            print(0)

if __name__ == '__main__':
    ex = MainWindow()
    
#%% Another test

"""Second example : 
The key press signal is added in QMainWindow ONLY
QMainWindow has the central widget myDialog
The signal is received at MainWindow on_key slot. There are two ways to connect
a signal to a slot. The first way is generic and involves a) defining a signal
with its appropriate call signature b) defining its slot with appropiate wrapper
c) binding the signal with its slot. Multiple slots can  be bound on a single 
signal (keyPressEvent is just a slot built into the QObject class)
Notice here that when focus is in myDialog widget, the key signal is not 
sent correctly, because the focus is in a widget that handles key input 
differently

The second way is shown below, where i use the existing keyPressEvent slot
and just connect my newly made signal to this slot. The slot already handles
an event input, and I can emit my signal from this function"""

class myDialog(QtWidgets.QDialog):
    
    def __init__(self, parent=None):
        super(myDialog, self).__init__(parent)
        
        leftGroupBox = QtWidgets.QGroupBox('A Group Label')
        text = QtWidgets.QTextEdit('Enter some text')
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(text)
        leftGroupBox.setLayout(layout)
        
        rightGroupBox = QtWidgets.QGroupBox('Label Options')
        label1 = QtWidgets.QCheckBox('ahu')
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(label1)
        rightGroupBox.setLayout(layout)
        
        # Create the main layout
        mainLayout = QtWidgets.QGridLayout()
        mainLayout.addWidget(leftGroupBox)
        mainLayout.addWidget(rightGroupBox)
        self.setLayout(mainLayout)
    

class MainWindow(QtWidgets.QMainWindow):
    keyPressed = QtCore.pyqtSignal(QtCore.QEvent)
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.keyPressed.connect(self.on_key)
        self.keyPressed.connect(self.anotherPressEvent)
        self.setCentralWidget(myDialog())
        self.show()
        
    @QtCore.pyqtSlot(QtCore.QEvent)
    def anotherPressEvent(self, event):
        super(MainWindow, self).keyPressEvent(event)
        print('pressed from MainWindow.anotherPressEvent: ', event.key())
        
    def keyPressEvent(self, event):
        super(MainWindow, self).keyPressEvent(event)
        print('pressed from MainWindow.keyPressEvent: ', event.key())
        self.keyPressed.emit(event)

    def on_key(self, event):
        print('event received @ MainWindow')
        if event.key() == QtCore.Qt.Key_0:
            print(0)

if __name__ == '__main__':
    ex = MainWindow()



