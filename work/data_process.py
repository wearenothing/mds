import MDSplus as mds
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt


def get_signals( shot, tree='east_1', resample=100, *signals,):
    """return time and data of corresponding resampled signals  """

    cn = mds.Connection('mds.ipp.ac.cn')
    cn.openTree(tree, shot)

    times,datas=[],[]
    for signal in signals:
        # Resample data and time, and convert the type of MDSplus.Float32Array to numpy.ndarray
        time = np.array(cn.get('dim_of(' + '\\' + signal + ')')[::resample])
        data = np.array(cn.get('\\' + signal)[::resample])
        times.append(time)
        datas.append(data)

    cn.closeAllTrees()

    return times,datas

def save_signals(shots,tree,resample,*signals):
    """Save the signals of shots as **.csv file"""

    # Generate a .csv file for each shot
    for shot in shots:
        df = pd.DataFrame(dtype=np.float32)
        # Read time & DAU1
        times, datas = get_signals(shot,tree,resample,*signals)
        for i in range(len(times)):
            df['Time'+str(i+1)],df['DAU'+str(i+1)] = times[i],datas[i]

        # Save as .csv file
        file_path = os.path.join('..','data','resample'+str(resample))
        os.makedirs(file_path,exist_ok=True)
        file_name = os.path.join(file_path,'shot'+str(shot)+'.csv')
        df.to_csv(file_name)

def visualize_files(*filenames,save=False):
    """Assertion: the time of all the file must have the same length"""
    for filename in filenames:
        df = pd.read_csv(filename)
        x = df['Time1']

    # Note that even in the OO-style, we use `.pyplot.figure` to create the Figure.
        fig, ax = plt.subplots(figsize=[10, 6], layout='constrained')
        for i in range(1, 14):
            signal = 'DAU' + str(i) #TODO: should not only work for DAU signals
            ax.plot(x, df[signal], label=signal)
        ax.set_xlabel('Time')  # Add an x-label to the axes.
        ax.set_ylabel('Value')  # Add a y-label to the axes.
        ax.set_title(filename[-14:-4]+" DAU signals")  # Add a title to the axes.
        ax.legend()  # Add a legend.
        # if save is true, save the graph
        if save:
            path = os.path.join('..','figs','')
            plt.savefig(path+filename[-14:-4]+'.png')
        plt.show()

# shots = range(100000,100020)
# shots = [100000]
# signals = ['DAU'+str(i+1) for i in range(13)]
# resample = 100
# tree = 'east_1'
# times,datas = get_signals(100000,tree,1,*signals)
# # save_signals(shots,tree,resample,*signals)
# print(len(times[0]))

# Visualize shot[100000:100020]
# path = os.path.join('..','data','resample100')
# filenames = ['shot'+str(100000+i) for i in range(20)]
# filenames = [os.path.join(path,filename+'.csv') for filename in filenames]
# visualize_files(*filenames,save=True)


# Normalize signals to see
times,signals=get_signals(110061,'east_1',1,'vldl1','LIIU2','DAU4')
print(len(times[0]))
print(len(times[1]))
# plt.plot(times[0],signals[0],label='vldl1')
# plt.plot(times[1],signals[1],label= 'LIIU2')
# plt.plot(times[2],signals[2],label= 'DAU4')
# plt.legend()
# plt.show()
