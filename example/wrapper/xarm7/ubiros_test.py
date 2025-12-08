#Sample Python Code to actutae the gripper fingers individualy.

import os
import sys
import time
import socket

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from ubiros.ubiros_control import UbirosGripper
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

gripper_ip = "192.168.1.184"
speed=55

with UbirosGripper(gripper_ip, read_reply=True, add_newline=False) as grip:
   grip.wifi_reset()
   
    # grip.open()                 # m0>
    # time.sleep(1)
    # ##arm.set_servo_angle(angle=[0, 0, 0, 0, 0, 0, 45], speed=speed, wait=True)
    # grip.set_preset(1, 30)      # p1:30>
    # grip.set_preset(2, 45)
    # grip.set_preset(3, 60)
    # grip.set_preset(4, 15)
    # grip.save_preset(1)
    # print("saved")
    # time.sleep(1)
    # grip.go_preset(1)           # g1>
    # time.sleep(1)
    # grip.close()                # m65>
    # time.sleep(1)