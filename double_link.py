import matplotlib.pyplot as plt
import numpy as np


# to do
# implement arm class to manage the states of all links


class Link():
    def __init__(self):
        self.length = 3
        self.angle = 0
        self.start_position= np.array([0,0])
        self.end_position = np.array([
            self.start_position[0] + (self.length*np.cos(self.angle)),
            self.start_position[1] + (self.length*np.sin(self.angle))
            ])
        self.xs = np.array([self.start_position[0],self.end_position[0]])
        self.ys = np.array([self.start_position[1],self.end_position[1]])

    def update_end(self):
        self.end_position = np.array([
            self.start_position[0] + (self.length*np.cos(self.angle)),
            self.start_position[1] + (self.length*np.sin(self.angle))
            ])
        self.xs = np.array([self.start_position[0],self.end_position[0]])
        self.ys = np.array([self.start_position[1],self.end_position[1]])

        

# Static stuff (Initialises plotting space and shit)
fig, ax = plt.subplots()
ax.set_aspect('equal')

ax.set_xlim(-10,10)
ax.set_ylim(-10,10)
# Static stuff

link1 = Link()
link2 = Link()
link2.start_position = link1.end_position
link2.update_end()

link2.angle = 45



link1_line, = ax.plot(link1.xs,link1.ys)



link2_line, = ax.plot(link2.xs,link2.ys)
    


plt.show()

