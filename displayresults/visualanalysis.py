#module to read in data and log files of stretched wire bench
#results taken from SW2 etc
#python 2.7
#Todo - Python 3

#TODO read in SW2 log to assign magnet numbers
#wrap as function with folder path as input
#bailout if SW2 log is not present
#spline fit & save


#ambition
#save to hdf5
#clean up graph settings

#comparison of two

import os
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
from operator import itemgetter

#set plot styles
#plt.rc('font', family='serif', serif='Times')
#plt.rc('text', usetex=True)
plt.rc('xtick', labelsize=8)
plt.rc('ytick', labelsize=8)
plt.rc('axes', labelsize=8)

#first function. Read data.
def read_data(directoryname, blocktype1, blocktype2 = 'defstring'):
    print ('reading '+blocktype1+' data from ' + directoryname)
    
    resultdict = {}
    #for file in directory
    #make a dict of measurements. Dict has meas number, logfile, data
    for datfile in os.listdir(directoryname):
        if (datfile.startswith(blocktype1) or datfile.startswith(blocktype2)) and datfile.endswith('.dat'):
            f = open(directoryname+'\\'+datfile[0:-4]+'.log', "r")
            d = np.loadtxt(directoryname + '\\' +datfile)
            lfile = f.readlines()
            tstamp = dt.datetime(int(lfile[0][-5:-1]),int(lfile[0][-8:-6]),int(lfile[0][-11:-9]),int(lfile[1][-9:-7]),int(lfile[1][-6:-4]),int(lfile[1][-3:-1]))
            resultdict[datfile[0:-4]] = {'logfile' : lfile, 'data' : d, 'timestamp' : tstamp}
            f.close()
            
            
    return resultdict

def read_MFMSW2(directoryname):
    print ('Loading Measurement History MFM_SW2.LST')
    
    measdict = {}
    f = open(directoryname+'\\MFM_SW2.LST', "r")
    d = f.readlines()
    for line in d:
        thisline = line.split()
        measdict[thisline[1][:-4]] = {'magname': thisline[0], 'datestamp': thisline[2], 'timestamp': thisline[3]}
    
    f.close()
    
    return measdict

def duplicated(thisdict):
    #find duplicated magnet names in list
    #but not for null, test, ref etc...
    duplicated_dict = {}
    
    for k, v in thisdict.items():
        duplicated_dict.setdefault(v['magname'],set()).add(k)
    
    print len(duplicated_dict)
    
    for k, v in duplicated_dict.items():
        if len(v) == 1: 
            duplicated_dict.pop(k)
            
    print len(duplicated_dict)
        
    for k, v in duplicated_dict.items():
        if k[0].isdigit() == False:
            duplicated_dict.pop(k)
            
    print len(duplicated_dict)
    
    return duplicated_dict
    

def mean_data(datadictionary, datakey):
    d = len(datadictionary)
    bw = next(iter(datadictionary.values()))[datakey].shape
    
    darray = np.zeros((bw[0],bw[1],d))
    i = 0
    for meas in datadictionary:
        darray[:,:,i] = datadictionary[meas][datakey]
        i = i + 1
    
    meandarray = darray.mean(axis = 2)
    
    return meandarray

def std_data(datadictionary, datakey):
    d = len(datadictionary)
    bw = next(iter(datadictionary.values()))[datakey].shape
    
    darray = np.zeros((bw[0],bw[1],d))
    i = 0
    for meas in datadictionary:
        darray[:,:,i] = datadictionary[meas][datakey]
        i = i + 1
    
    stdarray = darray.std(axis = 2)
    
    return stdarray


def maxmin_data(datadictionary, datakey):
    i = 0
    MaxMinYZ = np.zeros((4,len(datadictionary)))
    
    for meas in datadictionary:
        MaxMinYZ[0,i] = max(datadictionary[meas][datakey][:,1])
        MaxMinYZ[1,i] = min(datadictionary[meas][datakey][:,1])
        MaxMinYZ[2,i] = max(datadictionary[meas][datakey][:,2])
        MaxMinYZ[3,i] = min(datadictionary[meas][datakey][:,2])
        i = i+1
        
    return MaxMinYZ

#refine data

def backgroundsub(null,nullkeys):
    pass

def calcday0ref(dicto):
    copydict = dicto.copy()
    dictlist = [(key,copydict[key]['timestamp']) for key in copydict.keys()]
    dictlist.sort(key = itemgetter(1))
    
    a = np.zeros(len(dictlist))
    
    day0 = copydict[dictlist[0][0]]['timestamp'].date()
    
    for i in range(len(a)):
        a[i] = day0 < dictlist[i][1].date()
    
    for i in range(np.argmax(a)-2,len(a)):
        copydict.pop(dictlist[i][0])
    
    day0ref = mean_data(copydict, 'data')
    
    return day0ref
    
    
    

def refinedata(meas, null, ref):
    
    #for item in meas, get timestamp
    for key in meas:
        ts = meas[key]['timestamp']
        #find null before/after
        nullkeys = timeneighbours(ts, null)
        
        #find ref before/after
        refkeys = timeneighbours(ts, ref)
        
        #do background sub
        bgsub = np.zeros(meas[key]['data'].shape)
        bgsub[:,0] = meas[key]['data'][:,0]
        bgsub[:,1:3] = meas[key]['data'][:,1:3] - (null[nullkeys[0]]['data'][:,1:3]+null[nullkeys[1]]['data'][:,1:3])/2.0
        meas[key]['bgsub'] = bgsub
        
        #do refnormalisation
        refnormal = np.zeros(meas[key]['data'].shape)
        refnormal[:,0] = meas[key]['data'][:,0]
        day0ref = calcday0ref(ref)
        refnormal[:,1:3] = np.divide(np.multiply(bgsub[:,1:3],day0ref[:,1:3]), (ref[refkeys[0]]['data'][:,1:3]+ref[refkeys[1]]['data'][:,1:3])/2.0)
        
        
        meas[key]['refnormal'] = refnormal
    
    #meas[key]['refnormal'] = datarefnormalised
    
    
    return meas

def timeneighbours(timestmp, dict):
    #this is ugly as sin
    dictlist = [(key,dict[key]['timestamp']) for key in dict.keys()]
    dictlist.sort(key = itemgetter(1))
    a = np.zeros(len(dictlist))
    
    for i in range(len(a)):
        a[i]= timestmp<dictlist[i][1]
    
    keys = [dictlist[np.argmax(a)-1][0],dictlist[np.argmax(a)][0]]
    
    return keys

#second function. Plot null measurements

def plotnulldata(datadictionary, datakey):
    #TODO Plot Mean Data
    #Calculate Mean Data
    #meanvals = np.zeros((datadictionary[],len(datadictionary)))
    
    meandarray = mean_data(datadictionary, datakey)
    
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
    
def plotrefdata(datadictionary, datakey):
    #plot titles etc
    
    
    #maxlimit and minlimit lines for variation plots
    maxlimit = np.array([[-50,0.1],[50,0.1]])
    minlimit = np.array([[-50,-0.1],[50,-0.1]])
            
    
    #mean of collected data
    meandarray = mean_data(datadictionary, datakey )
    stdarray = std_data(datadictionary, datakey)
    
    #max of collected data
    MaxMinYZ = maxmin_data(datadictionary, datakey)
    
    #set up plot
    # set width and height
    width = 7
    height = 9
    
    #create the figure with nice margins
    fig, axs = plt.subplots(3,2, sharex = False, sharey = False)
    fig.subplots_adjust(left=.15, bottom=.16, right=.85, top= 0.9, wspace = 0.7, hspace = 0.6)
    fig.set_size_inches(width, height)
    
    if datadictionary == refdata:
        titlesubject = 'Reference Block'
        axs[1,0].set_ylim([-.0125, .0125])
        axs[1,1].set_ylim([-.0125, .0125])
        axs[2,0].set_ylim([0, .005])
        axs[2,1].set_ylim([0, .005])
        
    elif datadictionary == compare_dict:
        s = str()
        for key in datadictionary:
            if len(s) == 0:
                s+= key
            else:
                s+= ', '+key
        titlesubject = 'Out of Specification Measurements ' + s +'\n'
        axs[1,0].set_ylim([-.0125, .0125])
        axs[1,1].set_ylim([-.0125, .0125])
        axs[2,0].set_ylim([0, .005])
        axs[2,1].set_ylim([0, .005])
        
    elif datadictionary == tmp_dict:
        titlesubject = 'Type ' + datadictionary.keys()[0][0:2] + ' Series'
        axs[1,0].set_ylim([-.125, .125])
        axs[1,1].set_ylim([-.125, .125])
        axs[2,0].set_ylim([0, .05])
        axs[2,1].set_ylim([0, .05])
    
    fig.suptitle(titlesubject + ' Field Integral Measurements for UE56SESAME Blocks')    
    #Direct Field Integrals
    
    axs[0,0].set_xlim([-42.5,42.5])
    axs[0,0].set_ylim([-5, 5])
    axs[0,0].set_title('Vertical Field Integrals')
    axs[0,0].set_xlabel('z(mm)')
    axs[0,0].set_ylabel('IBydx(Tmm)')
    axs[0,0].set_yticks(np.arange(-4,6,2))
    axs[0,0].set_yticks(np.arange(-5,5,.5), minor=True)
    axs[0,0].grid(which = 'major')
    
    axs[0,1].set_xlim([-42.5,42.5])
    axs[0,1].set_ylim([-5, 5])
    axs[0,1].set_title('Horizontal Field Integrals')
    axs[0,1].set_xlabel('z(mm)')
    axs[0,1].set_ylabel('IBzdx(Tmm)')
    axs[0,1].grid(which = 'major')
    
    for meas in datadictionary:
        axs[0,0].plot(datadictionary[meas][datakey][:,0],datadictionary[meas][datakey][:,1])
        axs[0,1].plot(datadictionary[meas][datakey][:,0],datadictionary[meas][datakey][:,2])
    
    axs[0,0].plot(meandarray[:,0],meandarray[:,1],'r-')
    axs[0,1].plot(meandarray[:,0],meandarray[:,2],'r-')
    
    #Difference Field Integrals: signal - mean
    
    axs[1,0].set_xlim([-42.5,42.5])
    axs[1,0].set_title('Vertical Field Integrals\nVariation from Mean')
    axs[1,0].set_xlabel('z(mm)')
    axs[1,0].set_ylabel('IBydx(Tmm)')
#    axs[1,0].set_yticks(np.arange(-.01,.01,.002))
#    axs[1,0].set_yticks(np.arange(-.01,.01,.0005), minor=True)
    axs[1,0].grid(which = 'major')
    axs[1,0].plot(minlimit[:,0],minlimit[:,1],color='red', linewidth = 2, linestyle = 'dashed')
    axs[1,0].plot(maxlimit[:,0],maxlimit[:,1],color='red', linewidth = 2, linestyle = 'dashed')
    
    axs[1,1].set_xlim([-42.5,42.5])
    axs[1,1].set_title('Horizontal Field Integrals\nVariation from Mean')
    axs[1,1].set_xlabel('z(mm)')
    axs[1,1].set_ylabel('IBzdx(Tmm)')
    axs[1,1].grid(which = 'major')
    axs[1,1].plot(minlimit[:,0],minlimit[:,1],color='red', linewidth = 2, linestyle = 'dashed')
    axs[1,1].plot(maxlimit[:,0],maxlimit[:,1],color='red', linewidth = 2, linestyle = 'dashed')
    
    outofspec = []
    
    if datadictionary == compare_dict:
        for meas in datadictionary:
            axs[1,0].plot(datadictionary[meas][datakey][:,0],meandarray[:,1]-datadictionary[meas][datakey][:,1])
            axs[1,1].plot(datadictionary[meas][datakey][:,0],meandarray[:,2]-datadictionary[meas][datakey][:,2])
            
            #if abs 1 or 2 > 0.1 then 
            if max(abs(meandarray[:,1]-datadictionary[meas][datakey][:,1]))>0.1 or max(abs(meandarray[:,2]-datadictionary[meas][datakey][:,2]))>0.01:
                outofspec.append(meas)
        outofspecstr = ''
        for mag in outofspec:
            outofspecstr += mag + ', '
        
        #if compare dictionary
        #if comparisons are all ok, later measurement discarded
        #otherwise 'further analysis required
        
        fig.text(0.1,0.1,'Block ' + str(datadictionary[datadictionary.keys()[0]]['magname']) + ' has been measured ' + str(len(datadictionary)) + ' times')
    
        if len(outofspec) > 0:
            fig.text(0.1,0.08,'The Measurements of Block' + str(datadictionary[datadictionary.keys()[0]]['magname']) + ' Need Further Investigation')
        else:
            fig.text(0.1,0.08, 'Block ' + str(datadictionary[datadictionary.keys()[0]]['magname']) + ' Measurements Consistent')
    
    else:
        for meas in datadictionary:
            axs[1,0].plot(datadictionary[meas][datakey][:,0],meandarray[:,1]-datadictionary[meas][datakey][:,1])
            axs[1,1].plot(datadictionary[meas][datakey][:,0],meandarray[:,2]-datadictionary[meas][datakey][:,2])
            
            #if abs 1 or 2 > 0.1 then 
            if max(abs(meandarray[:,1]-datadictionary[meas][datakey][:,1]))>0.1 or max(abs(meandarray[:,2]-datadictionary[meas][datakey][:,2]))>0.1:
                outofspec.append(meas)
        outofspecstr = ''
        for mag in outofspec:
            outofspecstr += str(datadictionary[mag]['magname']) + ', '
        
        #if compare dictionary
        #if comparisons are all ok, later measurement discarded
        #otherwise 'further analysis required
        
        fig.text(0.1,0.1,'Set of '+str(len(datadictionary))+' Type '+datadictionary.keys()[0][0:2]+' Blocks have been measured')
    
        if len(outofspec) > 0:
            fig.text(0.1,0.08,'The Measurements of Blocks' + outofspecstr + ' Need Redoing')
        else:
            fig.text(0.1,0.08, 'All Block Measurements were Within Specification')
    
    #Standard Deviation of Field Integrals
    axs[2,0].set_title('Vertical Field Integrals\nStandard Deviation')
    axs[2,0].set_xlabel('z(mm)')
    axs[2,0].set_ylabel('IBydx(Tmm)')
#    axs[1,0].set_yticks(np.arange(-.01,.01,.002))
#    axs[1,0].set_yticks(np.arange(-.01,.01,.0005), minor=True)
    axs[2,0].grid(which = 'major')
    axs[2,0].text(-40,0.003,'Mean Value of\nStandard Deviation\n{:10.4f}'.format(stdarray[:,1].mean()))
    
    axs[2,1].set_title('Horizontal Field Integrals\nStandard Deviation')
    axs[2,1].set_xlabel('z(mm)')
    axs[2,1].set_ylabel('IBzdx(Tmm)')
    axs[2,1].grid(which = 'major')    
    axs[2,1].text(-40,0.003,'Mean Value of\nStandard Deviation\n{:10.4f}'.format(stdarray[:,2].mean()))
    
    axs[2,0].plot(datadictionary[meas][datakey][:,0],stdarray[:,1])
    axs[2,1].plot(datadictionary[meas][datakey][:,0],stdarray[:,2])
    
    
    #plot max/min of each curve

    #set up plot
    # set width and height
    width = 7
    height = 3
    
    #create the figure with nice margins
    fig2, axs2 = plt.subplots(1,2, sharex = True, sharey = False)
    fig2.subplots_adjust(left=.15, bottom=.16, right=.85, top= 0.6, wspace = 0.75, hspace = 0.6)
    fig2.set_size_inches(width, height)
    fig2.suptitle(titlesubject + ' Field Integral Measurements for UE56SESAME Blocks\nMax and Min of Series')

    

    axs2[0].set_title('Max/Min Vertical Field\n Integral Variation')
    axs2[0].set_xlabel('Block#')
    axs2[0].set_ylabel('Max IBydx(Tmm)', color = 'r')
    axs0twin = axs2[0].twinx()
    axs0twin.set_ylabel('Min IBydx(Tmm)', color = 'b')
    axs2[0].grid(which = 'major')
    
    axs2[1].set_title('Max/Min Horizontal Field\n Integrals Variation')
    axs2[1].set_xlabel('Block #')
    axs2[1].set_ylabel('Max IBzdx(Tmm)', color = 'r')
    axs2[1].grid(which = 'major')
    axs1twin = axs2[1].twinx()
    axs1twin.set_ylabel('Min IBzdx(Tmm)', color = 'b')
    
    axs2[0].plot(np.arange(len(MaxMinYZ[0,:])),MaxMinYZ[0,:], 'r-')
    axs0twin.plot(np.arange(len(MaxMinYZ[0,:])),MaxMinYZ[1,:],'b-')
    axs2[1].plot(np.arange(len(MaxMinYZ[0,:])),MaxMinYZ[2,:],'r-')
    axs1twin.plot(np.arange(len(MaxMinYZ[0,:])),MaxMinYZ[3,:], 'b-')
    
    plt.show()
    
    return fig,fig2
    

#main program

if __name__ == '__main__':
    measdatabase = read_MFMSW2(r'M:\Work\Measurements\UE56SESA')
    duplicates = duplicated(measdatabase)
    
    nulldata = {}
    refdata = {}
    measdata = {}
    compare_dict = {}
    
    
    
    nulldata = read_data(r'M:\Work\Measurements\UE56SESA','nu')
    refdata = read_data(r'M:\Work\Measurements\UE56SESA','r')
    measdata = read_data(r'M:\Work\Measurements\UE56SESA','0','1')
    
    for key in measdata:
        measdata[key]['magname'] = measdatabase[key]['magname']
    
    n1 = plotnulldata(nulldata, 'data')
    #n1.savefig('M:\Work\Measurements\UE56SESA\nullplot.pdf')
    
    r1a, r1b = plotrefdata(refdata, 'data')
    #r1a.savefig('M:\Work\Measurements\UE56SESA\\refblockplot1.pdf')
    #r1b.savefig('M:\Work\Measurements\UE56SESA\\refblockplot2.pdf')
    
    #null before and after measurements
    #pass in measdict, nulldict, refdict, return measdict enhanced with refnormalised and averagenull
    refined_data = refinedata(measdata, nulldata, refdata)
    
    #for each key of duplicates
    print(1)
    
    for key in duplicates:
        compare_dict = {}
        for val in duplicates[key]:
            compare_dict[val] = refined_data[val]
        
        a2a, a2b = plotrefdata(compare_dict, 'refnormal')
        
        fnameroot = 'block'+compare_dict[compare_dict.keys()[0]]['magname']+'compare'
        
        a2a.savefig(r'M:\Work\Measurements\UE56SESA\devfolder\\'+fnameroot +'stats.pdf')
        a2b.savefig(r'M:\Work\Measurements\UE56SESA\devfolder\\'+fnameroot +'peaksvariation.pdf')
            
    #for each item of value
    #make dictionary from refined_data
    #pop key
    #plotrefdata little dict
    
    #if data pass the filter - pop off extraneous (latest) keys
    
    #create part dict based on filter
    while len(refined_data) > 0:
        all_keys = refined_data.keys()
        tmpkeys = [all_keys[i] for i in range(len(all_keys)) if all_keys[i][0:2] == all_keys[0][0:2]]
        
        tmp_dict = {}
        tmp_dict = { your_key: refined_data[your_key] for your_key in tmpkeys }
        [refined_data.pop(mykey) for mykey in tmpkeys]
        
        #m1a, m1b = plotrefdata(tmp_dict, 'bgsub')
        m2a, m2b = plotrefdata(tmp_dict, 'refnormal')
        
        fnameroot = 'blockseries'+tmp_dict.keys()[0][:2]
        
        m2a.savefig(r'M:\Work\Measurements\UE56SESA\devfolder\\'+fnameroot +'stats.pdf')
        m2b.savefig(r'M:\Work\Measurements\UE56SESA\devfolder\\'+fnameroot +'peaksvariation.pdf')
        
        for mykey1 in tmpkeys:
            np.savetxt(r'M:\Work\Measurements\UE56SESA\devfolder\\'+mykey1 +'.da1', tmp_dict[mykey1]['bgsub'],fmt=('% 6.2f', '% 8.5f', '% 8.5f') )
            np.savetxt(r'M:\Work\Measurements\UE56SESA\devfolder\\'+mykey1 +'.da3', tmp_dict[mykey1]['refnormal'],fmt=('% 6.2f', '% 8.5f', '% 8.5f') )
        
        print (all_keys[i])
        
    
        

    
    #plotdata
    
    #list keys
    #read list
    #make dictionary
    #for meas in measdict append magnetnumber to measdict
    #create sublists for keys that begin with two numbers
    
    
    
    #save nulldata
    #save refdata



#fig.savefig('plot.pdf')