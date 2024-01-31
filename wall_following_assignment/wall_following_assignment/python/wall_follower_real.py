#!/usr/bin/env python
import rospy
from std_msgs.msg import String, Header, Float32
from ackermann_msgs.msg import AckermannDriveStamped
from sensor_msgs.msg import LaserScan
from dynamic_reconfigure.server import Server
from wall_following_assignment.cfg import WallFollowerConfig
from math import isnan

import matplotlib.pyplot as plt

class PID:
    def __init__(self, Kp, Td, Ti, dt):
        self.Kp = Kp
        self.Td = Td
        self.Ti = Ti
        self.curr_error = 0
        self.prev_error = 0
        self.sum_error = 0
        self.prev_error_deriv = 0
        self.curr_error_deriv = 0
        self.control = 0
        self.dt = dt

    def update_control(self, current_error, reset_prev=False):
        #todo: implement this
        #self.control = ?
        self.clip_control()#clip control signal based on actuator limits

    def clip_control(self, min=-0.340000003576, max=0.340000003576): 
        if self.control < min: 
            self.control = min 
        if self.control > max: 
            self.control = max 

    def get_control(self):
        return self.control


class WallFollowerRaceCar:
    def __init__(self):
        rospy.init_node('wall_follower_racecar', anonymous=True)
               
        self.forward_speed = rospy.get_param("~forward_speed")
        self.desired_distance_from_wall = rospy.get_param("~desired_distance_from_wall")
        self.hz = 50

        # todo: set up the command publisher to publish at topic '/ackermann_cmd'
        # using ackermann_msgs.AckermannDriveStamped messages
        # self.cmd_pub = ?

        # todo: set up the laser scan subscriber to subscribe to topic '/scan_filtered' this already as only the left side of the LIDAR sweep. 
        # this will set up a callback function that gets executed
        # upon each spinOnce() call, as long as a laser scan
        # message has been published in the meantime by another node
        # self.laser_sub = ??


    def laser_scan_callback(self, msg):
        # todo: implement this        
        # Populate this command based on the distance to the closest
        # object in laser scan. I.e. compute the cross-track error
        # as mentioned in the PID slides.

        # You can populate the command based on either of the following two methods:
        # (1) using only the distance to the closest wall
        # (2) using the distance to the closest wall and the orientation of the wall
        #
        # If you select option 2, you might want to use cascading PID control.

        # cmd.drive.steering_angle = ? 



    def run(self):
        rate = rospy.Rate(self.hz)
        while not rospy.is_shutdown():
            rate.sleep()



if __name__ == '__main__':
    wfh = WallFollowerRaceCar()
    wfh.run()
