'''
Created on 24 Jan 2020

@author: oqb
'''

from MagPacketDb import PacketDatabase as pd
import numpy as np

if __name__ == '__main__':
    measdb = pd(r'M:\Work\Measurements\UE56SESA')
    
    measurementlist = measdb.read_MFMSW2(r'M:\Work\Measurements\UE56SESA')
    
    #measdb.read_text_files_to_database()
    
    
    
    for key in measdb.datadict:
        print(measdb.datadict[key]['packettype'])
    
    #measdb.pickle_data()
    
    measdb.unpickle_data()
    
    for key in measdb.datadict:
        print(key)
        
    measdb.pickle_data_append()
        
    print('blah blah')
    
    for key in measdb.measdict:
        print(key)
        
    #TODOs - 
    #refine_data
    #plot diff data types
    #save plots
    #parse different types of packet from database