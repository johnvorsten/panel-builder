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


#%%


def Test(unittest.TestCase):



    def test_get_DEVICES_dataframe(self):
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

    def test_generate_report_larson
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

        # All systems within project
        unique_systems = MyBomGenerator.get_unique_systems()

        # Product database name (look up prices for parts)
        product_db_name = MyBomGenerator.get_product_database_name()

        # All devices within a project
        devices_df = MyBomGenerator.get_DEVICES_dataframe()

        MyBomGenerator.generate_report_larson(retro_flags=['IS NULL',"= '+'","= '*'"],
                                             unique_systems=unique_systems)

        return None

    def test_generate_report_standard(self):
        return None

    def test_generate_fancy_report(self):
        return None



    #%%


    if __name__ == '__main__':
        """Testing for BOMGenerator class, standard report style"""

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

        # All systems within project
        unique_systems = MyBomGenerator.get_unique_systems()

        # Product database name (look up prices for parts)
        product_db_name = MyBomGenerator.get_product_database_name()

        MyBomGenerator.generate_report_standard(retro_flags=['IS NULL',"= '+'","= '*'"],
                                             unique_systems=unique_systems)