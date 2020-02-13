# -*- coding: utf-8 -*-
"""
Created on Fri Dec  7 21:34:10 2018

@author: z003vrzk
"""

import pandas as pd
import sys
import os
import numpy as np
import math

class Reader():
    """Reader module intended use is to import user specifed worksheet.
    Have functionality to search sheet names for sheet containing point values.
    Output pandas dataframe of point names contained within user-specified
    worksheet.
    
    Module is outdated, use new MySQLHandling module"""
    
    
    path = None
    excelFile = None
    sheetNames = None
    sheetIndex = None
    pandasDataFrame = None
    sheetValues = None
    
    def __init__(self, path):
        self.path = path
    
    def import_sheet(self):
        #Import the excel sheet
        self.excelFile = pd.ExcelFile(self.path)
        self.sheetNames = self.excelFile.sheet_names
        
        
    def search_sheet_name(self):
        #Find the sheet name that we want to use
        i = None
        pointList = ['LAO', 'LAI', 'LDO', 'LDI', 'Point Name']
        for names in self.sheetNames:
            pd = self.excelFile.parse(names)
            val = pd.values
            boolian = np.zeros((val.shape))
            for types in pointList:
                tempBool = val == types
                boolian = tempBool + boolian
                if boolian.any():
                    print('Sheet index name: {}'.format(names))
                    i = self.sheetNames.index(names)
                    break
            
        self.sheetIndex = i #find out what index to use
        
    def array_out(self):
        #output an array of values for chosen sheet name
        self.pandasDataFrame = self.excelFile.parse(self.sheetNames[self.sheetIndex])
        self.sheetValues = self.pandasDataFrame.values
        return self.sheetValues

class Counter():
    columnIndex = None
    pointData = {}
    cleanData = None
    
    def __init__(self, sheetValues):
        self.sheetValues = sheetValues
        
    def clean_data(self):
        pass
    
    def get_column(self):
        test_list = ['LDI','LAO','LAI','LDO'] #create my test values
        for test_value in test_list:
            if np.any(self.sheetValues == test_value):
                b = np.where(self.sheetValues == test_value)
                self.columnIndex = max(set(list(b[1])), key=list(b[1]).count)
                print('at least one object in your testable point types exists in the data')
                print('column index = ', self.columnIndex, '\n')
                break
    
    def get_dictionary(self):
        unique = set(self.sheetValues[:, self.columnIndex])
        for item in unique:
            self.pointData[item] = max(sum(self.sheetValues == item))




path = r'D:\Project Documents\PointsReportExperiment.xls'
a = Reader(path = path)
a.import_sheet()
a.search_sheet_name()
sheetValues = a.array_out()
df1 = a.excelFile.parse()

sheetname = a.sheetNames
file = a.excelFile
#sheetindex = a.sheetIndex

b = Counter(sheetValues = sheetValues)
b.get_column()
b.get_dictionary()


#columnindex = b.columnIndex
pointData = b.pointData



#print(file)
#print(sheetname)
#print(sheetindex)




