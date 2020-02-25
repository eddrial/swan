'''
Created on 24 Jan 2020

@author: oqb
'''

import os
import numpy as np
import datetime as dt
import pickle
#from visualanalysis import timeneighbours
from operator import itemgetter
import matplotlib.pyplot as plt

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
        
        self.measdict = {} #measurement dictionary - from MFM_SW2
        self.datadict = {} #data dictionary - from individual log files identified from measdict
        self.ptypedict = {} #shuffle keys to be packet type - precursor to extracting type databases?
        self.nulldict = {} #null = background measurement dictionaries
        self.refdict = {} # reference packet measurements
        self.magdict = {} #shuffle keys to be magnet name
        self.ptypedictmean = {} #Database of packet-type mean
        
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
    
    def magname_to_measname(self, measurement_list):
        for key in self.measdict:
            self.datadict[key]['magname'] = measurement_list[key]['magname']
            

    #store and load pickles of data. File I/O
    def pickle_data_append(self):
        for key in self.datadict:
            self.measdict.pop(key)
        self.read_text_files_to_database()
        
        
    def pickle_data(self):
        with open(self.directoryname + '\\' + self.measdbasefile, 'wb') as output:
    # Pickle dictionary using protocol 0.
            pickle.dump(self.datadict, output)
            
    def unpickle_data(self):
        with open(self.directoryname + '\\' + self.measdbasefile, 'rb') as fp:
            self.datadict = pickle.load(fp)
        
    
    #Database conversions
    def measIDtoPacketType(self):
        for key in self.datadict:
            ptype = self.datadict[key]['packettype']
            if ptype in self.ptypedict:
                if (ptype == 'nu' or ptype == 'r0' or ptype == 'te'):
                    self.ptypedict[ptype].append(key)
                else:
                    if (max(self.magdict[self.datadict[key]['magname']])) not in self.ptypedict[ptype]:
                        self.ptypedict[ptype].append(max(self.magdict[self.datadict[key]['magname']]))            
            else:
                if (ptype == 'nu' or ptype == 'r0' or ptype == 'te'):
                    self.ptypedict[ptype] = [key]
                else: 
                    self.ptypedict[ptype] = [max(self.magdict[self.datadict[key]['magname']])]
    
    def extractNullDict(self):
        for meas in self.ptypedict['nu']:
            self.nulldict[meas] = self.datadict[meas]
    
    def extractRefDict(self):
        for meas in self.ptypedict['r0']:
            self.refdict[meas] = self.datadict[meas]
    
    def measIDtomagID(self):
        for key in self.datadict:
            mname = self.datadict[key]['magname']
            if mname in self.magdict:
                self.magdict[mname].append(key)            
            else:
                self.magdict[mname] = [key]
    
    #Refine Data - extend datadict
    def refinedata(self):
        self.extractNullDict()
        self.extractRefDict()
        for key in self.ptypedict:
            if (key == 'nu' or key == 'r0' or key == 'te'):
                pass
            else:
                '''
                for key in dict
                for meas in list
                get timestamp of meas
                
                '''
                for meas in self.ptypedict[key]:
                    ts = self.datadict[meas]['timestamp']
                    
                    #find null before/after
                    nullkeys = self.timeneighbours(ts, self.nulldict)
                    
                    #find ref before/after
                    refkeys = self.timeneighbours(ts, self.refdict)
                    
                    #do background sub
                    bgsub = np.zeros(self.datadict[meas]['data'].shape)
                    bgsub[:,0] = self.datadict[meas]['data'][:,0]
                    bgsub[:,1:3] = self.datadict[meas]['data'][:,1:3] - (self.nulldict[nullkeys[0]]['data'][:,1:3]+self.nulldict[nullkeys[1]]['data'][:,1:3])/2.0
                    self.datadict[meas]['bgsub'] = bgsub
                    
                    #do refnormalisation
                    refnormal = np.zeros(self.datadict[meas]['data'].shape)
                    refnormal[:,0] = self.datadict[meas]['data'][:,0]
                    day0ref = self.calcday0ref()
                    refnormal[:,1:3] = np.divide(np.multiply(bgsub[:,1:3],day0ref[:,1:3]), (self.refdict[refkeys[0]]['data'][:,1:3]+self.refdict[refkeys[1]]['data'][:,1:3])/2.0)
                    self.datadict[meas]['refnormal'] = refnormal
                    
        
            #if ref do nout
            #if anythingelse
            
    def timeneighbours(self, timestmp, thedict):
    #this is ugly as sin
        dictlist = [(key,thedict[key]['timestamp']) for key in thedict.keys()]
        dictlist.sort(key = itemgetter(1))
        a = np.zeros(len(dictlist))
        
        for i in range(len(a)):
            a[i]= timestmp<dictlist[i][1]
        
        keys = [dictlist[np.argmax(a)-1][0],dictlist[np.argmax(a)][0]]
        
        return keys       
    
    def calcday0ref(self):
        copydict = self.refdict.copy()
        dictlist = [(key,copydict[key]['timestamp']) for key in copydict.keys()]
        dictlist.sort(key = itemgetter(1))
        
        a = np.zeros(len(dictlist))
        
        day0 = copydict[dictlist[0][0]]['timestamp'].date()
        
        for i in range(len(a)):
            a[i] = day0 < dictlist[i][1].date()
        
        for i in range(np.argmax(a)-2,len(a)):
            copydict.pop(dictlist[i][0])
        
        day0ref = self.mean_data(copydict, 'data')
        
        return day0ref
    
    def mean_data(self, datadictionary, datakey):
        d = len(datadictionary)
        bw = next(iter(datadictionary.values()))[datakey].shape
        
        darray = np.zeros((bw[0],bw[1],d))
        i = 0
        for meas in datadictionary:
            darray[:,:,i] = datadictionary[meas][datakey]
            i = i + 1
        
        meandarray = darray.mean(axis = 2)
    
        return meandarray
    
    def mean_sets(self):
        for typeset in self.ptypedict:
            meandata = None
            if typeset == 'te' or typeset == 'r0' or typeset == 'nu':
                pass
            else:
                
                for meas in self.ptypedict[typeset]:
                    if meandata is None:
                        meandata = self.datadict[meas]['refnormal']
                    else:
                        meandata[:,1:] += self.datadict[meas]['refnormal'][:,1:]
                meandata[:,1:] /= len(self.ptypedict[typeset])
                self.ptypedictmean[typeset + 'mean'] = meandata
                
                
            print(self.ptypedict[typeset])
            
            
