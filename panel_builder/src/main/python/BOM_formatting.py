# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 15:15:52 2020

@author: z003vrzk
"""

# Python imports
from collections import namedtuple

# Third party imports
import numpy as np

# Local imports
from read_j_vars import read_vars_to_dict

# Instantiate classes
cell = namedtuple('cell',['row','col','data', 'format'])

#%% Class definitions


