import MDSplus as mds
import numpy as np
import pandas as pd
from MDSplus import mdsExceptions

shots = np.arange(100000, 110000)
cn = mds.Connection("mds.ipp.ac.cn")
long_pulse_shots = []
for shot in shots:
    try:
        cn.openTree("pcs_east", shot)
    except mds.mdsExceptions.TreeFOPENR:
        print(f"The tree of #{shot} is not exist")
    else:
        try:
            time_ip = cn.get("dim_of(\pcrl01)").data()  # 等离子体电流
            ip = cn.get('\pcrl01').data()
        except mds.mdsExceptions.TreeNODATA:
            print(f'No pcrl01 data available for #{shot}')
        else:
            # print(ip[:10])
            if time_ip[-1] - time_ip[0] > 60 and max(ip) > 2e5:  # Existing time >= 60
                long_pulse_shots.append(shot)
        finally:
            cn.closeTree("pcs_east", shot)
            if shot % 1000 == 0:
                print(f'{shot} / shots[-1]')
                print('---------------------------')
print(long_pulse_shots)
