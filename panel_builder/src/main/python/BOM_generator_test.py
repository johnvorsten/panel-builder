# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 09:15:30 2020

@author: z003vrzk
"""
# Python imports
import os, unittest

# Third party imports

# Local imports
from BOM_generator import BOMGenerator
from sql_tools import SQLBase

#%%


def Test(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)

        server_name = '.\DT_SQLEXPRESS'
        driver_name = 'SQL Server Native Client 11.0'
        path_mdf = r"C:\Users\z003vrzk\.spyder-py3\Scripts\Work\PanelBuilder\panel_builder\SQLTest\JHW\JobDB.mdf"
        path_ldf = r"C:\Users\z003vrzk\.spyder-py3\Scripts\Work\PanelBuilder\panel_builder\SQLTest\JHW\JobDB_Log.ldf"
        database_name = 'PBJobDB_test'

        sqlbase = SQLBase(server_name, driver_name)
        # Check to see if a database already exists
        (file_used_bool,
         name_used_bool,
         existing_database_name) = sqlbase.check_existing_database(path_mdf, database_name)
        # Attach a database on path_mdf
        if not any((file_used_bool, name_used_bool)):
            sqlbase.attach_database(path_mdf, path_ldf, database_name)
        else:
            # The database is already attached
            pass

        sqlbase.init_database_connection(database_name)

        return None

    def test_get_DEVICES_dataframe(self):

        # Create bom generator
        bom = BOMGenerator(path_mdf, path_ldf, path_j_vars, database_name, sqlbase)

        get_DEVICES_dataframe


        return None

    def test_report_basic(self):
        return None

    def test_get_parts_dataframe(self):
        return None

    def test__get_line_price_formula(self):
        return None

    def test__get_bom_price_formula(self):
        return None

    def test__create_report_directory(self):
        return None

    def test_generate_report_larson(self):
        """Testing for BOMGenerator class larson report style"""

        path_mdf = os.path.join(r"C:\Users\z003vrzk\.spyder-py3\Scripts\Work\PanelBuilder\panel-builder\SQLTest\JHW", "JobDB.mdf")
        path_jvars = os.path.join(r"C:\Users\z003vrzk\.spyder-py3\Scripts\Work\PanelBuilder\panel-builder\SQLTest\JHW", "j_vars.ini")
        server_name = '.\DT_SQLEXPR2008'
        driver_name = 'SQL Server Native Client 10.0'
        database_name = 'PBJobDB'
        # Instantiate class
        MyBomGenerator = BOMGenerator(path_mdf,
                                      path_jvars,
                                      server_name=server_name,
                                      driver_name=driver_name,
                                      database_name=database_name)

        # Product database name (look up prices for parts)
        product_db_name = MyBomGenerator.get_product_database_name()

        # All devices within a project
        devices_df = MyBomGenerator.get_DEVICES_dataframe()

        MyBomGenerator.generate_report_larson(retro_flags=['IS NULL',"= '+'","= '*'"],
                                             unique_systems=unique_systems)

        return None

    def test_generate_report_standard(self):

        server_name = '.\DT_SQLEXPRESS'
        driver_name = 'SQL Server Native Client 11.0'
        path_mdf = r"C:\Users\z003vrzk\.spyder-py3\Scripts\Work\panel_builder\SQLTest\JHW\JobDB.mdf"
        path_ldf = r"C:\Users\z003vrzk\.spyder-py3\Scripts\Work\panel_builder\SQLTest\JHW\JobDB_Log.ldf"
        path_j_vars = r"C:\Users\z003vrzk\.spyder-py3\Scripts\Work\panel_builder\SQLTest\JHW\j_vars.ini"
        database_name = 'PBJobDB_test'

        sqlbase = SQLBase(server_name, driver_name)
        # Check to see if a database already exists
        (file_used_bool,
         name_used_bool,
         existing_database_name) = sqlbase.check_existing_database(path_mdf, database_name)
        # Attach a database on path_mdf
        if not any((file_used_bool, name_used_bool)):
            sqlbase.attach_database(path_mdf, path_ldf, database_name)
        else:
            # The database is already attached
            database_name = existing_database_name
            pass

        sqlbase.init_database_connection(database_name)


        # Generate report
        BomGenerator = BOMGenerator(path_mdf,
                                    path_ldf,
                                    path_j_vars,
                                    database_name,
                                    sqlbase)

        # Unique systems to include in report
        sql = """
        SELECT [SYSTEM]
        FROM [{db_name}].[dbo].[DEVICES]
        GROUP BY [SYSTEM]""".format(db_name=database_name)
        df = sqlbase.pandas_execute_sql(sql)
        unique_systems = df['SYSTEM'].to_list()

        # Location of products database
        sql = """select t1.[name] as logical_name, t1.physical_name,
                    (select name
                    from [master].[sys].[databases] as t2
                    where t2.database_id = t1.database_id) as [database_name]
                FROM [master].[sys].[master_files] as t1
                where [name] = 'ProductDB'"""


        df = sqlbase.pandas_execute_sql(sql)
        if df.shape[0] == 0:
            product_db = None
        else:
            product_db = df.loc[0, 'database_name']

        # Flags to include
        retro_flags=['IS NULL',"= '+'","= '*'"]

        # Generate report
        BomGenerator.generate_report_standard(retro_flags=retro_flags,
                                              unique_systems=unique_systems,
                                              product_db=product_db)

        return None

    def test_generate_fancy_report(self):
        return None



class Test_BOM_Format(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(Test_BOM_Format, self).__init__(*args, **kwargs)

        return None

    def test_(self):
        return None

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