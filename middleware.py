import odrive.enums
import drive
import time


def main():
    odrv = drive.OdriveController()
    print("Setting axis state...")
    odrv.set_axis_state(odrive.enums.AXIS_STATE_CLOSED_LOOP_CONTROL)
    print("Setting control mode...")
    odrv.set_control_mode(odrive.enums.CTRL_MODE_VELOCITY_CONTROL)
    print("Done, please standby...")
    time.sleep(1)
    while True:
        print("Setting high motor speed...")
        odrv.set_all_motors_speed(5000)
        print("Motor now has high speed.")
        time.sleep(5)
        odrv.set_all_motors_speed(0)
        print("Speed = 0")
        time.sleep(5)

if __name__ == "__main__":
    main()
