# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 15:46:18 2020

@author: z003vrzk
"""

import re

#%%

def read_vars_to_dict(file_path):
    """Outputs a dictionary structure after iterating through all lines in an
    input text/ini file. The output dict represents a key:value mapping of 
    the .ini file.
    This assumes the .ini file stores key:value pairs in the following format →
    key=value
    inptus
    -------
    file_path : (str) .txt file of 'system profile' report from commissiong tool
    outputs
    -------
    vars_dict : (dict) {key:value} read from variable file
    """

    reg_var = re.compile('=')
    
    # result = regex.match(string)
    vars_dict = {}
    
    with open(file_path, 'r') as f:
        for line in f:
            
            # Each regex pattern search result returns a regex match object
            result = reg_var.search(line)
            
            # Each regex match object has useful attributes and methods
            # re.match.end() : (int) position of end of string matched by match object
            if result:
                field_pos = result.end()
                key_name = line[:field_pos-1]
                
                value = line[field_pos:-1] # Return string
                value_clean = value.strip() # Clean string
                vars_dict[key_name] = value_clean # Add to dictionary struct
                
    return vars_dict


#%%
    
if __name__ == '__main__':
    file_path = r"D:\Jobs\44OP-268394-401_Congress_Reed_Smith_18th_Floor_Ste_1800\Design Tool\MDT\j_vars.ini"
    vars_dict = read_vars_to_dict(file_path)
