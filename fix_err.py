from xarm.wrapper import XArmAPI

ip = '192.168.1.150'
arm = XArmAPI(ip, is_radian=False)

# 1) Clear faults/warnings and enable
arm.clean_error(); arm.clean_warn()
arm.motion_enable(enable=True)

# 2) Position mode & ready state
arm.set_mode(0)   # position mode
arm.set_state(0)  # ready

# 3) Nudge only Joint 3 away from the negative limit (small + move)
#    Adjust angle step if needed; keep it small and safe.
arm.set_servo_angle(j=3, angle=-10, speed=10, wait=True)  # if your zeroing puts negative as 'up', flip sign accordingly

# 4) If no errors now, try a gentle joint move or gohome
ret = arm.move_gohome(wait=True)
print('gohome ret:', ret)

