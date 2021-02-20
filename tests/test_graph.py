# yes, the Theta data jumps from pi to -pi, that's part of the intentional design of fastslam.. it does mean the derivative data jumps though

import matplotlib.pyplot as plt
import sys
import ast

from MSPStreamMaths.StreamMaths import StreamMaths

def test_graph_all():

    ddt, fs2_out = import_dicts("tests/fs_data.txt")
        
    sm = StreamMaths(lpf_avg_length=3, lpf_smoothing=3)
    avg = {'x':[], 'y':[], 'theta':[]}
    smooth = {'x':[], 'y':[], 'theta':[]}

    # LPF signals 
    for var in ['x', 'y', 'theta']:
        for i in range(len(ddt['x'])):

            avg[var].append(sm.lpf_moving_avg(ddt[var][i]))
            smooth[var].append(sm.lpf_smooth(ddt[var][i]))

    # plotting logic
    fig, axs = plt.subplots(3,2,sharex='col')

    for i, var in [ [0, 'x'], [1, 'y'], [2, 'theta']]:

        axs[i][1].plot(fs2_out[var], label=var)
        axs[i][0].plot(ddt[var], label="numerical diff")
        axs[i][0].plot(avg[var], label="moving avg")
        axs[i][0].plot(smooth[var], label="smooth")
        axs[i][0].legend(loc="lower right")



    # axis labels
    from matplotlib.transforms import offset_copy
    plt.setp([axs[2][0], axs[2][1]], xlabel='time (secs * 10)')
    for ax in axs.flat:
        ax.grid()
    
    # y ax labels
    axs[0][1].set_ylabel('dist (m)')
    axs[0][0].set_ylabel('velocity (m/s)')
    axs[1][1].set_ylabel('dist (m)')
    axs[1][0].set_ylabel('velocity (m/s)')
    axs[2][1].set_ylabel('bearing (rad)')
    axs[2][0].set_ylabel('angular velocity (rad/s)')

    # column headings
    for ax, col in zip(axs[0], ['derivative', 'signal']):
        ax.set_title(col)

    # row titles
    pad = 0
    for ax, row in zip(axs[:,0], ['x', 'y', 'theta']):
        ax.annotate(row + '-axis', xy=(0, 0.5), xytext=(-ax.yaxis.labelpad - pad, 0),
                    xycoords=ax.yaxis.label, textcoords='offset points',
                    size='large', ha='right', va='center')
    fig.tight_layout()
    fig.subplots_adjust(left=0.15, top=0.95)

    plt.show()

def import_dicts(fname):
    """
    read in data from the data file, and pull out the dictionaries
    """
    # messy, but does the job
    with open(fname, "r") as f:
        # breaks up the input file into 2 dictionaries and replaces the assignment operator
        contents = f.read().split("fs2_out=")
        ddt = ast.literal_eval(contents[0].replace("ddt=",""))
        fs2_out = ast.literal_eval(contents[1])
    
    # to account for the newly written bearing derivative calculator, let's
    # take the derivative of the actual bearing stream with the new and 
    # improved version
    import_sm = StreamMaths()
    new_out = []
    for datum in fs2_out['theta']:
        if datum == -1.651277367294096: datum = -2.88520079892029 - 0.03        # override the single weird data point that doesn't fit any trends
        new_out.append(import_sm.derivative_bearing(datum, 0.1))
    ddt['theta'] = new_out
    return ddt, fs2_out