# -*- coding: utf-8 -*-
"""
Created on Sat Dec 15 20:53:08 2018

@author: z003vrzk
"""

import pyodbc
import sqlalchemy
import pandas

##Using windows authentication:
##engine = sqlalchemy.create_engine("mssql+pyodbc://server/database")
##Try to access database already attached
##Database = master
#engine = sqlalchemy.create_engine('mssql+pyodbc://MD1QKDPC\DT_SQLEXPR2008/master?driver=SQL+Server+Native+Client+10.0')
#engine.connect()
#
##PointBAS = pandas.read_sql_table('POINTBAS', engine)
#
#conn = pyodbc.connect('DRIVER={SQL Server Native Client 10.0};SERVER=MD1QKDPC\DT_SQLEXPR2008;DATABASE=master;Trusted_Connection=yes;')
#cursor = conn.cursor() #conn.commit() or conn.rollback() to commit or rollback work w/ cursor
#
#sql = """
#    CREATE DATABASE JobDB
#        ON (Filename = 'C:\SQLTest\JobDB.mdf'), (Filename = 'C:\SQLTest\JobDB_Log.ldf')
#        FOR Attach"""
#
#conn.autocommit = True
#cursor.execute(sql)
#conn.autocommit = False
#
#
##cursor.execute()
#
##conn.commit() #after you do your work
##conn.close() #close the connection

jvsql = MySQLHandling()
jvsql.create_master_connection()
path = 'C:\SQLTest\JobDB.mdf'
jvsql.attach(path)
jvsql.create_PBDB_connection()

class MySQLHandling():
    global cursorMaster
    global connMaster
    global engineMaster #connection to master Database
    global cursor
    global conn
    global engine #Connection to PBJobDB Database
    
    def create_master_connection(self):
        """Used for connection to the master database under the server
        .\DT_SQLEXPR2008 where . is the users desktop and DT_SQLEXPR2008
        is the SQL server setup on each users desktop.
        
        In order to attach a certain job database, use the MySQLHandling.attach()
        method
        """
        #Create SQLAlchemy connection
        engineMaster = sqlalchemy.create_engine('mssql+pyodbc://.\DT_SQLEXPR2008/master?driver=SQL+Server+Native+Client+10.0')
        engineMaster.connect()
        
        #Create pyodbc connection
        connMaster = pyodbc.connect('DRIVER={SQL Server Native Client 10.0}; SERVER=.\DT_SQLEXPR2008;DATABASE=master;Trusted_Connection=yes;')
        cursorMaster = connMaster.cursor()
        
    def attach(self, pathMDF):
        """Used to attach a user-specified job database. Note: The database added
        will have the default name PBJobDB aka. Panel Builder JobDB.  This 
        is intended to distinguish it from any databases Design Tool may add
        
        path = user specified path to .MDF file. LDF file must be in same directory.
        Assumed names are JobDB.mdf and JobDB_Log.ldf
        """
        dirPathIndex = pathMDF == 'JobDB.mdf'
        dirPath = pathMDF[0:dirPathIndex]
        pathLDF = dirPath + 'JobDB_Log.ldf'
        
        sql = """
            CREATE DATABASE PBJobDB
                ON (Filename = ?), (Filename = ?)
                FOR Attach """
                
        connMaster.autocommit = True
        cursorMaster.execute(sql, (pathMDF, pathLDF))
        connMaster.autocommit = False
        
        print(sql)
        
    def detach(self, database): #detach PBJobDB
        """Used to detach the user-specified job database.  Note: I should use
        this once I get the information needed from the database.  This will
        NOT call cursor.close() and engine.dispose()"""
        
        sql = """EXEC sp_detact_db ?, 'true';"""
        
        cursorMaster.execute(sql, (database))
        cursorMaster.commit()
        
    def create_PBDB_connection(self):
        """Used in connection to PBJobDB database.  This is the connection to
        the database specifeid by the user, and the job database.  User the standard
        global outputs "conn" (pyodbc) and "engine" (sqlalchemy) to execute sql
        querys or manipulate data with pandas"""
        
        engine = sqlalchemy.create_engine('mssql+pyodbc://.\DT_SQLEXPR2008/PBJobDB?driver=SQL+Server+Native+Client+10.0')
        engine.connect()
        
        conn = pyodbc.connect('DRIVER={SQL Server Native CLient 10.0};SERVER=.\DT_SQLEXPR2008;DATABASE=PBJobDB;Trusted_Connection=yes;')
        cursor = conn.cursor()
        

        
        
        