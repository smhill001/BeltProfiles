# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 07:11:14 2018

@author: Steven Hill
"""

import sys
drive='f:'
sys.path.append(drive+'\\Astronomy\Python Play\Util')
sys.path.append(drive+'\\Astronomy\Python Play\BeltProfiles')

import ConfigFiles as CF
import BeltPlotLib as BPL
import matplotlib.pyplot as pl
import pylab

path=drive+"/Astronomy/Projects/Planets/Jupiter/Imaging Data/Mapping/"


NEBPlotParams=CF.PlotSetup("BeltPlotConfig.txt")
NEBPlotParams.loadplotparams(drive,"Jupiter_NEB","Belt")
NEBPlotParams.Setup_Plot()

AppYears=[2005,2006,2007,2008,2009,2010,2012,2013,2014,2015,2016]

for AppYear in AppYears:
    print AppYear
    fn="Jupiter"+str(AppYear)+"Belts.txt"

    test=BPL.BeltEdgeMeasList(path+fn)
    L=BPL.ListofProfiles("BeltDataFiles.txt")
    L.load_select_data("Jupiter",AppYear)
    Bands=L.Filter
    print Bands
    for B in Bands:
        print B
        test.load_select_data(B,7.,18.)
        print test.North,test.South,test.Center
        print L.Date,L.Date
        pl.scatter([L.Date[0],L.Date[0]],[test.North,test.South],
                   color=BPL.FilterLineColor(B),s=5,label=B)

itemp=0
spacing=0.05
for B in ["380NUV","450BLU","550GRN","650RED","685NIR","740NIR","807NIR","889CH4"]:
    print B
    pl.annotate(s=B, xy=(0.,0.),xytext=(0.9,0.8-itemp*spacing),xycoords='figure fraction',textcoords='figure fraction',
                 fontsize=8,color=BPL.FilterLineColor(B),horizontalalignment="left")
    print BPL.FilterLineColor(B)
    itemp=itemp+1
#pl.legend(loc=3,ncol=1, borderaxespad=0.,prop={'size':4})
pl.subplots_adjust(left=0.09, right=0.97, top=0.90, bottom=0.10, wspace=0.001)

pylab.savefig(path+"Jupiter_NEB_EdgeDetection.png",dpi=300)
