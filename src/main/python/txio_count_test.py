# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 09:55:59 2021

@author: z003vrzk
"""

import unittest
from datetime import datetime
from sql_tools import SQLBase


class TXIOTest(unittest.TestCase):

    def __init__(self):

        # Initialize connection to SQL database
        sql_server = 'MD2E4BFC\DT_SQLEXPRESS'
        sql_driver = "SQL Server Native Client 11.0"
        database_name = 'JobDB'
        sql_base = SQLBase(sql_server, sql_driver)
        sql_base.init_database_connection(database_name)

        # Other globals
        path_mdf = r"C:\Users\z003vrzk\.spyder-py3\Scripts\Work\panel_builder\SQLTest\301295_HCA_Clear_Lake_Chiller_Upfit\JobDB.mdf"
        controller_name = 'TEMPLATE_PXC';
        point_type = 'LAI'
        sensor_type = 'CURRENT'
        virtual = 0
        point_type_tuple = ('LDI','LPACI')

        return None


    def test_sql_points_single_type(self):
        return None
    def test_(self):
        return None
    def test_(self):
        return None
    def test_(self):
        return None
    def test_(self):
        return None
    def test_(self):
        return None
    def test_(self):
        return None
    def test_(self):
        return None
    def test_(self):
        return None
    def test_(self):
        return None
    def test_(self):
        return None
    def test_(self):
        return None

"""Counter Stuff"""
def count_test():
    global pathMDF, panelName, count, pointbas, pointfun, pointsen, netdev, pointDict
    pathMDF = 'C:\SQLTest\JobDB.mdf'
    panelName = 'JHW.PXCM01'
    count = Counter(pathMDF)
    pointbas = count.POINTBAS
    pointfun = count.POINTSEN
    pointsen = count.POINTSEN
    pointDict = count.pointDict
    netdev = count.NETDEV
    uniquePanels = count.uniquePanels
    count.count_all_io(panelName, 4)
    count.add_TXIO(panelName)
    count.report(panelName, 4)
    ##count.jvsql.detach()

"""NEW STUFF"""
def device_test():
    global devices
    device = AddDevice(count.engine, count.cursor)
    devices = device.DEVICES
    device.add_device(count.TXIODict, panelName)




def count_all_io(self, panelName, configuration):
    """Convenience wrapper. Calls count_LDO, count_LDI, count_LAO, count_LAI
    and generates a report.
    Special Note: Must call Count.report() to initialize printing functinoality
    Parameters
    --------------
    panelName : User specified panelName. Counts only IO for that panel
    configuration : TXIO configuration for Analog points. see Counter.count_LAnalog::
    """
    self.count_LDO(panelName)
    self.count_LDI(panelName)
    self.count_LAnalog(panelName, configuration)

    print('Number of standard DO = ', self.pointDict['totalLDO'])
    print('Number of L2SL DO points = ', self.pointDict['totalL2SL'])
    print('total number of LDO points : ', self.pointDict['DO_SUM'])
    print('total number of LDO points with 5% added = ', self.pointDict['extraDO'])
    print('total number of TXM1.6R-M required = ', self.pointDict['TXM1_6RM'], '\n')

    print('Total LDI : ', self.pointDict['totalLDI'])
    print('Number of L2SL DI points = ', self.pointDict['totalL2SL'])
    print('Number of LPACI DI points = ', self.pointDict['totalLPACI'])
    print('Total LDI w/ 5% added = ', self.pointDict['extraDI'])
    print('total number of TXM1.16D required = ', self.pointDict['TXM1_16D'], '\n')

    print('Total LAI : ', self.pointDict['AI_SUM'])
    print('Total Current : ', self.pointDict['totalCurrent_AI'])
    print('Total Standard : ', self.pointDict['totalStandard_AI'])
    print('Total Current w/ 5% : ', self.pointDict['extraCurrent_AI'])
    print('Total Standard w/ 5% : ', self.pointDict['extraStandard_AI'], '\n')

    print('Total LAO : ', self.pointDict['AO_SUM'])
    print('Total Current : ', self.pointDict['totalCurrent_AO'])
    print('Total Standard : ', self.pointDict['totalStandard_AO'])
    print('Total Current w/ 5% : ', self.pointDict['extraCurrent_AO'])
    print('Total Standard w/ 5% : ', self.pointDict['extraStandard_AO'],'\n')

    print('Number of TXM1.8X-ML w/ 5% : ', self.pointDict['TXM1_8XML'])
    print('Number of TXM1.8U-ML w/ 5% = ', self.pointDict['TXM1_8UML'])
    print('Number of TXM1.8X w/ 5% = ', self.pointDict['TXM1_8X'])
    print('Number of TXM1.8U w/ 5%= ', self.pointDict['TXM1_8U'])

    print('Empty DI : ', self.pointDict['emptyDI'])
    print('Empty DO : ', self.pointDict['emptyDI'])
    print('Empty XML : ', self.pointDict['emptyXML'])
    print('Empty X : ', self.pointDict['emptyX'])
    print('Empty UML : ', self.pointDict['emptyUML'])
    print('Empty U : ', self.pointDict['emptyU'])
