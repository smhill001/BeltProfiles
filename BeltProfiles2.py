# -*- coding: utf-8 -*-
"""
Created on Tue Aug 26 13:38:06 2014

@author: steven.hill

BeltProfiles2.py

"""

drive='f:'
import sys
sys.path.append('f:\\Astronomy\Python Play')
sys.path.append('f:\\Astronomy\Python Play\BeltProfileProcessingLibraries')

import matplotlib.pyplot as pl
import pylab
import numpy as np
import scipy as sp
import BeltProfileProcessor as BPP

###############################################################################
#Initialize inputs and plot parameters

#Target="Saturn"
Target="Jupiter"

#AppYear="2014"
AppYear="2015"
#AppYear="2016"
x0,x1,xtks=0.,1.,11

if Target=="Saturn":
    datapath=drive+"//Astronomy/Projects/Planets/"+Target+"/Imaging Data/"
    Bands=["NUV","BLU","GRN","RED","HAL","NIR","CH4"]
    Colors=np.array([[0.4,0.2,0.6],[0.1,0.1,0.7],[0.1,0.6,0.1],
                     [0.6,0.5,0.2],[0.7,0.3,0.1],[0.6,0.1,0.0],[0.0,0.0,0.0]])
    Offsets=np.array([0.0,0.0,0.0,0,0,0,0.0])        
    #Offsets=np.array([0.4,0.4,0.3,0,0,0,0.4])        
    Smoothing=np.array([13,11,11,9,11,7,15])
    y0,y1,ytks=-90,90,19
elif Target=="Jupiter" and AppYear=="2015":
    datapath=drive+"//Astronomy/Projects/Planets/"+Target+"/Imaging Data/Mapping/"
    Bands=["NUV","BLU","GRN","RED","685","CH4"]
    Colors=np.array([[0.4,0.2,0.6],[0.1,0.1,0.7],[0.1,0.6,0.1],
                     [0.6,0.5,0.2],[0.6,0.1,0.0],[0.0,0.0,0.0]])
    Offsets=np.array([0.0,0.0,0.0,0,0,0,0.0])        
    Smoothing=np.array([5,5,5,5,5,5])  
    y0,y1,ytks=-90,90,19
elif Target=="Jupiter" and AppYear=="2016":
    datapath=drive+"//Astronomy/Projects/Planets/"+Target+"/Imaging Data/Mapping/"
    Bands=["NUV","BLU","GRN","RED","685","807","889"]
    Colors=np.array([[0.4,0.2,0.6],[0.1,0.1,0.7],[0.1,0.6,0.1],
                     [0.6,0.5,0.2],[0.6,0.1,0.0],[0.6,0.1,0.0],[0.0,0.0,0.0]])
    Offsets=np.array([0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3])        
    Smoothing=np.array([5,5,5,5,5,5,5])
    y0,y1,ytks=-90,90,19

fig=pl.figure(figsize=(6.5, 3.5), dpi=150,facecolor="white")
ax1=fig.add_subplot(1, 3, 1,axisbg="white")
pl.xlim(0.0,1.0)
pl.xticks(np.linspace(0.0,1.0,xtks, endpoint=True))
pl.ylim(y0,y1)
pl.yticks(np.linspace(y0,y1,ytks, endpoint=True))
pl.grid()
pl.tick_params(axis='both', which='major', labelsize=6)
pl.ylabel("Latitude (deg)",fontsize=7)
pl.xlabel("Relative Brightness",fontsize=7)
pl.setp(ax1.get_xticklabels(),visible=False)
#pl.title(Target+AppYear+" Belt Profile",fontsize=9)

ax3=fig.add_subplot(1, 3, 3,axisbg="white",sharey=ax1)
pl.xlim(x0,x1)
pl.xticks(np.linspace(x0,x1,xtks, endpoint=True))
pl.ylim(y0,y1)
#pl.yticks(np.linspace(y0,y1,ytks, endpoint=True))
pl.grid()
pl.tick_params(axis='x', which='major', labelsize=6)
#pl.ylabel("Latitude (deg)",fontsize=7)
pl.xlabel("Belt/Zone Classification",fontsize=7)
pl.setp(ax3.get_yticklabels(),visible=False)
pl.setp(ax3.get_xticklabels(),visible=False)
#pl.title(Target+AppYear+" Belt Profile",fontsize=9)

###############################################################################
#fun test

testimage=np.zeros((1,180))

for i in range(0,len(Bands)):
    if Target=="Jupiter" and AppYear=="2016":
        fn=datapath+"Profile of 2016-04-03-0651.8_2016-05-04-0334.3-Hill-RGB_MAP-"+Bands[i]+"-BARE.txt"
    if Target=="Jupiter" and AppYear=="2015":
        fn=datapath+"Profile of 2015-03-1X-XXXX.X-Hill-"+Target+"-"+Bands[i]+"-bare.txt"
    if Target=="Saturn":
        fn=datapath+"Profile of 2014-Hill-"+Target+"-"+Bands[i]+"-Master-bare.txt"
    print "Band=",Bands[i]
    #Compute differences for band and zone identification
    Belts,Zones,lat,profile,dlat,dprofile,ddlat,ddprofile,latbelts,belts = \
        BPP.BeltProfileProcessor(fn,[0,180],Smoothing[i])
    #Plot profiles and belt/zone identification
    ax1.plot(profile+Offsets[i],lat,'-',color=Colors[i,:],label=Bands[i],zorder=1)
    ax3.plot(belts*0.9+(0.9-0.12*i),latbelts,'-',color=Colors[i,:],zorder=1)
    #print lat,profile
    #print dlat,dprofile
    #print ddlat,ddprofile
    #Write belts and zones as ASCII files
    Belts=np.array(Belts)
    Zones=np.array(Zones)
    for j in range(0,Belts.size/3):
        #print "j=",j,Belts.size/3
        if j==0 and i==0:
            tempfile=open(datapath+Target+AppYear+"Belts.txt","w")
            tempfile.write("Band,North,South,Center\n")    
            tempfile.write(str(Bands[i])+","+str(Belts[j,0])+","+str(Belts[j,1])+","+str(Belts[j,2])+"\n")
        else:
            tempfile=open(datapath+Target+AppYear+"Belts.txt","a")
            tempfile.write(str(Bands[i])+","+str(Belts[j,0])+","+str(Belts[j,1])+","+str(Belts[j,2])+"\n")
        tempfile.close()
    for j in range(0,Zones.size/3):
        if j==0 and i==0:
            tempfile=open(datapath+Target+AppYear+"Zones.txt","w")
            tempfile.write("Band,North,South,Center\n")    
            tempfile.write(str(Bands[i])+","+str(Zones[j,0])+","+str(Zones[j,1])+","+str(Zones[j,2])+"\n")
        else:
            tempfile=open(datapath+Target+AppYear+"Zones.txt","a")
            tempfile.write(str(Bands[i])+","+str(Zones[j,0])+","+str(Zones[j,1])+","+str(Zones[j,2])+"\n")
        tempfile.close()
            
    testimage[0,:]=profile[:]
    temp=np.array(profile)    
    for k in range(1,31):    
        print testimage.shape,temp.shape
        testimage=np.append(testimage,[temp],0)
        
    testimage1=sp.misc.imresize(testimage,[118,180])

ax1.legend(loc=3,ncol=4, borderaxespad=0.,prop={'size':4})

#fig2=pl.figure(figsize=(6.5, 4.5), dpi=150,facecolor="white")
ax2=fig.add_subplot(1, 3, 2,axisbg="white")
#im=pl.imshow(np.transpose(testimage1[:,19:160]),cmap='gray')
im=pl.imshow(np.fliplr(np.transpose(testimage1)),cmap='gray')
pl.tick_params(axis='both', which='major', labelsize=6)
#pl.ylabel("Latitude (deg)",fontsize=7)
pl.xlabel("Longitudinal Brightness Average",fontsize=7)
pl.suptitle(Target+" "+AppYear+" Belt Profile",fontsize=9)
pl.setp(ax2.get_yticklabels(),visible=False)
pl.setp(ax2.get_xticklabels(),visible=False)

itemp=len(Bands)-1
spacing=118/float(len(Bands))
#Bands.reverse()
for B in Bands:
    print B
    ax2.annotate(B, xy=(0,0),xytext=(0.5*spacing+itemp*spacing, 175),
                 horizontalalignment='center',fontsize=6,color=Colors[len(Bands)-itemp-1])
    itemp=itemp-1
#Overplotting test, does not work right as of 8/16/2016
#im=ax3.imshow(np.transpose(testimage1),zorder=0,cmap='gray',origin='upper',extent=[-50,50,90,-90])


pl.subplots_adjust(left=0.08, right=0.97, top=0.93, bottom=0.10, wspace=0.001)

pylab.savefig(datapath+Target+AppYear+"BeltProfile.png",dpi=300)
