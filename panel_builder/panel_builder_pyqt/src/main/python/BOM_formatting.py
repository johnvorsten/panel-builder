# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 15:15:52 2020

@author: z003vrzk
"""

# Python imports
from collections import namedtuple

# Third party imports
import numpy as np

# Local imports
from read_j_vars import read_vars_to_dict

# Instantiate classes
cell = namedtuple('cell',['row','col','data', 'format'])

#%% Class definitions


class BOMFormat():

    def __init__(self, initialization_file_path):
        """
        inputs
        -------
        initialization_file_path : (str) or path to j_vars.ini file that stores
        design tool job related information"""

        self.initialization_dict = read_vars_to_dict(initialization_file_path)

        return None


    def _generate_doc_header_std(self, head_start_row=0):
        """Generate a list of 'cell' objects which contain (row, col, data, format)
        information for writing into a workbook.  Standard formatting
        inptus
        -------
        head_start_row : (int) row to start writing header at
        outputs
        -------
        head_cells : (list) of cell named tuple objects for writing data"""

        head_cells = []
        # Formatting dictionaries
        standard = {'font_name':'Arial'}
        bold = {'bold':True,
                'font_name':'Arial'}
        underline_bold = {'bold':True,
                          'font_name':'Arial',
                          'bottom':1}

        # Retrieve information from job variables file .ini
        job_name = self.initialization_dict['j_name']
        job_number = self.initialization_dict['j_number']
        project_manager = self.initialization_dict['j_brncon']
        project_engineer = self.initialization_dict['j_engr']

        # Formatting for document header
        _cell = cell(head_start_row+0, 0, 'Project Name', bold)
        head_cells.append(_cell)
        _cell = cell(head_start_row+0, 1, job_name, standard)
        head_cells.append(_cell)

        _cell = cell(head_start_row+1, 0, 'Project #', bold)
        head_cells.append(_cell)
        _cell = cell(head_start_row+1, 1, job_number, standard)
        head_cells.append(_cell)

        _cell = cell(head_start_row+2, 0, 'Project Manager', bold)
        head_cells.append(_cell)
        _cell = cell(head_start_row+2, 1, project_manager, standard)
        head_cells.append(_cell)

        _cell = cell(head_start_row+3, 0, 'Eng.', bold)
        head_cells.append(_cell)
        _cell = cell(head_start_row+3, 1, project_engineer, standard)
        head_cells.append(_cell)

        # Total project cost
        _cell = cell(head_start_row+1, 8, 'Total Material Cost', bold)
        head_cells.append(_cell)
        _cell = cell(head_start_row+2, 8, '=SUM(J:J)', bold)
        head_cells.append(_cell)

        # Individual BOM headers
        _cell = cell(head_start_row+5, 0, 'Ordered', underline_bold)
        head_cells.append(_cell)
        _cell = cell(head_start_row+5, 1, 'BOM Name', underline_bold)
        head_cells.append(_cell)
        _cell = cell(head_start_row+5, 2, 'Qty', underline_bold)
        head_cells.append(_cell)
        _cell = cell(head_start_row+5, 3, 'Component', underline_bold)
        head_cells.append(_cell)
        _cell = cell(head_start_row+5, 4, 'Part Number', underline_bold)
        head_cells.append(_cell)
        _cell = cell(head_start_row+5, 5, 'Vendor', underline_bold)
        head_cells.append(_cell)
        _cell = cell(head_start_row+5, 6, 'Vendor Number', underline_bold)
        head_cells.append(_cell)
        _cell = cell(head_start_row+5, 7, 'Description', underline_bold)
        head_cells.append(_cell)
        _cell = cell(head_start_row+5, 8, 'Est Price (ea)', underline_bold)
        head_cells.append(_cell)
        _cell = cell(head_start_row+5, 9, 'Line Price', underline_bold)
        head_cells.append(_cell)
        _cell = cell(head_start_row+5, 10, 'Notes', underline_bold)
        head_cells.append(_cell)
        _cell = cell(head_start_row+5, 11, 'Tracking', underline_bold)
        head_cells.append(_cell)

        return head_cells

    def _generate_node_header_std(self, system_name, node_start_row=0):
        """Generate a list of 'cell' objects which contain (row, col, data, format)
        information for writing into a workbook.  OG Larson format
        inptus
        -------
        system_name : (str) name of BOM node
        node_start_row : (int) row to start writing node header at
        outputs
        -------
        node_cells : (list) of cell named tuple objects for writing data"""

        # Spreadsheet cells
        node_cells = []

        # Formatting dictionaries
        standard = {'font_name':'Arial'}
        italic = {'italic':True}

        # Cells
        _cell = cell(node_start_row+1, 1, system_name, standard)
        node_cells.append(_cell)
        _cell = cell(node_start_row, 7, 'Node Cost : ', italic)
        node_cells.append(_cell)

        return node_cells


    def _generate_doc_header_larson(self, head_start_row=0):
        """Generate a list of 'cell' objects which contain (row, col, data, format)
        information for writing into a workbook. OG Larson format
        inptus
        -------
        head_start_row : (int) row to start writing header at
        outputs
        -------
        head_cells : (list) of cell named tuple objects for writing data"""

        head_cells = []

        # Formatting for document header
        _cell = cell(head_start_row+1, 4, 'Jobsite Address', {'bold':True,
                                                              'italic':None,
                                                              'font_name':'Arial',
                                                              'bg_color':False})
        head_cells.append(_cell)
        _cell = cell(head_start_row+2, 4, (self.initialization_dict['j_add1'] +
                                           self.initialization_dict['j_add2'] +
                                           self.initialization_dict['j_city'] +
                                           self.initialization_dict['j_zip']),
                                            {'top':1,'bg_color':'#c5d9f1'})
        head_cells.append(_cell)

        _cell = cell(head_start_row+2, 2, self.initialization_dict['j_name'],
                                                     {'bold':None,
                                                      'italic':True,
                                                      'font_name':'Arial',
                                                      'bg_color':'#c5d9f1',
                                                      'top':2,'bottom':2,'left':2})
        head_cells.append(_cell)

        _cell = cell(head_start_row+2, 3, self.initialization_dict['j_number'],
                     {'bold':None,
                      'italic':True,
                      'font_name':'Arial',
                      'bg_color':'#c5d9f1',
                      'top':2,'bottom':2,'right':2})
        head_cells.append(_cell)

        _cell = cell(head_start_row+4, 4, 'Total Material Cost:  ', {'bold':None,'italic':True,'font_name':'Arial','bg_color':False})
        head_cells.append(_cell)

        _cell = cell(head_start_row+4, 6, 'Text', {'border':2})
        head_cells.append(_cell)

        return head_cells


    def _generate_node_header_larson(self, system_name, node_start_row=0):
        """Generate a list of 'cell' objects which contain (row, col, data, format)
        information for writing into a workbook.  OG Larson format
        inptus
        -------
        system_name : (str) name of BOM node
        node_start_row : (int) row to start writing node header at
        outputs
        -------
        node_cells : (list) of cell named tuple objects for writing data"""

        node_cells = []
        # Formatting for each row
        _cell = cell(node_start_row, 2, 'BOM Node:', {'bold':True,'italic':None,
                                                      'font_name':'Arial',
                                                      'bg_color':False, 'top':2,
                                                      'left':1,'bottom':1})
        node_cells.append(_cell)

        _cell = cell(node_start_row, 3, str(system_name), {'bold':True,'italic':None,
                                                    'font_name':'Arial',
                                                    'bg_color':'#c5d9f1',
                                                    'bottom':1,'right':1,'top':2})
        node_cells.append(_cell)

        _cell = cell(node_start_row, 5, 'BOM Cost:  ', {'bold':None,'italic':True,
                                                        'font_name':'Arial',
                                                        'bg_color':False,'top':2})
        node_cells.append(_cell)

        _cell = cell(node_start_row, 6, 'Text', {'top':2,'bottom':1,
                                                   'left':1,'right':1})
        node_cells.append(_cell)

        _cell = cell(node_start_row+1, 2, 'Order Date:', {'bold':None,'italic':True,
                                                          'font_name':'Arial',
                                                          'bg_color':False})
        node_cells.append(_cell)

        _cell = cell(node_start_row+1, 3, 'xx/xx/xxxx', {'bold':None,'italic':True,
                                                         'font_name':'Arial',
                                                         'bg_color':'#c5d9f1'})
        node_cells.append(_cell)

        _cell = cell(node_start_row+1, 4, 'Ship to: ', {'bold':None,'italic':True,
                                                        'font_name':'Arial',
                                                        'bg_color':'#c5d9f1'})
        node_cells.append(_cell)

        _cell = cell(node_start_row+2, 1, 'QTY', {'bold':True,'italic':None,
                                                  'font_name':'Arial',
                                                  'bg_color':False,'left':2,'bottom':1})
        node_cells.append(_cell)

        _cell = cell(node_start_row+2, 2, 'Part #', {'bold':True,'italic':None,
                                                     'font_name':'Arial',
                                                     'bg_color':False,'bottom':1})
        node_cells.append(_cell)

        _cell = cell(node_start_row+2, 3, 'Vendor', {'bold':True,'italic':None,
                                                     'font_name':'Arial',
                                                     'bg_color':False,'bottom':1})
        node_cells.append(_cell)

        _cell = cell(node_start_row+2, 4, 'Description', {'bold':True,'italic':None,
                                                          'font_name':'Arial',
                                                          'bg_color':False,'bottom':1})
        node_cells.append(_cell)

        _cell = cell(node_start_row+2, 5, 'Est Price (ea)', {'bold':True,'italic':None,
                                                             'font_name':'Arial',
                                                             'bg_color':False,'bottom':1})
        node_cells.append(_cell)

        _cell = cell(node_start_row+2, 6, 'Line price', {'bold':True,'italic':None,
                                                         'font_name':'Arial',
                                                         'bg_color':False,'bottom':1})
        node_cells.append(_cell)

        _cell = cell(node_start_row+2, 7, 'Ordered', {'bold':True,'italic':None,
                                                      'font_name':'Arial',
                                                      'bg_color':False,'bottom':1})
        node_cells.append(_cell)

        _cell = cell(node_start_row+2, 8, 'Comments', {'bold':True,'italic':None,
                                                       'font_name':'Arial',
                                                       'bg_color':False,'bottom':1,
                                                       'right':2})
        node_cells.append(_cell)

        # Add borders...
        _cell = cell(node_start_row, 1, '', {'left':2,'top':2})
        node_cells.append(_cell)
        _cell = cell(node_start_row, 4, None, {'top':2})
        node_cells.append(_cell)
        _cell = cell(node_start_row, 5, '', {'top':2})
        node_cells.append(_cell)
        _cell = cell(node_start_row, 7, '', {'top':2})
        node_cells.append(_cell)
        _cell = cell(node_start_row, 8, '', {'top':2,'right':2})
        node_cells.append(_cell)
        _cell = cell(node_start_row+1, 1, '', {'left':2})
        node_cells.append(_cell)
        _cell = cell(node_start_row+1, 8, '', {'right':2})
        node_cells.append(_cell)

        return node_cells