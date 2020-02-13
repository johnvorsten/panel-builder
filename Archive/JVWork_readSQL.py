# -*- coding: utf-8 -*-
"""
Created on Sun Dec  9 16:58:47 2018

@author: z003vrzk
"""

import pandas as pd
import pyodbc
import sqlalchemy

#engine = sqlalchemy.create_engine('mssql+pyodbc://z003vrzk:Goodday4@')


#example of connecting with dsn.. see https://github.com/mkleehammer/pyodbc/wiki/Connecting-to-SQL-Server-from-Windows for connecting using a DSN
#engine = sqlalchemy.create_engine('mssql+pyodbc://mydsn') 

#DT SQL servername: DT_SQLEXPR2008
#User logon cred: accountname: ad001\zoo3vrzk
#User logon cred: password: Goodday4 (or the user password.. may need to know this)


#SQLAlchemy engine conneciton string using DSN:
#engine = sqlalchemy.create_engine("mssql+pyodbc://<username>:<password>@some_dsn")

#SQLAlchemy engine conneciton string using hostname connection:
#engine = sqlalchemy.create_engine("mssql+pyodbc://<username>:<password>@myhost:port/databasename?driver=SQL+Server+Native+Client+10.0")
#This uses the SQL Server Native Client 10.0 which is on my computer

#engine = sqlalchemy.create_engine("mssql+pyodbc://ad001\z003vrzk:Goodday4@myhost:3183/databasename?driver=SQL+Server+Native+Client+10.0")

#Using windows authentication:
#engine = sqlalchemy.create_engine("mssql+pyodbc://server/database")
#engine = sqlalchemy.create_engine("mssql+pyodbc://DT_SQLEXPR2008/database")


engine = sqlalchemy.create_engine("mssql+pyodbc://z003vrzk:Goodday4@DT_SQLEXPR2008/D:\Jobs\44OP-239338_ACC_Bond_Rio_Grande_Retro\MDT\JobDB.mdf?driver=SQL+Server+Native+Client+10.0")

engine = sqlalchemy.create_engine("mssql+pyodbc://z003vrzk:Goodday4@DT_SQLEXPR2008/D:\Jobs\44OP-239338_ACC_Bond_Rio_Grande_Retro\MDT\JobDB.mdf?driver=SQL+Server+Native+Client+10.0")
#
#engine.connect()

#conn = pyodbc.connect('DRIVER={SQL Server};SERVER=server;DATABASE=database;UID=user;PWD=password')

server = r'.\DT_SQLEXPR2008'
user = r'z003vrzk'
password = r'Goodday4'
database = r'D:\Jobs\44OP-239338_ACC_Bond_Rio_Grande_Retro\MDT\JobDB.mdf'

conn = pyodbc.connect('DRIVER={SQL Server};SERVER=server;DATABASE=database;UID=user;PWD=password')

