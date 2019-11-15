#module to read in data and log files of stretched wire bench
#results taken from SW2 etc

import os
import numpy as np
import matplotlib.pyplot as plt

#set plot styles
#plt.rc('font', family='serif', serif='Times')
#plt.rc('text', usetex=True)
plt.rc('xtick', labelsize=8)
plt.rc('ytick', labelsize=8)
plt.rc('axes', labelsize=8)

#first function. Read data.
def read_data(directoryname, blocktype):
    print ('reading '+blocktype+' data from ' + directoryname)
    
    resultdict = {}
    #for file in directory
    #make a dict of measurements. Dict has meas number, logfile, data
    for datfile in os.listdir(directoryname):
        if datfile.startswith(blocktype) and datfile.endswith('.dat'):
            f = open(directoryname+'\\'+datfile[0:-4]+'.log', "r")
            d = np.loadtxt(directoryname + '\\' +datfile)
            resultdict[datfile[0:-4]] = {'logfile' : f.read(), 'data' : d}
            f.close()
            
            
    return resultdict

def mean_data(datadictionary):
    d = len(datadictionary)
    bw = next(iter(datadictionary.values()))['data'].shape
    
    darray = np.zeros((bw[0],bw[1],d))
    i = 0
    for meas in datadictionary:
        darray[:,:,i] = datadictionary[meas]['data']
        i = i + 1
    
    meandarray = darray.mean(axis = 2)
    
    return meandarray

def maxmin_data(datadictionary):
    i = 0
    MaxMinYZ = np.zeros((4,len(datadictionary)))
    
    for meas in datadictionary:
        MaxMinYZ[0,i] = max(datadictionary[meas]['data'][:,1])
        MaxMinYZ[1,i] = min(datadictionary[meas]['data'][:,1])
        MaxMinYZ[2,i] = max(datadictionary[meas]['data'][:,2])
        MaxMinYZ[3,i] = min(datadictionary[meas]['data'][:,2])
        i = i+1
        
    return MaxMinYZ

#second function. Plot null measurements

def plotnulldata(datadictionary):
    #TODO Plot Mean Data
    #Calculate Mean Data
    #meanvals = np.zeros((datadictionary[],len(datadictionary)))
    
    meandarray = mean_data(datadictionary)
    
    #set up plot
    # set width and height
    width = 7
    height = 3
    
    #create the figure with nice margins
    fig, axs = plt.subplots(1,2, sharex = True, sharey = False)
    fig.subplots_adjust(left=.15, bottom=.16, right=.85, top=.85)
    fig.set_size_inches(width, height)
    fig.suptitle('Background Field Integral Measurements for UE56SESAME Block Measurements')
    
    plt.subplots_adjust(top= 0.8, wspace = 0.4)
    
    axs[0].set_ylim([-0.01, 0.01])
    

    axs[0].set_title('Vertical Field Integrals')
    axs[0].set_xlabel('z(mm)')
    axs[0].set_ylabel('IBydx(Tmm)')
    axs[0].set_yticks(np.arange(-.01,.01,.002))
    axs[0].set_yticks(np.arange(-.01,.01,.0005), minor=True)
    axs[0].grid(which = 'major')
    
    axs[1].set_ylim([-0.01, 0.01])
    axs[1].set_title('Horizontal Field Integrals')
    axs[1].set_xlabel('z(mm)')
    axs[1].set_ylabel('IBzdx(Tmm)')
    axs[1].grid(which = 'major')

    #loop: create line and add to plot
    for meas in datadictionary:
        axs[0].plot(datadictionary[meas]['data'][:,0],datadictionary[meas]['data'][:,1], linewidth = 0.75)
        axs[1].plot(datadictionary[meas]['data'][:,0],datadictionary[meas]['data'][:,2], linewidth = 0.75)

        #print(x, by, bz)

    
    #plot the mean values
    axs[0].plot(meandarray[:,0],meandarray[:,1],'r-')
    axs[1].plot(meandarray[:,0],meandarray[:,2],'r-')
    
    
    plt.show()
    
    return fig
    #save it as pdf
    
def plotrefdata(datadictionary):
    #mean of collecte data
    meandarray = mean_data(datadictionary)
    
    #max of collected data
    MaxMinYZ = maxmin_data(datadictionary)
    
    #set up plot
    # set width and height
    width = 7
    height = 9
    
    #create the figure with nice margins
    fig, axs = plt.subplots(3,2, sharex = False, sharey = False)
    fig.subplots_adjust(left=.15, bottom=.16, right=.85, top=.85)
    fig.set_size_inches(width, height)
    fig.suptitle('RefBlock Field Integral Measurements for UE56SESAME Block Measurements')
    
    plt.subplots_adjust(top= 0.9, wspace = 1, hspace = 0.6)
    
    #Direct Field Integrals
    
    axs[0,0].set_ylim([-5, 5])
    axs[0,0].set_title('Vertical Field Integrals')
    axs[0,0].set_xlabel('z(mm)')
    axs[0,0].set_ylabel('IBydx(Tmm)')
    axs[0,0].set_yticks(np.arange(-4,6,2))
    axs[0,0].set_yticks(np.arange(-5,5,.5), minor=True)
    axs[0,0].grid(which = 'major')
    
    axs[0,1].set_ylim([-5, 5])
    axs[0,1].set_title('Horizontal Field Integrals')
    axs[0,1].set_xlabel('z(mm)')
    axs[0,1].set_ylabel('IBzdx(Tmm)')
    axs[0,1].grid(which = 'major')
    
    for meas in datadictionary:
        axs[0,0].plot(datadictionary[meas]['data'][:,0],datadictionary[meas]['data'][:,1])
        axs[0,1].plot(datadictionary[meas]['data'][:,0],datadictionary[meas]['data'][:,2])
    
    axs[0,0].plot(meandarray[:,0],meandarray[:,1],'r-')
    axs[0,1].plot(meandarray[:,0],meandarray[:,2],'r-')
    
        #Difference Field Integrals: signal - mean
    
    axs[1,0].set_ylim([-.01, .01])
    axs[1,0].set_title('Vertical Field Integrals Variation')
    axs[1,0].set_xlabel('z(mm)')
    axs[1,0].set_ylabel('IBydx(Tmm)')
#    axs[1,0].set_yticks(np.arange(-.01,.01,.002))
#    axs[1,0].set_yticks(np.arange(-.01,.01,.0005), minor=True)
    axs[1,0].grid(which = 'major')
    
    axs[1,1].set_ylim([-.01, .01])
    axs[1,1].set_title('Horizontal Field Integrals Variation')
    axs[1,1].set_xlabel('z(mm)')
    axs[1,1].set_ylabel('IBzdx(Tmm)')
    axs[1,1].grid(which = 'major')
    
    for meas in datadictionary:
        axs[1,0].plot(datadictionary[meas]['data'][:,0],meandarray[:,1]-datadictionary[meas]['data'][:,1])
        axs[1,1].plot(datadictionary[meas]['data'][:,0],meandarray[:,2]-datadictionary[meas]['data'][:,2])
    
    #plot max/min of each curve

    
#    axs[2,0].set_ylim([-.01, .01])
    axs[2,0].set_title('Max/Min Vertical Field\n Integral Variation')
    axs[2,0].set_xlabel('Block#')
    axs[2,0].set_ylabel('Max IBydx(Tmm)', color = 'r')
    axs20twin = axs[2,0].twinx()
    axs20twin.set_ylabel('Min IBydx(Tmm)', color = 'b')
    
#    axs[1,0].set_yticks(np.arange(-.01,.01,.002))
#    axs[1,0].set_yticks(np.arange(-.01,.01,.0005), minor=True)
    axs[2,0].grid(which = 'major')
    
#    axs[2,1].set_ylim([-.01, .01])
    axs[2,1].set_title('Max/Min Horizontal Field\n Integrals Variation')
    axs[2,1].set_xlabel('Block #')
    axs[2,1].set_ylabel('Max IBzdx(Tmm)', color = 'r')
    axs[2,1].grid(which = 'major')
    axs21twin = axs[2,1].twinx()
    axs21twin.set_ylabel('Min IBzdx(Tmm)', color = 'b')
    
    axs[2,0].plot(np.arange(len(MaxMinYZ[0,:])),MaxMinYZ[0,:], 'r-')
    axs20twin.plot(np.arange(len(MaxMinYZ[0,:])),MaxMinYZ[1,:],'b-')
    axs[2,1].plot(np.arange(len(MaxMinYZ[0,:])),MaxMinYZ[2,:],'r-')
    axs21twin.plot(np.arange(len(MaxMinYZ[0,:])),MaxMinYZ[3,:], 'b-')
    
    plt.show()
    
    return fig
    

#main program

if __name__ == '__main__':
    nulldata = read_data('M:\Work\Measurements\UE56SESA','nu')
    refdata = read_data('M:\Work\Measurements\UE56SESA','r')
    
    #n1 = plotnulldata(nulldata)
    #n1.savefig('M:\Work\Measurements\UE56SESA\nullplot.pdf')
    
    r1 = plotrefdata(refdata)
    r1.savefig('M:\Work\Measurements\UE56SESA\\refplot.pdf')
    

    #print(nulldata)

#read data
#plot nulls



#fig.savefig('plot.pdf')