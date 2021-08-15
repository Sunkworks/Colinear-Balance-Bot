import math
import time

import odrive.enums

import drive
import mpu
#import remote
import pid_class


class ManualNavigator:
    def __init__(self, max_angle=45, max_setpoint_angle=5, scaling_factor=1000, max_collinear_offset=100):
        self.MAX_ANGLE = math.radians(max_angle)
        self.MAX_SETPOINT_ANGLE = math.radians(max_setpoint_angle)
        self.MAX_COLLINEAR_OFFSET = max_collinear_offset
        self.SCALING_FACTOR = scaling_factor
        self.pid = pid_class.PID()
        self.pid.update_constants()
        self.pid_output = 0
        self.imu = mpu.Sensors(1, 0x68)
        #self.remote = remote.RemoteController()
        #self.update_user_angle()
        self.odrv = drive.OdriveController()
        self.setup_odrive()
        self.angle = self.dt = 0  # Values set in update_pid
        self.running = False
        self.update_pid()

    def start(self):
        self.running = True
        self.angle = self.imu.reset_angle()

    def stop(self):
        self.running = False
        self.odrv.set_collinear_offsets(0)
        self.odrv.set_all_motors_speed(0)

    def cleanup(self):
        self.odrv.set_all_motors_speed(0)
        self.odrv.set_axis_state(odrive.enums.AXIS_STATE_IDLE)
        self.imu.bus.close()

    def setup_odrive(self):
        print("Starting calibration...")
        self.odrv.calibrate()
        print("Calibration finished.")
        print("Setting axis state...")
        self.odrv.set_axis_state(odrive.enums.AXIS_STATE_CLOSED_LOOP_CONTROL)
        print("Setting control mode...")
        self.odrv.set_control_mode(odrive.enums.CTRL_MODE_VELOCITY_CONTROL)
        print("Done, please standby...")
        time.sleep(1)

    def update_user_angle(self):
        main_axis_input = self.remote.get_ly_axis()
        angle = main_axis_input * self.MAX_SETPOINT_ANGLE
        self.pid.set_setpoint(angle)

    def update_collinear_offset(self):
        collinear_input = self.remote.get_lx_axis()
        collinear_offset = collinear_input * self.MAX_COLLINEAR_OFFSET
        self.odrv.set_collinear_offsets(collinear_offset)

    def update_pid(self):
        self.angle, self.dt = self.imu.get_angle()
        self.pid.set_process_variable(self.angle, self.dt)
        self.pid_output = self.pid.get_control_variable()

    def update_odrive_output(self):
        velocity = self.pid_output * self.SCALING_FACTOR
        self.odrv.set_all_motors_speed(velocity)

    def main_task(self):
        """ Returns: true if ok, false if not"""
        #self.update_user_angle()
        #self.update_collinear_offset()
        self.update_pid()
        self.update_odrive_output()
        if self.fallen_over:
            self.stop()
        return not self.fallen_over

    def print_telemetry(self):
        print(f"Setpoint: {math.degrees(self.pid.setpoint)}")
        print(f"Angle: {math.degrees(self.angle)}\tOutput: {self.pid_output}")

    @property
    def fallen_over(self):
        if abs(self.imu.angle) > self.MAX_ANGLE:
            print("has fallen over, ", math.degrees(self.imu.angle), "\t", math.degrees(self.MAX_ANGLE))
            return True
        return False
