# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 06:49:41 2020

@author: z003vrzk
"""
# Python imports
import time

# Third party imports
from bacpypes.iocb import IOCB, IOController


#%%

"""IO Control Blocks (IOCB) holds parameters for an operation, and holds a place
for the result of the operation
The IO Controller processes the IOCB, and returns the result to the caller"""

"""What if the controller is busy when a method is called?
What if the controller is waiting for network fuctions before it can complete
a request?
What if the application that calls the controller is on a remote machine?"""

# Build an IOCB
iocb = IOCB(1,2,a=3) # Arbitrary variables
iocb.args
iocb.kwargs

# Build a controller (will perform operation)
class MyController(IOController):

    def process_io(self, iocb):
        self.complete_io(iocb, iocb.args[0] + iocb.args[1] * iocb.kwargs['a'])

    def process_io_wait(self, iocb):
        time.sleep(5) # Demonstrate threading
        self.complete_io(iocb, iocb.args[0] + iocb.args[1] * iocb.kwargs['a'])


mycontroller = MyController()
mycontroller.request_io(iocb)
iocb.ioComplete # Threading event
iocb.ioComplete.is_set() # True after processed
iocb.ioState #
iocb.ioResponse # Number 7
iocb.ioError # None

# Invalid IOCB for controller
iocb2 = IOCB(1,2,a='letter')
mycontroller.request_io(iocb2)
iocb2.ioComplete # Threading event
iocb2.ioComplete.is_set() # True after processed
assert iocb2.ioState  == bacpypes.iocb.ABORTED
assert iocb2.ioResponse is None
assert isinstance(iocb2.ioError, TypeError)

# Threading
"""IOController is not thread safe (what does this mean?)
The thread initiating the request to the controller will wait for the completion
event to be set"""
iocb3 = IOCB(1,2,a=3)
mycontroller.process_io_wait(iocb3)
iocb.ioComplete.wait()






