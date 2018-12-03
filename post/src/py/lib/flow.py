
def laminar(y, Vdot, sym=False):
    '''
    sym = True --> returns half profile
    sym = False --> returns full profile
    '''
    ymin = min(y)
    H = max(y)-ymin
    if sym:
        # to-do:
        a = 0
        b = 0
        c = 0
    else:
        a = -6*Vdot/(H**3)
        b = +6*Vdot*(H+2*ymin)/(H**3)
        c = -6*ymin*(ymin+H)*Vdot/(H**3)
    return a*y**2+b*y+c

def laminar2(y, Umax, sym=False):
    '''
    sym = True --> returns half profile
    sym = False --> returns full profile
    '''
    ymin = min(y)
    H = max(y)-ymin
    if sym:
        a = -4*Umax/H**2
        b = (4*(2*ymin+H))*Umax/H**2
        c = -4*ymin*(ymin+H)*Umax/H**2
    else:
        a = -4*Umax/(H**2)
        b = 4*Umax*(2*ymin+H)/(H**2)
        c = -4*ymin*(ymin+H)*Umax/(H**2)
    return a*y**2+b*y+c


def turbulent():
    return None
    

def energeticIntegrateOfFlowQuantity(x, y, fac):
    L = 1#max(x)-min(x)
    print("L:",L)
    dx = [(b-a) for (a, b) in zip(x[:-1],x[1:])]
    fac_mid = [(a+b)/2 for (a, b) in zip(fac[:-1],fac[1:])]
    y_mid = [(a+b)/2 for (a, b) in zip(y[:-1],y[1:])]
    res = [a*b*f for (a, b,f) in zip(y_mid, dx,fac_mid)]
    return sum(res)/L


def writeProfile2CFXInletBC(x, y, z, u, name, filename="inletBC.csv"):
    '''
    writes inlet Profile for CFX calculation
    :param x: x-position
    :param y: y-vector
    :param y: z-vector (typically symmetry/depth)
    :param u: u-vel-profile
    :param filename: filename
    :return: none
    '''
    zero = 0
    f = open(filename, 'w')
    f.write('\n')
    f.write('[Name]\n')
    f.write('%s\n' % name)
    f.write('\n')
    f.write('[Spatial Fields]\n')
    f.write('x, y, z\n')
    f.write('\n')
    f.write('[Data]\n')
    f.write('x [m], y [m], z [m], Velocity u [m s^-1], Velocity v [m s^-1], Velocity w [m s^-1]\n')
    for (ypos, uval) in zip(y, u):
        for zpos in z:
            f.write("%e, %e, %e, %e, %e, %e\n" % (x, ypos, zpos, uval, zero, zero))
    f.close()
