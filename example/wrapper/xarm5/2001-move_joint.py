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
arm.set_servo_angle(angle=[0, 0, 0, 0, 0], speed=speed, wait=True)
print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=True))

point_b=[-165, -70, -25, 95, 3]

if arm.get_forward_kinematics(angles=point_b, input_is_radian=None, return_is_radian=None) is not []:
    arm.set_servo_angle(angle=point_b, speed=speed, wait=True)







# arm.set_servo_angle(angle=[90, 0, -60, 0, 0], speed=speed, wait=True)
# print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=True))
# arm.set_servo_angle(angle=[90, -30, -60, 0, 0], speed=speed, wait=True)
# print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=True))
# arm.set_servo_angle(angle=[0, -30, -60, 0, 0], speed=speed, wait=True)
# print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=True))
# arm.set_servo_angle(angle=[0, 0, -60, 0, 0], speed=speed, wait=True)
# print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=True))
# arm.set_servo_angle(angle=[0, 0, 0, 0, 0], speed=speed, wait=True)
# print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=True))


# arm.move_gohome(wait=True)
# speed = math.radians(50)
# arm.set_servo_angle(angle=[math.radians(90), 0, 0, 0, 0], speed=speed, is_radian=True, wait=True)
# print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=True))
# arm.set_servo_angle(angle=[math.radians(90), 0, math.radians(-60), 0, 0], speed=speed, is_radian=True, wait=True)
# print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=True))
# arm.set_servo_angle(angle=[math.radians(90), math.radians(-30), math.radians(-60), 0, 0], speed=speed, is_radian=True, wait=True)
# print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=True))
# arm.set_servo_angle(angle=[0, math.radians(-30), math.radians(-60), 0, 0], speed=speed, is_radian=True, wait=True)
# print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=True))
# arm.set_servo_angle(angle=[0, 0, math.radians(-60), 0, 0], speed=speed, is_radian=True, wait=True)
# print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=True))
# arm.set_servo_angle(angle=[0, 0, 0, 0, 0], speed=speed, is_radian=True, wait=True)
# print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=True))


arm.move_gohome(wait=True)
arm.disconnect()


def get_orientation_2_points(self, desired_p, objective_2_point):
        """
        Given a desired point, get the orientation RPY s.t it points toward objective_2_point.
        :param desired_p: [x_e, y_e, z_e] 
        :param objective_2_point: [x_c, y_c, z_c]
        return: final pose with desired orientation
        """
        # get next position
        x_e, y_e, z_e = desired_p

        # Worldframe direction to target
        x_c, y_c, z_c = objective_2_point
        dx, dy, dz = x_c - x_e, y_c - y_e, z_c - z_e
        length = math.sqrt(dx*dx + dy*dy + dz*dz)
        if length < 1e-8:
            raise ValueError("Cone point coincides with EE; cannot compute orientation.")

        # Normalize
        dx /= length
        dy /= length
        dz /= length

        pose = None

        # 1. try every yaw angle (1Â° step)
        # 2. for each yaw, get the roll and pitch angle
        for yaw in range(0, 360, 1):
            
            # yaw candidate
            yaw_rad = math.radians(yaw)

            # compute roll and pitch given tha yaw candidate
            cos_y = math.cos(yaw_rad); sin_y = math.sin(yaw_rad)
            vx =  cos_y*dx + sin_y*dy
            vy = -sin_y*dx + cos_y*dy
            vz = dz
            vy_clamped = max(-1.0, min(1.0, vy))
            phi = -math.asin(vy_clamped)
            cos_phi = math.cos(phi)
            if abs(cos_phi) < 1e-6:
                theta = 0.0
            else:
                theta = math.atan2(vx, vz)
            roll = math.degrees(phi)
            pitch = math.degrees(theta)

            # test (roll, pitch, yaw) with IK:
            # if success     -> (roll,pitch,yaw) correctly points toward objective_2_point
            # if not success -> try next yaw
            code_ik, _ = arm.get_inverse_kinematics([x_e, y_e, z_e, roll, pitch, yaw], input_is_radian=False, return_is_radian=False)
            if code_ik == 0:
                pose = [x_e, y_e, z_e, roll, pitch, yaw]
                break
            else:
                continue
        
        if pose is None:
            raise RuntimeError("No valid IK solution found for pointing pose.")

        return pose



def execute_path(self):
        """
        Execute the loaded path (self.path) using the robot controller.
        At each pose:
          - Move to the pose (with orientation pointing at the cone center if needed)
          - Wait until the robot reaches the pose and is not moving
          - Check for errors
          - Pause for image capture (user or camera interface)
        """

        # initial sanity check
        if not self.ctrl:
            print("Error", "Robot not connected.")
            return
        if not self.path or len(self.path) == 0:
            print("Error", "No path loaded. Please load a path first.")
            return

        # use the cone center as the look-at point for orientation
        if len(self.ctrl.cone_center) >= 3:
            xc, yc, zc, _, _, _ = self.ctrl.cone_center
            cone_center = [xc,yc,zc]
        else:
            cone_center = [0, 0, 0]
        
        # self.path is a list of cartesian coordinates (xyz) 
        for idx, p in enumerate(self.path, start=1):
            try:
                # given xyz of p, retrieve rpy to point toward cone_center
                pose = self.ctrl.get_orientation_2_points(p,cone_center)

                # if no orientation was found
                if not pose:
                    self.update_status(f"IK error at step {idx}")
                    print("IK Error", f"No orientation could satisfy IK requirements at step {idx}")
                    return

                #if orientation was found -> move
                code = self.arm.set_position(*pose,
                                     speed=self.speed, mvacc=self.mvacc, # 250 mm/s^2 , 2500 mm/s^2  
                                     wait=False, motion_type=1) # we use wait = False otherwise the Emergency button doesn't work during the motion
                
                if code != 0:
                    self.update_status(f"Motion error at step {idx}: code {code}")
                    print("Motion error", f"Motion error code {code} at step {idx}")
                    return
                
                # condition-triggered loop until robot stops:

                # ? QUESTION BELOW:

                # SOMETIMES THIS DOESN'T WORK,   
                # BECAUSE THE ROBOT IS NOT MOVING WHEN THIS LINE IS EXECUTED
                # MAYBE BECAUSE OF COMPUTATIONAL OVERHEAD OF set_position() ABOVE
                # WHICH MAKES THE ROBOT MOTION NOT IMMEDIATE
                # MAYBE get_state() != 4 works???
                while self.arm.get_is_moving():
                    time.sleep(0.1)

                # check for errors/warnings after the motion is completed
                if self.ctrl.has_error():
                    self.update_status(f"Robot error at step {idx}: code {self.ctrl.get_error()}")
                    print("Robot Error", f"Robot error code {self.ctrl.get_error()} at step {idx}")
                    return
                if self.ctrl.has_warn():
                    self.update_status(f"Robot warning at step {idx}: code {self.ctrl.get_warn()}")
                    print("Robot Warning", f"Robot warning code {self.ctrl.get_warn()} at step {idx}")
                
                # trigger camera to capture image
                self.update_status(f"At pose {idx}/{len(self.path)}. Capturing image now.")
                print(f"Moved to pose {idx}/{len(self.path)}")
                
                ################################################
                #TODO call camera interface for capturing image
                #TODO otherwise pause for user capture triggering
                ################################################

                self.update_variables_label()

                time.sleep(1)    #delay of 3 sec for image capturing

            except Exception as e:
                self.update_status(f"Exception at step {idx}: {e}")
                print("Exception", f"Exception at step {idx}: {e}")
                return  

        self.update_status("Path execution complete.")
        print("Success", "Path Execution completed successfully!")