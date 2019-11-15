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
            f = open('M:\Work\Measurements\UE56SESA\\'+datfile[0:-4]+'.log', "r")
            d = np.loadtxt(directoryname + '\\' +datfile)
            resultdict[datfile[0:-4]] = {'logfile' : f.read(), 'data' : d}
            f.close()
            
    return resultdict


#second function. Plot null measurements

def plotnulldata(datadictionary):
    
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
    
    for meas in datadictionary:
        axs[0].plot(datadictionary[meas]['data'][:,0],datadictionary[meas]['data'][:,1])
        axs[1].plot(datadictionary[meas]['data'][:,0],datadictionary[meas]['data'][:,2])
        
        #print(x, by, bz)
    #loop: create line and add to plot
    
    plt.show()
    
    return fig
    #save it as pdf
    
    

#main program

if __name__ == '__main__':
    nulldata = read_data('M:\Work\Measurements\UE56SESA','nu')
    refdata = read_data('M:\Work\Measurements\UE56SESA','r')
    
    n1 = plotnulldata(nulldata)
    n1.savefig('M:\Work\Measurements\UE56SESA\plot.pdf')
    

    #print(nulldata)

#read data
#plot nulls



#fig.savefig('plot.pdf')