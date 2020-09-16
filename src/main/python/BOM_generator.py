# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 14:30:02 2019

@author: z003vrzk
"""

# Python imports
import subprocess, os
from collections import namedtuple
import win32com.client as win32
from datetime import datetime

# Third party imports
import pandas as pd
import xlsxwriter

# local imports
from read_j_vars import read_vars_to_dict

# Instantiate classes
cell = namedtuple('cell',['row','col','data', 'format'])

#%%

class DatabaseValueError(Exception):
    pass

class BOMGenerator():
    """BOMGenerator class is used to create system BOM & procurement
    plans. See methods for more explanation"""

    def __init__(self,
                 path_mdf,
                 path_ldf,
                 path_j_vars,
                 database_name,
                 SQLBase):
        """
        inputs
        -------
        path_mdf : (str) path to master database file (MSSQL)
        path_ldf : (str) path to log database file (MSSQL)
        path_j_vars : (str) path to j_vars.ini file found in each job folder
        database_name : (str) name of database to connect as
        SQLBase : (sql_tools.SQLBase) class with instantiated database
            connection
        """

        #Begin SQL connection to import data
        self.SQLBase = SQLBase

        """Make sure the SQLBase class passed already has an active
        Database connection
        The Qt Application should instantiate and handle SQL database connections
        It is not the responsibility of this class to handle database
        connections"""
        if 'database_connection' not in self.SQLBase.__dict__:
            msg=('database connection is not instantiated. There may be an' +
                 ' issue with Qt Instantiating a connection')
            raise NameError(msg)

        """The database and name should already be connected
        Verify this through SQLBase
        If a database is already attached then file_used_bool will be True
        If name_used_bool is True then the logical database name is in use
        existing_database_name is a string if file_used_bool is True"""
        (file_used_bool,
         name_used_bool,
         existing_database_name) = self.SQLBase\
            .check_existing_database(path_mdf, database_name)

        msg='The selected MDF File {} is not connected to SQL Server'
        assert(file_used_bool == True), msg.format(path_mdf)
        msg=('The selected database name {} does not currently exist in SQL' +
             ' Server')
        assert(name_used_bool == True), msg.format(database_name)
        msg=('The passed database_name and database name connected to SQL' +
            ' Server do not match. Got {}, expected {}')
        msg = msg.format(database_name, existing_database_name)
        assert(existing_database_name == database_name), msg

        # Instantiate a BOMFormat class
        self.BOMFormat = BOMFormat(path_j_vars)

        # Class attributes
        self.database_name = database_name

        return None


    def get_DEVICES_dataframe(self):
        """Retrieve the DEVICE table from database_name"""
        sql = """SELECT * FROM [DEVICES]"""
        device_df = self.SQLBase.pandas_execute_sql(sql)
        return device_df


    def report_basic(self, partsDataFrame, systemName):
        """Generate EXCEL report for user validation and PM procurement.
        This BASIC report only outputs part number, quantity, and description
        parameters
        -------
        partsDataFrame : dataframe of part, quantity, description to save to
        excel format"""
        writer = pd.ExcelWriter('BOM_Report.xlsx', engine='xlsxwriter')

        partsDataFrame.to_excel(writer,
                                sheet_name=systemName,
                                startrow= 0,
                                startcol= 0,
                                header=True,
                                index=True)
        writer.save()
        report_path = os.path.join(os.getcwd(),
                                   'reports',
                                   'BOM_Report_basic.xlsx')
        os.system('start EXCEL.EXE ' + report_path)

        return None


    def _autofit_cells(self, filepath, sheetname):

        excel = win32.gencache.EnsureDispatch('Excel.Application')
        wb = excel.Workbooks.Open(filepath)
        ws = wb.Worksheets(sheetname)
        ws.Columns.AutoFit()
        wb.Save()
        excel.Application.Quit()

        return


    def get_parts_dataframe(self, database_name, system, product_db):
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
                                    product_db=product_db)

        df = self.SQLBase.pandas_execute_sql(sql_aggregate)

        # Clean nan values
        for row in df.itertuples(index=True):
            if row.RETRO is None:
                df.loc[row.Index, 'RETRO'] = ''

        df = df.fillna('N/A')

        return df

    @staticmethod
    def _get_line_price_formula(current_row, col1, col2):
        """Multiple quantity and item price with an excel formula.
        Excel is 1-indexed and xlswriter is 0-indexed
        current_row : (int) row to write foumula at
        col1 : (str) index/letter of cell column at current row to muliply in
        formula
        col2 : (str) index/letter of cell column at current row to muliply in
        formula"""

        formula_str = '={col1}{row_num} * {col2}{row_num}'.format(col1=col1,
                         col2=col2,
                         row_num=current_row + 1)

        return formula_str


    @staticmethod
    def _get_bom_price_formula(col_start, row_start, col_end, row_end):
        """Return an excel formula to find the sum of a range of cells
        The range of cells is variable based on number of parts and
        where the formula should be inserted
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


    def generate_report_standard(self, retro_flags, unique_systems, product_db):
        """
        inputs
        -------
        retro_flags : (list of str) user input of which retro flags to include
            Can include any or all of ['IS NULL',"= '+'","= '*'"]
        unique_systems : (list of str) user input of which systems to output
            on the BOM"""

        # Instantiate a connection and attach the table
        database_name = self.database_name

        # Initial Values
        head_start = 0 # Where to start printing main document header
        node_start = 0 # Where to start printing each node
        n_node_rows = 1 # Number of rows for a specific BOM node header
        n_head_rows = 6 # Rows until start of first node_head
        blank_rows = 1 # Number of blank between nodes

        # Create workbook and worksheet
        report_path = os.path.join(os.getcwd(), 'reports', 'BOM_Report.xlsx')
        self._create_report_directory(os.path.join(os.getcwd(), 'reports'))
        sheetname = 'BOM_Report'
        workbook = xlsxwriter.Workbook(report_path)
        worksheet = workbook.add_worksheet(sheetname)
        currency = workbook.add_format({'font_name':'Arial',
                                      'italic':True,
                                      })
        cell_format_green = workbook.add_format({'bg_color':   '#C6EFCE'})
        cell_format_red = workbook.add_format({'bg_color':   '#FFC7CE'})

        # Head cells are written once for the 'header' of the report
        head_cells = self.BOMFormat._generate_doc_header_std(head_start_row=head_start)
        # Write header data
        for row, col, data, formatDict in head_cells:
            worksheet.write(row, col, data, workbook.add_format(formatDict))

        current_row = node_start + n_head_rows
        for system_name in unique_systems:

            # Get part data
            parts_df = self.get_parts_dataframe(database_name,
                                                system=system_name,
                                                product_db=product_db)

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
            # This report style will include (1) Node cost, and a name
            node_cells = self.BOMFormat.\
                _generate_node_header_std(system_name, node_start_row=0)
            for row, col, data, formatDict in node_cells:
                worksheet.write(row + current_row, col, data, workbook.add_format(formatDict))

            # Write a BOM cost formula
            formula_str = self._get_bom_price_formula('J',
                                                      current_row + 1,
                                                      'J',
                                                      current_row + 1 + parts_df.shape[0]-1)
            worksheet.write(current_row, 8, formula_str, currency)

            # Increment the current row to write at
            current_row += n_node_rows

            # Write conditional formatting
            worksheet.conditional_format(current_row,
                                         0,
                                         current_row + parts_df.shape[0] - 1,
                                         0,
                                         {'type':'cell',
                                          'criteria':'not equal to',
                                          'value':'"y"',
                                          'format':cell_format_red})
            worksheet.conditional_format(0,
                                         current_row,
                                         0,
                                         current_row + parts_df.shape[0] - 1,
                                         {'type':'cell',
                                          'criteria':'equal to',
                                          'value':'"y"',
                                          'format':cell_format_green})

            # Write part data
            for part in parts_df.iterrows():
                worksheet.write(current_row, 2, part[1]['QUANTITY'], {}) # Qty
                worksheet.write(current_row, 3, part[1]['PARTNO'], {}) # Component
                worksheet.write(current_row, 4, part[1]['PARTNO'], {}) # Part Number
                worksheet.write(current_row, 5, part[1]['VENDOR'], {}) # Vendor
                # Vendor number - not shown
                worksheet.write(current_row, 7, part[1]['DESCRIPT'], {}) # Description
                worksheet.write(current_row, 8, part[1]['MATER_COST'], {}) # Est price (ea)
                worksheet.write(current_row, 9, self._get_line_price_formula(current_row,
                                                                             col1='C',
                                                                             col2='I')) # Line Price
                worksheet.write(current_row, 10, part[1]['RETRO'], {}) # Notes
                current_row += 1

            # Increment row with blanks and head
            current_row += blank_rows

        workbook.close()

        # Autofit columns
        self._autofit_cells(report_path, sheetname)

        subprocess.run('start EXCEL.exe "%s"' %report_path, shell=True)

        return

    def generate_report_larson(self, retro_flags, unique_systems, product_db):
        """
        inputs
        -------
        retro_flags : (list of str) user input of which retro flags to include
            Can include any or all of ['IS NULL',"= '+'","= '*'"]
        system_names : (list of str) user input of which systems to output
            on the BOM."""

        # Instantiate a connection and attach the table
        database_name = self.database_name

        # Initial Values
        head_start = 0 # Where to start printing main head
        node_start = 0 # Where to start printing
        n_node_rows = 3 # node header rows
        n_head_rows = 6 # Rows until start of first node_head
        blank_rows = 2 # Number of blank between nodes

        # Create workbook and worksheet
        report_path = os.path.join(os.getcwd(), 'reports', 'BOM_Report.xlsx')
        # Create report directory if it does not already exist
        self._create_report_directory(os.path.join(os.getcwd(), 'reports'))
        sheetname = 'BOM_Report'
        workbook = xlsxwriter.Workbook(report_path)
        worksheet = workbook.add_worksheet(sheetname)
        left_border = workbook.add_format({'left':2})
        right_border = workbook.add_format({'right':2})
        bom_cost_border = workbook.add_format({'top':2,'left':1,'right':1,'bottom':1})
        cell_format_green = workbook.add_format({'bg_color':   '#C6EFCE'})
        cell_format_red = workbook.add_format({'bg_color':   '#FFC7CE'})

        # Head cells are written once for the 'header' of the report
        head_cells = self.BOMFormat._generate_doc_header_larson(head_start_row=head_start)

        # Write header data
        for row, col, data, formatDict in head_cells:
            worksheet.write(row, col, data, workbook.add_format(formatDict))

        current_row = node_start + n_head_rows
        for system_name in unique_systems:

            # Get part data
            parts_df = self.get_parts_dataframe(database_name,
                                                system=system_name,
                                                product_db=product_db)

            if 'IS NULL' not in retro_flags:
                index = parts_df[[part is None for part in parts_df['RETRO']]].index
                parts_df.drop(index=index, inplace=True)
            if "= '+'" not in retro_flags:
                index = parts_df[parts_df['RETRO'] == '+'].index
                parts_df.drop(index=index, inplace=True)
            if "= '*'" not in retro_flags:
                index = parts_df[parts_df['RETRO'] == '*'].index
                parts_df.drop(index=index, inplace=True)

            # Write node data (A header for each individual BOM node)
            node_cells = self.BOMFormat.\
                _generate_node_header_larson(system_name, node_start_row=0)
            for row, col, data, formatDict in node_cells:
                worksheet.write(row + current_row,
                                col,
                                data,
                                workbook.add_format(formatDict))

            # Write a BOM cost formula
            formula_str = self._get_bom_price_formula('G',
                                                      current_row+3,
                                                      'G',
                                                      current_row+3+parts_df.shape[0]-1)
            worksheet.write(current_row, 6, formula_str, bom_cost_border)

            current_row += n_node_rows

            # Write conditional formatting for 'ordered' column
            # Columns are green if material has been ordered ('y' in cell)
            # Write formatting from current row to end of individual BOM node
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
                worksheet.write(current_row, 6, self._get_line_price_formula(current_row,
                                                                             col1='B',
                                                                             col2='F'))
                worksheet.write(current_row, 8, part[1]['RETRO'], right_border)
                current_row += 1

            # Increment row with blanks and head
            current_row += blank_rows

        workbook.close()

        # Autofit columns
        self._autofit_cells(report_path, sheetname)

        subprocess.run('start EXCEL.exe "%s"' %report_path, shell=True)

        return


    def generate_fancy_report(self, retro_flags, unique_systems, style):
        """
        inputs
        -------
        retro_flags : (list of str) user input of which retro flags to include
            Can include any or all of ['IS NULL',"= '+'","= '*'"]
        system_names : (list of str) user input of which systems to output
            on the BOM.
        style : (str) style of report to generate. This affects the rows
            and visual style of the outputted EXCEL workbook. One of 'larson' or
            'standard"""

        head_start = 0 # Where to start printing main head

        # Instantiate a connection and attach the table
        database_name = self.database_name

        # Create workbook and worksheet
        report_path = os.path.join(os.getcwd(), 'reports', 'BOM_Report.xlsx')
        self._create_report_directory(os.path.join(os.getcwd(), 'reports'))
        sheetname = 'BOM_Report'
        workbook = xlsxwriter.Workbook(report_path)
        worksheet = workbook.add_worksheet(sheetname)
        left_border = workbook.add_format({'left':2})
        right_border = workbook.add_format({'right':2})
        bom_cost_border = workbook.add_format({'top':2,'left':1,'right':1,'bottom':1})
        cell_format_green = workbook.add_format({'bg_color':   '#C6EFCE'})
        cell_format_red = workbook.add_format({'bg_color':   '#FFC7CE'})


        # Generate document header and configure each report style
        if style == 'larson':
            head_cells = self.BOMFormat._generate_doc_header_larson(head_start)
            # Initial Values
            head_start = 0 # Where to start printing main head
            node_start = 0 # Where to start printing
            n_node_rows = 3 # node header rows
            n_head_rows = 6 # Rows until start of first node_head
            blank_rows = 2 # Number of blank between nodes

        elif style == 'standard':
            head_cells = self.BOMFormat._generate_doc_header_std(head_start_row=head_start)
            # Initial Values
            head_start = 0 # Where to start printing main head
            node_start = 0 # Where to start printing
            n_node_rows = 0 # node header rows
            n_head_rows = 5 # Rows until start of first node_head
            blank_rows = 1 # Number of blank between nodes

        else:
            raise ValueError('Improper configuration of workbook style')

        # Write header data
        for row, col, data, formatDict in head_cells:
            worksheet.write(row, col, data, workbook.add_format(formatDict))

        # Write part data
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
            formula_str = self._get_bom_price_formula('G',
                                                      current_row+3,
                                                      'G',
                                                      current_row+3+parts_df.shape[0]-1)
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
                worksheet.write(current_row, 6, self._get_line_price_formula(current_row,
                                                                             col1='B',
                                                                             col2='F'))
                worksheet.write(current_row, 8, part[1]['RETRO'], right_border)
                current_row += 1

            # Increment row with blanks and head
            current_row += blank_rows

        workbook.close()

        # Autofit columns
        self._autofit_cells(report_path, sheetname)

        subprocess.run('start EXCEL.exe "%s"' %report_path, shell=True)

        return



class BOMFormat:

    def __init__(self, initialization_file_path):
        """
        inputs
        -------
        initialization_file_path : (str) or path to j_vars.ini file that stores
        design tool job related information"""

        self.initialization_dict = read_vars_to_dict(initialization_file_path)

        return None


    def _generate_doc_header_std(self, head_start_row=0):
        """Generate a list of 'cell' objects which contain (row, col, data, format)
        information for writing into a workbook.  Standard formatting
        inptus
        -------
        head_start_row : (int) row to start writing header at
        outputs
        -------
        head_cells : (list) of cell named tuple objects for writing data"""

        head_cells = []
        # Formatting dictionaries
        standard = {'font_name':'Arial'}
        bold = {'bold':True,
                'font_name':'Arial'}
        underline_bold = {'bold':True,
                          'font_name':'Arial',
                          'bottom':1}

        # Retrieve information from job variables file .ini
        job_name = self.initialization_dict['j_name']
        job_number = self.initialization_dict['j_number']
        project_manager = self.initialization_dict['j_brncon']
        project_engineer = self.initialization_dict['j_engr']

        # Formatting for document header
        _cell = cell(head_start_row+0, 0, 'Project Name', bold)
        head_cells.append(_cell)
        _cell = cell(head_start_row+0, 1, job_name, standard)
        head_cells.append(_cell)

        _cell = cell(head_start_row+1, 0, 'Project #', bold)
        head_cells.append(_cell)
        _cell = cell(head_start_row+1, 1, job_number, standard)
        head_cells.append(_cell)

        _cell = cell(head_start_row+2, 0, 'Project Manager', bold)
        head_cells.append(_cell)
        _cell = cell(head_start_row+2, 1, project_manager, standard)
        head_cells.append(_cell)

        _cell = cell(head_start_row+3, 0, 'Eng.', bold)
        head_cells.append(_cell)
        _cell = cell(head_start_row+3, 1, project_engineer, standard)
        head_cells.append(_cell)

        # Total project cost
        _cell = cell(head_start_row+1, 8, 'Total Material Cost', bold)
        head_cells.append(_cell)
        _cell = cell(head_start_row+2, 8, '=SUM(J:J)', bold)
        head_cells.append(_cell)

        # Individual BOM headers
        _cell = cell(head_start_row+5, 0, 'Ordered', underline_bold)
        head_cells.append(_cell)
        _cell = cell(head_start_row+5, 1, 'BOM Name', underline_bold)
        head_cells.append(_cell)
        _cell = cell(head_start_row+5, 2, 'Qty', underline_bold)
        head_cells.append(_cell)
        _cell = cell(head_start_row+5, 3, 'Component', underline_bold)
        head_cells.append(_cell)
        _cell = cell(head_start_row+5, 4, 'Part Number', underline_bold)
        head_cells.append(_cell)
        _cell = cell(head_start_row+5, 5, 'Vendor', underline_bold)
        head_cells.append(_cell)
        _cell = cell(head_start_row+5, 6, 'Vendor Number', underline_bold)
        head_cells.append(_cell)
        _cell = cell(head_start_row+5, 7, 'Description', underline_bold)
        head_cells.append(_cell)
        _cell = cell(head_start_row+5, 8, 'Est Price (ea)', underline_bold)
        head_cells.append(_cell)
        _cell = cell(head_start_row+5, 9, 'Line Price', underline_bold)
        head_cells.append(_cell)
        _cell = cell(head_start_row+5, 10, 'Notes', underline_bold)
        head_cells.append(_cell)
        _cell = cell(head_start_row+5, 11, 'Tracking', underline_bold)
        head_cells.append(_cell)

        return head_cells

    def _generate_node_header_std(self, system_name, node_start_row=0):
        """Generate a list of 'cell' objects which contain (row, col, data, format)
        information for writing into a workbook.  OG Larson format
        inptus
        -------
        system_name : (str) name of BOM node
        node_start_row : (int) row to start writing node header at
        outputs
        -------
        node_cells : (list) of cell named tuple objects for writing data"""

        # Spreadsheet cells
        node_cells = []

        # Formatting dictionaries
        standard = {'font_name':'Arial'}
        italic = {'italic':True}

        # Cells
        _cell = cell(node_start_row+1, 1, system_name, standard)
        node_cells.append(_cell)
        _cell = cell(node_start_row, 7, 'Node Cost : ', italic)
        node_cells.append(_cell)

        return node_cells


    def _generate_doc_header_larson(self, head_start_row=0):
        """Generate a list of 'cell' objects which contain (row, col, data, format)
        information for writing into a workbook. OG Larson format
        inptus
        -------
        head_start_row : (int) row to start writing header at
        outputs
        -------
        head_cells : (list) of cell named tuple objects for writing data"""

        head_cells = []

        # Formatting for document header
        _cell = cell(head_start_row+1, 4, 'Jobsite Address', {'bold':True,
                                                              'italic':None,
                                                              'font_name':'Arial',
                                                              'bg_color':False})
        head_cells.append(_cell)
        _cell = cell(head_start_row+2, 4, (self.initialization_dict['j_add1'] +
                                           self.initialization_dict['j_add2'] +
                                           self.initialization_dict['j_city'] +
                                           self.initialization_dict['j_zip']),
                                            {'top':1,'bg_color':'#c5d9f1'})
        head_cells.append(_cell)

        _cell = cell(head_start_row+2, 2, self.initialization_dict['j_name'],
                                                     {'bold':None,
                                                      'italic':True,
                                                      'font_name':'Arial',
                                                      'bg_color':'#c5d9f1',
                                                      'top':2,'bottom':2,'left':2})
        head_cells.append(_cell)

        _cell = cell(head_start_row+2, 3, self.initialization_dict['j_number'],
                     {'bold':None,
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


    def _generate_node_header_larson(self, system_name, node_start_row=0):
        """Generate a list of 'cell' objects which contain (row, col, data, format)
        information for writing into a workbook.  OG Larson format
        inptus
        -------
        system_name : (str) name of BOM node
        node_start_row : (int) row to start writing node header at
        outputs
        -------
        node_cells : (list) of cell named tuple objects for writing data"""

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