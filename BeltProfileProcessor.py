# -*- coding: utf-8 -*-
"""
Created on Wed Aug 27 12:12:55 2014

@author: steven.hill

BeltProfileProcessorJupiter1.py

INPUTS:
    filename=filename to read for the raw profile data. Data starts at the
            north and moves southward. Pixel numbers in first column
            are assumed to be equivalent to colatitudes. This assumes that the
            maps from which the profiles are generated are 360x180 pixels
    colatrange=array of two numbers indicating the starting colatitude and ending
            colatitude, e.g., the north pole is latitude zero and increases
            southward.
    N=smoothing box size
    
OUTPUTS:
    lat=latitude of the input 
    profilesmooth=smoothed brightness profile
    dlat=latitude of the first derivative of the brightness
    dprofilesmooth=first derivative of the brightness
    ddlat=latitude of the second derivative of the brightness
    ddprofile=second derivative of the brightness
    latbelts=belt/zone classification (belt=-1, zone=+1) as a fn of latitude
    belts=latitude of the belts classification (same as ddlat)
"""

def BeltProfileProcessor(filename,colatrange,N):
    import sys
    sys.path.append('g:\\Astronomy\Python Play')
    #import matplotlib.pyplot as pl
    import pylab as pl
    import numpy as np
    import scipy
    from copy import deepcopy
    from PyAstronomy import pyasl #This is where the best smoothing algorithm is!
    
    #Loadfile and reshape
    Temp= scipy.fromfile(file=filename, dtype=float, count=-1, sep=" ")
    Temp1=scipy.reshape(Temp,[Temp.size/4.,4])
    lat=90.-Temp1[colatrange[0]:colatrange[1],0]
    profile=Temp1[colatrange[0]:colatrange[1],1]
    
    latsmooth=lat
    profilesmooth=pyasl.smooth(profile,N,'flat')/255.

    dlat=latsmooth[1:]+0.5    
    dprofile=(profilesmooth[1:colatrange[1]]-profilesmooth[0:(colatrange[1]-1)])*10.+0.2
    dprofilesmooth=pyasl.smooth(dprofile,N,'flat')
    
    ddlat=dlat[1:]+0.5
    ddprofile=(dprofilesmooth[0:(colatrange[1]-2)]-dprofilesmooth[1:(colatrange[1]-1)])*10.
    
    belts=((ddprofile>=0.0).astype(float)-0.5)*0.1
    latbelts=ddlat

    dbeltslat=ddlat[1:]+0.5
    dbelts=(belts[0:(colatrange[1]-3)]-belts[1:(colatrange[1]-1)])*10.

    #From north to south
    ToBelt=dbeltslat[np.where(dbelts==1)]
    ToZone=dbeltslat[np.where(dbelts==-1)]

    Belts=np.zeros((1,3))    
    Zones=np.zeros((1,3))
    
    if ToBelt[0]>ToZone[0]:
        Zones[0,:]=[90.,ToBelt[0],np.mean([90.,ToBelt[0]])]
        Belts[0,:]=[ToBelt[0],ToZone[0],np.mean([ToBelt[0],ToZone[0]])]
        for i in range(0,np.min([len(ToZone),len(ToBelt)])-1):
            Zones=np.append(Zones,[[ToZone[i],ToBelt[i+1],np.mean([ToZone[i],ToBelt[i+1]])]],0)            
            Belts=np.append(Belts,[[ToBelt[i+1],ToZone[i+1],np.mean([ToZone[i+1],ToBelt[i+1]])]],0)            
    else:
        Belts[0,:]=[90.,ToZone[0],np.mean([90.,ToZone[0]])]
        Zones[0,:]=[ToZone[0],ToBelt[0],np.mean([ToBelt[0],ToZone[0]])]
        for i in range(0,np.min([len(ToZone),len(ToBelt)])-1):
            Zones=np.append(Zones,[[ToZone[i+1],ToBelt[i+1],np.mean([ToZone[i+1],ToBelt[i+1]])]],0)            
            Belts=np.append(Belts,[[ToBelt[i],ToZone[i+1],np.mean([ToZone[i],ToBelt[i+1]])]],0)            
        
        
    print "Belts=",Belts
    print "Zones=",Zones

    #print "To Belt",ToBelt
    #print "To Zone",ToZone
    #print ' '
    
    
    return Belts,Zones,lat,profilesmooth,dlat,dprofilesmooth,ddlat,ddprofile,latbelts,belts