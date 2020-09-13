'''
* Author List : Dhanajit kapali, Shubham kumar , Pankaj masiwal , Ritik verma
* Filename: task5-main.py
* Theme: Supply bot
* Functions: circle_detection , check_node_aruco , check_node_circle , angle_calculate , detect_Aruco , mark_Aruco , calculate_Robot_State 
* Global Variables: cap,CONSTANT,x_axis,y_axis,centre,frame1,node_circle,node_aruco,flag,flag1,x_axis1,yaxis1
* variables :ret,frame,img,
'''

import numpy as np
import cv2
import cv2.aruco as aruco
from aruco_lib import *
from circle_detection import *
from check_node_circle import *
from check_node_aruco import *
import time
import serial

cap = cv2.VideoCapture(0)  #variable to store frames from live video
CONSTANT = 1               #used as flag variable to trigger circle detection function
x_axis = 0                 #x axis of the detected circle in list
y_axis = 0                 #y axis of the detected circle in list 
x_axis_1 = 0               #x axis of the detected circle in numpy
y_axis_1 = 0               #y axis of the detected circle in numpy

centre = 0                 #center of the aruco detected
frame1 = 0                 #frame for the aruco detection
node_circle = 0            #contains node of the detected circle
node_aruco = 0             #contains node of the detected aruco
a =0                       #used to store the coordinates of the detected circle
b=0
flag = 0                   #used to control the no print of the node of circle
flag1 = 0
det_aruco_list = {}

while (True):
        ret,frame = cap.read()
        frame1 = frame
        cv2.imshow('raw video',frame)
        det_aruco_list = detect_Aruco(frame1)
        if(det_aruco_list):
                img = mark_Aruco(frame1,det_aruco_list)
                robot_state,centre = calculate_Robot_State(img,det_aruco_list)
        
        cv2.imshow('aruco',frame)
        if CONSTANT==1 :
                x_axis_1,y_axis_1=circle_detection(frame,CONSTANT)
        x_axis = x_axis_1.tolist()
        y_axis = y_axis_1.tolist()
        node_circle = check_node_circle(x_axis,y_axis)
        if flag1 ==0:
                print(" aid at:",node_circle)
                flag1 = flag1 +1
        
        node_aruco = check_node_aruco(centre)
                
        
        if flag ==0:
                if node_aruco!=None:
                        
                        flag = 1
                        print("bot at node",node_aruco)
        else:
                flag = 0
        ser = serial.Serial('COM4', 9600)  
        if node_circle == node_aruco:
                ser.write(b'0')
        if node_circle != node_aruco:
                ser.write(b'1')
        if node_aruco == 1:
                ser.write(b'5')
                                
        if cv2.waitKey(1) & 0xFF == ord('q'):
                break

cap.release()
cv2.destroyAllWindows()


'''
* Function Name: circle_detection
* Input: img ->numpy array of image , CONSTANT ->used as a flag variable
* Output: a,b ->numpy carrying center coordinates of the detected circle
* Logic: the image is converted to blurred grayscale image on which HoughCircle() is used to detect the circle
* Example Call: circle_detection(frame,CONSTANT)
'''
def circle_detection(img,CONSTANT):




    CONSTANT = CONSTANT +1
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Blur using 3 * 3 kernel.
    gray_blurred = cv2.blur(gray, (3, 3))
    # Apply Hough transform on the blurred image.
    detected_circles = cv2.HoughCircles(gray_blurred,
                                        cv2.HOUGH_GRADIENT, 1, 20, param1=50,
                                        param2=15, minRadius=1, maxRadius=10)

    if detected_circles is not None:
        # Convert the circle parameters a, b and r to integers.
        detected_circles = np.uint16(np.around(detected_circles))
    for pt in detected_circles[0, :]:
        if pt[1]!=216 or pt[1]!=217 or pt[1]!=218 :
            a, b, r = pt[0], pt[1], pt[2]
        
        
    cv2.imshow("circle detected", img)
    return a,b
    
'''
* Function Name: check_node_circle
* Input: x_axis ->int carrying x axis of the detected circle , y_axis ->int carrying y axis of the detected circle
* Output: node_circle ->int carrying position of the detected circle according to the nodes
* Logic: the node is calculated after dividing the arena in sectors
* Example Call: check_node_circle(x_axis,y_axis)
'''
def check_node_circle(x_axis,y_axis):
        if x_axis >335 and x_axis< 345 and y_axis >329 and y_axis <339:
            node_circle = 1
            return node_circle
        if x_axis >247 and x_axis <257 and y_axis >303 and y_axis <313:
            node_circle = 2
            return node_circle
        if x_axis >200 and x_axis <220 and y_axis >240 and y_axis <260:
            node_circle = 3
            return node_circle
        if x_axis >213 and x_axis <223 and y_axis >151 and y_axis <171:
            node_circle = 4
            return node_circle
        if x_axis >271 and x_axis <281 and y_axis >105 and y_axis <115:
            node_circle = 5
            return node_circle
        if x_axis >327 and x_axis <337 and y_axis >95 and y_axis <107:
            node_circle = 6
            return node_circle
        if x_axis >401 and x_axis <411 and y_axis >121 and y_axis <131:
            node_circle = 7
            return node_circle
        if x_axis >445 and x_axis <445 and y_axis >191 and y_axis <201:
            node_circle = 8
            return node_circle
        if x_axis >430 and x_axis <445 and y_axis >265 and y_axis <284:
            node_circle = 9
            return node_circle
            
'''
* Function Name: check_node_aruco
* Input: center ->list carrying x,y coordinates of the detected aruco 
* Output: node_aruco ->int carrying position of the detected aruco according to the nodes
* Logic: the node is calculated after dividing the arena in sectors
* Example Call: check_node_aruco(centre)
'''
def check_node_aruco(centre):
    for i in range (9):
        
        if centre[0]>333 and centre[0]<343 and centre[1]>384 and centre[1]<394:
            node_aruco = 1
            return node_aruco

        if centre[0]>215 and centre[0]<225 and centre[1]>350 and centre[1]<358:
            node_aruco = 2
            return node_aruco

        if centre[0]>143 and centre[0]<160 and centre[1]>255 and centre[1]<270:
            node_aruco = 3
            return node_aruco

        if centre[0]>150 and centre[0]<170 and centre[1]>125 and centre[1]<147:
            node_aruco = 4
            return node_aruco

        if centre[0]>232 and centre[0]<247 and centre[1]>50 and centre[1]<70:
            node_aruco = 5
            return node_aruco

        if centre[0]>332 and centre[0]<342 and centre[1]>36 and centre[1]<46:
            node_aruco = 6
            return node_aruco

        if centre[0]>445 and centre[0]<465 and centre[1]>70 and centre[1]<90:
            node_aruco = 7
            return node_aruco

        if centre[0]>506 and centre[0]<520 and centre[1]>183 and centre[1]<193:
            node_aruco = 8
            return node_aruco

        if centre[0]>470 and centre[0]<490 and centre[1]>310 and centre[1]<325:
            node_aruco = 9
            return node_aruco

'''
* Function Name: angle_calculate
* Input: pt1,pt2,trigger -> it contans the coordinates of the detected aruco
* Output: angle ->int carrying angle
* Logic: the angle is calculated of the aruco measuring the corners of it
* Example Call: angle_calculate(pt1, pt2)
'''        
def angle_calculate(pt1,pt2, trigger = 0):  # function which returns angle between two points in the range of 0-359
    angle_list_1 = list(range(359,0,-1))
    #angle_list_1 = angle_list_1[90:] + angle_list_1[:90]
    angle_list_2 = list(range(359,0,-1))
    angle_list_2 = angle_list_2[-90:] + angle_list_2[:-90]
    x=pt2[0]-pt1[0] # unpacking tuple
    y=pt2[1]-pt1[1]
    angle=int(math.degrees(math.atan2(y,x))) #takes 2 points nad give angle with respect to horizontal axis in range(-180,180)
    if trigger == 0:
        angle = angle_list_2[angle]
    else:
        angle = angle_list_1[angle]
    return int(angle)

'''
* Function Name: detect_Aruco
* Input: img -> numpy carrying image details
* Output: angle ->list
* Logic: the aruco is detected using aruco_dict
* Example Call: detect_Aruco(frame1)
'''        
def detect_Aruco(img):  #returns the detected aruco list dictionary with id: corners
    aruco_list = {}
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_50)   #creating aruco_dict with 5x5 bits with max 250 ids..so ids ranges from 0-249
    parameters = aruco.DetectorParameters_create()  #refer opencv page for clarification
    #lists of ids and the corners beloning to each id
    corners, ids, _ = aruco.detectMarkers(gray, aruco_dict, parameters = parameters)
    #corners is the list of corners(numpy array) of the detected markers. For each marker, its four corners are returned in their original order (which is clockwise starting with top left). So, the first corner is the top left corner, followed by the top right, bottom right and bottom left.
    # print len(corners), corners, ids
    gray = aruco.drawDetectedMarkers(gray, corners,ids)
    # cv2.imshow('frame',gray)
    #print (type(corners[0]))
    if len(corners):    #returns no of arucos
        #print (len(corners))
        #print (len(ids))
        for k in range(len(corners)):
            temp_1 = corners[k]
            temp_1 = temp_1[0]
            temp_2 = ids[k]
            temp_2 = temp_2[0]
            aruco_list[temp_2] = temp_1
        return aruco_list

'''
* Function Name: mark_Aruco
* Input: img -> numpy carrying image details, aruco_list
* Output: img ->image marked with aruco no
* Logic: the aruco is mark using aruco_dict
* Example Call: mark_Aruco(frame1,det_aruco_list)
'''        
def mark_Aruco(img, aruco_list):    #function to mark the centre and display the id
    key_list = aruco_list.keys()
    font = cv2.FONT_HERSHEY_SIMPLEX
    for key in key_list:
        dict_entry = aruco_list[key]    #dict_entry is a numpy array with shape (4,2)
        centre = dict_entry[0] + dict_entry[1] + dict_entry[2] + dict_entry[3]#so being numpy array, addition is not list addition
        centre[:] = [int(x / 4) for x in centre]    #finding the centre
        #print centre
        orient_centre = centre + [0.0,5.0]
        #print orient_centre
        centre = tuple(centre)  
        orient_centre = tuple((dict_entry[0]+dict_entry[1])/2)
        #print centre
        #print orient_centre
        cv2.circle(img,centre,1,(0,0,255),8)
        cv2.circle(img,tuple(dict_entry[0]),1,(0,0,255),8)
        cv2.circle(img,tuple(dict_entry[1]),1,(0,255,0),8)
        cv2.circle(img,tuple(dict_entry[2]),1,(255,0,0),8)
        cv2.circle(img,orient_centre,1,(0,0,255),8)
        cv2.line(img,centre,orient_centre,(255,0,0),4) #marking the centre of aruco
        cv2.putText(img, str(key), (int(centre[0] + 20), int(centre[1])), font, 1, (0,0,255), 2, cv2.LINE_AA) # displaying the idno
    return img


'''
* Function Name: calculate_Robot_State
* Input: img -> numpy carrying image details, aruco_list
* Output: robot_state , centre
* Logic: the aruco state is calculated using aruco_dict
* Example Call: calculate_Robot_State(img,det_aruco_list)
'''        
def calculate_Robot_State(img,aruco_list):  #gives the state of the bot (centre(x), centre(y), angle)
    robot_state = {}
    key_list = aruco_list.keys()
    font = cv2.FONT_HERSHEY_SIMPLEX

    for key in key_list:
        dict_entry = aruco_list[key]
        pt1 , pt2 = tuple(dict_entry[0]) , tuple(dict_entry[1])
        centre = dict_entry[0] + dict_entry[1] + dict_entry[2] + dict_entry[3]
        centre[:] = [int(x / 4) for x in centre]
        centre = tuple(centre)
        #print centre
        angle = angle_calculate(pt1, pt2)
        cv2.putText(img, str(angle), (int(centre[0] - 80), int(centre[1])), font, 1, (0,0,255), 2, cv2.LINE_AA)
        robot_state[key] = [key, int(centre[0]), int(centre[1]), angle]#HOWEVER IF YOU ARE SCALING IMAGE AND ALL...THEN BETTER INVERT X AND Y...COZ THEN ONLY THE RATIO BECOMES SAME
    #print (robot_state)

    return robot_state,centre
    
'''
det_aruco_list = {}
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    det_aruco_list=detect_Aruco(frame)
    img = mark_Aruco(frame,det_aruco_list)
    robot_state=calculate_Robot_State(img,det_aruco_list)
    print robot_state

    cv2.imshow('image',img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
 
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
'''


