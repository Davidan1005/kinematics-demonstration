import matplotlib.pyplot as plt
import numpy as np


# to do:
# Implement inverse kinematics with an animation showing the
# rm's mption toward new desired point
# 1. Structure
#    - Separate robot model, state, and visualization
#      - Model: store link lengths
#      - State: store joint angles and joint positions (coordinates)
#      - Methods: update_kinematics(), draw(ax)
#    - Avoid computing coordinates inside draw(); just read stored state
#    - Pass ax to draw() instead of using a global figure


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
        self.arm_length = 0

        for link in links:
            self.arm_length+=link.length

    def get_link_components(self,link,angle):
        return np.array([link.length*np.cos(angle), link.length*np.sin(angle)])

    def show_arm_range(self,ax):
        range = plt.Circle((0,0),self.arm_length, color='red', alpha=0.5)
        ax.add_patch(range)

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
        self.show_arm_range(ax)
    
    def update_state(self, new_state):
        """Only function with the responsibility of chnaging joint angle state"""
        self.angles = new_state

    def animate(self, ax, duration, frames,  new_state, static_point= np.array([0,0]), rate=0.1):

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

            ax.plot([static_point[0]], [static_point[1]], 'o')

            plt.pause(wait_time)
                
    def inverse_kinematics_2link(self,ax,target_pos):
        """Eventually you will move the arm by an angle to give it a partiicular end effector position"""
        absolute_distance_squared =  target_pos[0]**2 + target_pos[1]**2 

        theta2 = np.arccos( (absolute_distance_squared - self.links[0].length**2 - self.links[1].length**2)/(2*self.links[0].length*self.links[1].length))

        k1 = self.links[0].length + (self.links[1].length*np.cos(theta2))
        k2 = self.links[1].length*np.sin(theta2)

        theta1 = np.arctan2(target_pos[1],target_pos[0]) - np.arctan2(k2,k1) 

        target_angles = np.array([theta1,theta2])

        return target_angles

    


# Static stuff (Initialises plotting space and shit)
fig, ax = plt.subplots()
ax.set_aspect('equal')

ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
# Static stuff

# Initialise objects
link1 = Link(4)
link2 = Link(3)

links = [link1, link2]

arm = Arm(links)
# Initialise objects

goal = np.array([-2,-3])
new_angles = arm.inverse_kinematics_2link(ax, goal)
arm.animate(ax, 10, 1000, new_angles, static_point=goal)


# plt.show()
