import matplotlib.pyplot as plt
import numpy as np
from d2l import torch as d2l

x = np.linspace(-100,100)
y1 = np.cos(x)
y2 = np.sin(x)
y3 = np.cos(x) + np.sin(x)
# fig,axs = plt.subplots(3,1,subplot_kw=dict(projection="polar"))
d2l.plot(x,[y1,y2,y3])
# axs[0].plot(x,y1)

# axs[0].plot(x,y2)
# axs[0].plot(x,y3)
# axs[2].plot(x,y3)
# plt.subplot()
plt.plot(x,y1)
plt.plot(x,y2)
plt.plot(x,y3)
plt.show()