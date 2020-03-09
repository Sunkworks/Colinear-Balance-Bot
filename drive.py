# KISS, Keep It Simple Stupid!

import odrive
from odrive.enums import *
import time
import yaml

YML_FILE_NAME = "config.yml"


def configure_drive(drive, config):
    drive.config.brake_resistance = config["odrives"]["brake_resistance"]


def configure_axis(axis, config):
    axis.motor.config.current_lim = config["odrives"]['current_lim']
    axis.motor.config.calibration_current = config["odrives"]['calibration_current']
    axis.controller.config.pos_gain = config["odrives"]['pos_gain']
    axis.controller.config.vel_gain = config["odrives"]['vel_gain']
    axis.controller.config.vel_integrator_gain = config["odrives"]['vel_integrator_gain']
    axis.controller.config.vel_limit = config["odrives"]['vel_limit']


def save_drive_config(drive):
    drive.save_configuration()
    try:
        drive.reboot()
    except:
        pass


class OdriveController:
    def __init__(self, config_name=YML_FILE_NAME):
        self.drives = []  # A list of all odrives being controlled
        self.axises = []
        with open(config_name, "r") as yml_file:
            config = yaml.load(yml_file, Loader=yaml.FullLoader)
        # self.serial_numbers = [config["odrives"]["serialnumber0"] , config["odrives"]["serialnumber1"]]
        self.serial_numbers = [config["odrives"]["serialnumber0"]]
        # Makes sure that motors mounted the wrong way still work
        self.axises_forward_direction = [-1 if x else 1 for x in config["odrives"]["axis_inverted_forward_direction"]]
        self.find_odrives()
        if config["odrives"]["newConfig"]:
            self.configure(config)
            config["odrives"]["newConfig"] = False
            with open(YML_FILE_NAME, "w") as yml_file:
                yaml.dump(config, yml_file, default_flow_style=False, sort_keys=False)
            self.find_odrives()

    def find_odrives(self):
        """Finds odrives connected to computer"""
        # Clear lists
        del self.drives[:]
        del self.axises[:]
        for s in self.serial_numbers:
            odrv = odrive.find_any(serial_number=s)
            self.drives.append(odrv)
            self.axises.extend((odrv.axis0, odrv.axis1))
        print("ODrives found")

    def configure(self, config):
        """Updates configuration of all motors and axises
        config -- dict of same format as the config.yml file
        """
        print("Configuring ODrives...")
        for axis in self.axises:
            configure_axis(axis, config)
        for drive in self.drives:
            configure_drive(drive, config)
            save_drive_config(drive)
        print("ODrives configured, rebooting.")
        self.reboot()

    def reboot(self):
        for drive in self.drives:
            try:
                drive.reboot()
            except:
                pass

    def set_axis_state(self, new_state):
        """Sets requested_state of all axises to new_state.
        new_state -- an AXIS_STATE enum from odrive.enums
        """
        for axis in self.axises:
            axis.requested_state = new_state

    def set_control_mode(self, new_ctrl_mode):
        for axis in self.axises:
            axis.controller.config.control_mode = new_ctrl_mode

    def calibrate(self):
        """Calibrate all odrive axises. Leaves them in idle state."""

        def calibration_finished():
            for axis in self.axises:
                if axis.current_state != AXIS_STATE_IDLE:
                    return False
            return True

        print("Starting calibration...")
        self.set_axis_state(AXIS_STATE_FULL_CALIBRATION_SEQUENCE)
        while not calibration_finished():
            time.sleep(0.1)
        print("Calibration finished.")

    def dump_errors(self):
        """Prints errors on all axises."""
        print("Dumping errors:")
        for i, axis in enumerate(self.axises):
            print(f"axis: {i}")
            print(f"\taxis error: {axis.error}")
            print(f"\tmotor error: {axis.motor.error}")
            print(f"\tcontroller error: {axis.controller.error}")
            print(f"\tencoder error: {axis.encoder.error}")

    def reset_errors(self):
        """Resets errors on all axises."""
        print("Resetting errors...")
        for axis in self.axises:
            axis.error = 0
            axis.motor.error = 0
            axis.controller.error = 0
            axis.encoder.error = 0

    def set_motor_speed(self, axis_index: int, velocity: float):
        axis = self.axises[axis_index]
        axis_forward = self.axises_forward_direction[axis_index]
        # assert axis.current_state == CTRL_MODE_VELOCITY_CONTROL, "Motor isn't in velocity ctrl mode"
        axis.controller.vel_setpoint = velocity * axis_forward

    def set_all_motors_speed(self, velocity: float):
        for axis, forward in zip(self.axises, self.axises_forward_direction):
            axis.controller.vel_setpoint = velocity * forward
