import pandas as pd
import matplotlib.pyplot as plt


def view_data(file,signal,resample=1):
    df = pd.read_csv(file)
    plt.plot(df['Time'][::resample],df[signal][::resample]) # resample the data

view_data('shot-100000.csv','DAU13',100)
plt.show()
