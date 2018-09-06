# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 07:04:47 2018

@author: Steven Hill
"""

import sys
drive='f:'
sys.path.append(drive+'\\Astronomy\Python Play\Util')

import ConfigFiles as CF

class BeltEdgeMeasList(CF.readtextfilelines):
    pass
    def load_all_data(self):
        print "Hi in load_all_data"
        self.Band=['']   #Keyword for star identification
        self.North=['']           #Target, e.g., component of a multiple star
        self.South=['']           #Target, e.g., component of a multiple star
        self.Center=['']           #UT Date of observation: YYYYMMDDUT
        self.NObs=0               #Number of observatinos
        FirstTime=True

        for recordindex in range(1,self.nrecords):
            fields=self.CfgLines[recordindex].split(',')
            if FirstTime:
                self.Band[0]=str(fields[0])
                self.North[0]=float(fields[1])
                self.South[0]=float(fields[2])
                self.Center[0]=float(fields[3])
                FirstTime=False
                self.NObs=1
            else:
                self.Band.extend([str(fields[0])])
                self.North.extend([float(fields[1])])
                self.South.extend([float(fields[2])])
                self.Center.extend([float(fields[3])])
                self.NObs=self.NObs+1

    def load_select_data(self,Filter,MinCenterLat,MaxCenterLat):
        
        self.Band=['']   #Keyword for star identification
        self.North=['']           #Target, e.g., component of a multiple star
        self.South=['']           #Target, e.g., component of a multiple star
        self.Center=['']           #UT Date of observation: YYYYMMDDUT
        self.NObs=0               #Number of observatinos
        FirstTime=True

        for recordindex in range(1,self.nrecords):
            fields=self.CfgLines[recordindex].split(',')
            if fields[0]==Filter:
                #print MinCenterLat,float(fields[3]),MaxCenterLat
                #print MinCenterLat<float(fields[3])<MaxCenterLat
                if MinCenterLat<float(fields[3])<MaxCenterLat:
                    if FirstTime:
                        self.Band[0]=str(fields[0])
                        self.North[0]=float(fields[1])
                        self.South[0]=float(fields[2])
                        self.Center[0]=float(fields[3])
                        FirstTime=False
                        self.NObs=1
                    else:
                        self.Band.extend([str(fields[0])])
                        self.North.extend([float(fields[1])])
                        self.South.extend([float(fields[2])])
                        self.Center.extend([float(fields[3])])
                        self.NObs=self.NObs+1
                        FirstTime=False

def FilterLineColor(FilterName):
    import numpy as np
    #This class provides basic filter parameters for photometry        
    #print "FilterName=",FilterName
    FilterNames=["380NUV","450BLU","550GRN","650RED","656HAL","685NIR","740NIR","807NIR","889CH4"]
    LineColorList=np.array([[0.4,0.2,0.6],[0.1,0.1,0.7],[0.1,0.6,0.1],
                         [0.6,0.5,0.2],[0.6,0.5,0.2],[0.6,0.1,0.0],
                         [0.6,0.1,0.0],[0.6,0.1,0.0],[0.0,0.0,0.0]])
    FilterIndex = [k for k, x in enumerate(FilterNames) if x == FilterName] #what does this do!?
    FI=np.int(FilterIndex[0])
    LineColor=LineColorList[FI]
    return LineColor

class ListofProfiles(CF.readtextfilelines):
    pass
    def load_all_data(self):
        print "Hi in ListofProfiles: load_all_data"
        self.Target=['']   #Keyword for star identification
        self.AppYear=[0]           #Target, e.g., component of a multiple star
        self.Date=[0.0]
        self.Filter=['']           #Target, e.g., component of a multiple star
        self.Offset=[0.0]           #UT Date of observation: YYYYMMDDUT
        self.Smoothing=[0]
        self.NObs=0               #Number of observatinos
        FirstTime=True

        for recordindex in range(1,self.nrecords):
            fields=self.CfgLines[recordindex].split(',')
            if FirstTime:
                self.Target[0]=str(fields[0])
                self.AppYear[0]=float(fields[1])
                self.Date[0]=float(fields[2])
                self.Filter[0]=str(fields[3])
                self.Offset[0]=float(fields[4])
                self.Smoothing[0]=int(fields[5])
                FirstTime=False
                self.NObs=1
            else:
                self.Target.extend([str(fields[0])])
                self.AppYear.extend([float(fields[1])])
                self.Date.extend([float(fields[2])])
                self.Filter.extend([str(fields[3])])
                self.Offset.extend([float(fields[4])])
                self.Smoothing.extend([int(fields[5])])
                self.NObs=self.NObs+1

    def load_select_data(self,Target,AppYear):
        
        self.Target=['']   #Keyword for star identification
        self.AppYear=[0]           #Target, e.g., component of a multiple star
        self.Date=[0.0]
        self.Filter=['']           #Target, e.g., component of a multiple star
        self.Offset=[0.0]           #UT Date of observation: YYYYMMDDUT
        self.Smoothing=[0]
        self.NObs=0               #Number of observatinos
        FirstTime=True

        for recordindex in range(1,self.nrecords):
            fields=self.CfgLines[recordindex].split(',')
            if fields[0]==Target:
                #print fields[0]
                if int(fields[1])==int(AppYear):
                    #print fields[1]
                    if FirstTime:
                        self.Target[0]=str(fields[0])
                        self.AppYear[0]=float(fields[1])
                        self.Date[0]=float(fields[2])
                        self.Filter[0]=str(fields[3])
                        self.Offset[0]=float(fields[4])
                        self.Smoothing[0]=int(fields[5])
                        FirstTime=False
                        self.NObs=1
                    else:
                        self.Target.extend([str(fields[0])])
                        self.AppYear.extend([float(fields[1])])
                        self.Date.extend([float(fields[2])])
                        self.Filter.extend([str(fields[3])])
                        self.Offset.extend([float(fields[4])])
                        self.Smoothing.extend([int(fields[5])])
                        self.NObs=self.NObs+1
                        FirstTime=False