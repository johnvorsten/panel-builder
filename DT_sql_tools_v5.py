import pyodbc
import sqlalchemy
import subprocess
import pandas as pd

class MySQLHandling():
    engineMaster = object
    connMaster = object
    cursorMaster = object
    engine = object
    conn = object
    cursor = object
    
    def create_master_connection(self):
        """Used for connection to the master database under the server
        .\DT_SQLEXPR2008 where . is the users desktop and DT_SQLEXPR2008
        is the SQL server setup on each users desktop.
        
        return cursorMaster, connMaster"""
        #Create pyodbc connection
        self.connMaster = pyodbc.connect('DRIVER={SQL Server Native Client 10.0}; SERVER=.\DT_SQLEXPR2008;DATABASE=master;Trusted_Connection=yes;')
        self.cursorMaster = self.connMaster.cursor()
        return self.cursorMaster, self.connMaster
        
    def attach(self, pathMDF):
        """Used to attach PBJobDB. Note: The database added
        will have the default name PBJobDB to distinguish it from any databases.
        
        path = user specified path to .MDF file. LDF file must be in same directory.
        Assumed names are JobDB.mdf and JobDB_Log.ldf
        """
        
        if self.check_db_exist('PBJobDB'):
            print('Database name: {} is already connected'.format('PBJobDB'))
            return
        
#        server = '.\DT_SQLEXPR2008' #may need to have this be a user-entered value for computer name
#        scriptLocation = 'C:\SQLTest\AttachDatabase.sql' #may need o be dynamically defined w/ os.getcwd()
#        subprocess.call(['sqlcmd','-S',server,'-i',scriptLocation])
        dirPathIndex = pathMDF.find('JobDB.mdf')
        dirPath = pathMDF[0:dirPathIndex]
        pathLDF = dirPath + 'JobDB_Log.ldf'
                
        sql1 = "CREATE DATABASE PBJobDB"
        sql2 = "ON (Filename = '{pathMDF}'), (Filename = '{pathLDF}')".format(pathMDF = pathMDF, pathLDF = pathLDF)
        sql3 = "FOR Attach"
        sql = sql1 + " " + sql2 + " " + sql3

        self.connMaster.autocommit = True
        self.cursorMaster.execute(sql)
        self.connMaster.autocommit = False
        print('Database connected')
        
    def detach(self): #detach PBJobDB
        """Used to detach 'PBJobDB'.  Note: I should use
        this once I get the information needed from the database.  This will
        NOT call cursor.close() and engine.dispose(). Currently only closes PBJobDB
        
        I can add a dynamically named database by reading the sql file
        
        TODO - dynamically name database
        TODO - move .sql to CWD
        TODO - dynamically get script directory, or set relative to current"""
        
        server = '.\DT_SQLEXPR2008' #may need to have this be a user-entered value for computer name
        scriptLocation = 'C:\SQLTest\DetachDatabase.sql' #may need o be dynamically defined w/ os.getcwd()
        subprocess.call(['sqlcmd','-S',server,'-i',scriptLocation])
        print('Database removed')
        
    def create_PBDB_connection(self):
        """Used in connection to PBJobDB database.  This is the connection to
        the database specifeid by the user, and the job database.  User the standard
        global outputs "conn" (pyodbc) and "engine" (sqlalchemy) to execute sql
        querys or manipulate data with pandas
        
        return engine, conn, cursor"""
        
        self.engine = sqlalchemy.create_engine('mssql+pyodbc://.\DT_SQLEXPR2008/PBJobDB?driver=SQL+Server+Native+Client+10.0')
        self.engine.connect()
        
        self.conn = pyodbc.connect('DRIVER={SQL Server Native CLient 10.0};SERVER=.\DT_SQLEXPR2008;DATABASE=PBJobDB;Trusted_Connection=yes;')
        self.cursor = self.conn.cursor()
        return self.engine, self.conn, self.cursor
        
    def check_db_exist(self, database):
        sql = """SELECT name FROM master.sys.databases"""
        self.cursorMaster.execute(sql)
        names = self.cursorMaster.fetchall() #get all names
        names = [name[0] for name in names] #convert row object to list object
        
        return names.__contains__(database) #True if database is connected
        
    def read_table(self, tableName):
        sql = """SELECT * FROM {}""".format(tableName)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        
        column_ID = [column[0] for column in self.cursor.description]
        return rows, column_ID
    
    def get_UNC(self):
        """Return a users mapped network drives. UNC path will be used for 
        connecting to networked database"""
        output = subprocess.run(['net', 'use'], stdout = subprocess.PIPE).stdout #Bytes
        output = output.decode() #string
        alphabet = [chr(i) for i in range(65,91)]
        drives = []
        for letter in alphabet:
            if output.__contains__(letter + ':'):
                drives.append(letter)

        output = subprocess.run(['net', 'use'], stdout = subprocess.PIPE).stdout #Bytes
        output = output.decode() #string

        alphabet = [chr(i) for i in range(65,91)]
        drives = []
        for letter in alphabet:
            if output.__contains__(letter + ':'):
                drives.append(letter)
        
        #get UNC server names
        output = output.splitlines()
        serverUNC = []
        for lines in output:
            if lines.__contains__('\\'):
                serverUNC.append(lines[lines.index('\\'):len(lines)-1])
        myOutput = {}
        for index, letter in enumerate(drives):
            myOutput[letter] = serverUNC[index]
        return myOutput
    
    def traceon1807(self, Flag):
        """Turn on/off Trace Flag 1807 based on user input True or False
        Parameters
        ----------
        Flag : True for turn Trace 1807 ON; False for 1807 OFF"""
        if Flag:
            sql = """DBCC TRACEON(1807)"""
        else:
            sql = """DBCC TRACEOFF(1807)"""
        self.cursorMaster.execute(sql)
        self.cursorMaster.commit()
        

def test():
    mysql = MySQLHandling()
    mysql.create_master_connection()
    mysql.traceon1807(True)
    
    path = r'\\usaus000001dat.us009.siemens.net\JobData\JOBS\0 - Engineering Quality\SQLTest\JobDB.mdf'
    mysql.attach(path)
    mysql.create_PBDB_connection() #Connects only to database called PBJobDB
    
    mysql.detach() #only detaches PBJobDB currently










