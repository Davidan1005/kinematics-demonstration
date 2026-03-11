import matplotlib.pyplot as plt
import numpy as np


# to do

class Link():
    def __init__(self,angle=0):
        self.length = 3
        self.angle = angle

        
    def get_components(self,absolute_angle):
        return np.array([
            (self.length*np.cos(absolute_angle)),
            (self.length*np.sin(absolute_angle))
        ])
        




class Arm():

    def __init__(self, links):
        self.links = links

    def forward_kinematics(self):
        cumulative_position = np.array([0, 0])
        cumulative_angle = 0

        joint_positions = [cumulative_position.copy()]

        for link in self.links:
            cumulative_angle += link.angle
            cumulative_position = cumulative_position + link.get_components(cumulative_angle)

            joint_positions.append(cumulative_position.copy())

    

        return np.array(joint_positions) 

    def draw(self,ax, coordinates):
        ax.plot(coordinates[:,0],coordinates[:,1], marker='o')
            

# Static stuff (Initialises plotting space and shit)
fig, ax = plt.subplots()
ax.set_aspect('equal')

ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
# Static stuff

link1 = Link(np.pi/6)
link2 = Link(np.pi/2)

links = [link1, link2]

arm = Arm(links)
coordinates = arm.forward_kinematics()
arm.draw(ax,coordinates)


plt.show()
