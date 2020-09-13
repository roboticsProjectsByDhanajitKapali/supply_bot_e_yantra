###############################################################################
## Author: Team Supply Bot
## Edition: eYRC 2019-20
## Instructions: Do Not modify the basic skeletal structure of given APIs!!!
###############################################################################


######################
## Essential libraries
######################
import cv2
import numpy as np
import os
import math
import csv
import cv2.aruco as aruco
from aruco_lib import *
import copy



########################################################################
## using os to generalise Input-Output
########################################################################
codes_folder_path = os.path.abspath('.')
images_folder_path = os.path.abspath(os.path.join('..', 'Videos'))
generated_folder_path = os.path.abspath(os.path.join('..', 'Generated'))




############################################
## Build your algorithm in this function
## ip_image: is the array of the input image
## imshow helps you view that you have loaded
## the corresponding image
############################################
def process(ip_image):
    ###########################
    ## Your Code goes here

    #contast setting code
    img = ip_image

    b = img[:, :, 0]
    g = img[:, :, 1]
    r = img[:, :, 2]


    max_b = b.max()
    max_g = g.max()
    max_r = r.max()

    min_b = b.min()
    min_g = g.min()
    min_r = r.min()

    mb = 255 / (max_b - min_b)
    mg = 255 / (max_g - min_g)
    mr = 255 / (max_r - min_r)

    cb = 255 - mb * max_b
    cg = 255 - mg * max_g
    cr = 255 - mr * max_r

    img[:, :, 0] = mb * img[:, :, 0] + cb
    img[:, :, 1] = mg * img[:, :, 1] + cg
    img[:, :, 2] = mr * img[:, :, 2] + cr

  
    #  blurr removal code

    kernel_sharpening = np.array([[-1, -1, -1],
                                  [-1, 9.6, -1],
                                  [-1, -1, -1]])
    sharpened = cv2.filter2D(img, -1, kernel_sharpening)
  
    v = detect_Aruco(sharpened)
    print(v)
    
    id_list = []
    ###########################
    id_list.append(25)
    id_list.append(128)
    id_list.append(128)
    id_list.append(128)

    

    return ip_image, id_list


    
####################################################################
## The main program which provides read in input of one image at a
## time to process function in which you will code your generalized
## output computing code
## Do not modify this code!!!
####################################################################
def main(val):
    ################################################################
    ## variable declarations
    ################################################################
    i = 1
    ## reading in video 
    cap = cv2.VideoCapture(images_folder_path+"/"+"ArUco_bot.mp4")
    ## getting the frames per second value of input video
    fps = cap.get(cv2.CAP_PROP_FPS)
    ## getting the frame sequence
    frame_seq = int(val)*fps
    ## setting the video counter to frame sequence
    cap.set(1,frame_seq)
    ## reading in the frame
    ret, frame = cap.read()
    ## verifying frame has content
    print(frame.shape)
    ## display to see if the frame is correct
    cv2.imshow("window", frame)
    cv2.waitKey(0);
    ## calling the algorithm function
    op_image, aruco_info = process(frame)
    ## saving the output in  a list variable
    line = [str(i), "Aruco_bot.jpg" , str(aruco_info[0]), str(aruco_info[3])]
    ## incrementing counter variable
    i+=1
    ## verifying all data
    print(line)
    ## writing to angles.csv in Generated folder without spaces
    with open(generated_folder_path+"/"+'output.csv', 'w') as writeFile:
        print("About to write csv")
        writer = csv.writer(writeFile)
        writer.writerow(line)
    ## closing csv file    
    writeFile.close()



    

############################################################################################
## main function
############################################################################################
if __name__ == '__main__':
    main(input("time value in seconds:"))
