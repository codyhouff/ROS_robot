#!/usr/bin/env python
import rospy
import roslib
from std_msgs.msg import String
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist

import numpy as np
import cv2 as cv2
import sys, time
#from scipy.ndimage import filters
from cv_bridge import CvBridge, CvBridgeError

def callback(msg):
    


def listen_and_talk(key, key2):
    rospy.init_node('find', anonymous=True)
    ros_data = rospy.Subscriber("/raspicam_node/image/compressed",Image,callback)



