from .fileManagement import readPropFile, get_xH_data
import os, sys
import numpy as np
from scipy import interpolate


def interpolateSime2Exp(ySim, yExp, uSim, uExp):
    f = interpolate.interp1d(ySim,uSim)
    ySimInterp = yExp
    uSimInterp = f(ySimInterp) 
    return ySimInterp, uSimInterp


def compareSimAndExp(ySim, yExp, uSim, uExp):
    ySimInterp, uSimInterp = interpolateSime2Exp(ySim, yExp, uSim, uExp)
    delta=uSimInterp-uExp
    return ySimInterp, delta



class Slicedata:
    
    def __init__(self):
        self.xh  = []
        self.y   = []
        self.u   = []
        self.v   = []
        self.uav = 0
        self.ps  = []
        self.psav  = []
        self.pt  = []
        self.ptav  = []
        self.path = ""
        self.vfr = -1
        
    def calcAbsoluteVelocity(self):
        if self.u and self.v:
            for (u, v) in zip(self.u, self.v):
                self.c = np.sqrt(u**2+v**2)
        else:
            print(" [ERROR in calcAbsoluteVelocity]: Not enough data")
    
    def volumeFlowRate(self, rho):
        dy   = [(b-a) for (a, b) in zip(self.y[:-1], self.y[1:])]
        umid = [(a+b)/2 for (a, b) in zip(self.u[:-1], self.u[1:])]
        self.vfr = sum([a*b for (a, b) in zip(umid, dy)])
        print(self.vfr)
    
    def averagePt(self, rho):
        dy    = [(b-a) for (a, b) in zip(self.y[:-1], self.y[1:])]
        umid  = [(a+b)/2 for (a, b) in zip(self.u[:-1], self.u[1:])]
        ptmid = [(a+b)/2 for (a, b) in zip(self.pt[:-1], self.pt[1:])]
        self.ptav = sum([a*b*u for (a, b, u) in zip(ptmid, dy, umid)])*rho/self.vfr
    
    def averagePs(self, rho):
        dy    = [(b-a) for (a, b) in zip(self.y[:-1], self.y[1:])]
        umid  = [(a+b)/2 for (a, b) in zip(self.u[:-1], self.u[1:])]
        ptmid = [(a+b)/2 for (a, b) in zip(self.ps[:-1], self.ps[1:])]
        self.psav = sum([a*b*u for (a, b, u) in zip(ptmid, dy, umid)])*rho/self.vfr
               
        

class Result:

    def __init__(self, path, geomtype, casename = ""):
        self.path = path
        self.geomtype = geomtype
        self.casename = casename
        self.slicedata = []
        self.h_step = 0
        self.h_out = 0
        self.L1 = 0
        self.L2 = 0
        self.rho = -1
        self.mu  = -1
        self.Re = -1
        
     
    def setFlowProp(self, flname):
        flProp   = readPropFile(flname)
        self.rho = float(flProp[0][1])
        self.mu  = float(flProp[1][1])
        
        
    def calc_Re_from_slice(self,x):
        print(" > Calculating Reynolds number from slice x/h=%i ..." % x)
        for (i, sl) in enumerate(self.slicedata):
            if sl.xh == x:
                break;
            
        if self.slicedata:
            D = max(self.slicedata[i].y)-min(self.slicedata[i].y)
            Umax = max(self.slicedata[i].u)
            self.Re = self.rho*Umax*D/self.mu
            print("                                                 ... Re=%f" % self.Re)
        else:
            print(" [Error in calc_Re_from_slice]: no slice data. Unable to calculate Re for slice x/h=%i" % x)
            sys.exit()
       
       
class Simulation(Result):
    
    def __init__(self, path, geomtype, casename = ""):
        Result.__init__(self, path, geomtype, casename)
        self.rtype = 'sim'
        self.taux = []
        self.xtaux = []
        self.ytaux = []
            
        
    def readSliceData(self):
        # 1.) read *.slice:
        flname = os.path.join(self.path, "slice")
        sliceXYData = readPropFile(flname)
        self.slicedata = []
        for d in sliceXYData:
            self.slicedata.append(Slicedata())
            self.slicedata[-1].xh = float(d[0])
        
        for sl in self.slicedata:
            sliceName = "XH%i.csv" % (sl.xh)
            flname = os.path.join(self.path, "post", sliceName)
            sl.path=flname
            sl.y, sl.ps = get_xH_data(flname, 1, 2, ',')
            sl.y, sl.pt = get_xH_data(flname, 1, 3, ',')
            sl.y, sl.u  = get_xH_data(flname, 1, 5, ',')
            
            
    def readTauX(self):
        tauxname="taux.csv"
        flname = os.path.join(self.path, "post", tauxname)
        print(flname)
        self.xtaux, self.taux = get_xH_data(flname, 0, 2, ',')
        self.xtaux, self.ytaux = get_xH_data(flname, 0, 1, ',')
        

        
    def setGeomProp(self, flname):
        bfsGeom = readPropFile(flname)
        self.h_step = float(bfsGeom[0][1])
        self.h_out = float(bfsGeom[1][1])
        self.L1 = float(bfsGeom[2][1])
        self.L2 = float(bfsGeom[3][1]) 
        if self.geomtype == "pocket":
            self.b = float(bfsGeom[4][1]) 
            self.f = float(bfsGeom[5][1]) 
            self.d = float(bfsGeom[6][1]) 
            self.e = float(bfsGeom[7][1]) 
        self.expansion = self.h_out/self.h_step
    
    
    def plot_geometry(self, ax):
        if self.geomtype == "classic":
            ax.plot([0, 0], [0, 1], 'k-', linewidth=2)
            ax.plot([-2.5, 0], [1, 1], 'k-', linewidth=2)
            ax.plot([0, 17.5], [0, 0], 'k-', linewidth=2)
            ax.plot([-2.5, 17.5], [2, 2], 'k-', linewidth=2)
        elif self.geomtype == "pocket":
            ax.plot([0, -2.5], [1, 1], 'k-', linewidth=2)
            ax.plot([-2.5, 17.5], [2, 2], 'k-', linewidth=2)
            ax.plot([17.5, 17.5], [2, 0.0], 'k-', linewidth=2)
            ax.plot([17.5, self.f], [0.0,0.0], 'k-', linewidth=2)
            ax.plot([self.f,self.f], [0, -self.d], 'k-', linewidth=2)
            ax.plot([self.f, -self.b], [-self.d,-self.d], 'k-', linewidth=2)
            ax.plot([-self.b, -self.b], [-self.d, 1-self.e*self.h_step], 'k-', linewidth=2)
            ax.plot([-self.b, 0], [1-self.e*self.h_step, 1-self.e*self.h_step], 'k-', linewidth=2)
            ax.plot([0, 0], [1-self.e*self.h_step,1], 'k-', linewidth=2)
        
        
    
class Experiment(Result):
    
    def __init__(self, path, geomtype, casename = ""):
        Result.__init__(self, path, geomtype, casename)
        self.rtype = 'exp'
        
    
    def setSlicePositions(self, xh_ls):
        self.slicedata = []
        for xh in xh_ls:
            self.slicedata.append(Slicedata())
            self.slicedata[-1].xh = xh
        
        
    def readSliceData(self):   
        for sl in self.slicedata:
            sliceName = "XH%i.exp" % (sl.xh)
            flname = os.path.join(self.path, sliceName)
            sl.path=flname
            sl.y, sl.u = get_xH_data(flname, 0, 1, ',')
            
            
    def checkExpData(self):
        print("checking experimental data ...")
        for sl in self.slicedata:
            try:
                f = open(sl.path)
                f.close()
                print(" > %s successful" % sl.path)
            except:
                print(" > %s failed" % sl.path)
