import os
import sys
import time
import math
#import ah_wrapper

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from xarm.wrapper import XArmAPI
#from ah_wrapper import AHSerialClient            # PSYONIC wrapper


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

# ---- Connect to the robot arm ----
arm = XArmAPI(ip)
arm.motion_enable(enable=True)
arm.set_mode(0)     # position mode
arm.set_state(state=0)    # ready

speed = 10
##arm.set_servo_angle(angle=[0, 0, 0, 0, -45, 0], speed=speed, wait=True)
print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=True))

arm.reset(speed=None, mvacc=None, mvtime=None, is_radian=None, wait=False, timeout=None)
arm.set_tgpio_modbus_baudrate(2000000)
print(arm.get_tgpio_modbus_baudrate())
code = arm.set_tgpio_modbus_timeout(timeout=30, is_transparent_transmission=True)
# code, ret = arm.getset_tgpio_modbus_data(datas= [0x01, 0x10, 0x00, 0x01, 0x00, 0x07, 0x7E, 0x50, 0x1D, 0x01, 0xFF, 0x93, 0x7E], is_transparent_transmission=False, use_503_port=False)
##code, ret = arm.getset_tgpio_modbus_data(datas= [126, 80, 18, 95, 29, 59, 39, 40, 47, 4, 51, 200, 49, 56, 212, 45, 126], host_id=9, is_transparent_transmission=True, use_503_port=True)
# code, ret = arm.getset_tgpio_modbus_data(datas=[126, 80, 29, 1, 255, 147, 126], is_transparent_transmission=False, use_503_port=False)
##code, ret = arm.getset_tgpio_modbus_data(datas= [0x01, 0x10, 0x00, 0x01, 0x00, 0x07, 0x7E, 0x50, 0x1D, 0x00, 0xFF, 0x94, 0x7E], is_transparent_transmission=False, use_503_port=False)
code, ret = arm.getset_tgpio_modbus_data(datas= [0x00, 0x01, 0x00, 0x02, 0x00, 0x0B, 0x7C, 0x09, 0x08, 0x10, 0x01, 0x00, 0x00, 0x01, 0x02, 0x00, 0x01], host_id=9, is_transparent_transmission=False, use_503_port=False)
code, ret = arm.getset_tgpio_modbus_data(datas= [0x00, 0x01, 0x00, 0x02, 0x00, 0x0D, 0x7C, 0x09, 0x08, 0x10, 0x07,0x00, 0x00,0x02, 0x04, 0x00, 0x00, 0x01, 0x90], host_id=9, is_transparent_transmission=False, use_503_port=False)

##arm.disconnect()
