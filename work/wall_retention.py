import MDSplus as mds
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def get_retention(shot):
    KH2 = 2.4
    KD2 = 2.9
    Pam2D = 4.82e20
    V_smbi2 = 2.0431e-4
    V_smbi3 = 2.0431e-4 + 3.78e-3
    V_jhg1 = 3.118e-4


    cn = mds.Connection('mds.ipp.ac.cn')
    cn.openTree('east_1', shot)

    time = np.array(cn.get('dim_of(' + '\\' + 'jhg1' + ')'))
    jhg1 = (np.array(cn.get('\\jhg1')) - 1) * 2.5e4
    # jhg1 = jhg1(1:length(ipm));
    jhg1 = signal.savgol_filter(jhg1, 1000,3)

    puff_jhg1 = np.mean(jhg1[:6000])-jhg1
    puff = puff_jhg1 * V_jhg1

    pjs205 = np.array(cn.get('\\pjs205')) * 2e3
    pjs205 = signal.savgol_filter(pjs205, 1000, 3)
    pjs204 = np.array(cn.get('\\pjs204')) * 4e5
    pjs204 = signal.savgol_filter(pjs204, 1000, 3)

    if np.max(pjs205) > 1.9e4:
        smbi = V_smbi2 * (np.mean(pjs204[:6000])-pjs204)
    else:
        smbi = -V_smbi2 * (np.mean(pjs205[6000])-pjs205)

    # index = np.find(smbi < 0)

    return time,smbi

time, smbi = get_retention(100001)
df = pd.DataFrame(dtype=np.float32)
df['time'] = time[::100]
df['smbi'] = smbi[::100]
df.to_csv('smbi.csv')
print(len(smbi))
print(smbi)
print(time)
plt.plot(time,smbi,xlabel='time',ylabel='smbi')
plt.show()



