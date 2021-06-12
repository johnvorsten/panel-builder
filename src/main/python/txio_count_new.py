# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 10:11:44 2021

@author: johnvorsten
"""

# Python imports
import pandas as pd
import math
from datetime import date
import os
import copy

# Third party imports
import numpy as np

# Local imports
from sql_tools import SQLBase

# Local declarations
point_dict = \
    {'LAI_current':None,
     'LAI_standard':None,
     'LAO_current':None,
     'LAO_standard':None,
     'LDI':None,
     'LDO':None,
     'LPACI':None,
     }

txio_dict = \
    {'TXM1_8XML':0, # Number of hardware part number TXM1_8XML desired
     'TXM1_8UML':0, # Number of hardware part number TXM1_8UML desired
     'TXM1_8X':0, # Number of hardware part number TXM1_8X desired
     'TXM1_8U':0, # Number of hardware part number TXM1_8U desired
     'TXM1_16D':0,
     'TXM1_6RM':0,

     'empty_LAI_current':None, # Number of empty LAI Current capable slots after TXIO is recommended
     'empty_LAI_standard':None, # Number of empty LAI Standard capable slots after TXIO is recommended
     'empty_LAO_current':None, # Number of empty LAO Current capable slots after TXIO is recommended
     'empty_LAO_standard':None, # Number of empty LAO Standard capable slots after TXIO is recommended
     'empty_LDI':None, # Number of empty LDI dedicated slots after TXIO is recommended
     'empty_LDO':None, # Number of empty LDO capable slots after TXIO is recommended
     }



#%%

class TXIOCounter():
    """Counter class is used to count number of TXIO modules required for a
    PXC Modular. See methods for more explanation"""

    def __init__(self):
        return None

    def count_LAnalog(self, panelName, configuration):
        """Count all Logical Analog points on a specific panel.  Makes differentiation between
        SUPER and STANDARD universal points
        Parameters
        ----------
        panelName : String, DT panel name; see Count.uniquePanels for set of
        unique panels
        configuration : int, which IO counter to run.
        configuration map
        0 -> TXM18XML() - 8xml on all
        1 -> TXM18X() - 8x on all
        2 -> TXM18X_8U() - 8x and 8u
        3 -> TXM18XML_8UML() - 8xml and 8uml on all
        4 -> TXM18XML_8UML_8X_8U() - 8xml AO, 8x AI, 8uml AO, 8U AI

        Outputs
        ---------
        dictionary of keys : {AO_SUM, totalCurrent_AO, extraCurrent_AO, totalStandard_AO,
        extraStandard_AO, totalCurrent_AI, extraCurrent_AI,
        totalStandard_AI, extraStandard_AI, TXM1_8XML, TXM1_8UML,
        TXM1_8X, TXM1_8U, emptyXML, emptyUML, emptyX, emptyU}"""

        AO_SUM = sum((self.POINTBAS.loc[:,'TYPE'] == 'LAO') & (self.POINTBAS.loc[:,'NETDEVID'] == panelName))
        AI_SUM = sum((self.POINTBAS.loc[:,'TYPE'] == 'LAI') & (self.POINTBAS['NETDEVID']==panelName))

        dataframe_AO = pd.DataFrame(np.zeros((self.POINTSEN.shape[0],3)))
        for i in range(0,self.POINTSEN.shape[0]): #Match POINTID with NETDEVID to select panel only
            dataframe_AO.loc[i,0] = self.POINTSEN.loc[i,'POINTID']
            index = np.where(self.POINTBAS['POINTID']==self.POINTSEN.loc[i,'POINTID'])[0][0]
            dataframe_AO.loc[i,1] = self.POINTBAS.loc[index, 'TYPE']
            dataframe_AO.loc[i,2] = self.POINTBAS.loc[index, 'NETDEVID']
        totalCurrent_AO = sum((self.POINTSEN['SENSORTYPE'] == 'CURRENT') & (dataframe_AO[2] == panelName) & (dataframe_AO[1] == 'LAO'))
        totalStandard_AO = sum((self.POINTSEN['SENSORTYPE'] != 'CURRENT') & (dataframe_AO[2] == panelName) & (dataframe_AO[1] == 'LAO'))
        extraCurrent_AO = math.ceil(totalCurrent_AO*1.05)
        extraStandard_AO = math.ceil(totalStandard_AO*1.05)

        dataframe_AI = pd.DataFrame(np.zeros((self.POINTSEN.shape[0],3)))
        for i in range(0,self.POINTSEN.shape[0]):
            dataframe_AI.loc[i,0] = self.POINTSEN.loc[i,'POINTID']
            index = np.where(self.POINTBAS['POINTID']==self.POINTSEN.loc[i,'POINTID'])[0][0]
            dataframe_AI.loc[i,1] = self.POINTBAS.loc[index, 'TYPE']
            dataframe_AI.loc[i,2] = self.POINTBAS.loc[index, 'NETDEVID']
        totalCurrent_AI = sum((self.POINTSEN['SENSORTYPE'] == 'CURRENT') & (dataframe_AI[2] == panelName) & (dataframe_AI[1] == 'LAI'))
        totalStandard_AI = sum((self.POINTSEN['SENSORTYPE'] != 'CURRENT') & (dataframe_AI[2] == panelName) & (dataframe_AI[1] == 'LAI'))
        extraCurrent_AI = math.ceil(totalCurrent_AI*1.05)
        extraStandard_AI = math.ceil(totalStandard_AI*1.05)

        def TXM18XML():
            """8X-ML for all analog ponits"""
            TXM1_8XML = math.ceil((extraCurrent_AO + extraStandard_AO + extraCurrent_AI + extraStandard_AI)/8)
            TXM1_8UML = 0
            TXM1_8X = 0
            TXM1_8U = 0
            emptyXML = TXM1_8XML*8 - (totalCurrent_AO + totalStandard_AO + totalCurrent_AI + totalStandard_AI)
            emptyUML = 0
            emptyX = 0
            emptyU = 0
            mydict = {'AO_SUM':AO_SUM, 'totalCurrent_AO':totalCurrent_AO, 'extraCurrent_AO':extraCurrent_AO, 'totalStandard_AO':totalStandard_AO,
                   'extraStandard_AO':extraStandard_AO, 'AI_SUM':AI_SUM,'totalCurrent_AI':totalCurrent_AI, 'extraCurrent_AI':extraCurrent_AI,
                    'totalStandard_AI':totalStandard_AI, 'extraStandard_AI':extraStandard_AI, 'TXM1_8XML':TXM1_8XML, 'TXM1_8UML':TXM1_8UML,
                    'TXM1_8X':TXM1_8X, 'TXM1_8U':TXM1_8U, 'emptyXML':emptyXML, 'emptyUML':emptyUML, 'emptyX':emptyX, 'emptyU':emptyU}
            for key in mydict:
                self.pointDict[key] = mydict[key]
            return mydict

        def TXM18X():
            """8X for all analog points"""
            TXM1_8XML = 0
            TXM1_8UML = 0
            TXM1_8X = math.ceil((extraCurrent_AO + extraStandard_AO + extraCurrent_AI + extraStandard_AI)/8)
            TXM1_8U = 0
            emptyXML = 0
            emptyUML = 0
            emptyX = TXM1_8X*8 - (totalCurrent_AO + totalStandard_AO + totalCurrent_AI + totalStandard_AI)
            emptyU = 0
            mydict = {'AO_SUM':AO_SUM, 'totalCurrent_AO':totalCurrent_AO, 'extraCurrent_AO':extraCurrent_AO, 'totalStandard_AO':totalStandard_AO,
                   'extraStandard_AO':extraStandard_AO, 'AI_SUM':AI_SUM,'totalCurrent_AI':totalCurrent_AI, 'extraCurrent_AI':extraCurrent_AI,
                    'totalStandard_AI':totalStandard_AI, 'extraStandard_AI':extraStandard_AI, 'TXM1_8XML':TXM1_8XML, 'TXM1_8UML':TXM1_8UML,
                    'TXM1_8X':TXM1_8X, 'TXM1_8U':TXM1_8U, 'emptyXML':emptyXML, 'emptyUML':emptyUML, 'emptyX':emptyX, 'emptyU':emptyU}
            for key in mydict:
                self.pointDict[key] = mydict[key]
            return mydict

        def TXM18X_8U():
            """8U and 8X for all analog points"""
            TXM1_8XML = 0
            TXM1_8UML = 0
            TXM1_8X = math.ceil((extraCurrent_AO + extraCurrent_AI)/8)
            emptyX = TXM1_8X*8 -totalCurrent_AO - totalCurrent_AI
            TXM1_8U = math.ceil((extraStandard_AO + extraStandard_AI - emptyX)/8)
            emptyU = TXM1_8U*8 - totalStandard_AO - totalStandard_AI
            emptyXML = 0
            emptyUML = 0
            if emptyU < 0:
                if abs(emptyU) < (TXM1_8X*8 - totalCurrent_AO - totalCurrent_AI): #Place them on the extra X slots
                    emptyU = 0
                    emptyX = TXM1_8X*8 - totalCurrent_AO - totalCurrent_AI - (abs(TXM1_8U*8 - totalStandard_AO - totalStandard_AI))
                else:
                    print('Error')
            else:
                emptyX = (TXM1_8X*8 - totalCurrent_AO - totalCurrent_AI)
            mydict = {'AO_SUM':AO_SUM, 'totalCurrent_AO':totalCurrent_AO, 'extraCurrent_AO':extraCurrent_AO, 'totalStandard_AO':totalStandard_AO,
                   'extraStandard_AO':extraStandard_AO, 'AI_SUM':AI_SUM,'totalCurrent_AI':totalCurrent_AI, 'extraCurrent_AI':extraCurrent_AI,
                    'totalStandard_AI':totalStandard_AI, 'extraStandard_AI':extraStandard_AI, 'TXM1_8XML':TXM1_8XML, 'TXM1_8UML':TXM1_8UML,
                    'TXM1_8X':TXM1_8X, 'TXM1_8U':TXM1_8U, 'emptyXML':emptyXML, 'emptyUML':emptyUML, 'emptyX':emptyX, 'emptyU':emptyU}
            for key in mydict:
                self.pointDict[key] = mydict[key]
            return mydict

        def TXM18XML_8UML():
            """8U-ML and 8X-ML for all analog points"""
            TXM1_8XML = math.ceil((extraCurrent_AO + extraCurrent_AI)/8) #Assume AO 4-20mA is possible w/ 4 slots per module
            TXM1_8X = 0
            TXM1_8U = 0
            emptyU = 0
            emptyX = 0
            emptyXML = TXM1_8XML*8 -totalCurrent_AO - totalCurrent_AI
            TXM1_8UML = math.ceil((extraStandard_AO + extraStandard_AI - emptyXML)/8)
            emptyUML = TXM1_8UML*8 - totalStandard_AO - totalStandard_AI
            if emptyUML < 0:
                if abs(emptyUML) < (TXM1_8XML*8 - totalCurrent_AO - totalCurrent_AI): #Place them on the extra X slots
                    emptyUML = 0
                    emptyXML = TXM1_8XML*8 - totalCurrent_AO - totalCurrent_AI - (abs(TXM1_8UML*8 - totalStandard_AO - totalStandard_AI))
                else:
                    print('Error')
            mydict = {'AO_SUM':AO_SUM, 'totalCurrent_AO':totalCurrent_AO, 'extraCurrent_AO':extraCurrent_AO, 'totalStandard_AO':totalStandard_AO,
                   'extraStandard_AO':extraStandard_AO, 'AI_SUM':AI_SUM,'totalCurrent_AI':totalCurrent_AI, 'extraCurrent_AI':extraCurrent_AI,
                    'totalStandard_AI':totalStandard_AI, 'extraStandard_AI':extraStandard_AI, 'TXM1_8XML':TXM1_8XML, 'TXM1_8UML':TXM1_8UML,
                    'TXM1_8X':TXM1_8X, 'TXM1_8U':TXM1_8U, 'emptyXML':emptyXML, 'emptyUML':emptyUML, 'emptyX':emptyX, 'emptyU':emptyU}
            for key in mydict:
                self.pointDict[key] = mydict[key]
            return mydict

        def TXM18XML_8UML_8X_8U():
            """8X-ML and 8U-ML for outputs, 8U and 8X for inputs"""
            #TODO - if there are more empty XML than currentAI, then the emptyXML will be underutilized (unlikely scenario)
            #Could be better to apply UML to XML in this case
            TXM1_8XML = math.ceil((extraCurrent_AO)/4) #Only 4 AO ports per module
            emptyXML = TXM1_8XML*8 - totalCurrent_AO
            TXM1_8X = math.ceil((extraCurrent_AI - emptyXML)/8)
            emptyX = TXM1_8X*8 - totalCurrent_AI
            if emptyX < 0:
                if abs(emptyX) < (TXM1_8XML*8 - totalCurrent_AO):
                    emptyX = 0
                    emptyXML = TXM1_8XML*8 - totalCurrent_AO - abs(TXM1_8X*8 - totalCurrent_AI)
                else:
                    print('Error')

            #Apply standard outputs to 8UML
            TXM1_8UML = math.ceil((extraStandard_AO)/8)
            emptyUML = TXM1_8UML*8 - totalStandard_AO
            #Apply standard inputs to 8U
            TXM1_8U = math.ceil((extraStandard_AI - emptyUML - emptyX)/8)
            emptyU = TXM1_8U*8 - totalStandard_AI
            if emptyU < 0:
                if abs(emptyU) < (emptyUML + emptyX):
                    spaceNeeded = abs(emptyU)
                    if spaceNeeded > emptyX:
                        spaceNeeded = spaceNeeded - emptyX #apply to X
                        emptyU = emptyU + emptyX #apply to X
                        emptyX = 0 #apply to X, reinit to 0
                        emptyUML = emptyUML - spaceNeeded #apply rest to UML
                        spaceNeeded = spaceNeeded - emptyUML #apply rest to UML
                        if spaceNeeded > 0:
                            print('Error')
                    elif spaceNeeded <= emptyX:
                        spaceNeeded = spaceNeeded - emptyX
                        emptyX = emptyX + emptyU
                        emptyU = 0
                else:
                    print('Error')
            mydict = {'AO_SUM':AO_SUM, 'totalCurrent_AO':totalCurrent_AO, 'extraCurrent_AO':extraCurrent_AO, 'totalStandard_AO':totalStandard_AO,
                   'extraStandard_AO':extraStandard_AO, 'AI_SUM':AI_SUM,'totalCurrent_AI':totalCurrent_AI, 'extraCurrent_AI':extraCurrent_AI,
                    'totalStandard_AI':totalStandard_AI, 'extraStandard_AI':extraStandard_AI, 'TXM1_8XML':TXM1_8XML, 'TXM1_8UML':TXM1_8UML,
                    'TXM1_8X':TXM1_8X, 'TXM1_8U':TXM1_8U, 'emptyXML':emptyXML, 'emptyUML':emptyUML, 'emptyX':emptyX, 'emptyU':emptyU}
            for key in mydict:
                self.pointDict[key] = mydict[key]
            return mydict

        #Map based on function call?
        """configuration map
        0 -> TXM18ML()
        1 -> TXM18X()
        2 -> TXM18X_8U()
        3 -> TXM18XML_8UML()
        4 -> TXM18XML_8UML_8X_8U()"""
        flist = [TXM18XML, TXM18X, TXM18X_8U, TXM18XML_8UML, TXM18XML_8UML_8X_8U]
        flist[configuration]()



class PointsCounter():
    """Counts the number of logical points assocaited with a specific
    controller"""

    def __init__(self,
                 path_mdf,
                 path_ldf,
                 path_j_vars,
                 database_name,
                 SQLBase):
        """
        Construct a points dictionary and output the accumulated points
        inputs
        -------
        path_mdf : (str) path to master database file (MSSQL)
        path_ldf : (str) path to log database file (MSSQL)
        path_j_vars : (str) path to j_vars.ini file found in each job folder
        database_name : (str) name of database to connect as
        SQLBase : (sql_tools.SQLBase) class with instantiated database
            connection
        """

        #Begin SQL connection to import data
        self.SQLBase = SQLBase

        """Make sure the SQLBase class passed already has an active
        Database connection
        The Qt Application should instantiate and handle SQL database connections
        It is not the responsibility of this class to handle database
        connections"""
        if 'database_connection' not in self.SQLBase.__dict__:
            msg=('database connection is not instantiated. There may be an' +
                 ' issue with Qt Instantiating a connection')
            raise NameError(msg)

        """The database and name should already be connected
        Verify this through SQLBase
        If a database is already attached then file_used_bool will be True
        If name_used_bool is True then the logical database name is in use
        existing_database_name is a string if file_used_bool is True"""
        (file_used_bool,
         name_used_bool,
         existing_database_name) = self.SQLBase\
            .check_existing_database(path_mdf, database_name)

        msg='The selected MDF File {} is not connected to SQL Server'
        assert(file_used_bool == True), msg.format(path_mdf)
        msg=('The selected database name {} does not currently exist in SQL' +
             ' Server')
        assert(name_used_bool == True), msg.format(database_name)
        msg=('The passed database_name and database name connected to SQL' +
            ' Server do not match. Got {}, expected {}')
        msg = msg.format(database_name, existing_database_name)
        assert(existing_database_name == database_name), msg

        return None

    def unique_panels(self):
        """Returns a set of unique panels detected. Count.uniquePanels"""
        uniquePanels = set(self.POINTBAS['NETDEVID'])
        uniquePanels = list(uniquePanels) #return as list for access
        return uniquePanels


    @staticmethod
    def sql_points_single_type(sql_base
                                 controller_name,
                                 point_type,
                                 sensor_type,
                                 virtual):
        """Count all LDO points on a specific panel.
        inputs
        ----------
        controller_name : (str) name of controller
        point_type : (str) point type. One of
            ['LAI','LAO','LDI','LDO','LPACI','L2SL']
        sensor_type : (str) sensor type
        virtual : (bool/int) it should be 0

        Example
        count = count_points_single_type('some-controller','LAI','CURRENT',0)
        """

        sql = """SELECT count([t1].[POINTID]) as TOTAL_COUNT
                FROM (select [POINTFUN].[POINTID], [TYPE], [VIRTUAL], [NETDEVID], [SENSORTYPE]
                	from POINTFUN
                	full JOIN POINTSEN ON POINTFUN.POINTID = POINTSEN.POINTID) AS [t1]
                WHERE [t1].[TYPE] = '{point_type}'
                AND [t1].[NETDEVID] = '{controller_name}'
                AND [t1].[SENSORTYPE] = '{sensor_type}'
                AND [t1].[VIRTUAL] = {virtual}"""\
                    .format(point_type=point_type,
                            sensor_type=sensor_type,
                            virtual=virtual,
                            controller_name=controller_name)

        dataframe = sql_base.pandas_execute_sql(sql)

        return dataframe['TOTAL_COUNT'].values


    @staticmethod
    def sql_points_list_type(sql_base,
                             controller_name,
                             point_type_tuple,
                             sensor_type,
                             virtual):
        """Count all points on a specific panel.
        inputs
        ----------
        controller_name : (str) name of controller
        point_type_tuple : (tuple) of point types. Example ('LDI','L2SL', 'LPACI')
        sensor_type : (str) sensor type
        virtual : (bool/int) it should be 0
        """

        sql = """SELECT count([t1].[POINTID]) as TOTAL_COUNT
                FROM (select [POINTFUN].[POINTID], [TYPE], [VIRTUAL], [NETDEVID], [SENSORTYPE]
                	from POINTFUN
                	full JOIN POINTSEN ON POINTFUN.POINTID = POINTSEN.POINTID) AS [t1]
                WHERE [t1].[TYPE] in {point_type}
                AND [t1].[NETDEVID] = '{controller_name}'
                AND [t1].[SENSORTYPE] = '{sensor_type}'
                AND [t1].[VIRTUAL] = {virtual}"""\
                    .format(point_type=point_type_tuple,
                            sensor_type=sensor_type,
                            virtual=virtual,
                            controller_name=controller_name)

        dataframe = sql_base.pandas_execute_sql(sql)

        return dataframe['TOTAL_COUNT'].values


    @staticmethod
    def sql_all_points(sql_base,
                       controller_name):
        # Total query
        controller_name = 'TIDWELL.L04.71602'
        sql = """
        select
        sum(case when [t1].[TYPE] = 'LAI' AND [t1].[NETDEVID] = '{controller_name}' AND [t1].[SENSORTYPE] = 'CURRENT' AND [t1].[VIRTUAL] = 0 then 1 else 0 end) AS [LAICurrent],
        sum(case when [t1].[TYPE] = 'LAI' AND [t1].[NETDEVID] = '{controller_name}' AND [t1].[SENSORTYPE] != 'CURRENT' AND [t1].[VIRTUAL] = 0 then 1 else 0 end) AS [LAIStandard],
        sum(case when [t1].[TYPE] = 'LAO' AND [t1].[NETDEVID] = '{controller_name}' AND [t1].[SENSORTYPE] = 'CURRENT' AND [t1].[VIRTUAL] = 0 then 1 else 0 end) AS [LAOCurrent],
        sum(case when [t1].[TYPE] = 'LAO' AND [t1].[NETDEVID] = '{controller_name}' AND [t1].[SENSORTYPE] != 'CURRENT' AND [t1].[VIRTUAL] = 0 then 1 else 0 end) AS [LAOStandard],
        sum(case when [t1].[TYPE] = 'LDI' AND [t1].[NETDEVID] = '{controller_name}' AND [t1].[VIRTUAL] = 0 then 1 else 0 end) AS [LDI],
        sum(case when [t1].[TYPE] = 'LDO' AND [t1].[NETDEVID] = '{controller_name}' AND [t1].[VIRTUAL] = 0 then 1 else 0 end) AS [LDO],
        sum(case when [t1].[TYPE] = 'LPACI' AND [t1].[NETDEVID] = '{controller_name}' AND [t1].[VIRTUAL] = 0 then 1 else 0 end) AS [LPACI]
        	FROM (select [POINTFUN].[POINTID], [TYPE], [VIRTUAL], [NETDEVID], [SENSORTYPE]
        		from POINTFUN
        		full JOIN POINTSEN
        		ON POINTFUN.POINTID = POINTSEN.POINTID) AS [t1];
        """.format(controller_name=controller_name)

        dataframe = sql_base.pandas_execute_sql(sql)

        return None



#%%
"""Add to a separate class"""
    # def report(self, panelName, configuration):
    #     """Generate EXCEL report for user visualization
    #     Opens report once generated
    #     parameters
    #     ----------
    #     panelName : panel/system name saved in SQL database
    #     configuration : method of counting TXIO - see Counter.count_LAnalog"""
    #     #TODO - format certain cells
    #     self.count_all_io(panelName, configuration)
    #     reportTime = str(date.today().day) +'/'+ str(date.today().month) +'/'+ str(date.today().year)
    #     values = pd.DataFrame({'Values' : [panelName,'',reportTime,'','',self.pointDict['totalLDO'],self.pointDict['totalL2SL'],
    #                                        self.pointDict['DO_SUM'],self.pointDict['extraDO'],'','',
    #                                        self.pointDict['totalLDI'],self.pointDict['totalL2SL'],self.pointDict['totalLPACI'],
    #                                        self.pointDict['DI_SUM'],self.pointDict['extraDI'],'','',
    #                                        self.pointDict['AO_SUM'],self.pointDict['totalCurrent_AO'],self.pointDict['totalStandard_AO'],
    #                                        self.pointDict['extraCurrent_AO'],self.pointDict['extraStandard_AO'],'','',
    #                                        self.pointDict['AI_SUM'],self.pointDict['totalCurrent_AI'],self.pointDict['totalStandard_AI'],
    #                                        self.pointDict['extraCurrent_AI'],self.pointDict['extraStandard_AI'],'','',
    #                                        self.pointDict['TXM1_6RM'],self.pointDict['TXM1_16D'],
    #                                        self.pointDict['TXM1_8XML'],self.pointDict['TXM1_8X'], self.pointDict['TXM1_8UML'],
    #                                        self.pointDict['TXM1_8U'], self.pointDict['emptyDO'],self.pointDict['emptyDI'],
    #                                        self.pointDict['emptyXML'],self.pointDict['emptyX'], self.pointDict['emptyUML'],
    #                                        self.pointDict['emptyU']]})
    #     labels = pd.DataFrame({'Labels' : ['Panel Name :','Report generated by Panel Builder App','Date',
    #                                '','LDO Points','Number of standard DO','Number of L2SL DO points',
    #                                'Total number of LDO points','Total number of LDO points w/ 5% added',
    #                                '','LDI Points','Number of standard DI',
    #                                'Number of L2SL DI points','Total number of LPACI points','Total number of LDI points',
    #                                'Total number of LDI points w/ 5% added',
    #                                '','LAO points','Total LAO','Total Current','Total Standard',
    #                                'Total Current w/ 5%', 'Total Standard w/ 55', '', 'LAI Points',
    #                                'Number of LAI','Total Current','Total Standard',
    #                                'Total Current w/ 5%', 'Total Standard w/ 5%',
    #                                '','Total System Stats:', 'Total TXM1.6R-M', 'Total TXM1.16D',
    #                                'Total TXM1.8X-ML', 'Total TXM1.8X', 'Total TXM1.8U-ML',
    #                                'Total TXM1.8U', 'Empty (TXM1.6R-M) Slots', 'Empty (TXM1.16D) Slots',
    #                                'Empty (TXM1.8X-ML) Slots','Empty (TXM1.8X) Slots', 'Empty (TXM1.8U-ML) Slots',
    #                                'Empty (TXM1.8U) Slots']})
    #     global df
    #     df = labels.join(values)
    #     writer = pd.ExcelWriter('TXIO_Test1.xlsx', engine='xlsxwriter')

    #     df.to_excel(writer, sheet_name=panelName, startrow= 0, startcol= 0, header=False, index=False)
    #     writer.save()
    #     path = r'start EXCEL.EXE ' + os.getcwd() + r"\TXIO_Test1.xlsx"
    #     os.system(path)






"""Add to a separate class"""
    # def add_TXIO(self, panelName):
    #     """Automatically add TXIO to panel specified. Call this conditionally,
    #     and only after the pointDict has been populated"""


    #     def descriptor_lookup(txio):
    #         descriptorDict = {'TXM1.6R-M':'6 DO Relay w/HOA', 'TXM1.16D':'16 DI',
    #                           'TXM1.8U':'8 Universal','TXM1.8U-ML':'8 Universal w/LOID',
    #                           'TXM1.8X':'8 Sup Univ w/4-20mA','TXM1.8X-ML':'8 Sup Univ w/4-20 w/LOID',
    #                           'TXS1.EF4':'Bus Extender 4A Fuse', 'TXS1.12F4':'Pwr Supply 1.2A 4A Fuse'}
    #         try:
    #             descriptor = descriptorDict[txio]
    #         except:
    #             return False
    #             print('Unknown TXIO')
    #         return descriptor

    #     def get_parentid(panelName):
    #         #search NETDEV table for panel name - then get the parentID
    #         loc = np.where(self.NETDEV['PARENTID']==panelName)
    #         return self.NETDEV.loc[loc[0][0], 'NETDEVID']

    #     def check_existing_any():
    #         #see if panel already has ANY TXIO assigned to it
    #         index = 0
    #         indexlist = []
    #         for names in self.NETDEV['NETDEVID']:
    #             for i in range(0,len(names) - len(panelName)):
    #                 section = names[0+i:len(panelName)+i]
    #                 if section == panelName:
    #                     indexlist.append(index)
    #             index += 1
    #         txioModules = self.NETDEV.loc[indexlist, 'PARTNO']
    #         txioList = ['TXM1.6R-M', 'TXM1.16D','TXM1.8U','TXM1.8U-ML','TXM1.8X',
    #                     'TXM1.8X-ML']
    #         for items in txioList:
    #             if txioModules.str.contains(items).any():
    #                 return True
    #             else:
    #                 return False

    #     def check_existing_device(device):
    #         #Check for existance of SPECIFIC device - any of TXIOList
    #         #return true if at least one device  exists
    #         index = 0
    #         indexlist = []
    #         for names in self.NETDEV['NETDEVID']:
    #             for i in range(0,len(names) - len(panelName)):
    #                 section = names[0+i:len(panelName)+i]
    #                 if section == panelName:
    #                     indexlist.append(index)
    #             index += 1
    #         txioModules = self.NETDEV.loc[indexlist, 'PARTNO']
    #         if txioModules.str.contains(device).any():
    #             return True
    #         else:
    #             return False

    #     def order_txio(_TXIODict):
    #         #Order to add IO modules
    #         defaultOrder = ['TXM1.8X-ML','TXM1.8U-ML','TXM1.8U','TXM1.8X','TXM1.6R-M','TXM1.16D']
    #         txioOrder = []
    #         for txio in defaultOrder: #order other TXIO
    #             number2add = _TXIODict[txio]
    #             for i in range(0,number2add):
    #                 txioOrder.append(txio)
    #         txioSum = 0
    #         for item in txioOrder: #Number of TXIO currently
    #             if defaultOrder.__contains__(item):
    #                 txioSum += 1
    #                 if txioSum == 3:
    #                     txioOrder.insert(3,'TXS1.EF4')
    #         if _TXIODict['TXS1.12F4'] == 1: #Add power supply to slot 1
    #             txioOrder.insert(0, 'TXS1.12F4')
    #         return txioOrder

    #     def get_start_index():
    #         index = 0
    #         indexlist = []
    #         for names in self.NETDEV['NETDEVID']:
    #             for i in range(0,len(names) - len(panelName)):
    #                 section = names[0+i:len(panelName)+i]
    #                 if section == panelName:
    #                     indexlist.append(index)
    #             index += 1
    #         IDList = self.NETDEV.loc[indexlist,'NETDEVID']
    #         values = [val[len(val)-3:] for val in IDList]
    #         values = [int(val) for val in values]
    #         try:
    #             maxval = max(values)
    #         except ValueError:
    #             maxval = 0
    #         return maxval

    #     def get_address1(txioOrder):
    #         address1 = []
    #         for partno in txioOrder:
    #             if partno == 'TXS1.EF4':
    #                 num2add = 39
    #                 str2add = str()
    #                 for i in range(0,num2add):
    #                     str2add = str2add.__add__(' ')
    #                 address1.append(str2add + 'Y')
    #             elif partno == 'TXS1.12F4':
    #                 num2add = 39
    #                 str2add = str()
    #                 for i in range(0,num2add):
    #                     str2add = str2add.__add__(' ')
    #                 address1.append(str2add + 'X')
    #             else:
    #                 stripAddress = [item.replace(' ','') for item in address1]
    #                 addressValues = [int(item) for item in stripAddress if item.isnumeric()]
    #                 try:
    #                     maxval = max(addressValues)
    #                 except ValueError:
    #                     maxval = 0
    #                 maxval = maxval + 1
    #                 num2add = 40 - len(str(maxval))
    #                 str2add = str()
    #                 for i in range(0,num2add):
    #                     str2add = str2add.__add__(' ')
    #                 address1.append(str2add + str(maxval))
    #         return address1

    #     def write_to(_values):
    #         global values
    #         values = _values
    #         """Writes a list of values to a row in a database"""
    #         sql = """INSERT INTO NETDEV
    #         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
    #          ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    #         self.cursor.execute(sql, _values)
    #         self.cursor.commit()

    #     def get_address3(indexList):
    #         address3 = []
    #         for index in indexList:
    #             if len(str(index)) == 1:
    #                 num2add = 39
    #                 str2add = str()
    #                 for i in range(0,num2add):
    #                     str2add = str2add.__add__(' ')
    #                 address3.append(str2add + str(index))
    #             elif len(str(index)) == 2:
    #                 num2add = 38
    #                 str2add = str()
    #                 for i in range(0,num2add):
    #                     str2add = str2add.__add__(' ')
    #                 address3.append(str2add + str(index))
    #             elif len(str(index)) == 3:
    #                 num2add = 37
    #                 str2add = str()
    #                 for i in range(0,num2add):
    #                     str2add = str2add.__add__(' ')
    #                 address3.append(str2add + str(index))
    #         return address3

    #     def get_address2(indexList):
    #         address2 = []
    #         for index in indexList:
    #             str2add = str()
    #             for i in range(0,39):
    #                 str2add = str2add.__add__(' ')
    #             address2.append(str2add + '0')
    #         return address2

    #     self.TXIODict = {'TXM1.6R-M':self.pointDict['TXM1_6RM'], 'TXM1.16D':self.pointDict['TXM1_16D'],
    #                    'TXM1.8X-ML':self.pointDict['TXM1_8XML'],'TXM1.8U-ML':self.pointDict['TXM1_8UML'],
    #                    'TXM1.8X':self.pointDict['TXM1_8X'], 'TXM1.8U':self.pointDict['TXM1_8U'],
    #                    'TXS1.EF4':0, 'TXS1.12F4':0} #Dict of TXIO

    #     if check_existing_device('TXS1.12F4'): #Add power supply if not existing
    #         self.TXIODict['TXS1.12F4']=0
    #     elif not(check_existing_device('TXS1.12F4')):
    #         self.TXIODict['TXS1.12F4']=1

    #     sumTXIO = (self.pointDict['TXM1_6RM'] + self.pointDict['TXM1_16D'] + self.pointDict['TXM1_8XML'] +
    #                self.pointDict['TXM1_8UML'] + self.pointDict['TXM1_8X'] + self.pointDict['TXM1_8U'])
    #     if (sumTXIO >= 3) & (not(check_existing_device('TXS1.EF4'))): #Add Bus extender if > 3 modules
    #         self.TXIODict['TXS1.EF4'] = 1
    #     else:
    #         self.TXIODict['TXS1.EF4'] = 0

    #     TXIOOrder = order_txio(self.TXIODict) #get ordered list of TXIO to add
    #     start = get_start_index()+1 #Construct index, device name, netdevid (-X00), address
    #     indexList = [index+start for index, val in enumerate(TXIOOrder)]
    #     ID = []
    #     for ind in indexList:
    #         if len(str(ind)) == 1:
    #             ID.append('00'+str(ind))
    #         elif len(str(ind)) == 2:
    #             ID.append('0'+str(ind))
    #         else:
    #             print('Error')
    #     netdevidtest = [panelName + '-X' + ID for ID in ID]
    #     address1 = get_address1(TXIOOrder)
    #     address2 = get_address2(indexList)
    #     address3 = get_address3(indexList)
    #     global txiodf
    #     txiodf = pd.DataFrame({'INDEX':indexList, 'PARTNO':TXIOOrder,'NETDEVID':netdevidtest,'ADDRESS1':address1,
    #                            'ADDRESS2':address2, 'ADDRESS3':address3})

    #     for i in txiodf.index:
    #         NETDEVID =  txiodf.loc[i, 'NETDEVID'] #'PanelName' + '-X###', see rules for assigning numbers to ###
    #         PARENTID = get_parentid(panelName) #Search panelName -> get PARENTID
    #         NAME = NETDEVID
    #         CTSYSNAME = None #Check on complete job
    #         DESCRIPTOR = descriptor_lookup(txiodf.loc[i, 'PARTNO']) #use descriptor_lookup()
    #         TYPE = 'FLN DEVICE'
    #         SUBTYPE = 'TXIO'
    #         DWG_NAME = None
    #         ADDRNAME1 = 'Node Number'
    #         ADDRESS1 = txiodf.loc[i, 'ADDRESS1']
    #         ADDRNAME2 = 'FLN Number'
    #         ADDRESS2 = txiodf.loc[i,'ADDRESS2']
    #         ADDRNAME3 = 'Order'
    #         ADDRESS3 = txiodf.loc[i,'ADDRESS3'] #Same as ### on NETDEVID..
    #         STARTADDR = float(0)
    #         ADDRSTYLE = 'APOGEE'
    #         PARTNO = txiodf.loc[i,'PARTNO'] #Lookup the part number... TXM1.16D etc
    #         REFERNAME = None
    #         TBLOCKID = float(7)
    #         BAUDRATE = None
    #         ONETOFOUR = 'N'
    #         FLNTYPE = 'P1'
    #         INSTANCE = None
    #         DNS = None
    #         MACADDRESS = None
    #         NODEADDR = None
    #         SITENAME = None

    #         global values
    #         values = [NETDEVID, PARENTID, NAME, CTSYSNAME, DESCRIPTOR,
    #                   TYPE, SUBTYPE, DWG_NAME, ADDRNAME1, ADDRESS1,
    #                   ADDRNAME2, ADDRESS2, ADDRNAME3, ADDRESS3,
    #                   STARTADDR, ADDRSTYLE, PARTNO, REFERNAME,
    #                   TBLOCKID, BAUDRATE, ONETOFOUR, FLNTYPE,
    #                   INSTANCE, DNS, MACADDRESS, NODEADDR, SITENAME]
    #         write_to(values) #send all items to SQL table NETDEV

    # def check_existing_any(self, panelName):
    #     """Checks to see if a system (panelName) has any TXIO devices attached to it.
    #     TXIO devices are defined as any I/O carrying devices.  This does not include power
    #     supplies, IBE, the controller.
    #     parameters
    #     ----------
    #     panelName : name of system you wish to check for TXIO"""
    #     index = 0
    #     indexlist = []
    #     for names in self.NETDEV['NETDEVID']:
    #         for i in range(0,len(names) - len(panelName)):
    #             section = names[0+i:len(panelName)+i]
    #             if section == panelName:
    #                 indexlist.append(index)
    #         index += 1
    #     txioModules = self.NETDEV.loc[indexlist, 'PARTNO']
    #     txioList = ['TXM1.6R-M', 'TXM1.16D','TXM1.8U','TXM1.8U-ML','TXM1.8X',
    #                 'TXM1.8X-ML']
    #     for items in txioList:
    #         if txioModules.str.contains(items).any():
    #             return True
    #         else:
    #             return False












class AddDevice():

    def __init__(self, engine, cursor):
        self.engine = engine
        self.cursor = cursor
        self.DEVICES = pd.read_sql_table('DEVICES', self.engine)

    def add_device(self, partDict, system, newPart = 0):
        """Add devices to the DEVICE table in Job Database. No support for part
        number description lookup. Current version only supports TXIO devices.
        No support for : device number, location
        Parameters
        ----------
        partDict : Dictionary {} of part number(s) to be added w/ quantity (see TXIODict)
        system : string of system to add devices to
        newPart ; 1 if new, 0 if existing (no support for 1 yet)
        """
        def increment_part_type(system):
            mybool = ((self.DEVICES['SYSTEM'] == system) & (self.DEVICES['DEV_NUMBER'] == '   000'))
            sysindex = [index for index, boolian in enumerate(mybool) if boolian]
            partVal = self.DEVICES.loc[sysindex, 'PART_TYPE']
            partVal = [int(val) for val in partVal if val.isnumeric()]
            maxVal = max(partVal)
            partTypeIncrement = maxVal + 1
            partTypeStr = 2*chr(32) + str(partTypeIncrement) #2x chr(32) + string
            return partTypeStr

        def descriptor_lookup(txio):
            descriptorDict = {'TXM1.6R-M':'6 DO Relay w/HOA', 'TXM1.16D':'16 DI',
                              'TXM1.8U':'8 Universal','TXM1.8U-ML':'8 Universal w/LOID',
                              'TXM1.8X':'8 Sup Univ w/4-20mA','TXM1.8X-ML':'8 Sup Univ w/4-20 w/LOID',
                              'TXS1.EF4':'Bus Extender 4A Fuse', 'TXS1.12F4':'Pwr Supply 1.2A 4A Fuse'}
            try:
                descriptor = descriptorDict[txio]
            except:
                return False
                print('Unknown TXIO')
            return descriptor

        deviceDF = self.get_existing_0(system)
        print('Old Existing Devices : {}'.format(deviceDF))
        for part in partDict:
            mybool = deviceDF['PARTNO'] == part
            if mybool.any(): #change quantity of existing line
                sqlQuantity = """SELECT QUANTITY FROM DEVICES
                WHERE SYSTEM = ? AND PARTNO = ? AND DEV_NUMBER = ?"""
                global oldQuantity
                self.cursor.execute(sqlQuantity, (system, part, '   000'))
                rowList = self.cursor.fetchall()
                row = rowList[0]
                oldQuantity = row.QUANTITY
                quantity = int(oldQuantity) + partDict[part]
                sqlUpdate = """UPDATE (DEVICES)
                SET QUANTITY = ?
                WHERE SYSTEM = ? AND PARTNO = ? AND DEV_NUMBER = ?"""
                self.cursor.execute(sqlUpdate, (quantity, system, part, '   000'))

            else:
                #Increment part_type and add new line
                BMS_SYS_NO = None
                CS = 'PXCM'
                DEV_NUMBER = '   000' #3x space + number
                SYSTEM = system
                INDWG = None
                JOR_ITEM = None
                LOCATION = 'PANEL'
                MOD_FIELD = None
                PARTNO = part
                PART_TYPE = increment_part_type(system) #lookup the highest number and add 1
                QUANTITY = float(partDict[part]) #From dictionary quantity
                RETRO = None
                DESCRIPT = descriptor_lookup(part)
                ISA_DEV_ID = None
                RH = None
                TEMP = None
                STPT = None
                PTNAME = None
                AREA1 = None
                AREA2 = None
                AREA3 = None
                AREA4 = None
                ROOM1 = None
                ROOM2 = None
                ROOM3 = None
                ROOM4 = None

                values = [BMS_SYS_NO,CS,DEV_NUMBER,SYSTEM,INDWG,JOR_ITEM,LOCATION,MOD_FIELD,PARTNO,
                       PART_TYPE,QUANTITY,RETRO,DESCRIPT,ISA_DEV_ID,RH,TEMP,STPT,PTNAME,AREA1,
                       AREA2,AREA3,AREA4,ROOM1,ROOM2,ROOM3,ROOM4]
                self.write_to_database(values)

        newSQL = """SELECT DEVICES
        WHERE SYSTEM = ? AND DEV_NUMBER = ?"""
        self.cursor.execute(newSQL, (system, '   000')) #Error checking purpose?
        newDF = self.cursor.fetchall()
        print('New Dataframe : {}'.format(newDF))

    def get_existing_0(self, system):
        """Returns current devices under a system (only 000 PXCM parts)"""
        mybool = ((self.DEVICES['SYSTEM'] == system) & (self.DEVICES['DEV_NUMBER'] == '   000'))
        sysindex = [index for index, boolian in enumerate(mybool) if boolian]
        global partDevicesDF
        partDevicesDF = self.DEVICES.loc[sysindex, :]
        return partDevicesDF

    def get_existing_1(self, system):
        """Returns current devices under a system (all device numbers)"""
        pass

    def write_to_database(self, _values):
        """Writes a list of values to a row in a database"""
        sql = """INSERT INTO NETDEV
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
         ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        self.cursor.execute(sql, _values)
        self.cursor.commit()

