import MDSplus as mds
import numpy as np
import scipy.signal as sig
import pandas as pd
import os

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

def visualize_signals(*files):
    """Assertion: the time of all the file must have the same length"""
    for file in files:
        pass

shots = range(100000,100020)
# shots = [100000]
signals = ['DAU'+str(i+1) for i in range(13)]
resample = 100
tree = 'east_1'
save_signals(shots,tree,resample,*signals)



