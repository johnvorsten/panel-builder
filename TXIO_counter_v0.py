# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import sys
import os
import numpy as np
import math

data = pd.ExcelFile(r'D:\Project Documents\PointsReportExperiment.xls')
sheetName = data.sheet_names
df1 = data.parse(sheetName[0])
values = df1.values

#Find row with data type I am interested in
test_list = ['LDI','LAO','LAI','LDO'] #create my test values
for test_value in test_list:
    if np.any(values == test_value):
        b = np.where(values == test_value)
        column_Index = b[1][0]
        print('at least one object in your testable point types exists in the data')
        print('column index = ', column_Index, '\n\n')
        break

#Find unique point types
unique = set(values[:, column_Index])

#Create my data handling array
pointData = {}

for item in unique:
    a = item
    pointData[a] = max(sum(values == item))

#Find the number of Digital input modules required
#sum the number of LDI, L2SL, LPACI
#look up the positions of those points in pointData dict
DI_Types = ['LDI', 'L2SL', 'LPACI']
DI_SUM = 0
for types in DI_Types:
    if types == "L2SL":
        print('Number of ', types, ' = ', pointData[types]/2)
        DI_SUM = pointData[types]/2 + DI_SUM
    else:
        try:
            print('Number of ', types, ' = ', pointData[types])
            DI_SUM = pointData[types] + DI_SUM
        except KeyError:
            print('There are no ', types, ' points here and they were not counted')
print('total number of DI points : ', DI_SUM)
print('total number of DI points with 5% added = ', math.ceil(DI_SUM*1.05))
print('total number of TXM1.16D required = ', math.ceil(DI_SUM*1.05/16), '\n\n')

#find hte number of Digital Output moduels required
#sum the number of L2SL, LDO
#look up positions of those pooints in pointData dict
DO_Types = ['LDO', 'L2SL']
DO_SUM = 0
for types in DO_Types:
    if types == 'L2SL':
        print('Number of ', types, ' = ', pointData[types]/2)
        DO_SUM = pointData[types]/2 + DO_SUM
    else:
        try:
            print('Number of ', types, ' = ', pointData[types])
            DO_SUM = pointData[types] + DO_SUM
        except KeyError:
            print('There are no', types, ' points here and they were not counted')
print('total number of DO points : ', DO_SUM)
print('total number of DO points with 5% added = ', math.ceil(DO_SUM*1.05))
print('total number of TXM1.6R-M required = ', math.ceil(DO_SUM*1.05/6), '\n\n')

#find hte number of Analog Output moduels required
#sum the number of LAO
#look up positions of those pooints in pointData dict
AO_Types = ['LAO']
AO_SUM = 0
for types in AO_Types:
    print('Number of ', types, ' = ', pointData[types])
    AO_SUM = pointData[types] + AO_SUM
print('total number of AO points : ', AO_SUM)
AO4_20 = int(input('How many of the Analog Outputs are 4-20mA Devices?'))
standard_AO = AO_SUM - AO4_20
print('Number of TXM1.8X-ML for 4-20mA output required w/ 5% = ', math.ceil(AO4_20*1.05/8))
empty_universal = math.ceil(AO4_20*1.05/8)*8 - AO4_20
if AO_SUM > 8 & AO4_20 > 0:
    print('Number of TXM1.8U-ML for 0-10vdc out etc. required = ', math.ceil((standard_AO - empty_universal)*1.05/8), '\n\n')
    empty_universal = 0
else:
    print('Number of TXM1.8U-ML for 0-10vdc out etc. required = ', math.ceil((standard_AO)*1.05/8), '\n\n')

#find hte number of Analog Input moduels required
#sum the number of LAI
#look up positions of those pooints in pointData dict
AI_Types = ['LAI']
AI_SUM = 0
for types in AI_Types:
    print('Number of ', types, ' = ', pointData[types])
    AI_SUM = pointData[types] + AI_SUM
    
print('total number of AI points : ', AI_SUM)
AI4_20 = int(input('How many of the Analog Inputs are 4-20mA Devices?'))
standard_AI = AI_SUM - AI4_20
print('Number of TXM1.8X for 4-20mA Input required w/ 5% = ', math.ceil(AI4_20*1.05/8))
empty_universal = math.ceil(AI4_20*1.05/8)*8 - AI4_20
if AI_SUM > 8:
    print('Number of TXM1.8U for 0-10vdc in etc. required = ', math.ceil((standard_AI- empty_universal)*1.05/8), '\n\n')
    empty_universal = 0





