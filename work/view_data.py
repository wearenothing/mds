import pandas as pd
import matplotlib.pyplot as plt


def view_data(file, signal, resample):
    df = pd.read_csv(file)
    plt.plot(df['Time'][::resample], df[signal][::resample])  # resample the data


file = 'shot-100000.csv'
resample = 100
df = pd.read_csv(file)
x = df['Time'][::resample]  # Sample data.

# Note that even in the OO-style, we use `.pyplot.figure` to create the Figure.
fig, ax = plt.subplots(figsize=[10, 6], layout='constrained')
for i in range(1, 14):
    signal = 'DAU' + str(i)
    ax.plot(x, df[signal][::resample], label=signal)

ax.set_xlabel('Time')  # Add an x-label to the axes.
ax.set_ylabel('Value')  # Add a y-label to the axes.
ax.set_title("DAU Signals")  # Add a title to the axes.
ax.legend()  # Add a legend.
# view_data('shot-100000.csv', 'DAU13', 100)
plt.show()
