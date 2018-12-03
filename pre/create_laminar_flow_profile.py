#!/bin/python
import lib.flowProfiles as fprof
from lib.fileManagement import read_file_xy, writeLaminarInletBcFile
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import sys, getopt


#Re_ls = np.array([1.,5.,10.,50.,100.,500.,1000.,5000.,10000.])
#umax_ls = Re_ls*MU/DENSITY/0.025


    
def main(argv):
    #
    DENSITY=1.185
    MU=1.831e-5
    profile_half_full = 'full'
    doplot=False
    flname='non_given'
    try:
        opts, args = getopt.getopt(argv,"hvr:p:d:m:o:",["re=","visualize=","profile=","density=","mu=","output="])
        print(opts,args)
    except getopt.GetoptError:
        print('create_laminar_profile.py -p -r <Re> -o <option> -d <density> -m <mu>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('create_laminar_profile.py -p -r <Re> -o <option> -d <density> -m <mu>')
            sys.exit()
        elif opt in ("-v", "--visualize"):
            doplot=True
        elif opt in ("-r", "--re"):
            re=float(arg)
        elif opt in ("-p", "--profile"):
            profile_half_full=arg
        elif opt in ("-d", "--density"):
            DENSITY=float(arg)
        elif opt in ("-m", "--mu"):
            MU=float(arg)  
        elif opt in ("-o", "--output"):
            flname=arg  
    
    if flname=='non_given':
        flname = "LaminarInletBCRe%i_half.csv" % re
    
    umax = re*MU/DENSITY/0.025
    if profile_half_full=='half':
        y = np.linspace(0.025, 2*0.05, 100)
    else: 
        y = np.linspace(0.025, 0.05, 100)
                
    lam_u = fprof.laminar2(y, umax)
    if profile_half_full=='half':
        writeLaminarInletBcFile(y[:50], lam_u[:50], flname)
    else:
        writeLaminarInletBcFile(y, lam_u, flname)
    
    if doplot:
        plt.plot(lam_u,y)
        plt.show()
        

if __name__ == "__main__":
    main(sys.argv[1:])
