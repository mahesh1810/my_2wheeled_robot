#! /usr/bin/env python

import rospy

from sensor_msgs.msg import LaserScan


def callback_laser(msg):
    regions = [
        min(min(msg.ranges[0:143]), 10),   #right region
        min(min(msg.ranges[144:287]), 10), #front right region
        min(min(msg.ranges[288:431]), 10), #front region
        min(min(msg.ranges[432:575]), 10), #front left region
        min(min(msg.ranges[576:713]), 10), #left region
    ]

def main():
    rospy.init_node('laser_reading')
    sub = rospy.Subscriber('/m2wr/laser/scan', LaserScan, callback_laser)
    rospy.spin()

if __name__ == '__main__':
    main()
