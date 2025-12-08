import os
import sys
import time
import math

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from xarm.wrapper import XArmAPI

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


arm = XArmAPI(ip, is_radian=True)
arm.motion_enable(enable=True)
arm.set_mode(0)
arm.set_state(state=0)

arm.move_gohome(wait=True)

speed = 50

arm = XArmAPI(ip)
arm.motion_enable(enable=True)
arm.set_mode(1)
arm.set_state(state=0)

arm.move_gohome(wait=True)

speed = 50
arm.set_servo_angle(angle=[45, -10, 15, 35, 0, 45, -40], speed=speed, wait=True)
print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=True))
arm.set_servo_angle(angle=[90, 0, 0, 0, 0, 0, 0], speed=speed, wait=True)
print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=True))
arm.move_gohome(wait=True)
time.sleep(1)

speed = 100
arm.set_servo_angle(angle=[45, -10, 15, 35, 0, 45, -40], speed=speed, wait=True)
print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=True))
arm.set_servo_angle(angle=[90, 0, 0, 0, 0, 0, 0], speed=speed, wait=True)
print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=True))
arm.move_gohome(wait=True)
time.sleep(1)

arm.move_gohome(wait=True)
arm.disconnect()
