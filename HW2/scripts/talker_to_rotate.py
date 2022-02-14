#!/usr/bin/env python
import rospy

from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + ' Heard %s', data.data)

def listen_and_talk(key, key2):
    rospy.init_node('talker_to_rotate', anonymous=True)   #find_object  rotate_robot

    #rospy.Subscriber(key, String, callback)        #listener key   camera

    pub = rospy.Publisher(key2, String, queue_size = 10)  #talker  key2  to rotate_robot debugger
    pub2 = rospy.Publisher(key, PoseStamped, queue_size = 10)
    rate = rospy.Rate(10)

    geometry = PoseStamped()

    while not rospy.is_shutdown():
        angle = input("Type your distance (degrees):")
        angle = str(angle)
        
        geometry.pose.position.x = int(input("x:"))
        geometry.pose.position.y = int(input("y:"))
        
        pub.publish(angle)
        pub2.publish(geometry)
        rate.sleep()


if __name__ == '__main__':
    listen_and_talk('multi', 'chats')

