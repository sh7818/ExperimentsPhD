#!/usr/bin/env python3
# Author: Savvas Hadjixenophontos, Vinman, U-Factory.
#


import os
import sys
import csv
import time
import math
import random
from xarm.wrapper import XArmAPI

ip = "192.168.1.150"
csv_path = "Data/"+str(time.time())+'.csv'
arm = XArmAPI(ip)

start = 0
repetitions = 100


arm.clean_warn()
arm.clean_error()
arm.motion_enable(True)
arm.set_mode(0)
arm.set_state(state=0)
arm.move_gohome(wait=False)

arm.set_tool_position(x=100, y=100, z=0, roll=0, pitch=0, yaw=0, radius=None,speed=20, wait=False)


cumul       =   [50,50,50]
cumulr      =   [0,0,0]
boundaries  =   [[50,150],[50,150],[-100,0]]
boundariesr =   [[-15,15],[-15,15],[-15,15]]

def random_translation(low,high,axis):

  ri =  random.randint(low,high)

  if (ri + cumul[axis] < boundaries[axis][0]) or (ri + cumul[axis] > boundaries[axis][1]):
      return  random_translation(low,high,axis)
  else:
      cumul[axis] += ri
      return ri

def random_rotation(low,high,axis):

  ri =  random.randint(low,high)

  if (ri + cumulr[axis] < boundariesr[axis][0]) or (ri + cumulr[axis] > boundariesr[axis][1]):
      return  random_rotation(low,high,axis)
  else:
      cumulr[axis] += ri
      return ri




for i in range(1,repetitions+1):

    xr = random_translation(-100,100,0)
    yr = random_translation(-100,100,1)
    zr = random_translation(-50,50,2)
    rr = random_rotation(-15,15,0)
    pr = random_rotation(-15,15,1)
    yr = random_rotation(-15,15,2)

    arm.set_tool_position(x=int(xr), y=int(yr), z=int(zr), roll=int(rr), pitch=int(pr), yaw=int(yr), radius=None,speed=20, wait=False)



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
