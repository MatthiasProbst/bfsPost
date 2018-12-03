
'''
author: Matthias Probst (matthias.probst@kit.edu)

all about file management
'''

def writeLaminarInletBcFile(y, u, flname):
    '''
    :param x: vector
    :param y: vector
    :param flname: string
    :param delimeter: string
    :return: True or False
    '''
    h = 0.025
    xx = -20
    z = [0, 4]
    vv = 0
    ww = 0
    try:
        fl = open(flname, 'w')
        # headers:
        fl.write("%s\n" % "[Name]")
        fl.write("%s\n\n" % "inletBC")
        fl.write("%s\n" % "[Spatial Fields]")
        fl.write("%s\n\n" % "x, y, z")
        fl.write("%s\n" % "[Data]")
        fl.write("%s\n" % "x [m], y [m], z [m], Velocity u [m s^-1], Velocity v [m s^-1], Velocity w [m s^-1]")
        for (yy, uu) in zip(y, u):
            for zz in z:
                fl.write("%f,%f,%f,%f,%f,%f\n" % (xx*h, yy, zz*h, uu, vv, ww))
        fl.close()
        return True
    except:
        return False
    

def writeInletBcFile(y, u, flname):
    '''
    :param x: vector
    :param y: vector
    :param flname: string
    :param delimeter: string
    :return: True or False
    '''
    h = 0.025
    xx = -20
    z = [0, 4]
    vv = 0
    ww = 0
    umax = 9.27089
    try:
        fl = open(flname, 'w')
        # headers:
        fl.write("%s\n" % "[Name]")
        fl.write("%s\n\n" % "inletBC")
        fl.write("%s\n" % "[Spatial Fields]")
        fl.write("%s\n\n" % "x, y, z")
        fl.write("%s\n" % "[Data]")
        fl.write("%s\n" % "x [m], y [m], z [m], Velocity u [m s^-1], Velocity v [m s^-1], Velocity w [m s^-1]")
        for (yy, uu) in zip(y, u):
            for zz in z:
                fl.write("%f,%f,%f,%f,%f,%f\n" % (xx*h, yy*h, zz*h, uu*umax, vv*umax, ww*umax))
        fl.close()
        return True
    except:
        return False
    

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


def read_file_xy_fromTecPlot(flname, delimiter):
    '''
    !!!first line and last two lines will not be returned!!!
    :param flname: string
    :param delimeter: string
    :return: x,y
    '''
    with open(flname, 'r') as fl:
        data = [line.strip().split(delimiter) for line in fl]
    return data[1:-1]
