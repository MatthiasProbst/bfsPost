#!/bin/python

# import own packages:
from lib.my_plotting_lib import myplot, adjustFigAspect, plot_geometry, beautify_plot
from lib.fileManagement import get_xH_data, readPropFile
from lib.flow import energeticIntegrateOfFlowQuantity
from lib.result import Simulation, Experiment, compareSimAndExp
# import python packages:
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import os, sys, getopt


# geometry constants:
#H_STEP=0.025                # [m]
#H_OUTLET = 2*h_step         # [m]
#EXPANSION = H_OUTLET/H_STEP # [-]

#  TODO 1
#  shear stress analysis --> da gibt es schon etwas
#  pressure analysis --> tecplot-macro
#  --> zusammen in bfs_analysis library
#  geometry constants as input parameter --> make other expansion ratios be analysable



def main(argv):
    # default solver if user does not pass one:
    CFX=True
    SPARC=False
    COMPARE=False
    geomtype="classic"
    #
    try:
        opts, args = getopt.getopt(argv,"hn:e:s:v:g:",["casename=","expfolder=","simfolder=","solver=","geomtype="])
        print(opts,args)
    except getopt.GetoptError:
        print('plot_U_profiles.py -n <casename> -e <exp_file_folder> -s <sim_file_folder>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('plot_U_profiles.py -n <casename> -e <exp_file_folder> -s <sim_file_folder>')
            sys.exit()
        elif opt in ("-n", "--casename"):
            casename = arg
        elif opt in ("-e", "--expfolder"):
            expData_path = arg
            COMPARE=True
        elif opt in ("-s", "--simfolder"):
            simData_path = arg
        elif opt in ("-g", "--geomtype"):
            geomtype = arg
        elif opt in ("-v", "--solver"):
            if arg=="cfx":
                CFX=True
                SPARC=False
            elif arg=="sparc":
                CFX=False
                SPARC=True
            else:
                print('plot_U_profiles.py -e <exp_file_folder> -s <sim_file_folder>')
                sys.exit()

    # print arguments:
    print("*** INFO ***")
    print("sim path: %s" % simData_path)
    if COMPARE:
      print("sim path: %s" % expData_path)

    # create result object for simulation:
    sim = Simulation(simData_path, geomtype, casename)
    sim.readSliceData()
    # add material properties to simulation:
    sim.setFlowProp(os.path.join(simData_path, "matprop"))
    # read geometry parameters:
    sim.setGeomProp(os.path.join(simData_path, "geomprop"))
    # calculate Reynolds number for slice @x/h=-2
    sim.calc_Re_from_slice(-2)
    sim.readTauX()
    
    xh_slices = [x.xh for x in sim.slicedata]
    if COMPARE:
      # create result object for experimental data:
      exp = Experiment(expData_path, geomtype)
      exp.setSlicePositions(xh_slices)
      exp.readSliceData()
      exp.setFlowProp(os.path.join(simData_path, "matprop"))
      # check if experimental data exist
      exp.checkExpData()
      
      
    def init_plotting(casename):
        pic_path = os.path.join('pics',casename)
        if not os.path.isdir('pics'):
            if not os.path.isdir(pic_path):
                os.makedirs(pic_path)
        elif not os.path.isdir(pic_path):
                os.makedirs(pic_path)
        return pic_path
      
    pic_path = init_plotting(sim.casename)
      
    # plotting--------------------------------------------------------------------
    
    # initialize figure with aspect size of 2:
    w, h = plt.figaspect(0.5)
    fig, ax = plt.subplots(figsize=(w, h))
    
    if COMPARE:
      # plot experimental data. note, that data is dimensionless!
      for sl in exp.slicedata:
        myplot(sl.u+sl.xh, sl.y, m='*', ls=None, col='black', ax=ax)
    
    # plot simulation data. Note, that data is not yet made dimensionless!
    u_entdim = max(sim.slicedata[0].u)
    for sl in sim.slicedata:
        if sl.xh == 0:
            print(sl.y)
        myplot(sl.u/u_entdim+sl.xh, sl.y/sim.h_step, m='*', ls=None, col='red', ax=ax)
    
    beautify_plot(ax, x_label='x/h', y_label='y/h', xmin=-2.5, xmax=17.5)
    sim.plot_geometry(ax)
    plt.title("Velocity-Comp. U: Exp. (black) vs. Sim. (red)")
    plt.savefig(os.path.join(pic_path,'vel.png'))
    
    
    for sl in sim.slicedata:
        sl.volumeFlowRate(sim.rho)
        sl.averagePt(sim.rho)
        sl.averagePs(sim.rho)
           
        
    plt.figure()
    
    plt.plot(xh_slices, [sl.ptav for sl in sim.slicedata], '^-', label='pt sim')
    plt.legend()
    dpt = sim.slicedata[-1].ptav-sim.slicedata[0].ptav
    print("Total pressure difference between x/h=15 and x/h=-2: %f" % (dpt))
    pdyn_in = sim.slicedata[0].ptav-sim.slicedata[0].psav
    print("Inlet dynamic pressure: %f" % pdyn_in)
    print("Pressure loss coeff = dpt/pdyn_in: %f" % (dpt/pdyn_in))
    
    if COMPARE:
      plt.figure()
      yentdim = sim.h_step
      for (slSim, slExp) in zip(sim.slicedata, exp.slicedata):
        ySimInterp, deltaU = compareSimAndExp(slSim.y/yentdim, slExp.y, slSim.u/u_entdim, slExp.u)
        #plt.plot(deltaU+slSim.xh, ySimInterp, '^-', label='pt sim')
        labeltext="X/H=%i" % slExp.xh
        print(labeltext)
        plt.plot(ySimInterp, deltaU/slExp.u*100, '^-', label=labeltext)
        #plt.plot(deltaU/slExp.u*100, ySimInterp, '^-', label='pt sim')
      plt.legend()
      plt.savefig(os.path.join(pic_path,'du.png'))
    
    
    print(sim.taux)
    ixtau = [i for (i,y) in enumerate(sim.ytaux) if y==0]
    sim.xtaux = sim.xtaux[ixtau[0]:ixtau[-1]]
    sim.taux = sim.taux[ixtau[0]:ixtau[-1]]
    # find zero-crossing:
    zero_crossing_x = []
    zero_crossing_y = []
    for (x1, x2, y1, y2) in zip(sim.xtaux[:-1],sim.xtaux[1:],sim.taux[:-1],sim.taux[1:]):
        if np.sign(y1) != np.sign(y2):
            m = (y2-y1)/(x2-x1)
            n = y1 - m*x1
            zero_crossing_x.append(-n/m)
            zero_crossing_y.append(0)
    plt.figure()
    plt.plot(sim.xtaux, sim.taux)
    if zero_crossing_x: # if there are entries in zero_crossing_x
        plt.plot(zero_crossing_x, zero_crossing_y, '+')
        print("Reattachment length xR/H=%f" % (zero_crossing_x[-1]/sim.h_step))
        plt.xlabel("x [m]")
        plt.ylabel("tau_x [Pa]")
    else:
        print("No crossings found")
    plt.savefig(os.path.join(pic_path,'tau.png'))
    plt.show()
    
    # write integral data to *.ires
    f=open("%s.ires" % sim.casename, 'w')
    f.write("#Re\n")
    f.write("%f\n" % sim.Re)
    f.write("#tau\n")
    if zero_crossing_x: 
        f.write("%f\n" % (zero_crossing_x[-1]/sim.h_step))
    else:
        f.write("-1.0")
    f.write("#dpt\n")
    f.write("%f\n" % dpt)
    f.close()
    

if __name__ == "__main__":
    main(sys.argv[1:])
