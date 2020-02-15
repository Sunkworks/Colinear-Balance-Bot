# KISS, Keep It Simple Stupid!

import odrive
from odrive.enums import *
import time
import yaml


def calibrate(axis):
    print("Starting calibration...")
    for x in axis:
        x.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
    while axis[len(axis)-1].current_state != AXIS_STATE_IDLE:
        time.sleep(0.1)
    print("Calibration finished.")


def closedLoopControl(axis):
    for x in axis:
        x.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL


def idle(axis):
    for x in axis:
        x.requested_state = AXIS_STATE_IDLE


def configure(cfg):
    print("Configuring ODrives...")
    odrv0 = odrive.find_any(serial_number=cfg['serialnumber0'])
    odrv1 = odrive.find_any(serial_number=cfg['serialnumber1'])
    allDrives = [odrv0, odrv1]
    allAxis = [odrv0.axis0, odrv0.axis1, odrv1.axis0, odrv1.axis1]

    for x in allDrives:
        x.config.brake_resistance = cfg['brake_resistance']
    for x in allAxis:
        x.motor.config.current_lim = cfg['current_lim']
        x.motor.config.calibration_current = cfg['calibration_current']
        x.controller.config.pos_gain = cfg['pos_gain']
        x.controller.config.vel_gain = cfg['vel_gain']
        x.controller.config.vel_integrator_gain = cfg['vel_integrator_gain']
        x.controller.config.vel_limit = cfg['vel_limit']
    for x in allDrives:
        x.save_configuration()
        try:
            x.reboot()
        except:
            pass
    print("ODrives configured, rebooting.")


def dumpErrors(axis):
    print("Dumping errors:")
    i = 0
    for x in axis:
        print("axis" + str(i))
        print("    axis error: " + str(x.error if x.error else "no error"))
        print("    motor error: " + str(x.motor.error if x.motor.error else "no error"))
        print("    controller error: " + str(x.controller.error if x.controller.error else "no error"))
        print("    encoder error: " + str(x.encoder.error if x.controller.error else "no error"))
        i += 1


def resetErrors(axis):
    print("Resetting errors.")
    for x in axis:
        x.error = 0
        x.motor.error = 0
        x.controller.error = 0
        x.encoder.error = 0


def main():
    with open("config.yml", "r") as ymlfile:
        config = yaml.load(ymlfile, Loader=yaml.FullLoader)
    cfg = config['odrives']

    if cfg['newConfig']:
        configure(cfg)
        config['odrives']['newConfig'] = False
        with open("config.yml", "w") as ymlfile:
            yaml.dump(config, ymlfile)

    print("Looking for ODrives...")
    odrv0 = odrive.find_any(serial_number=cfg['serialnumber0'])
    odrv1 = odrive.find_any(serial_number=cfg['serialnumber1'])
    print("ODrives found!")

    allDrives = [odrv0, odrv1]
    allAxis = {odrv0.axis0, odrv0.axis1, odrv1.axis0, odrv1.axis1}

    dumpErrors(allAxis)


main()