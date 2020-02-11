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
    #append magnet number to measurement data
    measdb.magname_to_measname(measurementlist)
    
    #magdb from measdb
    measdb.measIDtomagID()
    
    measdb.measIDtoPacketType()
    
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
    
    measdb.pickle_data()
    
    #swap meas key to mag key
    #create database of keys based on largest meas number
    #plot groups
    
    print(1)
    

        
        
    #TODOs - 
    #plot diff data types
    #save plots
    #parse different types of packet from database