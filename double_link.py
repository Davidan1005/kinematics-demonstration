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

# 6. Performance & Style
#    - Avoid np.append() in loops; use lists + np.array at the end
#    - Prefer NumPy arrays for slicing and vector math over Python lists
#    - Keep a clear separation of responsibilities: computation vs drawing vs state

class Link():
    def __init__(self, angle=0):
        self.length = 3
        self.angle = angle

    def get_components(self, absolute_angle):
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
            cumulative_position = cumulative_position + \
                link.get_components(cumulative_angle)

            joint_positions.append(cumulative_position.copy())

        return np.array(joint_positions)

    def draw(self, ax, coordinates):
        ax.plot(coordinates[:, 0], coordinates[:, 1], marker='o')


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
arm.draw(ax, coordinates)


plt.show()
