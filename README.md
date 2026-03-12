**Kinematics Simulator**

This project started as a personal experiment to apply forward and inverse kinematics. Initially, it simulated a single-link manipulator in Python using Matplotlib. As my knowledge advanced, it was extended to 2-link robotic arms in 2D, implementing both forward and inverse kinematics for real-time simulation.


**Features:**

2D Multi-Link Arm Simulation: Supports one or two links.

Forward Kinematics: Calculate end-effector position from joint angles.

Inverse Kinematics: Compute joint angles for a desired end-effector position.

Interactive Plot: Click to move the arm’s end-effector in real time.

Smooth Animation: Gradually moves toward the target position.

Modular Code: Easy to extend with more links or control logic.


**Usage:**

Run the main simulation script:

python double_link.py

Click anywhere in the Matplotlib window to move the end-effector.

Console outputs show the current joint angles and end-effector coordinates.


**How It Works:**

Forward Kinematics: Computes end-effector (x, y) from joint angles and link lengths.

Inverse Kinematics: Uses trigonometry (law of cosines, arctan2) to solve joint angles for a target position.

Animation: Updates the arm in real-time, smoothly moving toward the clicked target.


**Future Improvements:**

Extend to 3 or more links in 2D or 3D.

Add trajectory planning for smoother motion.

Implement obstacle detection and collision avoidance.

Create a GUI with sliders for manual joint control.


**References:**

Robotics Toolbox for Python

Introduction to Robotics: Mechanics and Control – John J. Craig
