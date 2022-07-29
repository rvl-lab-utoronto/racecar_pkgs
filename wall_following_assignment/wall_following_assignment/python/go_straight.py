#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
from ackermann_msgs.msg import AckermannDriveStamped    

def talker():
    pub = rospy.Publisher('/ackermann_cmd', AckermannDriveStamped, queue_size=1)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(50) # 10hz
    start = None
    while not rospy.is_shutdown():
        if start==None:
            a = input("Press Enter to continue...")
            start = rospy.get_time()
            print("start", start)
        else: 
            now = rospy.get_time()
            #print(now)
            if now - start < 3.0: 
                cmd = AckermannDriveStamped()
                cmd.header.stamp = rospy.get_rostime()
                cmd.drive.speed = 1.25
                cmd.drive.acceleration=0.0
                pub.publish(cmd)
            else: 
                print("current time: ", (now - start))
                exit()




if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
