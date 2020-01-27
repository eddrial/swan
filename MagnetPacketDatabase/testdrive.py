'''
Created on 24 Jan 2020

@author: oqb
'''

from MagPacketDb import PacketDatabase as pd
import numpy as np

if __name__ == '__main__':
    #create class
    measdb = pd(r'M:\Work\Measurements\UE56SESA')
    
    #read measurement list
    measurementlist = measdb.read_MFMSW2(r'M:\Work\Measurements\UE56SESA')
    
    #read files into measurement database
    measdb.read_text_files_to_database()
    
    for key in measdb.datadict:
        print(measdb.datadict[key]['packettype'])
    
    #pickle new db
    measdb.pickle_data()
    
    #unpickle and load data    
    measdb.unpickle_data()
    
    for key in measdb.datadict:
        print(key)
        
    #append to pickled data. 
#    measdb.pickle_data_append()
        
    print('blah blah')
    
    #ptypedict = {}
    
    measdb.measIDtoPacketType()
    
    measdb.refinedata()
    
    print(1)
    

        
    #from large dictionary make dict of types
    #for key find type
    #if type is new, create dict entry
    #else append key to type entry
    
    
        
    #TODOs - 
    #refine_data
    #plot diff data types
    #save plots
    #parse different types of packet from database