from matplotlib import pyplot as plt
import numpy as np

fig, ax = plt.subplots()  # Create a figure containing a single axes.
x = np.array([1, 2, 3, 4])
y = np.array([1, 4, 9, 16,20])
ax.plot(x)  # Plot some data on the axes.
ax.plot(y)
plt.savefig("test")