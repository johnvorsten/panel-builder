# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 14:30:02 2019

@author: z003vrzk
"""

# Python imports
import subprocess
from collections import namedtuple
import win32com.client as win32

# Third party imports
import pandas as pd
import os
import numpy as np
import xlsxwriter

# local imports
import DT_sql_tools_v6 as sql_tools

# Instantiate classes
cell = namedtuple('cell',['row','col','data', 'format'])

#%%

class DatabaseValueError(Exception):
    pass

class BOMGenerator(): 
    """BOMGenerator class is used to create system BOM & procurement
    plans. See methods for more explanation"""
    
    def __init__(self, path_mdf, 
                 server_name='.\DT_SQLEXPR2008', 
                 driver_name='SQL Server Native Client 10.0',
                 database_name='PBJobDB'):
        """
        
        Parameters
        ----------
        pathMDF : path to MDF file we are trying to read/write 
            (includes file name ex JOB.DB)
        server_name : (str) name of SQL server
        driver_name : (str) driver name string
        database_name : (str) name of database to connect as
        """
        
        #Begin SQL connection to import data
        self.MySQLHandler = sql_tools.SQLHandling(server_name=server_name, 
                                                    driver_name=driver_name)
        # Attach user specified database
        # MySQLHandler returns a confirmed database name
        # It may be different than what the user requested if that name is 
        # Already in use
        self.database_name = self.MySQLHandler.attach_database(path_mdf, 
                                            database_name=database_name)
                
        
    def get_DEVICES_dataframe(self):
        """Retrieve the DEVICE table from database_name"""
        device_df = self.MySQLHandler.read_table(self.database_name, 
                                                   'DEVICES')
        
        return device_df
            
    
    def get_unique_systems(self):
        """Return a list of unique systems from the database initially connected
        by the instance"""
        
        database_name = self.database_name
        sql = """
        SELECT [SYSTEM]
        FROM [{db_name}].[dbo].[DEVICES]
        GROUP BY [SYSTEM]""".format(db_name=database_name)
        
        df = self.MySQLHandler.pandas_read_sql(sql, database_name)
        
        return df['SYSTEM'].to_list()
    
    
    def report_basic(self, partsDataFrame, systemName):
        """Generate EXCEL report for user validation and PM procurement.
        This BASIC report only outputs part number, quantity, and description
        parameters
        -------
        partsDataFrame : dataframe of part, quantity, description to save to excel format"""
        writer = pd.ExcelWriter('BOM_Report.xlsx', engine='xlsxwriter')
        
        partsDataFrame.to_excel(writer, sheet_name=systemName, startrow= 0, startcol= 0, header=True, index=True)
        writer.save()
        report_path = os.path.join(os.getcwd(), 'reports', 'BOM_Report_basic.xlsx')
        os.system('start EXCEL.EXE ' + report_path)
        
        return None
        
        
    def _generate_doc_header(self, head_start_row=0):
        """Generate a list of 'cell' objects which contain (row, col, data, format)
        information for writing into a workbook
        inptus
        -------
        head_start_row : (int) row to start writing header at
        outputs
        -------
        head_cells : (list) of cell named tuple objects for writing data"""
        
        head_rows = np.arange(0, 5, 1)
        head_cols = np.arange(0, 9, 1)
        xv_head, yv_head = np.meshgrid(head_rows, head_cols)
        
        head_cells = []
        
        # Formatting for document header
        _cell = cell(head_start_row+1, 4, 'Jobsite Address', {'bold':True,
                                                              'italic':None,
                                                              'font_name':'Arial',
                                                              'bg_color':False})
        head_cells.append(_cell)
        _cell = cell(head_start_row+2, 4, '-', {'top':1,'bg_color':'#c5d9f1'})
        head_cells.append(_cell)
        
        _cell = cell(head_start_row+2, 2, 'jobname', {'bold':None,
                                                      'italic':True,
                                                      'font_name':'Arial',
                                                      'bg_color':'#c5d9f1',
                                                      'top':2,'bottom':2,'left':2})
        head_cells.append(_cell)
        
        _cell = cell(head_start_row+2, 3, '44OP-xxxxxx', {'bold':None,
                                                          'italic':True,
                                                          'font_name':'Arial',
                                                          'bg_color':'#c5d9f1',
                                                          'top':2,'bottom':2,'right':2})
        head_cells.append(_cell)
        
        _cell = cell(head_start_row+4, 4, 'Total Material Cost:  ', {'bold':None,'italic':True,'font_name':'Arial','bg_color':False})
        head_cells.append(_cell)
        
        _cell = cell(head_start_row+4, 6, 'Text', {'border':2})
        head_cells.append(_cell)
        
        return head_cells
    
    
    def _generate_node_header(self, system_name, node_start_row=0):  
        """Generate a list of 'cell' objects which contain (row, col, data, format)
        information for writing into a workbook
        inptus
        -------
        node_start_row : (int) row to start writing node header at
        outputs
        -------
        node_cells : (list) of cell named tuple objects for writing data"""
        
        node_rows = np.arange(node_start_row, 9, 1)
        node_cols = np.arange(0, 9, 1)
        xv_node, yv_node = np.meshgrid(node_rows, node_cols)
        
        node_cells = []
        # Formatting for each row
        _cell = cell(node_start_row, 2, 'BOM Node:', {'bold':True,'italic':None,
                                                      'font_name':'Arial',
                                                      'bg_color':False, 'top':2,
                                                      'left':1,'bottom':1})
        node_cells.append(_cell)
        
        _cell = cell(node_start_row, 3, str(system_name), {'bold':True,'italic':None,
                                                    'font_name':'Arial',
                                                    'bg_color':'#c5d9f1',
                                                    'bottom':1,'right':1,'top':2})
        node_cells.append(_cell)
        
        _cell = cell(node_start_row, 5, 'BOM Cost:  ', {'bold':None,'italic':True,
                                                        'font_name':'Arial',
                                                        'bg_color':False,'top':2})
        node_cells.append(_cell)
        
        _cell = cell(node_start_row, 6, 'Text', {'top':2,'bottom':1,
                                                   'left':1,'right':1})
        node_cells.append(_cell)
        
        _cell = cell(node_start_row+1, 2, 'Order Date:', {'bold':None,'italic':True,
                                                          'font_name':'Arial',
                                                          'bg_color':False})
        node_cells.append(_cell)
        
        _cell = cell(node_start_row+1, 3, 'xx/xx/xxxx', {'bold':None,'italic':True,
                                                         'font_name':'Arial',
                                                         'bg_color':'#c5d9f1'})
        node_cells.append(_cell)
          
        _cell = cell(node_start_row+1, 4, 'Ship to: ', {'bold':None,'italic':True,
                                                        'font_name':'Arial',
                                                        'bg_color':'#c5d9f1'})
        node_cells.append(_cell)
        
        _cell = cell(node_start_row+2, 1, 'QTY', {'bold':True,'italic':None,
                                                  'font_name':'Arial',
                                                  'bg_color':False,'left':2,'bottom':1})
        node_cells.append(_cell)
        
        _cell = cell(node_start_row+2, 2, 'Part #', {'bold':True,'italic':None,
                                                     'font_name':'Arial',
                                                     'bg_color':False,'bottom':1})
        node_cells.append(_cell) 
                  
        _cell = cell(node_start_row+2, 3, 'Vendor', {'bold':True,'italic':None,
                                                     'font_name':'Arial',
                                                     'bg_color':False,'bottom':1})
        node_cells.append(_cell)
        
        _cell = cell(node_start_row+2, 4, 'Description', {'bold':True,'italic':None,
                                                          'font_name':'Arial',
                                                          'bg_color':False,'bottom':1})
        node_cells.append(_cell)
        
        _cell = cell(node_start_row+2, 5, 'Est Price (ea)', {'bold':True,'italic':None,
                                                             'font_name':'Arial',
                                                             'bg_color':False,'bottom':1})
        node_cells.append(_cell)
        
        _cell = cell(node_start_row+2, 6, 'Line price', {'bold':True,'italic':None,
                                                         'font_name':'Arial',
                                                         'bg_color':False,'bottom':1})
        node_cells.append(_cell)
        
        _cell = cell(node_start_row+2, 7, 'Ordered', {'bold':True,'italic':None,
                                                      'font_name':'Arial',
                                                      'bg_color':False,'bottom':1})
        node_cells.append(_cell)
        
        _cell = cell(node_start_row+2, 8, 'Comments', {'bold':True,'italic':None,
                                                       'font_name':'Arial',
                                                       'bg_color':False,'bottom':1,
                                                       'right':2})
        node_cells.append(_cell)
        
        # Add borders...
        _cell = cell(node_start_row, 1, '', {'left':2,'top':2})
        node_cells.append(_cell)
        _cell = cell(node_start_row, 4, None, {'top':2})
        node_cells.append(_cell)
        _cell = cell(node_start_row, 5, '', {'top':2})
        node_cells.append(_cell)
        _cell = cell(node_start_row, 7, '', {'top':2})
        node_cells.append(_cell)
        _cell = cell(node_start_row, 8, '', {'top':2,'right':2})
        node_cells.append(_cell)
        _cell = cell(node_start_row+1, 1, '', {'left':2})
        node_cells.append(_cell)
        _cell = cell(node_start_row+1, 8, '', {'right':2})
        node_cells.append(_cell)

        return node_cells

        
    def _autofit_cells(self, filepath, sheetname):
        
        excel = win32.gencache.EnsureDispatch('Excel.Application')
        wb = excel.Workbooks.Open(filepath)
        ws = wb.Worksheets(sheetname)
        ws.Columns.AutoFit()
        wb.Save()
        excel.Application.Quit()
        
        return


    def get_product_database_name(self):
        """Return the database name (not logical or physical) of the associated
        products database. The product database has the logical_name 'ProductDB'
        in SQL server express"""
        
        
        sql = """select t1.[name] as logical_name, t1.physical_name,
                    (select name 
                    from [master].[sys].[databases] as t2
                    where t2.database_id = t1.database_id) as [database_name]
                FROM [sys].[master_files] as t1
                where [name] = 'ProductDB'"""
        
        
        df = self.MySQLHandler.pandas_read_sql(sql, 'master')
        if df.shape[0] == 0:
            return None
        else:
            product_database_name = df.loc[0, 'database_name']
        
        return product_database_name

    def get_parts_dataframe(self, database_name, system):
        """Run a sql query to retrieve a dataframe of unique parts in 'system' 
        aggregated on 'PARTNO' in 'DEVICES' and 'QUANTITY' of parts are summed
        The resulting dataframe has columns 
        ['PARTNO','QUANTITY','DESCRIPTION','RETRO']
        inputs
        -------
        database_name : (str) name of SQL database
        system : (str) name of 'SYSTEM' in 'DEVICES' table
        outputs
        -------
        df : (pandas.DataFrame)
        
        Example usage
        database_name = 'PBJobDB'
        retro_flag = 'IS NULL'
        system = '100 AHU-B1'
        
        MyBomGenerator = BOMGenerator(pathMDF)
        df = MyBomGenerator.get_parts_dataframe(database_name, retro_flag, system)
        """
        
        
        table_name = 'DEVICES'
        prodcut_db = self.get_product_database_name()
        
        sql_aggregate = """
        select t1.PARTNO, sum(t1.QUANTITY) AS QUANTITY, t1.RETRO,

        	(SELECT TOP(1) DESCRIPT
        	from [{db_name}].[dbo].[{table_name}] AS t2
        	where t2.PARTNO = t1.PARTNO
        	group by DESCRIPT
        	order by count(*) DESC) AS [DESCRIPT], 
        
        	(SELECT VENDOR
        	FROM [{product_db}].[dbo].[PRODUCT] AS t3
        	WHERE t3.PARTNO = t1.PARTNO) AS [VENDOR],
        
        	(SELECT MATER_COST
        	FROM [{product_db}].[dbo].[PRODUCT] AS t4
        	WHERE t4.PARTNO = t1.PARTNO) as [MATER_COST]
    
        FROM [{db_name}].[dbo].[{table_name}] AS t1
        WHERE [SYSTEM] = '{system}'
        GROUP BY t1.PARTNO, t1.RETRO""".format(db_name=database_name, 
                                    table_name=table_name, 
                                    system=system,
                                    product_db=prodcut_db)
        
        df = self.MySQLHandler.pandas_read_sql(sql_aggregate, 
                                                 database_name)
        
        # Clean nan values
        for row in df.itertuples(index=True):
            if row.RETRO is None:
                df.loc[row.Index, 'RETRO'] = ''
                
        df = df.fillna('N/A')
        
        return df
    
    @staticmethod
    def _get_line_price_formula(current_row):
        """Multiple quantity and item price with an excel formula.
        Excel is 1-indexed and xlswriter is 0-indexed"""
        
        formula_str = '=F{row_num} * B{row_num}'.format(row_num=current_row + 1)
        
        return formula_str
    
    @staticmethod
    def _get_bom_price_formula(col_start, row_start, col_end, row_end):
        """Return an excel formula to find the sum of a range of cells
        The range of cells is variable based on number of parts and where the formula
        should be inserted
        col_start : (str) letter of column
        row_start : (int or str) start row (0 indexed like xlswriter)
        col_end : (str) letter of column to stop summing at
        row_end : (int or str) end row (0 indexed like xlswriter)"""
        
        formula_str = '=SUM({0}{1}:{2}{3})'.format(col_start, 
                                                  int(row_start)+1, 
                                                  col_end, 
                                                  int(row_end)+1)
        
        return formula_str
    
    def _create_report_directory(self, directory):
        """Create a directory specified if there is none created yet"""
        
        if os.path.isdir(directory):
            return None
        else:
            try:
                os.mkdir(directory)
            except FileNotFoundError:
                os.mkdir(os.path.split(directory)[0])
                os.mkdir(directory)
            
        return None
    
    def generate_fancy_report(self, retro_flags, unique_systems):
        """
        inputs
        -------
        retro_flags : (list of str) user input of which retro flags to include
            Can include any or all of ['IS NULL',"= '+'","= '*'"]
        system_names : (list of str) user input of which systems to output
            on the BOM. """
        
        # Instantiate a connection and attach the table
        database_name = self.database_name
        
        # Clean user input for system_names
        database_systems = self.get_unique_systems()
        msg = ('The system {} does not exist in the specified database. Please' + 
               'revise the list of unique_systems that are being requested')
        for system_name in unique_systems:
            assert system_name in database_systems, msg.format(system_name)
            
        # Create workbook and worksheet
        report_path = os.path.join(os.getcwd(), 'reports', 'BOM_Report.xlsx')
        self._create_report_directory(os.path.join(os.getcwd(), 'reports'))
        sheetname = 'BOM_Report'
        
        head_start = 0 # Where to start printing main head
        node_start = 0 # Where to start printing 
        n_node_rows = 3 # node header rows
        n_head_rows = 6 # Rows until start of first node_head
        blank_rows = 2 # Number of blank between nodes
        
        head_cells = self._generate_doc_header(head_start)
        
        workbook = xlsxwriter.Workbook(report_path)
        worksheet = workbook.add_worksheet(sheetname)
        left_border = workbook.add_format({'left':2})
        right_border = workbook.add_format({'right':2})
        bom_cost_border = workbook.add_format({'top':2,'left':1,'right':1,'bottom':1})
        cell_format_green = workbook.add_format({'bg_color':   '#C6EFCE'})
        cell_format_red = workbook.add_format({'bg_color':   '#FFC7CE'})
        
        # Write header data
        for row, col, data, formatDict in head_cells:
            worksheet.write(row, col, data, workbook.add_format(formatDict))
        
        current_row = node_start + n_head_rows
        for system_name in unique_systems:
            
            # Get part data
            parts_df = self.get_parts_dataframe(database_name, 
                                                system=system_name)
            
            if 'IS NULL' not in retro_flags:
                index = parts_df[[part is None for part in parts_df['RETRO']]].index
                parts_df.drop(index=index, inplace=True)
            if "= '+'" not in retro_flags:
                index = parts_df[parts_df['RETRO'] == '+'].index
                parts_df.drop(index=index, inplace=True)
            if "= '*'" not in retro_flags:
                index = parts_df[parts_df['RETRO'] == '*'].index
                parts_df.drop(index=index, inplace=True)
            
            # Write node data (BOM header)
            node_cells = self._generate_node_header(system_name, node_start_row=0)
            for row, col, data, formatDict in node_cells:
                worksheet.write(row + current_row, col, data, workbook.add_format(formatDict))
            
            # Write a BOM cost formula...
            formula_str = self._get_bom_price_formula('G', current_row+3, 'G', current_row+3+parts_df.shape[0]-1)
            worksheet.write(current_row, 6, formula_str, bom_cost_border)
            
            current_row += n_node_rows
            
            # Write conditional formatting
            worksheet.conditional_format(current_row, 
                                         7,
                                         current_row + parts_df.shape[0] - 1, 
                                         7,
                                         {'type':'cell',
                                          'criteria':'not equal to',
                                          'value':'"y"',
                                          'format':cell_format_red})
            worksheet.conditional_format(7, 
                                         current_row, 
                                         7, 
                                         current_row + parts_df.shape[0] - 1, 
                                         {'type':'cell',
                                          'criteria':'equal to',
                                          'value':'"y"',
                                          'format':cell_format_green})
            
            # Write part data
            for part in parts_df.iterrows():
                worksheet.write(current_row, 1, part[1]['QUANTITY'], left_border)
                worksheet.write(current_row, 2, part[1]['PARTNO'], {})
                worksheet.write(current_row, 3, part[1]['VENDOR'], {})
                worksheet.write(current_row, 4, part[1]['DESCRIPT'], {})
                worksheet.write(current_row, 5, part[1]['MATER_COST'], {})
                worksheet.write(current_row, 6, self._get_line_price_formula(current_row))
                worksheet.write(current_row, 8, part[1]['RETRO'], right_border)
                current_row += 1
            
            # Increment row with blanks and head
            current_row += blank_rows
            
        workbook.close()
        
        # Autofit columns
        self._autofit_cells(report_path, sheetname)
        
        subprocess.run('start EXCEL.exe %s' %report_path, shell=True)
        
        return
    
