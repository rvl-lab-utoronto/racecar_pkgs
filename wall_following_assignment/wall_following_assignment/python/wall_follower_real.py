#!/usr/bin/env python
import rospy
from std_msgs.msg import String, Header, Float32
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from dynamic_reconfigure.server import Server
from wall_following_assignment.cfg import WallFollowerConfig
from math import isnan

from ackermann_msgs.msg import AckermannDriveStamped


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
        self.prev_error = self.curr_error
        self.curr_error = current_error
        self.prev_error_deriv = self.curr_error_deriv
        self.curr_error_deriv = (self.curr_error - self.prev_error) / self.dt
        self.sum_error = self.sum_error + self.curr_error

        self.control = self.Kp * self.curr_error + self.Td * self.curr_error_deriv + self.Ti * self.sum_error
        self.clip_control()

    def clip_control(self, min=-0.340000003576, max=0.340000003576): 
        if self.control < min: 
            self.control = min 
        if self.control > max: 
            self.control = max 

    def get_control(self):
        return self.control


class WallFollowerHusky:
    def __init__(self):
        rospy.init_node('wall_follower_husky', anonymous=True)

        self.forward_speed = rospy.get_param("~forward_speed")
        self.desired_distance_from_wall = rospy.get_param("~desired_distance_from_wall")
        self.hz = 50

        # using geometry_msgs.Twist messages
        self.cmd_pub = rospy.Publisher('/ackermann_cmd', AckermannDriveStamped, queue_size=10)

        # this will set up a callback function that gets executed
        # upon each spinOnce() call, as long as a laser scan
        # message has been published in the meantime by another node
        self.laser_sub = rospy.Subscriber("/scan_filtered", LaserScan, self.laser_scan_callback)
        self.cte_pub = rospy.Publisher('/cte', Float32, queue_size=1)

        self.pid_controller = PID(0.06, 0.61, 0., 1. / self.hz)
        self.reconfigure_server = Server(WallFollowerConfig, self.configure_callback)

    def laser_scan_callback(self, msg):
        # Populate this command based on the distance to the closest
        # object in laser scan. I.e. compute the cross-track error
        # as mentioned in the PID slides.
        
        #filter out only left wall points 
        current_error = min(filter(lambda x: not isnan(x), msg.ranges)) - self.desired_distance_from_wall
        self.cte_pub.publish(current_error)

        # You can populate the command based on either of the following two methods:
        # (1) using only the distance to the closest wall
        # (2) using the distance to the closest wall and the orientation of the wall
        #
        # If you select option 2, you might want to use cascading PID control.
        self.pid_controller.update_control(current_error)
        cmd = AckermannDriveStamped()
        cmd.header.stamp = rospy.get_rostime()
        cmd.drive.speed = self.forward_speed
        cmd.drive.steering_angle = self.pid_controller.get_control()
        self.cmd_pub.publish(cmd)

    def configure_callback(self, config, level):
        self.pid_controller.Kp = config['Kp']
        self.pid_controller.Td = config['Td']
        self.pid_controller.Ti = config['Ti']
        return config

    def run(self):
        rate = rospy.Rate(self.hz)
        while not rospy.is_shutdown():
            rate.sleep()


if __name__ == '__main__':
    wfh = WallFollowerHusky()
    wfh.run()
