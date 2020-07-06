# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 09:15:30 2020

@author: z003vrzk
"""
# Python imports
import os

# Third party imports

# Local imports
from BOM_generator import BOMGenerator


#%%

def test_get_unique_systems():
    """"""
    path_mdf = os.path.join(r"C:\Users\z003vrzk\.spyder-py3\Scripts\Work\PanelBuilder\panel-builder\SQLTest\JHW", "JobDB.mdf")
    path_ldf = os.path.join(r'C:\Users\z003vrzk\.spyder-py3\Scripts\Work\PanelBuilder\panel-builder\SQLTest\JHW', 'JobDB_Log.ldf')
    path_jvars = os.path.join(r"C:\Users\z003vrzk\.spyder-py3\Scripts\Work\PanelBuilder\panel-builder\SQLTest\JHW", "j_vars.ini")
    server_name = '.\DT_SQLEXPR2008'
    driver_name = 'SQL Server Native Client 10.0'
    database_name = 'PBJobDB'

    MyBomGenerator = BOMGenerator(path_mdf,
                                  path_ldf,
                                  path_jvars,
                                  server_name=server_name,
                                  driver_name=driver_name,
                                  database_name=database_name)

    # All systems within project
    unique_systems = MyBomGenerator.get_unique_systems()

    return unique_systems







if __name__ == '__main__':
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