import mpu, pid_class, drive, odrive.enums
import time, math

MAX_ANGLE = 45  # Angle at which code stops
SCALING_FACTOR = 1000 # Multiplier

def main():
    print(odrive.enums.AXIS_STATE_CLOSED_LOOP_CONTROL)
    sensors = mpu.Sensors(1, 0x68)
    control = pid_class.PID()
    control.update_constants()
    print("Welcome to ODRIVE!")
    odrv = drive.OdriveController()
    odrv.calibrate()
    print("Setting axis state...")
    odrv.set_axis_state(odrive.enums.AXIS_STATE_CLOSED_LOOP_CONTROL)
    print("Setting control mode...")
    odrv.set_control_mode(odrive.enums.CTRL_MODE_VELOCITY_CONTROL)
    print("Done, please standby...")
    time.sleep(1)
    try:
        while True:
            count = 0
            while True:
                count += 1
                if count == 100:
                    control.update_constants()
                    print("Constants updated.")
                    count = 0
                angle, dt = sensors.get_angle()
                if abs(math.degrees(angle)) > MAX_ANGLE:
                    break
                    #raise ValueError(f"Angle outside maximum allowed range, {angle}")
                control.set_process_variable(angle, dt)
                output = control.get_control_variable() 
                odrv.set_all_motors_speed(output * SCALING_FACTOR)
                print(f"Angle: {math.degrees(angle)}\tOutput: {output}")
                time.sleep(0.01)
            odrv.set_all_motors_speed(0)
            input("Angle too big, press enter to continue")
    finally:
        odrv.set_all_motors_speed(0)
        odrv.set_axis_state(odrive.enums.AXIS_STATE_IDLE)
        sensors.bus.close()


if __name__ == '__main__':
    main()
