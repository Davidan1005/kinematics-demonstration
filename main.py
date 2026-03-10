import matplotlib.pyplot as plt
import numpy as np

# Initialisation of static shit
fig, ax = plt.subplots()

ax.set_xlim(-10,10)
ax.set_ylim(-10,10)

originx = 0
originy = 0

ax.plot([originx],[originy],'o')
# Initialisation of static shit


# Initialisation of non static shit
dot, = ax.plot([0], [0], "ro")
line, = ax.plot([originx,0],[originy,0])
link_end, = ax.plot([0], [0], "o")
# Initialisation of non static shit


def track_cursor(event):
    if event.inaxes:
        dot.set_data([event.xdata], [event.ydata])

        clamping_constant = ((event.xdata**2) + (event.ydata**2))**0.5
        length_constant = 5

        line.set_data([originx,(event.xdata*length_constant)/clamping_constant], [originy,event.ydata*length_constant/clamping_constant])
        
        link_end.set_data([event.xdata*length_constant/clamping_constant], [event.ydata*length_constant/clamping_constant])
        # line.set_data([originx,event.xdata], [originy,event.ydata])
        
        fig.canvas.draw_idle()

fig.canvas.mpl_connect("motion_notify_event", track_cursor)
plt.show()
