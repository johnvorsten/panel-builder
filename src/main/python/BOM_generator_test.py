# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 09:15:30 2020

@author: z003vrzk
"""
# Python imports
import os, unittest

# Third party imports
import pandas as pd

# Local imports
from BOM_generator import BOMGenerator, BOMFormat
from sql_tools import SQLBase

#%%


class Test_BOM_Generator(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(Test_BOM_Generator, self).__init__(*args, **kwargs)

        global sqlbase, BomGenerator, server_name, driver_name, path_mdf
        global path_ldf, path_j_vars, database_name, product_db

        server_name = '.\DT_SQLEXPRESS'
        driver_name = 'SQL Server Native Client 11.0'
        path_mdf = r"C:\Users\z003vrzk\.spyder-py3\Scripts\Work\panel_builder\SQLTest\JHW\JobDB.mdf"
        path_ldf = r"C:\Users\z003vrzk\.spyder-py3\Scripts\Work\panel_builder\SQLTest\JHW\JobDB_Log.ldf"
        path_j_vars = r"C:\Users\z003vrzk\.spyder-py3\Scripts\Work\panel_builder\SQLTest\JHW\j_vars.ini"
        database_name = 'PBJobDB_test'
        product_db = 'ProductDB'

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

        BomGenerator = BOMGenerator(path_mdf,
                                    path_ldf,
                                    path_j_vars,
                                    database_name,
                                    sqlbase)
        return None

    def test_get_DEVICES_dataframe(self):

        # Get all objects from DEVICES SQL table
        devices = BomGenerator.get_DEVICES_dataframe()

        # Test result (shold I test the exact results?)
        part = devices['PARTNO'].iloc[0]
        system = devices['SYSTEM'].iloc[0]
        cs = devices['CS'].iloc[0]
        part_test = 'SS3'
        system_test = '101 AHU-1A'
        cs_test = 'LLS'

        self.assertTrue(part==part_test)
        self.assertTrue(system==system_test)
        self.assertTrue(cs==cs_test)

        return None

    def test_report_basic(self):
        return None

    def test_get_parts_dataframe(self):

        # List of unique systems
        sql = """
        SELECT [SYSTEM]
        FROM [{db_name}].[dbo].[DEVICES]
        GROUP BY [SYSTEM]""".format(db_name=database_name)
        unique_systems = sqlbase.execute_sql(sql)
        system = unique_systems[0][0] # '000 Riser'

        # Return part numbers associated with the system '000 Riser'
        res = BomGenerator.get_parts_dataframe(database_name, system, product_db)
        test_res = ['A12126GSC', 'NP3024PP', 'PXA-SB115V192VA',
                    'RHC302408', 'RSCG040424', 'TR100VA001']
        for part, test_part in zip(res['PARTNO'], test_res):
            self.assertEqual(part, test_part)

        return None

    def test__get_line_price_formula(self):
        return None

    def test__get_bom_price_formula(self):
        return None

    def test__create_report_directory(self):
        return None

    def test_generate_report_larson(self):
        """Testing for BOMGenerator class larson report style"""

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

        BomGenerator.generate_report_larson(retro_flags=retro_flags,
                                            unique_systems=unique_systems,
                                            product_db=product_db)

        return None

    def test_generate_report_standard(self):

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

        ini_file = r"C:\Users\z003vrzk\.spyder-py3\Scripts\Work\panel_builder\SQLTest\JHW\j_vars.ini"
        # Instantiate class
        BomFormat = BOMFormat(ini_file)

        # Class attributes
        self.ini_file = ini_file
        self.BomFormat = BomFormat

        return None

    def test_initialization_dict(self):
        BomFormat = self.BomFormat

        # Look at job variables
        for key, val in BomFormat.initialization_dict.items():
            print(key, val)

        return None

    def test__generate_doc_header_std(self):
        return None

    def test__generate_doc_header_larson(self):
        return None
    def test__generate_doc_header_std(self):
        return None
    def test__generate_node_header_larson(self):
        return None
    def test__generate_node_header_std(self):
        return None


if __name__ == '__main__':
    pass