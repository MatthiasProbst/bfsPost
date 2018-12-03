'''
author: Matthias Probst (matthias.probst@kit.edu)

all customized plotting functions for all kind of purposes
'''
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


def myplot(xval, yval, m=None, ls='--', col='black', c_label=None, ax=None):
    # cml = color marker line = format
    if ax==None:
        fig, ax = plt.subplots()

    ax.plot(xval, yval, marker=m, markersize=2, linestyle=ls, color=col, label=c_label)

    if c_label is not None:
      ax.legend(loc='best', framealpha=1)


def errplot(xval, yval, x_err=None, y_err=None, col='black', x_label='x', y_label='y', c_label=None, marker=None, ax=None):

    if ax==None:
        fig, ax = plt.subplots()

    if x_err == None:
        if y_err == None:
            #ax.errorbar(xval, yval, marker=marker, capsize=2, label=c_label)
            ax.errorbar(xval, yval, fmt='.', capsize=2, label=c_label, color=col)
        else:
            ax.errorbar(xval, yval, yerr=y_err, marker=marker, capsize=2, label=c_label, color=col)
    else:
        if y_err == None:
            ax.errorbar(xval, yval, xerr=x_err, marker=marker, capsize=2, label=c_label, color=col)
        else:
            ax.errorbar(xval, yval, xerr=x_err, marker=marker, capsize=2, label=c_label)

    if c_label is not None:
      ax.legend(loc='best', framealpha=1)


def beautify_plot(ax, x_label, y_label):
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_xlim([-2.5, 17.5])
    #ax.set_ylim([0, 1])
    #ax.grid()
    ax.ticklabel_format(axis='x', style='sci', useMathText=True, scilimits=(0, 2))


def plot_geometry(ax):
    ax.plot([0, 0], [0, 1], 'k-', linewidth=2)
    ax.plot([-2.5, 0], [1, 1], 'k-', linewidth=2)
    ax.plot([0, 17.5], [0, 0], 'k-', linewidth=2)
    ax.plot([-2.5, 17.5], [2, 2], 'k-', linewidth=2)


def plot_bfs(xval, yval, uval, x_label='x', y_label='y', c_label='Data plot', marker=None, freetext='', ax=None):
    '''
    plot eroftac data for backward facing step (bfs)
    :return: True or False
    '''

    if ax==None:
        fig, ax = plt.subplots()

    yvec = [yval[0]]
    uvec = [uval[0]]
    maxu = max(uval)
    for (i, x) in enumerate(xval[1:]):
        if x == xval[i]:
            yvec.append(yval[i+1])
            uvec.append(uval[i+1])
        else:  # write into new xvec:
            xcorr = xval[i]
            ax.plot(uvec/maxu+xcorr, yvec, '--', marker=marker, label=c_label)
            yvec = [yval[i+1]]
            uvec = [uval[i+1]]
    xcorr = xval[i]
    ax.plot(uvec/maxu+xcorr, yvec, '--', marker=marker, label=c_label)

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.grid()
    ax.ticklabel_format(axis='x', style='sci', useMathText=True, scilimits=(0, 2))
    # ax.legend(loc='best', framealpha=1)

    ax.plot([0, 0], [0, 1], 'k-')
    ax.plot([-2, -2], [1, 2], 'k-')
    ax.plot([-2, 0], [1, 1], 'k-')
    ax.plot([16, 16], [0, 2], 'k-')
    ax.plot([0, 16], [0, 0], 'k-')
    ax.plot([-2, 16], [2, 2], 'k-')
    ax.set_xlim([-3, 17])
    ax.set_ylim([-1, 3])
    ax.text(7, 2.5, freetext)

    return ax


def adjustFigAspect(fig,aspect=1):
    '''
    Adjust the subplot parameters so that the figure has the correct
    aspect ratio.
    '''
    xsize,ysize = fig.get_size_inches()
    minsize = min(xsize,ysize)
    xlim = .4*minsize/xsize
    ylim = .4*minsize/ysize
    if aspect < 1:
        xlim *= aspect
    else:
        ylim /= aspect
    fig.subplots_adjust(left=.5-xlim,
                        right=.5+xlim,
                        bottom=.5-ylim,
                        top=.5+ylim)
