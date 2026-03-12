import matplotlib.pyplot as plt
import numpy as np

last_click = np.array([1,1])


# to do:
#  click to move inverse kinematics

def onclick(event):
    global last_click
    if event.xdata is not None and event.ydata is not None:
        last_click = np.array([event.xdata, event.ydata])
        print(f'x={event.xdata:.2f}, y={event.ydata:.2f}')
        plt.plot(event.xdata, event.ydata, 'ro') # Plot point
        plt.draw() # Update figure
    
    new_angles = arm.inverse_kinematics_2link(last_click)
    arm.animate(ax, 10, 1000, new_angles, last_click)
    plt.draw()



class Link():
    def __init__(self,length):
        self.length = length

class Arm():
    def __init__(self, links):
        self.links = links
        self.angles = np.zeros(len(self.links))
        self.arm_length = 0
        # Static points shouldn't be arms responsibility, this is temporary
        self.static_points = []

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

            ax.plot([static_point[0]], [static_point[1]], 'o', color = 'green' )

            self.static_points.append(static_point)

            plt.pause(wait_time)
                
    def inverse_kinematics_2link(self,target_pos):
        """Eventually you will move the arm by an angle to give it a partiicular end effector position"""
        absolute_distance_squared =  target_pos[0]**2 + target_pos[1]**2 

        cos_theta2 = (
            absolute_distance_squared
            - self.links[0].length**2
            - self.links[1].length**2
        )/(2*self.links[0].length*self.links[1].length)

        cos_theta2 = np.clip(cos_theta2,-1,1)

        theta2 = np.arccos(cos_theta2)

        k1 = self.links[0].length + (self.links[1].length*np.cos(theta2))
        k2 = self.links[1].length*np.sin(theta2)

        theta1 = np.arctan2(target_pos[1],target_pos[0]) - np.arctan2(k2,k1) 

        target_angles = np.array([theta1,theta2])

        return target_angles

    def click_IK(self,ax):
        """This will let you select a point on the axes click it and the arm will inverse kinematics its way there."""
        self.draw(ax, self.forward_kinematics())
        new_angles = self.inverse_kinematics_2link(last_click)
        self.animate(ax, 10,1000, new_angles, last_click, 0.1)



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
new_angles = arm.inverse_kinematics_2link( goal)
# arm.animate(ax, 10, 1000, new_angles, static_point=goal)


arm.draw(ax,np.array([[0,0],[arm.links[0].length,0],[arm.links[0].length + arm.links[1].length,0]]))
cid = fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()
