#!/usr/bin/python
import sys
import os,csv
InspvaArray=[]
with open("/home/user1/Data/kvh_clean.csv", 'w') as outfile:
    with open("/home/user1/Data/kvh_INSPVAA.csv", 'rb') as infile:
        content = infile.readlines()
        for row in content:
            #if ('\0' not in row) and (('BESTGNSSPOSA'in row) or ('INSPVAA'in row)): # remove unparsed bytes found when in SBAS mode.
            if (('BESTGNSSPOSA'in row) or ('INSPVAA'in row)): # remove unparsed bytes found when in SBAS mode.
                if ('\0' not in row):
                    InspvaArray.append(row.split(','))
                    print row.split(',')
                else:
                    row=row.split('#')[-1].split(',') 
                    row[0]='#'+row[0]
                    InspvaArray.append(row) 
                    print row
        #for item in InspvaArray:
            #print item
            
            



'''


                    if ('#INSPVAA'==row[0]): 
                        outfile.write(byte)



        try:
            byte = infile.read(1)
            while byte != '':
                if ord(byte) >= 128:
                    pass
                else:
                    outfile.write(byte)
                byte = infile.read(1)
        finally:
            infile.close()
'''
