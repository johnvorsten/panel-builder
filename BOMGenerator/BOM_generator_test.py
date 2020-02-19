# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 09:15:30 2020

@author: z003vrzk
"""

from BOM_generator import BOMGenerator
import os

#%% 

if __name__ == '__main__':
    """Testing..."""

    path_mdf = os.path.join(r"D:\Jobs\246728_TXSU_Chemistry_Bldg_Reno\MDT", "JobDB.mdf")
    server_name = '.\DT_SQLEXPR2008'
    driver_name = 'SQL Server Native Client 10.0'
    database_name = 'PBJobDB'
    # Instantiate class
    MyBomGenerator = BOMGenerator(path_mdf, 
                                  server_name=server_name, 
                                  driver_name=driver_name, 
                                  database_name=database_name)
    
    # All systems within project
    unique_systems = MyBomGenerator.get_unique_systems()
    
    # Product database name (look up prices for parts)
    product_db_name = MyBomGenerator.get_product_database_name()
    
    # All devices within a project
    devices_df = MyBomGenerator.get_DEVICES_dataframe()
    
    MyBomGenerator.generate_fancy_report(retro_flags=['IS NULL',"= '+'","= '*'"], 
                                         unique_systems=unique_systems)
    
    
    pathMDF = input('Please enter a path to the SQL database master-data-file .mdf : ')
    MyBomGenerator = BOMGenerator(pathMDF)
    unique_systems = MyBomGenerator.unique_systems('PBJobDB')
    MyBomGenerator.generate_fancy_report(retro_flags=['IS NULL',"= '+'","= '*'"], 
                                         unique_systems=unique_systems)