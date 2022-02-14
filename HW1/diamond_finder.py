import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import os
from matplotlib.colors import hsv_to_rgb
from mpl_toolkits.mplot3d import axes3d
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib import colors

input_folder = 'input_imgs'
output_folder = './output_imgs'
if (os.path.isdir(output_folder) == False): 
    os.mkdir(output_folder)

temp = cv.imread('template.jpg')
temp_hsv=cv.cvtColor(temp, cv.COLOR_BGR2HSV)
#temp_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
temp_gray = cv.cvtColor(temp, cv.COLOR_BGR2GRAY)

dictionary = {}
dict_array = []
#array_add = []
point_array = []
duplicate = False

for filename in sorted(os.listdir(input_folder)):
    img = cv.imread(os.path.join(input_folder,filename))

    img_hsv=cv.cvtColor(img, cv.COLOR_BGR2HSV)

    # broad mask (no black)
    lower_red = np.array([0,0,50]) #([4,0,55]) 
    upper_red = np.array([185,190,190]) #([75,40,190])
    mask3 = cv.inRange(img_hsv, lower_red, upper_red)

    # join my masks
    broad_mask = mask3

    # set my output img to zero everywhere except my mask
    broad_img = img.copy()
    broad_img[np.where(broad_mask==0)] = [133,123,121]
    
    #cv.waitKey()
    img_gray = cv.cvtColor(broad_img, cv.COLOR_BGR2GRAY)

    img_blur = cv.GaussianBlur(img_gray,(5,5),cv.BORDER_DEFAULT)
    
    for temp_size in range(15,100,10):
        scale_percent = temp_size # percent of original size
        width = int(temp.shape[1] * scale_percent / 100)
        height = int(temp.shape[0] * scale_percent / 100)
        dim = (width, height)
          
        # resize 
        temp_resized = cv.resize(temp_gray, dim, interpolation = cv.INTER_AREA) 
            

        w, h = temp_resized.shape[::-1]
        res = cv.matchTemplate(img_gray,temp_resized,cv.TM_CCOEFF_NORMED)
        threshold = 0.9
        loc = np.where( res >= threshold)
        
        
        for pt in zip(*loc[::-1]):
            box_x = pt[0] + w
            box_y = pt[1] + h
            point_x = pt[0]
            point_y = pt[1]
            
            #check for doublicate boxes for the same diamond
            padding = 8     #setting the boundary for duplicate detection, +-8 pixels on both x and y
            for xy_point in point_array:
                prev_x_point, prev_y_point = xy_point
                if ((abs(point_x-prev_x_point)<padding) and (abs(point_y-prev_y_point)<padding)): #check for dublicates within x,y padding area
                    duplicate = True
            if(duplicate == False):
                cv.rectangle(img, pt, (box_x, box_y), (0,0,255), 1)    

                point_array.append([point_x,point_y])
                print([filename, point_x,point_y])
                dict_array.append([point_x,point_y])

            duplicate = False
    point_array = []
    #if (dict_array != []):
        #dictionary[filename] = dict_array
    dictionary[filename] = dict_array
    dict_array = []
    cv.imwrite('./'+output_folder+'/'+filename,img)
          
print(dictionary)
