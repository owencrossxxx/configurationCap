from numpy.core.fromnumeric import size

import time
import sys
import csv
import numpy as np
import math
import matplotlib.pyplot as plt
import datetime
import random
import pandas as pd
from itertools import zip_longest


from lib.tracker import Tracker

# Loop number
counter = 0
diameter = 28

x_value = []
y_value = []
z_value = []

namafile = 'data3D.csv'
header1 = "x_value"
header2 = "y_value"
header3 = "z_value"
fieldnames = [header1, header2, header3]

with open(namafile, 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

# with gui enabled
tracker1 = Tracker(gui=False,cam_index=2)
tracker1.addColorBlob("yellow1", r=255, g=255, b=0, r_min=140, r_max=255, g_min=140, g_max=255, b_min=0, b_max=100)
# tracker.setCroppingPoints(tl_x=20, tl_y=20, br_x=100, br_y=100) 
tracker1.setMorphologicalOperationParameters(dilation_size=12, erosion_size=2)

tracker2 = Tracker(gui=False,cam_index=4)
tracker2.addColorBlob("yellow2", r=255, g=255, b=0, r_min=140, r_max=255, g_min=140, g_max=255, b_min=0, b_max=100)
# tracker.setCroppingPoints(tl_x=20, tl_y=20, br_x=100, br_y=100) 
tracker2.setMorphologicalOperationParameters(dilation_size=12, erosion_size=2)


# while True:
while counter <10000:
    counter += 1
    tracker1.processCamera("yellow1")
    tracker1.updateVisualizations()

    tracker2.processCamera("yellow2")
    tracker2.updateVisualizations()

    points1 = np.asfarray(tracker1.getPoints("yellow1"))
    points2 = np.asfarray(tracker2.getPoints("yellow2"))


    if points1 == []:
        print("No marker detected by Cam1")

    if points2 == []:
        print("No marker detected by Cam2")

    # if point1.size  != point2.size:
    #     print("Not enough markers")
    #     break
    
    #print(point1,point2)
    #print(point1[:,1])

    
    if counter == 1:
        point1_original_y = np.min(points1[:,1])
        #point1_original_x = point1[np.where(np.min(point1[:,1]))[0],0][0]
        point1_original_x = points1[:,0]

        point2_original_y = np.min(points2[:,1])
        #point2_original_x = point2[np.where(np.min(point2[:,1]))[0],0][0]
        point2_original_x = points2[:,0]
        
        #scale
        sc = (np.max(points1[:,1])- np.min(points1[:,1]))/np.max(points2[:,1])- np.min(points2[:,1])
    
    if size(points1)+size(points2) > 2*size(points1):
        print("Too many markers detected")
        continue
    if size(points1)+size(points2) < 2*size(points1):
        print("Not enough markers detected")
        continue
    else:
        points1 = points1 - [0,point1_original_y]
        points2 = points2 - [0,point2_original_y]

        points1[:,0] = points1[:,0] - point1_original_x
        points2[:,0] = points2[:,0] - point2_original_x

        
        
        
        x_value = x_value+points1[:,0].tolist()
        y_value = y_value+points1[:,1].tolist()
        z_value = z_value+(points2[:,0]*sc).tolist()

        #Threshold


        #print(point1[:,0].tolist())
        #print(x_value)
        
        rows = [x_value,y_value,z_value]

        export_data = zip_longest(*rows, fillvalue = '')
        with open(namafile, 'w', encoding="ISO-8859-1", newline='') as myfile:
            wr = csv.writer(myfile)
            wr.writerow(("x", "y","z"))
            wr.writerows(export_data)
        #myfile.close()