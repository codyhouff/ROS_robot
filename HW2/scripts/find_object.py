#!/usr/bin/env python
import rospy
import roslib
from std_msgs.msg import String
from geometry_msgs.msg import Point
from sensor_msgs.msg import CompressedImage

import numpy as np
import cv2 as cv2
import sys, time

from matplotlib import pyplot as plt
import matplotlib.pyplot as plt
import os
#from matplotlib.colors import hsv_to_rgb
#from mpl_toolkits.mplot3d import axes3d
#from mpl_toolkits.mplot3d import Axes
from matplotlib import colors
i = 0

def turn_direction(temp_gray, x):
    temp_width = int(temp_gray.shape[1])
    img_center = 205
    center_padding = img_center*2*.08

    temp_width_center = x+temp_width/2

    #print("temp_width_center", temp_width_center)
    if(x == None):
        return 0, temp_width_center  #no turn
         
    if(temp_width_center>img_center+center_padding):
        return 5, temp_width_center #turn right
    elif(temp_width_center<img_center-center_padding):
        return -5, temp_width_center #turn left
    else:
        return 0, temp_width_center #no turn
    

def turn_degree(x, y):
    center_x = 410/2
    center_y = 308/2

    temp_x = float(x) - center_x
    turn_ang = temp_x/center_x*45

    return (turn_ang)


def diamond_finder(img, count):
    car_turn = 0
    img_center = 205
    temp_width_center = 0

    temp = cv2.imread("/home/burger/catkin_ws/src/ch_jm_object_follower/scripts/template.jpeg")
    #img = cv2.imread("/home/burger/catkin_ws/src/ch_jm_object_follower/scripts/input_imgs/test.jpg")
    
    #print('img %s' %type(img))
    #print('temp %s' %type(temp))

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    temp_gray = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)

    duplicate = False

    temp_gray = cv2.GaussianBlur(temp_gray,(5,5),cv2.BORDER_DEFAULT)
    img_gray = cv2.GaussianBlur(img_gray,(5,5),cv2.BORDER_DEFAULT)
          
    # resize 
    #temp_resized = cv2.resize(temp_gray, dim, None) 
    scale_percent = 80  # percent of original size
    width = int(temp.shape[1] * scale_percent / 100)
    height = int(temp.shape[0] * scale_percent / 100)
    dim = (width, height)
          
    # resize 
    temp_gray = cv2.resize(temp_gray, dim, interpolation = cv2.INTER_AREA)             

    w, h = temp_gray.shape[::-1]
    res = cv2.matchTemplate(img_gray,temp_gray,cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    #print("res: ",res)
    loc = np.where( res >= threshold)
        
        
    for pt in zip(*loc[::-1]):
    	box_x = pt[0] + w
        box_y = pt[1] + h
        point_x = pt[0]
        point_y = pt[1]
    	cv2.rectangle(img, pt, (box_x, box_y), (0,0,255), 1)    
        #point_array.append([point_x,point_y])
    	#print('point = %s %s' %(point_x,point_y))
        #car_degree = turn_degree(point_x, point_y)
        car_turn, temp_width_center = turn_direction(temp_gray,point_x)
        #print("car_turn",car_turn)
        #print('car degree %s' %car_degree)
        #pub.publish(str(car_degree))
        pub.publish(str(car_turn))
	break
    
    #print('no degree to turn')
    pub.publish(str(0))
    point_x = 0
    point_y = 0

    #cv2.imwrite("/home/burger/catkin_ws/src/ch_jm_object_follower/scripts/pictures/" + str(count)+"_" + str(img_center)+"_" + str(temp_width_center) +"_" +str(car_turn)+ ".jpeg",img)
    
def callback(ros_data):
    #time.sleep(2)
    global count
    global i
    count+=1
    i+=1
    np_arr = np.fromstring(ros_data.data,np.uint8)
    #print("image captured")
    cv_image = cv2.imdecode(np_arr,cv2.IMREAD_COLOR)
    #cv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if(i==5):
        diamond_finder(cv_image, count)
        i = 0

    #cv2.imwrite("/home/burger/catkin_ws/src/ch_jm_object_follower/scripts/pictures/"+str(count)+".jpeg",cv_image)
    #print("after dimond_finder")


rospy.init_node('find_object', anonymous=True)
#img_pub = rospy.Publisher("/output/pixels",Point,queue_size=10)
#print('subscriber')
img_sub = rospy.Subscriber("/raspicam_node/image/compressed",CompressedImage,callback, queue_size = 1)
pub = rospy.Publisher('chats', String, queue_size = 1)   # rotate_robot
rate = rospy.Rate(10)
count = 0

rospy.spin()
