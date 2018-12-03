
'''
author: Matthias Probst (matthias.probst@kit.edu)

all about file management
'''
import os, sys
import numpy as np

def write2file_xy(x, y, flname, delimeter=';'):
    '''
    :param x: vector
    :param y: vector
    :param flname: string
    :param delimeter: string
    :return: True or False
    '''
    try:
        fl = open(flname, 'w')
        for (i, j) in zip(u,y):
            fl.write("%f%s%f\n" % (i, delimeter, j))
        fl.close()
        return True
    except:
        return False


def read_file_xy(flname):
    '''
    :param flname: string
    :param delimeter: string
    :return: x,y
    '''
    with open(flname, 'r') as fl:
        data = [line.strip().split() for line in fl]
    return data
    
    

def readPropFile(flname):
    '''
    reads properties from file
    '''
    if not os.path.isfile(flname):
        print(" [ERROR] Path %s does not exist" % flname)
        sys.exit()
        return None
    else:
        with open(flname, 'r') as fl:
            data = [line.strip().split(',') for line in fl if line[0] != "#"]
        return data
    


def read_file_xy_fromTecPlot(flname, delimiter):
    '''
    !!!first line and last two lines will not be returned!!!
    :param flname: string
    :param delimeter: string
    :return: x,y
    '''
    with open(flname, 'r') as fl:
        data = [line.strip().split(delimiter) for line in fl if (line[0] != "\n" and line[0] != "X" and line[0] != "#")]
    return data
    


def get_xH_data(flname, index1, index2, delimeter):
    # read data from x/h-File:
    data = read_file_xy_fromTecPlot(flname, delimeter)
    lendata = len(data)
    # init vectors:
    y = np.zeros(lendata)
    u = np.zeros(lendata)
    # go through data and plot
    for (i, d) in enumerate(data):
        y[i] = float(d[index1])
        u[i] = float(d[index2])
    return y, u
