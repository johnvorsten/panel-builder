# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 15:47:21 2020

@author: z003vrzk
"""

# Python imports
import os

# Third party imports
import xlsxwriter

# Local imports
from BOM_formatting import BOMFormat


#%% 

if __name__ == '__main__':
    """Testing for BOMFormat class"""

    initialization_file_path = os.path.join(r"C:\Users\z003vrzk\.spyder-py3\Scripts\Work\PanelBuilder\panel-builder\SQLTest\JHW", "j_vars.ini")
    # Instantiate class
    MyBomFormatter = BOMFormat(initialization_file_path)
    
    # Look at job variables
    for key, val in MyBomFormatter.initialization_dict.items():
        print(key, val)
        
        
    # Create workbook and worksheet
    report_path = os.path.join(os.getcwd(), 'reports', 'BOM_Report.xlsx')

    sheetname = 'BOM_Report'
    workbook = xlsxwriter.Workbook(report_path)
    worksheet = workbook.add_worksheet(sheetname)
    bom_cost_border = workbook.add_format({'top':2,'left':1,'right':1,'bottom':1})
    cell_format_green = workbook.add_format({'bg_color':   '#C6EFCE'})
    cell_format_red = workbook.add_format({'bg_color':   '#FFC7CE'})
        
        
    head_cells = MyBomFormatter._generate_doc_header_std(head_start_row=0)
    for row, col, data, formatDict in head_cells:
        # print(data, formatDict)
        print(type(data))
        print(type(formatDict))
        worksheet.write(row, col, data, workbook.add_format(formatDict))