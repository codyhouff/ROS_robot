#!/usr/bin/env python
import rospy

from std_msgs.msg import String
from geometry_msgs.msg import Twist

angle = 0

def callback(msg):
    #print('I am rotate_robot: %s' %msg.data)
    global angle
    angle = float(msg.data)
    move = Twist()
    
    move.linear.x = 0
    move.linear.y = 0
    move.linear.z = 0
    move.angular.x = 0
    move.angular.y = 0
    speed = 20
    
    #print('angle %d' %angle)
    if angle > 0:
    	relative_angle = -angle*2*3.1415/360
    	angular_speed = -speed*2*3.1415/360
    else:
    	relative_angle = -angle*2*3.1415/360
    	angular_speed = speed*2*3.1415/360
    	
    move.angular.z = angular_speed
    t0 = rospy.Time.now().to_sec()
    current_angle = 0

    while (abs(current_angle) < abs(relative_angle)):
        pub.publish(move)
        t1 = rospy.Time.now().to_sec()
        current_angle = abs(angular_speed)*(t1-t0)

    #force robot to stop
    angle = 0
    move.angular.z = 0
    pub.publish(move)
    
def listen_and_talk(key, key2):
    rospy.init_node('rotate_robot', anonymous=True)   #find_object  rotate_robot

    sub = rospy.Subscriber(key, String, callback)       #listener key   camera

    #print("publishing")
    global pub
    pub = rospy.Publisher(key2, Twist, queue_size=5)  #talker  key2  to rotate_robot debugger
    #print("published")

    rate = rospy.Rate(10)
	
    move = Twist()

    move.linear.x = 0
    move.linear.y = 0
    move.linear.z = 0
    move.angular.x = 0
    move.angular.y = 0

    angle = 0
    speed = 100
    #print("Let's rotate your robot")
    #speed = input("Input your speed (degrees/sec):")
    #angle = input("Type your distance (degrees):")
    #relative_angle = angle*2*3.1415/360
    print('start')
    if angle > 0:
    	relative_angle = angle*2*3.1415/360
    	angular_speed = speed*2*3.1415/360
    else:
    	relative_angle = angle*2*3.1415/360
    	angular_speed = -speed*2*3.1415/360
    	
    move.angular.z = angular_speed
    t0 = rospy.Time.now().to_sec()
    current_angle = 0

    while (current_angle < relative_angle):
        pub.publish(move)
        t1 = rospy.Time.now().to_sec()
        current_angle = angular_speed*(t1-t0)

    #force robot to stop 
    angle = 0
    move.angular.z = 0
    pub.publish(move)
    rospy.spin()



if __name__ == '__main__':
    try:
        listen_and_talk('chats','/cmd_vel')   #find_object should talk with 'chats'
    except ROSInterruptException:
        pass
