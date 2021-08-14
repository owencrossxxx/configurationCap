from numpy.core.fromnumeric import size

import time
import sys
import csv
import numpy as np
import math
import matplotlib.pyplot as plt
import datetime
import random
from numpy.lib.function_base import average
import pandas as pd
from itertools import zip_longest
import serial
import pyrobotskinlib as rsl
import statistics as stat

from lib.tracker import Tracker

arduino = serial.Serial('/dev/ttyACM0', 9600,timeout=1)
time.sleep(3)

S = rsl.RobotSkin("small_hexagon_001.json")
u = rsl.SkinUpdaterFromShMem(S)
u.start_robot_skin_updater()

# Loop number
counter = 0
angle = 120
diameter = 28

p_d = [0,0,0]
p = []
n_motors = 3
mean_p = []
dif_pos = []
flag_pressure = [False,False,False]
flag_position = [False,False,False]

x_value = []
y_value = []
z_value = []
pressure1 = []
pressure2 = []
pressure3 = []
stress1 = []
stress2 = []
stress3 = []
stress4 =[]
stress5 = []
stress6=[]
stress7=[]

hx_value = []
hy_value = []
hz_value = []
hpressure1 = [0]
hpressure2 = [0]
hpressure3 = [0]
hstress1 = []
hstress2 = []
hstress3 = []
hstress4 =[]
hstress5 = []
hstress6=[]
hstress7=[]
Time = []

switch = False
steady_state = False
rows=[]
next_pose = False

pressure = 0
log_cnt = 0

timestr = time.strftime("%Y%m%d-%H%M%S")
namafile = str('static_'+timestr+'.csv')
header1 = "x_value"
header2 = "y_value"
header3 = "z_value"
fieldnames = [header1, header2, header3]

with open(namafile, 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

# with gui enabled
tracker1 = Tracker(gui=False,cam_index=2)
tracker1.addColorBlob("red", r=255, g=0, b=0, r_min=90, r_max=255, g_min=0, g_max=80, b_min=0, b_max=80)
# tracker.setCroppingPoints(tl_x=20, tl_y=20, br_x=100, br_y=100) 
tracker1.setMorphologicalOperationParameters(dilation_size=12, erosion_size=2)

tracker2 = Tracker(gui=False,cam_index=4)
tracker2.addColorBlob("yellow", r=255, g=255, b=0, r_min=140, r_max=255, g_min=140, g_max=255, b_min=0, b_max=100)
# tracker.setCroppingPoints(tl_x=20, tl_y=20, br_x=100, br_y=100) 
tracker2.setMorphologicalOperationParameters(dilation_size=12, erosion_size=2)

sample = 3000
i=0

start = time.time()
# while True:
#while counter <sample:
while p_d[2]<=20:
    counter += 1

    tracker1.processCamera("red")
    tracker1.updateVisualizations()

    tracker2.processCamera("yellow")
    tracker2.updateVisualizations()

    point1 = np.asfarray(tracker1.getPoints("red"))
    point2 = np.asfarray(tracker2.getPoints("yellow"))

    #grid search
    if next_pose == True:

        next_pose = False

        if switch == False:
            p_d[0]+= 0.5
        else:
            p_d[0] -= 0.5

        if p_d[0]>=20 or p_d[0] <=0:
            p_d[2] += 0.5
        
        if p_d[0] >= 20:
            switch = True
        
        if p_d[0]<=0:
            switch = False

        # pressure_3 = random.uniform(0,20)
        # pressure_4 = random.uniform(0,20)
        
        arduino.flushInput()
        arduino.flushOutput()
        arduino.write(b'111;%.1f;113;%.1f;' %(p_d[0],p_d[2]))

        time.sleep(.1)


    # Markers detected, no?
    if point1.size == 0:
        print("No marker detected by Cam1")

    if point2.size == 0:
        print("No marker detected by Cam2")
    
    if counter == 1:
        point1_original_y = np.min(point1[:,1])
        #point1_original_x = point1[np.where(np.min(point1[:,1]))[0],0][0]
        point1_original_x = point1[:,0]

        point2_original_y = np.min(point2[:,1])
        #point2_original_x = point2[np.where(np.min(point2[:,1]))[0],0][0]
        point2_original_x = point2[:,0]
    
    if size(point1)+size(point2) > 2*size(point1):
        print("Too many marker2 detected")
        continue
    if size(point1)+size(point2) < 2*size(point1):
        print("Too many marker1 detected")
        continue
    else:
        point1 = point1 - [0,point1_original_y]
        point2 = point2 - [0,point2_original_y]

        point1[:,0] = point1[:,0] - point1_original_x
        point2[:,0] = point2[:,0] - point2_original_x
        
        

        x = point1[:,0][1]-point1[:,0][0]
        y = point2[:,1][1]-point2[:,1][0]
        z = point2[:,0][1]-point2[:,0][0]

        #read pressure from Serial
        #time.sleep(.01)
        msg = arduino.readline()
        
        while not '\\n' in str(msg):
            i +=1
            #msg = msg + b'\n'
            # This loop is entered only if serial read value doesn't contain \n
            # which indicates end of a sentence. 
            # str(val) - val is byte where string operation to check `\\n` 
            # can't be performed
            time.sleep(.001)                # delay of 1ms 
            temp = arduino.readline()           # check for serial output.
            if not not temp.decode():       # if temp is not empty.
                msg = (msg.decode()+temp.decode()).encode()

            if i >=100:
                i =0
                msg = msg+b'\n'
                break
                #   requrired to decode, sum, then encode because
                # long values might require multiple passes

        print(msg)
        
        msg = msg.decode('cp1252').encode('utf-8')
        msg = msg.decode()
        msg = msg.strip()
        #msg = msg.replace('!',',')
        msg_lst = msg.split(',')

        if len(msg_lst) >=4:
            p = [msg_lst[0]]+[msg_lst[1]]+[msg_lst[2]]

        else:
            p = [hpressure1[-1]]+[hpressure2[-1]]+[hpressure3[-1]]
        
        
        #history
        hpressure1 = hpressure1 + [float(p[0])]
        hpressure2 = hpressure2 + [float(p[1])]
        hpressure3 = hpressure3 + [float(p[2])]

        u.make_this_thread_wait_for_new_data()
        resp = S.get_taxel_responses()
        #uids = S.get_taxel_ids()
        s1 = resp[0]
        s2 = resp[1]
        s3 = resp[2]
        s4 = resp[3]
        s5 = resp[4]
        s6 = resp[5]
        s7 = resp[6]

        hstress1 = hstress1+ [s1]
        hstress2 =hstress2+ [s2]
        hstress3 =hstress3 +[s3]
        hstress4 =hstress4+[s4]
        hstress5 = hstress5+[s5]
        hstress6=hstress6+[s6]
        hstress7=hstress7+[s7]

        hx_value = hx_value + [float(x)]
        hy_value = hy_value + [float(y)]
        hz_value = hz_value + [float(z)]


        # Logging data
        # Two conditions have to be satisfied
        # 1. measured pressure stablised and matches desired pressure
        # 2. position stablised
        # compare pressure      
        if len(hx_value)<60:
            continue
        else:
            #mean_p= [stat.fmean(hpressure1[-10:])]+[stat.fmean(hpressure2[-10:])]+[stat.fmean(hpressure3[-10:])]

            dif_pos = [hx_value[-50] - float(x)]+[hy_value[-50]- float(y)]+[hz_value[-50]- float(z)]

            #print(mean_p,dif_pos)
            #pressure flag
            # for i in range(n_motors):
            #     if abs(mean_p[i]-p_d[i])<=0.2:
            #         flag_pressure[i] = True
            #     else:
            #         flag_pressure[i] = False

            #position flag
            for i in range(3):
                if abs(dif_pos[i])<=1:
                    flag_position[i] = True
                else:
                    flag_position[i] = False
            
            #both flag raised & log data
            if all(flag_position):
            #if all(flag_pressure) and all(flag_position):
                #log 10 sets
                if log_cnt>=10:
                    next_pose = True
                    log_cnt = 0
                else:
                    log_cnt+=1
            
            pressure1 = pressure1 + [p[0]]
            pressure2 = pressure2 + [p[1]]
            pressure3 = pressure3 + [p[2]]

            stress1 = stress1+ [s1]
            stress2 =stress2+ [s2]
            stress3 =stress3 +[s3]
            stress4 =stress4+[s4]
            stress5 =stress5+[s5]
            stress6=stress6+[s6]
            stress7=stress7+[s7]

            x_value = x_value + [x]
            y_value = y_value + [y]
            z_value = z_value + [z]

            end = time.time()
            Time = Time + [end-start]

            rows = [Time,pressure1,pressure2,pressure3,stress1,stress2,stress3,stress4,stress5,stress6,stress7,x_value,y_value,z_value]
            export_data = zip_longest(*rows, fillvalue = '')
            with open(namafile, 'w', encoding="ISO-8859-1", newline='') as myfile:
                wr = csv.writer(myfile)
                #wr.writerow(("p1","p2","p3","x", "y","z"))
                wr.writerow(("pressure1","pressure2","pressure3","stress1","stress2","stress3","stress4","stress5","stress6","stress7","x", "y", "z"))
                wr.writerows(export_data)
            myfile.close()

arduino.flushInput()
arduino.flushOutput()
arduino.write(b'253;')
arduino.close()

        # with open(namafile, 'a') as csv_file:
        #     csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        #     info = {
        #         header1: x_value,
        #         header2: y_value,
        #         header3: z_value
        #     }

        #     csv_writer.writerow(info)
            #print(x_value, y_value, z_value)


        #time.sleep(1)
        
    # Live 3D reconstruction