#! /usr/bin/env python

# import ros stuff
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

#initialize states and variables
pub_ = None
regions_ = {'right': 0,'fright': 0,'front': 0,'fleft': 0,'left': 0}
state_ = 0
state_dict_ = {
    0: 'finding the wall',
    1: 'turning left',
    2: 'following the wall',
}

def callback_laser(msg):
    regions = [
        min(min(msg.ranges[0:143]), 10),   #right region
        min(min(msg.ranges[144:287]), 10), #front right region
        min(min(msg.ranges[288:431]), 10), #front region
        min(min(msg.ranges[432:575]), 10), #front left region
        min(min(msg.ranges[576:713]), 10), #left region
    ]
    take_action()


def change_state(state):
    global state_, state_dict_
    if state is not state_:
        print 'Wall follower - [%s] - %s' % (state, state_dict_[state])
        state_ = state

def take_action():
    global regions_
    regions = regions_
    msg = Twist()
    linear_x = 0
    angular_z = 0
    dist = 1
    state_status = ''
    if regions['front'] > dist and regions['fleft'] > dist and regions['fright'] > dist:
        state_status = 'case 1 - nothing'
        change_state(0)
    elif regions['front'] < dist and regions['fleft'] > dist and regions['fright'] > dist:
        state_status = 'case 2 - front'
        change_state(1)
    elif regions['front'] > dist and regions['fleft'] > dist and regions['fright'] < dist:
        state_status = 'case 3 - fright'
        change_state(2)
    elif regions['front'] > dist and regions['fleft'] < dist and regions['fright'] > dist:
        state_status = 'case 4 - fleft'
        change_state(0)
    elif regions['front'] < dist and regions['fleft'] > dist and regions['fright'] < dist:
        state_status = 'case 5 - front and fright'
        change_state(1)
    elif regions['front'] < dist and regions['fleft'] < dist and regions['fright'] > dist:
        state_status = 'case 6 - front and fleft'
        change_state(1)
    elif regions['front'] < dist and regions['fleft'] < dist and regions['fright'] < dist:
        state_status = 'case 7 - front and fleft and fright'
        change_state(1)
    elif regions['front'] > dist and regions['fleft'] < dist and regions['fright'] < dist:
        state_status = 'case 8 - fleft and fright'
        change_state(0)
    else:
        state_status = 'error in case'


def find_wall():
    msg = Twist()
    msg.linear.x = 0.2
    msg.angular.z = -0.3
    return msg

def turn_left():
    msg = Twist()
    msg.angular.z = 0.3
    return msg

def follow_the_wall():
    global regions_
    msg = Twist()
    msg.linear.x = 0.5
    return msg

def main():
    global pub_
    rospy.init_node('laser_reading')
    pub_ = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    sub = rospy.Subscriber('/m2wr/laser/scan', LaserScan, callback_laser)
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        msg = Twist()
        if state_ == 0:
            msg = find_wall()
        elif state_ == 1:
            msg = turn_left()
        elif state_ == 2:
            msg = follow_the_wall()
            pass
        else:
            rospy.logerr('state error!')
        pub_.publish(msg)
        rate.sleep()

if __name__ == '__main__':
    main()
