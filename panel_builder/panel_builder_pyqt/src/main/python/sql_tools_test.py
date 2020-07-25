# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 09:14:49 2020

@author: z003vrzk
"""

# Python imports
import unittest

# local imports
from sql_tools import SQLBase

#%%

class SQLTest(unittest.TestCase):

    def test_get_pyodbc_database_connection_str(self):

        server_name = '.\DT_SQLEXPRESS'
        driver_name = 'SQL Server Native Client 11.0'
        path_mdf = r"C:\Users\z003vrzk\.spyder-py3\Scripts\Work\PanelBuilder\panel_builder\SQLTest\JHW\JobDB.mdf"
        database_name = 'PBJobDB'

        sqlbase = SQLBase(server_name=server_name, driver_name=driver_name)

        # Connects only to database called database_name
        # Use connection string to execute SQL if needed
        conn_str = sqlbase.get_pyodbc_database_connection_str(database_name)
        test_str = 'DRIVER={SQL Server Native Client 11.0}; SERVER=.\\DT_SQLEXPRESS; DATABASE=PBJobDB; Trusted_Connection=yes;'

        self.assertEqual(conn_str, test_str)
        return None


    def test_get_pyodbc_master_connection_str(self):

        server_name = '.\DT_SQLEXPRESS'
        driver_name = 'SQL Server Native Client 11.0'
        path_mdf = r"C:\Users\z003vrzk\.spyder-py3\Scripts\Work\PanelBuilder\panel_builder\SQLTest\JHW\JobDB.mdf"
        database_name = 'PBJobDB'

        sqlbase = SQLBase(server_name=server_name, driver_name=driver_name)

        # Connects only to database called database_name
        # Use connection string to execute SQL if needed
        conn_str = sqlbase.get_pyodbc_master_connection_str()
        test_str = 'DRIVER={SQL Server Native Client 11.0}; SERVER=.\\DT_SQLEXPRESS; DATABASE=master; Trusted_Connection=yes;'

        self.assertEqual(conn_str, test_str)
        return None


    def test_set_pyodbc_master_connection_str(self):

        server_name = '.\DT_SQLEXPRESS'
        driver_name = 'SQL Server Native Client 11.0'
        path_mdf = r"C:\Users\z003vrzk\.spyder-py3\Scripts\Work\PanelBuilder\panel_builder\SQLTest\JHW\JobDB.mdf"
        database_name = 'PBJobDB'

        sqlbase = SQLBase(server_name=server_name, driver_name=driver_name)

        # Connects only to database called database_name
        # Use connection string to execute SQL if needed
        conn_str = sqlbase.set_pyodbc_master_connection_str()
        conn_str_test = sqlbase.get_pyodbc_master_connection_str()
        conn_str_test2 = 'DRIVER={SQL Server Native Client 11.0}; SERVER=.\\DT_SQLEXPRESS; DATABASE=master; Trusted_Connection=yes;'

        self.assertEqual(conn_str, conn_str_test, conn_str_test2)
        return None

    def test_get_sqlalchemy_connection_str(self):

        server_name = '.\DT_SQLEXPRESS'
        driver_name = 'SQL Server Native Client 11.0'
        path_mdf = r"C:\Users\z003vrzk\.spyder-py3\Scripts\Work\PanelBuilder\panel_builder\SQLTest\JHW\JobDB.mdf"
        database_name = 'PBJobDB'

        sqlbase = SQLBase(server_name=server_name, driver_name=driver_name)

        sqlalchemy_str = sqlbase.get_sqlalchemy_connection_str(database_name)
        sqlalchemy_str_test = 'mssql+pyodbc://.\\DT_SQLEXPRESS/PBJobDB?driver={SQL Server Native Client 11.0}&trusted_connection=yes'

        self.assertEqual(sqlalchemy_str, sqlalchemy_str_test)
        return None


    def test_attach_database(self):

        server_name = '.\DT_SQLEXPRESS'
        driver_name = 'SQL Server Native Client 11.0'
        path_mdf = r"C:\Users\z003vrzk\.spyder-py3\Scripts\Work\PanelBuilder\panel_builder\SQLTest\JHW\JobDB.mdf"
        path_ldf = r"C:\Users\z003vrzk\.spyder-py3\Scripts\Work\PanelBuilder\panel_builder\SQLTest\JHW\JobDB_Log.ldf"
        database_name = 'PBJobDB'

        # Attach a database on path_mdf
        sqlbase = SQLBase(server_name=server_name, driver_name=driver_name)
        sqlbase.attach_database(path_mdf, path_ldf, database_name)

        # Execute transactions on the database to make sure its connected
        sql = """SELECT * FROM [master].[sys].[databases]"""
        with sqlbase.master_connection.cursor() as cursor:
            cursor.execute(sql)
            row = cursor.fetchone()
            while row:
                if row.name == database_name:
                    print('Found Myself')
                    break
                row = cursor.fetchone()
        if row.name != database_name:
            raise(ValueError('Did not fine {} in query'.format(database_name)))

        # Finish and detach database
        sqlbase.detach_database(database_name)

        return None


    def test_detach_database(self):

        server_name = '.\DT_SQLEXPRESS'
        driver_name = 'SQL Server Native Client 11.0'
        path_mdf = r"C:\Users\z003vrzk\.spyder-py3\Scripts\Work\PanelBuilder\panel_builder\SQLTest\JHW\JobDB.mdf"
        database_name = 'PBJobDB'

        sqlbase = SQLBase(server_name=server_name, driver_name=driver_name)

        # Attach a database on path_mdf
        database_name = sqlbase.attach_database(path_mdf, database_name)
        sqlbase.detach_database(database_name)

        # Make sure it is detached
        test_detached = None # TODO

        self.assertTrue(test_detached)
        return None


    def test_read_table(self):

        server_name = '.\DT_SQLEXPRESS'
        driver_name = 'SQL Server Native Client 11.0'
        path_mdf = r"C:\Users\z003vrzk\.spyder-py3\Scripts\Work\PanelBuilder\panel_builder\SQLTest\JHW\JobDB.mdf"
        database_name = 'PBJobDB'

        sqlbase = SQLBase(server_name=server_name, driver_name=driver_name)

        # Read a table
        df = sqlbase.read_table(database_name, table_name='POINTBAS')

        # Read sql into a pandas table
        sql = """select top(10) *
        from {}""".format(database_name)
        query_table = sqlbase.pandas_read_sql(sql, database_name)

        self.assertEqual()
        return None


    def test_attach_database_remote(self):

        # Connect to remote database
        server_name = '.\DT_SQLEXPRESS'
        driver_name = 'SQL Server Native Client 11.0'
        path_mdf = r"\\ustxca00064sto.ad001.siemens.net\grp$\FSA01313088\Jobs\Automation\Test\MDT\JobDB.mdf"
        path_ldf = r"\\ustxca00064sto.ad001.siemens.net\grp$\FSA01313088\Jobs\Automation\Test\MDT\JobDB_Log.ldf"
        database_name = 'TestDB'

        sqlbase = SQLBase(server_name=server_name, driver_name=driver_name)

        # Attach a database on path_mdf
        database_name = sqlbase.attach_database(path_mdf, database_name, path_ldf)

        # Connects only to database called database_name
        # Use connection and cursor objects to execute SQL if needed
        (file_used_bool,
         name_used_bool,
         existing_database_name) = sqlbase.check_existing_database(path_mdf, database_name)

        # Detach database_name
        sqlbase.detach_database(database_name)

        return None



if __name__ == '__main__':
    unittest.main()