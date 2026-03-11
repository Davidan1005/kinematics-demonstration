import matplotlib.pyplot as plt
import numpy as np

fig,ax = plt.subplots()

x = 0
y = 0
for frame in range(100):
    

    ax.clear()

    ax.plot([0],[0],'o')
    ax.plot([x],[y],'o')

    x+=1
    y+=1

    plt.pause(0.01)

