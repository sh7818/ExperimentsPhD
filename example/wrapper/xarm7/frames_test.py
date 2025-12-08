#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2019, UFACTORY, Inc.
# All rights reserved.
#
# Author: Vinman <vinman.wen@ufactory.cc> <vinman.cub@gmail.com>

"""
Description: Move Joint
"""

import os
import sys
import time
import math

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from xarm.wrapper import XArmAPI


#######################################################
"""
Just for test example
"""
if len(sys.argv) >= 2:
    ip = sys.argv[1]
else:
    try:
        from configparser import ConfigParser
        parser = ConfigParser()
        parser.read('../robot.conf')
        ip = parser.get('xArm', 'ip')
    except:
        ip = input('Please input the xArm ip address:')
        if not ip:
            print('input error, exit')
            sys.exit(1)
########################################################


arm = XArmAPI(ip)
arm.motion_enable(enable=True)
arm.set_mode(0)
arm.set_state(state=0)

arm.move_gohome(wait=True)

speed = 10

p1x1 = 250
p1y1 = -125
p1z1 = 100
p1x2 = 400
p1y2 = -125
p1z2 = 100
p1x3 = 250
p1y3 = 0
p1z3 = 100

p2x1 = 250
p2y1 = -125
p2z1 = 200
p2x2 = 400
p2y2 = -125
p2z2 = 200
p2x3 = 250
p2y3 = 0
p2z3 = 200

roll = 180
pitch = 0
yaw = 0

testx = 210
testy = 0
testz = 120
arm.set_world_offset(offset=[0, 0, 0, 0, 0, 0], is_radian=None, wait=True)
arm.set_state(state=0)
arm.move_gohome(wait=True)
#print('Arm is home')

arm.set_world_offset(offset=[-200, 0, 0, 0, 0, 0], is_radian=None, wait=True)
#print('Offset 1 created')
arm.set_state(state=0)
arm.set_position(x=200, y=0, z=150, roll=180, pitch=0, yaw=0, radius=None, speed=speed, mvacc=None, mvtime= None, relative= False, is_radian= None, wait= False, timeout= None)
#print('Moved to position 1')
time.sleep(1)

arm.set_world_offset(offset=[0, 100, 0, 0, 0, 0], is_radian=None, wait=True)
arm.set_state(state=0)
arm.set_position(x=200, y=0, z=150, roll=180, pitch=0, yaw=0, radius=None, speed=speed, mvacc=None, mvtime= None, relative= False, is_radian= None, wait= False, timeout= None)
time.sleep(1)

arm.set_world_offset(offset=[0, 0, 100, 0, 0, 0], is_radian=None, wait=True)
arm.set_state(state=0)
arm.set_position(x=200, y=0, z=150, roll=180, pitch=0, yaw=0, radius=None, speed=speed, mvacc=None, mvtime= None, relative= False, is_radian= None, wait= False, timeout= None)
time.sleep(1)

arm.set_world_offset(offset=[0, 0, 0, 0, 0, 0], is_radian=None, wait=True)

arm.move_gohome(wait=True)
time.sleep(1)
arm.disconnect()
