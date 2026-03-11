import matplotlib.pyplot as plt
import numpy as np


# to do

class Link():
    def __init__(self,angle=0):
        self.length = 3
        self.angle = angle

        
    def get_components(self,absolute_angle):
        self.components = np.array([
            (self.length*np.cos(absolute_angle)),
            (self.length*np.sin(absolute_angle))
        ])
        return self.components




class Arm():
    def __init__(self, links):

        self.links = links
        cumulative_position = np.array([0, 0])
        cumulative_angle = 0

        for link in self.links:
            cumulative_angle += link.angle

            ax.plot([cumulative_position[0], cumulative_position[0]+link.get_components(cumulative_angle)[0]],
                    [cumulative_position[1], cumulative_position[1]+link.get_components(cumulative_angle)[1]], marker='o')

            cumulative_position = cumulative_position+link.components
            


# Static stuff (Initialises plotting space and shit)
fig, ax = plt.subplots()
ax.set_aspect('equal')

ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
# Static stuff

link1 = Link(np.pi/2)
link2 = Link(np.pi/2)

links = [link1, link2]

arm = Arm(links)


plt.show()
