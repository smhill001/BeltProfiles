# -*- coding: utf-8 -*-
"""
Updated on Wed Apr 05 09:41:47 2017
###############################################################################
NAME:       BeltProfiles2.py

PURPOSE:    To determine band transition latitudes on Jupiter and Saturn
            by using custom edge detection on longitudinally averaged maps
            
INPUTS:     Two parameters currently (4/5/17) hardcoded, "Target" and "AppYear"
            that are used to construct custom paths, map file names and 
             identify filtersapplicable to that apparition year.
            
LIBRARIES:  This code calls the BeltProfileProcessor.py, which represents the
            start of a library. 

###############################################################################
@author: steven.hill
"""

drive='f:'
import sys
sys.path.append('f:\\Astronomy\Python Play')
sys.path.append('f:\\Astronomy\Python Play\BeltProfiles')

import matplotlib.pyplot as pl
import pylab
import numpy as np
import scipy as sp
import BeltProfileProcessor as BPP
import BeltPlotLib as BPL

###############################################################################
#Initialize inputs and plot parameters


x0,x1,xtks=0.,1.,11
y0,y1,ytks=-90,90,19

Target="Jupiter"
AppYear="2014"

datapath=drive+"//Astronomy/Projects/Planets/"+Target+"/Imaging Data/Mapping/"
L=BPL.ListofProfiles("BeltDataFiles.txt")
L.load_select_data(Target,AppYear)

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

for i in range(0,len(L.Filter)):
    if Target=="Jupiter" and float(AppYear)<2013:
        fn=datapath+"Profile of "+AppYear+"-Composite-Hill-Jupiter-Bare-"+L.Filter[i]+".txt"
    if Target=="Jupiter" and AppYear=="2010":
        fn=datapath+"Profile of 2010-Hill-Jupiter-RGB-Composite-Map-Bare-"+L.Filter[i]+".txt"
    if Target=="Jupiter" and (AppYear=="2013" or AppYear=="2014"):
        fn=datapath+"Profile of "+AppYear+"-Hill-Jupiter-Composite-Bare-"+L.Filter[i]+".txt"
    if Target=="Jupiter" and AppYear=="2015":
        fn=datapath+"Profile of 2015-03-1X-XXXX.X-Hill-"+Target+"-"+L.Filter[i]+"-bare.txt"
    if Target=="Jupiter" and AppYear=="2016":
        fn=datapath+"Profile of 2016-04-03-0651.8_2016-05-04-0334.3-Hill-RGB_MAP-"+L.Filter[i]+"-BARE.txt"
    if Target=="Saturn" and AppYear=="2014":
        fn=datapath+"Profile of 2014-Hill-"+Target+"-"+L.Filter[i]+"-Master-bare.txt"
    if Target=="Saturn" and AppYear=="2015":
        fn=datapath+"Profile of 2015-Composite-Hill-Saturn-Bare-"+L.Filter[i]+".txt"
    print "Band=",L.Filter[i]
    print fn
    print AppYear
    #Compute differences for band and zone identification
    Belts,Zones,lat,profile,dlat,dprofile,ddlat,ddprofile,latbelts,belts = \
        BPP.BeltProfileProcessor(fn,[0,180],L.Smoothing[i])
    #Plot profiles and belt/zone identification
    ax1.plot(profile+L.Offset[i],lat,'-',color=BPL.FilterLineColor(L.Filter[i]),label=L.Filter[i]+"<"+str(L.Smoothing[i])+">",zorder=1)
    ax3.plot(belts*0.9+(0.9-0.12*i),latbelts,'-',color=BPL.FilterLineColor(L.Filter[i]),zorder=1)
    #print lat,profile
    #print dlat,dprofile
    #print ddlat,ddprofile
    #Write belts and zones as ASCII files
    Belts=np.array(Belts)
    Zones=np.array(Zones)
    for j in range(0,Belts.size/3):
        print "j=",j,Belts.size/3
        if j==0 and i==0:
            tempfile=open(datapath+Target+AppYear+"Belts.txt","w")
            tempfile.write("Band,North,South,Center\n")    
            tempfile.write(str(L.Filter[i])+","+str(Belts[j,0])+","+str(Belts[j,1])+","+str(Belts[j,2])+"\n")
        else:
            tempfile=open(datapath+Target+AppYear+"Belts.txt","a")
            tempfile.write(str(L.Filter[i])+","+str(Belts[j,0])+","+str(Belts[j,1])+","+str(Belts[j,2])+"\n")
        tempfile.close()
    for j in range(0,Zones.size/3):
        if j==0 and i==0:
            tempfile=open(datapath+Target+AppYear+"Zones.txt","w")
            tempfile.write("Band,North,South,Center\n")    
            tempfile.write(str(L.Filter[i])+","+str(Zones[j,0])+","+str(Zones[j,1])+","+str(Zones[j,2])+"\n")
        else:
            tempfile=open(datapath+Target+AppYear+"Zones.txt","a")
            tempfile.write(str(L.Filter[i])+","+str(Zones[j,0])+","+str(Zones[j,1])+","+str(Zones[j,2])+"\n")
        tempfile.close()
            
    testimage[0,:]=profile[:]
    temp=np.array(profile)    
    for k in range(1,31):    
        print testimage.shape,temp.shape
        testimage=np.append(testimage,[temp],0)
        
    testimage1=sp.misc.imresize(testimage,[118,180])

ax1.legend(loc=3,ncol=1, borderaxespad=0.,prop={'size':4})

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

itemp=len(L.Filter)-1
spacing=118/float(len(L.Filter))
#Bands.reverse()
for B in L.Filter:
    print B
    ax2.annotate(B[0:3], xy=(0,0),xytext=(0.5*spacing+itemp*spacing, 175),
                 horizontalalignment='center',fontsize=6,color=BPL.FilterLineColor(B))
    itemp=itemp-1

pl.subplots_adjust(left=0.08, right=0.97, top=0.93, bottom=0.10, wspace=0.001)

pylab.savefig(datapath+Target+AppYear+"BeltProfile.png",dpi=300)
