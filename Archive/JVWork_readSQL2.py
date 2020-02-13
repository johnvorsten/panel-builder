# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 18:17:32 2018

@author: z003vrzk
"""
import pyodbc
import sqlalchemy
import pandas

#engine = create_engine('mssql+pymssql://zoo3vrzk:Goodday4@)
#cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=SQLSRV01;DATABASE=DATABASE;UID=USER;PWD=PASSWORD')
#cursor = cnxn.cursor()

#example of connecting with dsn.. see https://github.com/mkleehammer/pyodbc/wiki/Connecting-to-SQL-Server-from-Windows for connecting using a DSN
#engine = sqlalchemy.create_engine('mssql+pyodbc://mydsn') 
#engine = sqlalchemy.create_engine('mssql+pyodbc://mydsn')
#engine.connect()
#
#
##SQLAlchemy engine conneciton string using hostname connection:
##engine = sqlalchemy.create_engine("mssql+pyodbc://<username>:<password>@myhost:port/databasename?driver=SQL+Server+Native+Client+10.0")
#engine = sqlalchemy.create_engine("mssql+pyodbc://ad001\z003vrzk:Goodday4@.\DT_SQLEXPR2008/C:\SQLTest\JobDB.mdf?driver=SQL+Server+Native+Client+10.0")
#engine.connect()


#Using windows authentication:
#engine = sqlalchemy.create_engine("mssql+pyodbc://server/database")
#My SQL Server is setup for windows authentication only.
engine = sqlalchemy.create_engine('mssql+pyodbc://MD1QKDPC\DT_SQLEXPR2008/C:\SQLTest\JobDB.mdf?driver=SQL+Server+Native+Client+10.0')
engine.connect()


#Using windows authentication:
#Try to access database already attached
engine = sqlalchemy.create_engine('mssql+pyodbc://MD1QKDPC\DT_SQLEXPR2008/JobDB12112018083549?driver=SQL+Server+Native+Client+10.0')
engine.connect()

PointBAS = pandas.read_sql_table('POINTBAS', engine)

conn = pyodbc.connect('DRIVER={SQL Server Native Client 10.0};SERVER=MD1QKDPC\DT_SQLEXPR2008;DATABASE=JobDB12112018083549;Trusted_Connection=yes;')
cursor = conn.cursor() #conn.commit() or conn.rollback() to commit or rollback work w/ cursor

#conn.commit() #after you do your work
#conn.close() #close the connection



##Connection using pyodbc.connect()
#server = r'.\DT_SQLEXPR2008'
#user = r'z003vrzk'
#user2 = r'MD1QKDPC'
#password = r'Goodday4'
#database = r'C:\SQLTest\JobDB.mdf'
#
#conn = pyodbc.connect('DRIVER={SQL Server Native Client 10.0};SERVER=MD1QKDPC\DT_SQLEXPR2008;DATABASE=C:\SQLTest\JobDB.mdf;UID=AD001\z003vrzk;PWD=Goodday4')
#
#conn = pyodbc.connect('DRIVER={SQL Server Native Client 10.0};SERVER=server;DATABASE=database;UID=user;PWD=password')
