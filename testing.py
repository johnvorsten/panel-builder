# -*- coding: utf-8 -*-
"""
Created on Sun Jan 20 18:15:25 2019

@author: z003vrzk
"""

dictlabels = ['a','b','c']
dictvalues = [1,2,3]

mydict = {}
for index, item in enumerate(dictlabels):
    mydict[item] = dictvalues[index]
    
mydict = {'a':(False, 0), 'b':(False, 1), 'c':(False, 2)}

#filename = os.getcwd() + r"\PanelBuilderReadMe.pdf"
filename = os.path.join(r'C:\Users\z003vrzk\PycharmProjects\Work', 'PanelBuilderReadMe.pdf')
filename = r'C:\\Users\\z003vrzk\\PycharmProjects\\Work\\PanelBuilderReadMe.pdf'
print('filename : ', filename)
subprocess.run(['start', filename], shell=True)

mypath = os.path.join(os.getcwd(), r'\PanelBuilderReadMe.pdf')
print(mypath)