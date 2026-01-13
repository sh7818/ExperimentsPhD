#!/usr/bin/env python3
# Author: Savvas Hadjixenophontos, Vinman, U-Factory.
#


import os
import sys
import csv
import time
import math
from xarm.wrapper import XArmAPI

ip = "192.168.1.150"
csv_path = str(time.time())+'.csv'
arm = XArmAPI(ip)

start = 0
repetitions = 20


arm.clean_warn()
arm.clean_error()

arm.motion_enable(True)

arm.set_mode(0)
arm.set_state(state=0)
arm.move_gohome(wait=False)

arm.set_tool_position(x=50, y=50, z=0, roll=0, pitch=0, yaw=0, radius=None,speed=20, wait=False)


for i in range(1,repetitions+1):

    if i%2:
        s = 1
    else:
        s = -1

    arm.set_tool_position(x=s*100, y=0, z=0, roll=0, pitch=0, yaw=0, radius=None,speed=40, wait=False)
    arm.set_tool_position(x=0, y=s*100, z=0, roll=0, pitch=0, yaw=0, radius=None,speed=40, wait=False)
    arm.set_tool_position(x=0, y=0, z=s*-100, roll=0, pitch=0, yaw=0, radius=None,speed=40, wait=False)


with open(csv_path, mode='w', newline='') as file:
    writer = csv.writer(file)

    while(start==0):

       if(arm.get_state()[1]==1):
           start = 1
           print("Starting capture")
       else: pass

    while(arm.get_state()[1]==1):

           writer.writerow([time.time()]+arm.get_position(True)[1])

print("finished:", csv_path)
