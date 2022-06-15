#!/usr/bin/env python
import torch
import importlib
import rospy
from cv_bridge import CvBridge, CvBridgeError
import message_filters
from sensor_msgs.msg import Image
from geometry_msgs.msg import TwistStamped

PATH = 'model1'

class NNRunner:

    def __init__(self):

        # create a ros node
        rospy.init_node("nn_runner", anonymous=True)

        # initialize image streams
        self.bridge = CvBridge()
        self.image_stream = message_filters.Subscriber("/camera/color/image_raw", Image, self.image_stream_callback)

        # initialize neural net
        self.model = torch.load(PATH)

        # initialize publishing command variables
        self.cmd_pub = rospy.Publisher('/husky_1/cmd_vel', TwistStamped, queue_size=10)
        self.forward_speed = 1000
        self.hz = 50
        self.now = rospy.get_rostime()

    def image_stream_callback(self, image_msg):
        try:
            # grab nn output from image stream
            cv_image = self.bridge.imgmsg_to_cv2(image_msg, "bgr8")
            model_out = self.model(torch.Tensor(cv_image)) # TODO: fix; needs to be converted to proper nn image format

            # publish to /husky_1/cmd_vel
            cmd = TwistStamped()
            cmd.twist.linear.x = self.forward_speed
            cmd.twist.angular.z = model_out
            cmd.header.stamp.secs = self.now.secs
            cmd.header.stamp.nsecs = self.now.nsecs
            self.cmd_pub.publish(cmd)
                                
        except CvBridgeError as e:
            print(e)
    
    def run(self):
        rate = rospy.Rate(self.hz)
        while not rospy.is_shutdown():
            rate.sleep()

if __name__ == '__main__':
    nn = NNRunner()
    nn.run()