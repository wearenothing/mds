import MDSplus as mds
import numpy as np
import pandas as pd
from scipy import signal

long_pulse_shots = []
# shots= np.arange(106915,116915)
shots= np.arange(106915,107015)
cn = mds.Connection("mds.ipp.ac.cn")

for shot in shots:
    cn.openTree("pcs_east", shot)
    time_ip = cn.get("dim_of(\pcrl01)").data() # 等离子体电流
    if time_ip[-1] - time_ip[0] > 60: # Existing time >= 60
        long_pulse_shots.append(shot)


def get_dau(shot, res_size = 1):
    """Get all DAU signals, return (time, DAUs)"""
    cn.openTree("east_1",shot)
    time = cn.get("dim_of(\DAU1)").data()[::res_size]
    DAUs = []
    for i in range(1,14):
        signal = "\DAU" + str(i)
        DAUs.append(cn.get(signal).data()[::res_size])

    return time,DAUs


def cal_increase(shots):
    """return the increase percent  of values of dau-alpha signals"""

    columns = [f'DAU{i}' for i in range(1,14)]

    df = pd.DataFrame(index=shots,columns=columns)
    for shot in shots:
        time,DAUs = get_dau(shot, res_size=1000)
        smooth_DAUs = []
        for i in range(len(DAUs)):
            smooth_DAUs.append(signal.savgol_filter(DAUs[i],100,3,mode='nearest'))
        # smooth_DAUs = np.array(smooth_DAUs)

        increase = [(max(dau) - min(dau))/min(dau) for dau in smooth_DAUs]
        # increase = [(max(dau) - min(dau))/min(dau) for dau in smooth_DAUs]
        df.loc[shot] =  increase
    return df
# 106923有问题
long_pulse_shots.remove(106923)
# [106915,106921,106922,106969,106970,106971,106972,106973,106974,106975,106976,106977,106978]
df = cal_increase([106915,106921,106922,106969,106970,106971,106972,106973,106974,106975,106976,106977,106978])
df.to_csv('increase.csv',index_label='shot')
print(df)
