# -*- coding: utf-8 -*-
"""
Created on Fri Dec  7 21:34:10 2018

@author: z003vrzk
"""

import pandas as pd
import JVWork_readSQL5 as JVSQL
import math
import numpy as np
from datetime import date

class Counter():
    """Counter class is used to count number of TXIO modules required for a 
    PXC Modular. See methods for more explanation"""
    #TODO Option to place device on panel (through SQL)
    #TODO Make percent added dyamic w/ user input
    
    def __init__(self, pathMDF, panelName):
        """Connect to SQL master database
        Attach user-specified Job Database
        Connect to SQL specified Job Database
        Read in required SQL tables to dataframes
        Construct point dictionary
        Parameters
        ----------
        pathMDF : path to MDF file we are trying to read/write
        """
        #Begin SQL connection to import data
        jvsql = JVSQL.MySQLHandling() #JV SQL module
        self.cursorMaster, self.connMaster = jvsql.create_master_connection() #connect master database
        jvsql.attach(pathMDF) #attach user specified file
        self.engine, self.conn, self.cursor = jvsql.create_PBDB_connection() #connect PBJobDB database
        
        self.POINTBAS = pd.read_sql_table('POINTBAS', self.engine) #import POINTBAS table
        self.POINTFUN = pd.read_sql_table('POINTFUN', self.engine)
        self.POINTSEN = pd.read_sql_table('POINTSEN', self.engine)
        self.pointDict = {'LDO':0,'LDI':0,'LAO':{'Current':0, 'Standard':0},'LAI':{'Current':0, 'Standard':0},'L2SL':0,'LENUM':0,'LPACI':0}
        self.totalLDO, self.totalL2SL, self.DO_SUM, self.DO_SUM_EXTRA, self.TXM1_6RM = self.count_LDO(panelName)
        self.totalLDI, self.totalL2SL, self.totalLPACI, self.DI_SUM, self.DI_SUM_EXTRA, self.TXM1_16D = self.count_LDI(panelName)
        self.totalAO, self.totalCurrent_AO, self.totalStandard_AO, self.TXM1_8XML_AO, self.TXM1_8UML_AO, self.emptyULM_AO, self.emptyXML_AO = self.count_LAO(panelName)
        self.AI_SUM, self.totalCurrent_AI, self.totalStandard_AI, self.TXM1_8XML_AI, self.TXM1_8UML_AI, self.emptyULM_AI, self.emptyXML_AI = self.count_LAI(panelName)
        self.emptyDI = self.TXM1_16D*16 - self.DI_SUM
        self.emptyDO = self.TXM1_6RM*6 - self.DO_SUM
        self.emptyUniversal = 0
        
        
        
    def unique_panels(self):
        """Returns a set of unique panels detected. Count.uniquePanels"""
        self.uniquePanels = set(self.POINTBAS.loc[:, 'NETDEVID'])
        return self.uniquePanels
        
    def count_LDO(self, panelName):
        """Count all LDO points on a specific panel.
        Parameters
        ----------
        panelName : String, DT panel name; see Count.uniquePanels for set of
        unique panels
        """
        DO_Types = ['LDO', 'L2SL']
        totalLDO = sum((self.POINTBAS.loc[:, 'TYPE'] == 'LDO') & (self.POINTBAS.loc[:,'NETDEVID'] == panelName))
        totalL2SL = sum((self.POINTBAS.loc[:, 'TYPE'] == 'L2SL') & (self.POINTBAS.loc[:,'NETDEVID'] == panelName))
        DO_SUM = totalLDO + totalL2SL/2
        DO_SUM_EXTRA = math.ceil(DO_SUM*1.05)
        TXM1_6RM = math.ceil(DO_SUM*1.05/6)
        self.pointDict['LDO'] = DO_SUM
        
        print('Number of standard DO = ', totalLDO)
        print('Number of L2SL DO points = ', totalL2SL/2)
        print('total number of LDO points : ', DO_SUM)
        print('total number of LDO points with 5% added = ', DO_SUM_EXTRA)
        print('total number of TXM1.6R-M required = ', TXM1_6RM, '\n')
        return totalLDO, totalL2SL/2, DO_SUM, DO_SUM_EXTRA, TXM1_6RM
        
    def count_LDI(self, panelName):
        """Count all LDI points on a specific panel.
        Parameters
        ----------
        panelName : String, DT panel name; see Count.uniquePanels for set of
        unique panels
        """
        DI_TYPES = ['LDI','L2SL', 'LPACI']
        totalLDI = sum((self.POINTBAS.loc[:,'TYPE'] == 'LDI') & (self.POINTBAS.loc[:,'NETDEVID'] == panelName))
        totalL2SL = sum((self.POINTBAS.loc[:,'TYPE'] == 'L2SL') & (self.POINTBAS.loc[:,'NETDEVID'] == panelName))
        totalLPACI = sum((self.POINTBAS.loc[:,'TYPE'] == 'LPACI') & (self.POINTBAS.loc[:,'NETDEVID'] == panelName))
        DI_SUM = totalLDI + totalL2SL/2 + totalLPACI
        DI_SUM_EXTRA = math.ceil(DI_SUM*1.05)
        TXM1_16D = math.ceil(DI_SUM_EXTRA/16)
        self.pointDict['LDI'] = DI_SUM
        
        print('Total LDI : ', DI_SUM)
        print('Number of L2SL DI points = ', totalL2SL/2)
        print('Number of LPACI DI points = ', totalLPACI)
        print('Total LDI w/ 5% added = ', DI_SUM_EXTRA)
        print('total number of TXM1.16D required = ', TXM1_16D, '\n')
        return totalLDI, totalL2SL/2, totalLPACI, DI_SUM, DI_SUM_EXTRA, TXM1_16D
        
#    def count_LAO(self, panelName):
#        """Count all LAO points on a specific panel.  Makes differentiation between
#        SUPER and STANDARD universal points
#        Parameters
#        ----------
#        panelName : String, DT panel name; see Count.uniquePanels for set of
#        unique panels
#        """
#        #TODO Option of all on 8X
#        AO_SUM = sum((self.POINTBAS.loc[:,'TYPE'] == 'LAO') & (self.POINTBAS.loc[:,'NETDEVID'] == panelName))
#        dataframe = pd.DataFrame(np.zeros((self.POINTSEN.shape[0],3)))
#        for i in range(0,self.POINTSEN.shape[0]): #Match POINTID with NETDEVID to select panel only
#            dataframe.loc[i,0] = self.POINTSEN.loc[i,'POINTID']
#            index = np.where(self.POINTBAS['POINTID']==self.POINTSEN.loc[i,'POINTID'])[0][0]
#            dataframe.loc[i,1] = self.POINTBAS.loc[index, 'TYPE']
#            dataframe.loc[i,2] = self.POINTBAS.loc[index, 'NETDEVID']
#        
#        totalCurrent_AO = sum((self.POINTSEN['SENSORTYPE'] == 'CURRENT') & (dataframe[2] == panelName) & (dataframe[1] == 'LAO'))
#        totalStandard_AO = sum((self.POINTSEN['SENSORTYPE'] != 'CURRENT') & (dataframe[2] == panelName) & (dataframe[1] == 'LAO'))
#        self.pointDict['LAO']['Current'] = totalCurrent_AO
#        self.pointDict['LAO']['Standard'] = totalStandard_AO
#        current_Extra = totalCurrent_AO*1.05
#        standard_Extra = totalStandard_AO*1.05
#        TXM1_8XML = math.ceil(current_Extra/8)
#        emptyXML = TXM1_8XML*8 - totalCurrent_AO
#        TXM1_8UML = math.ceil((standard_Extra - emptyXML)/8)
#        emptyUML = TXM1_8UML*8 - totalStandard_AO
#        if emptyUML < 0:
#            if abs(emptyUML) < (TXM1_8XML*8 - totalCurrent_AO):
#                emptyUML = 0
#                emptyXML = TXM1_8XML*8 - totalCurrent_AO - (abs(TXM1_8UML*8 - totalStandard_AO))
#            else:
#                print('Error')
#        else:
#            emptyXML = (TXM1_8XML*8 - totalCurrent_AO)
#        
#        print('Total LAO : ', AO_SUM)
#        print('Total Current : ', totalCurrent_AO)
#        print('Total Standard : ', totalStandard_AO)
#        print('Total Current w/ 5% : ', current_Extra)
#        print('Total Standard w/ 5% : ', standard_Extra)
#        print('Number of TXM1.8X-ML for 4-20mA output required w/ 5% = ', TXM1_8XML)
#        print('Number of TXM1.8U-ML for standard out etc. required = ', TXM1_8UML)
##        print('Number of empty TXM1.8U-ML slots = ', self.emptyUniversal, '\n')
#        return totalAO, totalCurrent_AO, totalStandard_AO, TXM1_8XML, TXM1_8UML, emptyUML, emptyXML
#        
#    def count_LAI(self, panelName, emptyULM_AO, emptyXML_AO):
#        """Count all LAI points on a specific panel.  Makes differentiation between
#        SUPER and STANDARD universal points
#        Parameters
#        ----------
#        panelName : String, DT panel name; see Count.uniquePanels for set of
#        unique panels
#        """
#        #TODO Option of all on 8X
#        global dataframe
#        AI_SUM = sum((self.POINTBAS.loc[:,'TYPE'] == 'LAI') & (self.POINTBAS['NETDEVID']==panelName))
#        dataframe = pd.DataFrame(np.zeros((self.POINTSEN.shape[0],3)))
#        for i in range(0,self.POINTSEN.shape[0]):
#            dataframe.loc[i,0] = self.POINTSEN.loc[i,'POINTID']
#            index = np.where(self.POINTBAS['POINTID']==self.POINTSEN.loc[i,'POINTID'])[0][0]
#            dataframe.loc[i,1] = self.POINTBAS.loc[index, 'TYPE']
#            dataframe.loc[i,2] = self.POINTBAS.loc[index, 'NETDEVID']
#            
#        totalCurrent_AI = sum((self.POINTSEN['SENSORTYPE'] == 'CURRENT') & (dataframe[2] == panelName) & (dataframe[1] == 'LAI'))
#        totalStandard_AI = sum((self.POINTSEN['SENSORTYPE'] != 'CURRENT') & (dataframe[2] == panelName) & (dataframe[1] == 'LAI'))
#        self.pointDict['LAI']['Current'] = totalCurrent_AI
#        self.pointDict['LAI']['Standard'] = totalStandard_AI
#        current_Extra = totalCurrent_AI*1.05
#        standard_Extra = totalStandard_AI*1.05   
#        TXM1_8XML = math.ceil((current_Extra - emptyXML_AO)*1.05/8)
#        emptyXML = TXM1_8XML*8 + emptyXML_AO - totalCurrent_AI 
#        TXM1_8UML = math.ceil((totalStandard_AI - emptyULM_AO - emptyXML)*1.05/8)
#        
#
#        TXM1_8XML = math.ceil(current_Extra/8)
#        emptyXML = TXM1_8XML*8 - totalCurrent_AI
#        TXM1_8UML = math.ceil((standard_Extra - emptyXML)/8)
#        emptyUML = TXM1_8UML*8 - totalStandard_AI
#        if emptyUML < 0:
#            if abs(emptyUML) < (TXM1_8XML*8 - totalCurrent_AO):
#                emptyUML = 0
#                emptyXML = TXM1_8XML*8 - totalCurrent_AI - (abs(TXM1_8UML*8 - totalStandard_AI))
#            else:
#                print('Error')
#        else:
#            emptyXML = (TXM1_8XML*8 - totalCurrent_AI)
#        
#        print('Total LAI : ', AI_SUM)
#        print('Total Current : ', totalCurrent_AI)
#        print('Total Standard : ', totalStandard_AI)
#        print('Total Current w/ 5% : ', current_Extra)
#        print('Total Standard w/ 5% : ', standard_Extra)
#        print('Number of TXM1.8X-ML for 4-20mA Input required w/ 5% = ', TXM1_8XML)
#        print('Number of TXM1.8U-ML for standard Input etc. required = ', TXM1_8UML, '\n')
#        return AI_SUM, totalCurrent_AI, totalStandard_AI, TXM1_8XML, TXM1_8UML, emptyUML, emptyXML
    
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
        """
        #TODO Option of all on 8X
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
        extraCurrent_AO = math.floor(totalCurrent_AO*1.05)
        extraStandard_AO = math.floor(totalStandard_AO*1.05)
        
        dataframe_AI = pd.DataFrame(np.zeros((self.POINTSEN.shape[0],3)))
        for i in range(0,self.POINTSEN.shape[0]):
            dataframe_AI.loc[i,0] = self.POINTSEN.loc[i,'POINTID']
            index = np.where(self.POINTBAS['POINTID']==self.POINTSEN.loc[i,'POINTID'])[0][0]
            dataframe_AI.loc[i,1] = self.POINTBAS.loc[index, 'TYPE']
            dataframe_AI.loc[i,2] = self.POINTBAS.loc[index, 'NETDEVID']  
        totalCurrent_AI = sum((self.POINTSEN['SENSORTYPE'] == 'CURRENT') & (dataframe_AI[2] == panelName) & (dataframe_AI[1] == 'LAI'))
        totalStandard_AI = sum((self.POINTSEN['SENSORTYPE'] != 'CURRENT') & (dataframe_AI[2] == panelName) & (dataframe_AI[1] == 'LAI'))
        extraCurrent_AI = math.floor(totalCurrent_AI*1.05)
        extraStandard_AI = math.floor(totalStandard_AI*1.05)
        
        self.pointDict['LAO']['Current'] = totalCurrent_AO
        self.pointDict['LAO']['Standard'] = totalStandard_AO
        self.pointDict['LAI']['Current'] = totalCurrent_AI
        self.pointDict['LAI']['Standard'] = totalStandard_AI
        
        #Map based on function call?
        """configuration map
        0 -> TXM18ML()
        1 -> TXM18X()
        2 -> TXM18X_8U()
        3 -> TXM18XML_8UML()
        4 -> TXM18XML_8UML_8X_8U()"""
        flsit = [TXM18XML, TXM18X, TXM18X_8U, TXM18XML_8UML, TXM18XML_8UML_8X_8U]
        flist[configuration]()
        
        
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
            return (AO_SUM, totalCurrent_AO, extraCurrent_AO, totalStandard_AO, 
                    extraStandard_AO, totalCurrent_AI, extraCurrent_AI, 
                    totalStandard_AI, extraStandard_AI, TXM1_8XML, TXM1_8UML, 
                    TXM1_8X, TXM1_8U, emptyXML, emptyUML, emptyX, emptyU)
        
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
            return (AO_SUM, totalCurrent_AO, extraCurrent_AO, totalStandard_AO, 
            extraStandard_AO, totalCurrent_AI, extraCurrent_AI, 
            totalStandard_AI, extraStandard_AI, TXM1_8XML, TXM1_8UML, 
            TXM1_8X, TXM1_8U, emptyXML, emptyUML, emptyX, emptyU)
            
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
            return (AO_SUM, totalCurrent_AO, extraCurrent_AO, totalStandard_AO, 
            extraStandard_AO, totalCurrent_AI, extraCurrent_AI, 
            totalStandard_AI, extraStandard_AI, TXM1_8XML, TXM1_8UML, 
            TXM1_8X, TXM1_8U, emptyXML, emptyUML, emptyX, emptyU)
        
        def TXM18XML_8UML():
            """8U-ML and 8X-ML for all analog points"""
            TXM1_8XML = math.ceil((extraCurrent_AO + extraCurrent_AI)/8) #Assume AO 4-20mA is possible w/ 4 slots per module
            TXM1_8X = 0
            TXM1_8U = 0
            emptyXML = TXM1_8XML*8 -totalCurrent_AO - totalCurrent_AI
            TXM1_8UML = math.ceil((extraStandard_AO + extraStandard_AI - emptyXML)/8)
            emptyUML = TXM1_8UML*8 - totalStandard_AO - totalStandard_AI
            if emptyUML < 0:
                if abs(emptyUML) < (TXM1_8XML*8 - totalCurrent_AO - totalCurrent_AI): #Place them on the extra X slots
                    emptyUML = 0
                    emptyXML = TXM1_8XML*8 - totalCurrent_AO - totalCurrent_AI - (abs(TXM1_8UML*8 - totalStandard_AO - totalStandard_AI))
                else:
                    print('Error')
            return (AO_SUM, totalCurrent_AO, extraCurrent_AO, totalStandard_AO, 
            extraStandard_AO, totalCurrent_AI, extraCurrent_AI, 
            totalStandard_AI, extraStandard_AI, TXM1_8XML, TXM1_8UML, 
            TXM1_8X, TXM1_8U, emptyXML, emptyUML, emptyX, emptyU)
            
        def TXM18XML_8UML_8X_8U():
            """8X-ML and 8U-ML for outputs, 8U and 8X for inputs"""
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
                        spaceNeeded = spaceNeeded - emptyX
                        emptyX = 0
                        emptyUML = emptyUML - spaceNeeded
                        spaceNeeded = spaceNeeded - emptyUML
                        if spaceNeeded > 0:
                            print('Error')
                else:
                    print('Error')
            return (AO_SUM, totalCurrent_AO, extraCurrent_AO, totalStandard_AO, 
            extraStandard_AO, totalCurrent_AI, extraCurrent_AI, 
            totalStandard_AI, extraStandard_AI, TXM1_8XML, TXM1_8UML, 
            TXM1_8X, TXM1_8U, emptyXML, emptyUML, emptyX, emptyU)
        
        
        print('Total LAI : ', AI_SUM)
        print('Total Current : ', totalCurrent_AI)
        print('Total Standard : ', totalStandard_AI)
        print('Total Current w/ 5% : ', extraCurrent_AI)
        print('Total Standard w/ 5% : ', extraStandard_AI)
        print('Number of TXM1.8X-ML for 4-20mA Input required w/ 5% = ', TXM1_8XML)
        print('Number of TXM1.8U-ML for standard Input etc. required = ', TXM1_8UML, '\n')
        
        print('Total LAO : ', AO_SUM)
        print('Total Current : ', totalCurrent_AO)
        print('Total Standard : ', totalStandard_AO)
        print('Total Current w/ 5% : ', extraCurrent_AO)
        print('Total Standard w/ 5% : ', extraStandard_AO)
        print('Number of TXM1.8X-ML for 4-20mA output required w/ 5% = ', TXM1_8XML)
        print('Number of TXM1.8U-ML for standard out etc. required = ', TXM1_8UML)
        
    def count_all_io(self, panelName):
        """Convenience wrapper. Calls count_LDO, count_LDI, count_LAO, count_LAI
        and generates a report.  
        Parameters
        --------------
        panelName : User specified panelName. Counts only IO for that panel
        """
        self.count_LDO(panelName)
        self.count_LDI(panelName)
        self.count_LAO(panelName)
        self.count_LAI(panelName)
        
    def report(self, panelName):
        #TODO - create excel report
        labels = pd.DataFrame({'Labels' : ['Panel Name :','Report generated by Panel Builder App','Date',
                                   '','LDO Points','Number of standard DO','Number of L2SL DO points',
                                   'Total number of LDO points','Total number of LDO points w/ 5% added',
                                   'Total number of TXM1.6-RM','','LDI Points','Number of standard DI',
                                   'Number of L2SL DI points','Total number of LPACI points','Total number of LDI points',
                                   'Total number of LDI points w/ 5% added','Ttotal number of TXM1.16D',
                                   '','LAO points','Number of LAO','Total Current','Total Standard',
                                   'Number of TXM1.8X-ML for 4-20mA output required w/ 5%',
                                   'Number of TXM1.8U-ML for standard out required',
                                   '','LAI Points',
                                   'Number of LAI','Total Current','Total Standard',
                                   'Number of TXM1.8X-ML for 4-20mA Input required w/ 5%',
                                   'Number of TXM1.8U-ML for standard Input etc. required',
                                   '','Total System Stats:','Number of Empty DI (TXM1.16D)',
                                   'Number of Empty Universal (TXM1.8U-ML & TXM1.8U)',
                                   'Number of Empty SuperUniversal (TXM1.8X-ML & TXM1.8X)',
                                   'Total TXM1.16D','Total TXM1.6R-M','Total TXM1.8U',
                                   'Total TXM1.8U-ML','Total TXM1.8X','Total TXM1.8X-ML']})
        reportTime = str(date.today().day) +'/'+ str(date.today().month) +'/'+ str(date.today().year)
        values = pd.DataFrame({'Values' : [panelName,'',reportTime,'','','']})
        
        
        
        df = pd.DataFrame({'Data':[Values]})
        writer = pd.ExcelWriter('TXIO_Test1.xlsx', engine='xlsxwriter')
        
        df.to_excel(writer, sheet_name=panelName, startrow= 1, startcol= 1, header=False, index=False)
        
        workbook = writer.book
        worksheet = writer.sheets[panelName]
        


            
pathMDF = 'C:\SQLTest\JobDB.mdf'
panelName = 'JHW.PXCM01'
count = Counter(pathMDF, panelName)
pointbas = count.POINTBAS
pointfun = count.POINTSEN
pointsen = count.POINTSEN
pointDict = count.pointDict


count.count_LDO(panelName)
count.count_LDI(panelName)
count.count_LAO(panelName)
count.count_LAI(panelName)

uniquePanels = count.unique_panels()
















#"""Accessign pandas dataframes"""
#Using loc to access column names
#dataframe.loc[0:5,'POINTID']
##Slice index
#dataframe[0:5]
#














