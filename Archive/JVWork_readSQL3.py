# -*- coding: utf-8 -*-
"""
Created on Fri Dec 14 12:35:53 2018

@author: z003vrzk
"""
import pyodbc
import sqlalchemy
import pandas

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
#cursor.execute()



#conn.commit() #after you do your work
#conn.close() #close the connection