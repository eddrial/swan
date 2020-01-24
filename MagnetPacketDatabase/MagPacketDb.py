'''
Created on 24 Jan 2020

@author: oqb
'''

import os
import numpy as np
import h5py
import datetime as dt
import pickle

class PacketDatabase(object):
    '''
    classdocs
    '''


    def __init__(self, FolderPath):
        '''
        Constructor
        '''
        self.directoryname = FolderPath
        self.measlistname = 'MFM_SW2.LST'
        self.databasename = FolderPath[-8:]+'_Measurement_Database'
        self.measdbasefile = 'meas_data.pkl'
        
        self.measdict = {}
        self.datadict = {}
        
    def read_MFMSW2(self, directoryname):
        print ('Loading Measurement History' + self.measlistname)
        
        if os.path.exists(directoryname + '\\' + self.measlistname)==False:
            print ('file ' + directoryname + '\\MFM_SW2.LST does not exist. \nAborting Load ')
            pass
        else:
        
            f = open(directoryname+'\\' + self.measlistname, "r")
            
            d = f.readlines()
            for line in d:
                thisline = line.split()
                self.measdict[thisline[1][:-4]] = {'magname': thisline[0], 'datestamp': thisline[2], 'timestamp': thisline[3]}
            
            f.close()
            
            return self.measdict
        
    def read_text_files_to_database(self):
        for key in self.measdict:
            d = np.loadtxt(self.directoryname + '\\' +key + '.dat')
            f = open(self.directoryname+'\\'+ key +'.log', "r")
            lfile = f.readlines()
            tstamp = dt.datetime(int(lfile[0][-5:-1]),int(lfile[0][-8:-6]),int(lfile[0][-11:-9]),int(lfile[1][-9:-7]),int(lfile[1][-6:-4]),int(lfile[1][-3:-1]))
            self.datadict[key] = {'logfile' : lfile, 'data' : d, 'timestamp' : tstamp, 'packettype' : key[0:2]}
            
        return
        
    def pickle_data(self):
        with open(self.directoryname + '\\meas_data.pkl', 'wb') as output:
    # Pickle dictionary using protocol 0.
            pickle.dump(self.datadict, output)
        