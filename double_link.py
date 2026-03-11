import matplotlib.pyplot as plt
import numpy as np


# to do:
# Make arm responsible for all joint states including angle
# Implement inverse kinematics with an animation showing the
# rm's mption toward new desired point
# TODO: Project Improvements
# 1. Structure
#    - Separate robot model, state, and visualization
#      - Model: store link lengths
#      - State: store joint angles and joint positions (coordinates)
#      - Methods: update_kinematics(), draw(ax)
#    - Avoid computing coordinates inside draw(); just read stored state
#    - Pass ax to draw() instead of using a global figure

# 2. Forward Kinematics
#    - Return joint positions as an array of [x, y] (not separate x and y arrays)
#    - Make get_components() stateless (return displacement only)
#    - Store end effector position for convenience

# 3. Animation
#    - Use plt.pause() to update frames
#    - Gradually increment joint angles per frame for smooth motion
#      - Example: angle += (target_angle - angle) * 0.1
#      - Think of it as “exponentially approaching” the target
#      - Add a small threshold to stop when difference is tiny
#    - Clear and redraw each frame inside a loop for smooth animation
#    - Optional: animate toward a moving target

# 4. Inverse Kinematics (2-link planar arm)
#    - Use analytical solution (cosine law and arctangent)
#    - Gradually update angles to reach the target for smooth motion
#    - Consider both elbow-up and elbow-down solutions

# 5. Optional Professional Improvements
#    - Store joint angles as a vector (theta = [θ1, θ2, ...])
#    - Structure code to scale to 3+ links for future Jacobian-based IK
#    - Prepare for trajectory planning or path following in the future


class Link():
    def __init__(self,length):
        self.length = length

class Arm():
    def __init__(self, links):
        self.links = links
        self.angles = np.zeros(len(self.links))

    def get_link_components(self,link,angle):
        return np.array([link.length*np.cos(angle), link.length*np.sin(angle)])

    def forward_kinematics(self):
        """Reads state of angles then calculates all joint positions"""
        cumulative_position = np.array([0, 0])
        cumulative_angle = 0
        
        #incrementor
        joint = 0

        joint_positions = [cumulative_position.copy()]

        for link in self.links:

            cumulative_angle += self.angles[joint]
            
            cumulative_position = cumulative_position + \
                self.get_link_components(link,cumulative_angle)
            
            joint_positions.append(cumulative_position.copy())

            joint+=1

        self.effector = cumulative_position

        return np.array(joint_positions)

    def draw(self, ax, coordinates):
        ax.plot(coordinates[:, 0], coordinates[:, 1], marker='o')
    
    def update_state(self, new_state):
        """Only function with the responsibility of chnaging joint angle state"""
        self.angles = new_state

    def animate(self, ax, duration, frames, new_state,rate=0.1):

        wait_time = duration/frames

        for frame in range(frames):

            ax.clear()
            ax.set_aspect('equal')
            ax.set_xlim(-10, 10)
            ax.set_ylim(-10, 10)

            if np.linalg.norm(new_state-self.angles)> 0.001:
                self.update_state(self.angles + ((new_state-self.angles)*rate))
            else:
                self.update_state(new_state)
            
            self.draw(ax, self.forward_kinematics())

            plt.pause(wait_time)
                



# Static stuff (Initialises plotting space and shit)
fig, ax = plt.subplots()
ax.set_aspect('equal')

ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
# Static stuff

link1 = Link(5)
link2 = Link(3)

links = [link1, link2]

arm = Arm(links)
coordinates = arm.forward_kinematics()
arm.animate(ax,10,1000,np.array([2,5]),0.1)


# plt.show()
