#module to read in data and log files of stretched wire bench
#results taken from SW2 etc

import os
import numpy as np
from win32file import ReadFile

#first function. Read data.
def read_data(directoryname, blocktype):
    print ('reading data from ' + directoryname)
    
    resultdict = {}
    #for file in directory
    for file in os.listdir(directoryname):
        if file.startswith(blocktype) and file.endswith('.dat'):
            f = open('M:\Work\Measurements\UE56SESA\\'+file[0:-4]+'.log', "r")
            d = np.loadtxt(directoryname + '\\' +file)
            resultdict[file[0:-4]] = {'logfile' : f.read(), 'data' : d}
            f.close()
    #make list of .dat files
    #make list of .log files
    #read in for list
    
    #make a dict of measurements. Dict has meas number, logfile, datetime and data
    
    #E.g. x axis nulldata['nu571']['data'][:,0]
    
    return resultdict
#second function. Plot null measurements

#main program

if __name__ == '__main__':
    nulldata = read_data('M:\Work\Measurements\UE56SESA','nu')
    
    f = open("M:\Work\Measurements\UE56SESA\\nu571.log", "r")
    a = f.read()
    f.close()
    
    print(a.__sizeof__())
    print(nulldata)

#read data
#plot nulls