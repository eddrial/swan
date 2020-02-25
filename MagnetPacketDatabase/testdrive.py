'''
Created on 24 Jan 2020

@author: oqb
'''

from MagPacketDb import PacketDatabase as pd
import numpy as np
import matplotlib.pyplot as plt

def plotsetmeandata(datadictionary):
    #plot titles etc
    
    
    #maxlimit and minlimit lines for variation plots
    maxlimit = np.array([[-50,0.1],[50,0.1]])
    minlimit = np.array([[-50,-0.1],[50,-0.1]])
            
    
    #set up plot
    # set width and height
    width = 7
    height = 9
    
    #create the figure with nice margins
    fig, axs = plt.subplots(4,2, sharex = False, sharey = False)
    fig.subplots_adjust(left=.15, bottom=.06, right=.85, top= 0.9, wspace = 0.7, hspace = 0.8)
    fig.set_size_inches(width, height)
    
    #Sheet Title
    fig.suptitle('Field Integral Measurements for UE56SESAME Block Types')
    #ROW 0
    #axis limits
    
    axs[0,0].set_xlim([-42.5,42.5])
    axs[0,0].set_ylim([-5, 5])
    axs[0,0].set_title('Mean Vertical \n Field Integrals')
    axs[0,0].set_xlabel('z(mm)')
    axs[0,0].set_ylabel('IBydx(Tmm)')
    axs[0,0].set_xticks(np.arange(-40,60,20))
    axs[0,0].set_yticks(np.arange(-4,6,2))
    axs[0,0].set_yticks(np.arange(-5,5,.5), minor=True)
    axs[0,0].grid(which = 'major')
    
    axs[0,1].set_xlim([-40,40])
    axs[0,1].set_ylim([-5, 5])
    axs[0,1].set_title('Mean Horizontal \n Field Integrals')
    axs[0,1].set_xlabel('z(mm)')
    axs[0,1].set_ylabel('IBzdx(Tmm)')
    axs[0,1].set_xticks(np.arange(-40,60,20))
    axs[0,1].set_yticks(np.arange(-4,6,2))
    axs[0,1].set_yticks(np.arange(-5,5,.5), minor=True)
    axs[0,1].grid(which = 'major')
    
    #data
    for blocktype in datadictionary.ptypedictmean:
        if blocktype[0].isdigit():
            axs[0,0].plot(datadictionary.ptypedictmean[blocktype][:,0],datadictionary.ptypedictmean[blocktype][:,1])
            axs[0,1].plot(datadictionary.ptypedictmean[blocktype][:,0],datadictionary.ptypedictmean[blocktype][:,2])

    #ROW 1
    #axis limits
    axs[1,0].set_xlim([-42.5,42.5])
    axs[1,0].set_ylim([-0.1, 0.1])
    axs[1,0].set_title('N + N+2 \n Vertical Field')
    axs[1,0].set_xlabel('z(mm)')
    axs[1,0].set_ylabel('IBydx(Tmm)')
    axs[1,0].set_xticks(np.arange(-40,60,20))
    axs[1,0].set_yticks(np.arange(-0.1,0.12,0.05))
    axs[1,0].set_yticks(np.arange(-0.1,0.12,.01), minor=True)
    axs[1,0].grid(which = 'major')
    
    axs[1,1].set_xlim([-40,40])
    axs[1,1].set_ylim([-0.1, 0.1])
    axs[1,1].set_title('N + N+2 \n Horizontal Field')
    axs[1,1].set_xlabel('z(mm)')
    axs[1,1].set_ylabel('IBzdx(Tmm)')
    axs[1,1].set_xticks(np.arange(-40,60,20))
    axs[1,1].set_yticks(np.arange(-0.1,0.12,0.05))
    axs[1,1].set_yticks(np.arange(-0.1,0.12,.01), minor=True)
    axs[1,1].grid(which = 'major')
    
    #data
    #VFields
    axs[1,0].plot((datadictionary.ptypedictmean['01mean'][:,0]),datadictionary.ptypedictmean['01mean'][:,1]+datadictionary.ptypedictmean['03mean'][:,1])
    axs[1,0].plot(datadictionary.ptypedictmean['01mean'][:,0],datadictionary.ptypedictmean['02mean'][:,1]+datadictionary.ptypedictmean['04mean'][:,1])
    axs[1,0].plot(datadictionary.ptypedictmean['01mean'][:,0],datadictionary.ptypedictmean['05mean'][:,1]+datadictionary.ptypedictmean['07mean'][:,1])
    axs[1,0].plot(datadictionary.ptypedictmean['01mean'][:,0],datadictionary.ptypedictmean['06mean'][:,1]+datadictionary.ptypedictmean['08mean'][:,1])
    axs[1,0].plot(datadictionary.ptypedictmean['01mean'][:,0],datadictionary.ptypedictmean['09mean'][:,1]+datadictionary.ptypedictmean['11mean'][:,1])
    axs[1,0].plot(datadictionary.ptypedictmean['01mean'][:,0],datadictionary.ptypedictmean['10mean'][:,1]+datadictionary.ptypedictmean['12mean'][:,1])
    axs[1,0].plot(datadictionary.ptypedictmean['01mean'][:,0],datadictionary.ptypedictmean['13mean'][:,1]+datadictionary.ptypedictmean['15mean'][:,1])
    axs[1,0].plot(datadictionary.ptypedictmean['01mean'][:,0],datadictionary.ptypedictmean['14mean'][:,1]+datadictionary.ptypedictmean['16mean'][:,1])
    #HFields
    axs[1,1].plot(datadictionary.ptypedictmean['01mean'][:,0],datadictionary.ptypedictmean['01mean'][:,2]+datadictionary.ptypedictmean['03mean'][:,2])
    axs[1,1].plot(datadictionary.ptypedictmean['01mean'][:,0],datadictionary.ptypedictmean['02mean'][:,2]+datadictionary.ptypedictmean['04mean'][:,2])
    axs[1,1].plot(datadictionary.ptypedictmean['01mean'][:,0],datadictionary.ptypedictmean['05mean'][:,2]+datadictionary.ptypedictmean['07mean'][:,2])
    axs[1,1].plot(datadictionary.ptypedictmean['01mean'][:,0],datadictionary.ptypedictmean['06mean'][:,2]+datadictionary.ptypedictmean['08mean'][:,2])
    axs[1,1].plot(datadictionary.ptypedictmean['01mean'][:,0],datadictionary.ptypedictmean['09mean'][:,2]+datadictionary.ptypedictmean['11mean'][:,2])
    axs[1,1].plot(datadictionary.ptypedictmean['01mean'][:,0],datadictionary.ptypedictmean['10mean'][:,2]+datadictionary.ptypedictmean['12mean'][:,2])
    axs[1,1].plot(datadictionary.ptypedictmean['01mean'][:,0],datadictionary.ptypedictmean['13mean'][:,2]+datadictionary.ptypedictmean['15mean'][:,2])
    axs[1,1].plot(datadictionary.ptypedictmean['01mean'][:,0],datadictionary.ptypedictmean['14mean'][:,2]+datadictionary.ptypedictmean['16mean'][:,2])
    
    #ROW 2
    #axis limits
    axs[2,0].set_xlim([-42.5,42.5])
    axs[2,0].set_ylim([-0.1, 0.1])
    axs[2,0].set_title('N + N+4 \n Vertical Field')
    axs[2,0].set_xlabel('z(mm)')
    axs[2,0].set_ylabel('IBydx(Tmm)')
    axs[2,0].set_xticks(np.arange(-40,60,20))
    axs[2,0].set_yticks(np.arange(-0.1,0.12,0.05))
    axs[2,0].set_yticks(np.arange(-0.1,0.12,.01), minor=True)
    axs[2,0].grid(which = 'major')
    
    axs[2,1].set_xlim([-40,40])
    axs[2,1].set_ylim([-0.1, 0.1])
    axs[2,1].set_title('N + N+4 \n Horizontal Field')
    axs[2,1].set_xlabel('z(mm)')
    axs[2,1].set_ylabel('IBzdx(Tmm)')
    axs[2,1].set_xticks(np.arange(-40,60,20))
    axs[2,1].set_yticks(np.arange(-0.1,0.12,0.05))
    axs[2,1].set_yticks(np.arange(-0.1,0.12,.01), minor=True)
    axs[2,1].grid(which = 'major')
    
    #data
    #VFields
    axs[2,0].plot(datadictionary.ptypedictmean['01mean'][:,0],datadictionary.ptypedictmean['01mean'][:,1]+datadictionary.ptypedictmean['05mean'][:,1])
    axs[2,0].plot(datadictionary.ptypedictmean['01mean'][:,0],datadictionary.ptypedictmean['02mean'][:,1]+datadictionary.ptypedictmean['06mean'][:,1])
    axs[2,0].plot(datadictionary.ptypedictmean['01mean'][:,0],datadictionary.ptypedictmean['03mean'][:,1]+datadictionary.ptypedictmean['07mean'][:,1])
    axs[2,0].plot(datadictionary.ptypedictmean['01mean'][:,0],datadictionary.ptypedictmean['04mean'][:,1]+datadictionary.ptypedictmean['08mean'][:,1])
    axs[2,0].plot(datadictionary.ptypedictmean['01mean'][:,0],datadictionary.ptypedictmean['09mean'][:,1]+datadictionary.ptypedictmean['13mean'][:,1])
    axs[2,0].plot(datadictionary.ptypedictmean['01mean'][:,0],datadictionary.ptypedictmean['10mean'][:,1]+datadictionary.ptypedictmean['14mean'][:,1])
    axs[2,0].plot(datadictionary.ptypedictmean['01mean'][:,0],datadictionary.ptypedictmean['11mean'][:,1]+datadictionary.ptypedictmean['15mean'][:,1])
    axs[2,0].plot(datadictionary.ptypedictmean['01mean'][:,0],datadictionary.ptypedictmean['12mean'][:,1]+datadictionary.ptypedictmean['16mean'][:,1])
    #HFields
    axs[2,1].plot(datadictionary.ptypedictmean['01mean'][:,0],datadictionary.ptypedictmean['01mean'][:,2]+datadictionary.ptypedictmean['05mean'][:,2])
    axs[2,1].plot(datadictionary.ptypedictmean['01mean'][:,0],datadictionary.ptypedictmean['02mean'][:,2]+datadictionary.ptypedictmean['06mean'][:,2])
    axs[2,1].plot(datadictionary.ptypedictmean['01mean'][:,0],datadictionary.ptypedictmean['03mean'][:,2]+datadictionary.ptypedictmean['07mean'][:,2])
    axs[2,1].plot(datadictionary.ptypedictmean['01mean'][:,0],datadictionary.ptypedictmean['04mean'][:,2]+datadictionary.ptypedictmean['08mean'][:,2])
    axs[2,1].plot(datadictionary.ptypedictmean['01mean'][:,0],datadictionary.ptypedictmean['09mean'][:,2]+datadictionary.ptypedictmean['13mean'][:,2])
    axs[2,1].plot(datadictionary.ptypedictmean['01mean'][:,0],datadictionary.ptypedictmean['10mean'][:,2]+datadictionary.ptypedictmean['14mean'][:,2])
    axs[2,1].plot(datadictionary.ptypedictmean['01mean'][:,0],datadictionary.ptypedictmean['11mean'][:,2]+datadictionary.ptypedictmean['15mean'][:,2])
    axs[2,1].plot(datadictionary.ptypedictmean['01mean'][:,0],datadictionary.ptypedictmean['12mean'][:,2]+datadictionary.ptypedictmean['16mean'][:,2])
    
#ROW 3
    #axis limits
    axs[3,0].set_xlim([-42.5,42.5])
    axs[3,0].set_ylim([-0.2, 0.2])
    axs[3,0].set_title('BU + GO, BO + GU\n Total')
    axs[3,0].set_xlabel('z(mm)')
    axs[3,0].set_ylabel('IBydx(Tmm)')
    axs[3,0].set_xticks(np.arange(-40,60,20))
    axs[3,0].set_yticks(np.arange(-0.2,0.22,0.1))
    axs[3,0].set_yticks(np.arange(-0.2,0.22,.02), minor=True)
    axs[3,0].grid(which = 'major')
    
    axs[3,1].set_xlim([-40,40])
    axs[3,1].set_ylim([-0.2, 0.2])
    axs[3,1].set_title('BU + GO, BO + GU\n Total')
    axs[3,1].set_xlabel('z(mm)')
    axs[3,1].set_ylabel('IBzdx(Tmm)')
    axs[3,1].set_xticks(np.arange(-40,60,20))
    axs[3,1].set_yticks(np.arange(-0.2,0.22,0.1))
    axs[3,1].set_yticks(np.arange(-0.2,0.22,.02), minor=True)
    axs[3,1].grid(which = 'major')
    
    #data
    #AllFields
    bu = np.zeros(datadictionary.ptypedictmean['01mean'].shape)
    go = np.zeros(datadictionary.ptypedictmean['01mean'].shape)
    bo = np.zeros(datadictionary.ptypedictmean['01mean'].shape)
    gu = np.zeros(datadictionary.ptypedictmean['01mean'].shape)
    bu[:,0] = datadictionary.ptypedictmean['01mean'][:,0]
    go[:,0] = datadictionary.ptypedictmean['01mean'][:,0]
    bo[:,0] = datadictionary.ptypedictmean['01mean'][:,0]
    gu[:,0] = datadictionary.ptypedictmean['01mean'][:,0]
    
    bu[:,1:] = 4*(datadictionary.ptypedictmean['01mean'][:,1:]+datadictionary.ptypedictmean['02mean'][:,1:]+
                                                                 datadictionary.ptypedictmean['03mean'][:,1:]+datadictionary.ptypedictmean['04mean'][:,1:]+
                                                                 datadictionary.ptypedictmean['05mean'][:,1:]+datadictionary.ptypedictmean['06mean'][:,1:]+
                                                                 datadictionary.ptypedictmean['07mean'][:,1:]+datadictionary.ptypedictmean['08mean'][:,1:])
    
    go[:,1:] = -4*(np.flip(datadictionary.ptypedictmean['01mean'][:,1:],0)+np.flip(datadictionary.ptypedictmean['02mean'][:,1:],0)+
                                                                 np.flip(datadictionary.ptypedictmean['03mean'][:,1:],0)+np.flip(datadictionary.ptypedictmean['04mean'][:,1:],0)+
                                                                 np.flip(datadictionary.ptypedictmean['05mean'][:,1:],0)+np.flip(datadictionary.ptypedictmean['06mean'][:,1:],0)+
                                                                 np.flip(datadictionary.ptypedictmean['07mean'][:,1:],0)+np.flip(datadictionary.ptypedictmean['08mean'][:,1:],0))
    
    bo[:,1] = -4*(datadictionary.ptypedictmean['09mean'][:,1]+datadictionary.ptypedictmean['10mean'][:,1]+
                                                                 datadictionary.ptypedictmean['11mean'][:,1]+datadictionary.ptypedictmean['12mean'][:,1]+
                                                                 datadictionary.ptypedictmean['13mean'][:,1]+datadictionary.ptypedictmean['14mean'][:,1]+
                                                                 datadictionary.ptypedictmean['15mean'][:,1]+datadictionary.ptypedictmean['16mean'][:,1])
    bo[:,2] = 4*(datadictionary.ptypedictmean['09mean'][:,2]+datadictionary.ptypedictmean['10mean'][:,2]+
                                                                 datadictionary.ptypedictmean['11mean'][:,2]+datadictionary.ptypedictmean['12mean'][:,2]+
                                                                 datadictionary.ptypedictmean['13mean'][:,2]+datadictionary.ptypedictmean['14mean'][:,2]+
                                                                 datadictionary.ptypedictmean['15mean'][:,2]+datadictionary.ptypedictmean['16mean'][:,2])
    
    gu[:,1] = 4*(np.flip(datadictionary.ptypedictmean['09mean'][:,1])+np.flip(datadictionary.ptypedictmean['10mean'][:,1])+
                                                                 np.flip(datadictionary.ptypedictmean['11mean'][:,1])+np.flip(datadictionary.ptypedictmean['12mean'][:,1])+
                                                                 np.flip(datadictionary.ptypedictmean['13mean'][:,1])+np.flip(datadictionary.ptypedictmean['14mean'][:,1])+
                                                                 np.flip(datadictionary.ptypedictmean['15mean'][:,1])+np.flip(datadictionary.ptypedictmean['16mean'][:,1]))
    
    gu[:,2] = -4*(np.flip(datadictionary.ptypedictmean['09mean'][:,2])+np.flip(datadictionary.ptypedictmean['10mean'][:,2])+
                                                                 np.flip(datadictionary.ptypedictmean['11mean'][:,2])+np.flip(datadictionary.ptypedictmean['12mean'][:,2])+
                                                                 np.flip(datadictionary.ptypedictmean['13mean'][:,2])+np.flip(datadictionary.ptypedictmean['14mean'][:,2])+
                                                                 np.flip(datadictionary.ptypedictmean['15mean'][:,2])+np.flip(datadictionary.ptypedictmean['16mean'][:,2]))
    
    #VFields
    axs[3,0].plot(datadictionary.ptypedictmean['01mean'][:,0],bu[:,1]+go[:,1])
    axs[3,0].plot(datadictionary.ptypedictmean['01mean'][:,0],bo[:,1]+gu[:,1])
    axs[3,0].plot(datadictionary.ptypedictmean['01mean'][:,0],bu[:,1]+go[:,1]+bo[:,1]+gu[:,1])
    

    #HFields
    axs[3,1].plot(datadictionary.ptypedictmean['01mean'][:,0],bu[:,2]+go[:,2])
    axs[3,1].plot(datadictionary.ptypedictmean['01mean'][:,0],bo[:,2]+gu[:,2])
    axs[3,1].plot(datadictionary.ptypedictmean['01mean'][:,0],bu[:,2]+go[:,2]+bo[:,2]+gu[:,2])


    
    plt.show()
    
    return fig
    

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
    #measdb.pickle_data()
    
    #unpickle and load data    
    #measdb.unpickle_data()
        
    #append to pickled data. 
#    measdb.pickle_data_append()
        
    print('blah blah')
    
    #ptypedict = {}
    
    
    measdb.refinedata()
    
    #ptype dictionary sum data
    
    measdb.mean_sets()
    #measdb.pickle_data()
    
    #swap meas key to mag key
    #create database of keys based on largest meas number
    #plot groups
    
    #plotting

    final_summary = plotsetmeandata(measdb)
    
    final_summary.savefig(r'M:\Work\Measurements\UE56SESA\final_results\UE56SESAMESummary.pdf')
    
    print(1)
    

        
        
    #TODOs - 
    #plot diff data types
    #save plots
    #parse different types of packet from database