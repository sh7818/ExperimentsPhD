from xarm.wrapper import XArmAPI

arm = XArmAPI('192.168.1.150')
print(arm.get_version())

