import MDSplus as mds
import numpy as np
import scipy.signal as sig
import pandas as pd

def get_data(signal, shot, **kw):
    if 'tree' in kw:
        tree = kw['tree']
    else:
        tree = 'east'

    cn = mds.Connection('mds.ipp.ac.cn')
    cn.openTree(tree, shot)
    x = cn.get('\\' + signal).copy()
    t = cn.get('dim_of(' + '\\' + signal + ')').copy()
    cn.closeAllTrees()
    t = np.array(t, dtype=np.float64)
    x = np.array(x, dtype=np.float64)

    if 'timerange' in kw:
        timerange = kw['timerange']
        index = np.where((t >= np.min(timerange)) & (t <= np.max(timerange)))
        t = t[index]
        x = x[index]

    judge = signal[0:2]
    if judge == "G1":
        temp = x
        x = 10 ** (temp * 1.667 - 9.333)

    elif judge == "PA" or judge == "PJ":
        temp = x
        x = 2e3 * temp

    elif judge == "PP" or judge == "PD":
        temp = x
        x = 2e4 * temp

    if 'medfilt' in kw:
        n = kw['medfilt']
        x = sig.medfilt(x, n)

    if 'move' in kw:
        move = kw['move']
        t = t - move

    if 'smooth' in kw:
        win = kw['smooth'][0]
        k = kw['smooth'][1]
        x = sig.savgol_filter(x, win, k)

    if 'log' in kw:
        if kw['log'] == 10:
            x = np.log10(x)
        elif kw['log'] == 2:
            x = np.log2(x)
        else:
            x = np.log(x)

    if 'zoom' in kw:
        n = kw['zoom']
        x = n * x

    return t, x

def save_DAU(shot,tree):
    df = pd.DataFrame(dtype=np.float32)
    # Read time & DAU1
    df['Time'],df['DAU1'] = get_data('DAU1',shot,tree=tree)
    # Read DAU2~DAU13
    for i in range(2,14):
        signal = 'DAU'+str(i)
        _,df[signal] = get_data(signal,shot,tree=tree)
    # Save as .csv file
    file_name = 'Shot_'+str(shot)+'.csv'
    df.to_csv(file_name)


shot = 100000
tree = 'east_1'
save_DAU(shot,tree)


