import odrive
from odrive.enums import *
import yaml
import time

with open("config.yml", "r") as ymlfile:    # Loading config file
    config = yaml.load(ymlfile, Loader=yaml.FullLoader)

serialNumber1 = "206739834D4D"
serialNumber2 = "204F39824D4D"


def configure():  # Configure odrives based on yml file.
    cfg = config['odrives']
    if cfg['newConfig']:
        print("New ODrive settings found.")
        for x in drives:
            x.config.brake_resistance = cfg['brake_resistance']

        for x in axis:
            x.motor.config.current_lim = cfg['current_lim']
            x.motor.config.calibration_current = cfg['calibration_current']
            x.controller.config.pos_gain = cfg['pos_gain']
            x.controller.config.vel_gain = cfg['vel_gain']
            x.controller.config.vel_integrator_gain = cfg['vel_integrator_gain']
            x.controller.config.vel_limit = cfg['vel_limit']

        print("Rebooting & Reconnecting...")
        for x in drives:
            x.save_configuration()
            try:
                x.reboot()
            except:
                pass

        odrv0 = odrive.find_any(serial_number=serialNumber1)
        odrv1 = odrive.find_any(serial_number=serialNumber2)

        config['odrives']['newConfig'] = False
        with open("config.yml", "w") as ymlfile:
            yaml.dump(config, ymlfile)
        print("ODrives configured and reconnected!")


def calibrate():    # TODO: Talk to gyro & make sure bot stays still during calibration
    print("Starting calibration...")
    for x in axis:
        x.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
        while x.requested_state != AXIS_STATE_IDLE:
            time.sleep(0.1)


print("Looking for ODrives...")
odrv0 = odrive.find_any(serial_number=serialNumber1)
odrv1 = odrive.find_any(serial_number=serialNumber2)
print("ODrives found!")

axis = {odrv0.axis0, odrv0.axis1, odrv1.axis0, odrv1.axis1}
drives = {odrv0, odrv1}

if odrv0.vbus_voltage / 5 < config["general"]["minCellVoltage"]:
    print("VBus Low @" + str(round(odrv0.vbus_voltage, 3)) + "V   " + str(round(odrv0.vbus_voltage / 5, 3)) + "V/Cell")
    print("Unplug and charge batteries.")
else:
    print("VBus OK @" + str(round(odrv0.vbus_voltage, 3)) + "V")
    configure()
