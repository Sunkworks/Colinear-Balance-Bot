import mpu, pid_class
import time


def main():
    sensors = mpu.Sensors(1, 0x68)
    control = pid_class.PID()
    while True:
        angle, dt = sensors.get_angle()
        print(angle, dt)
        control.set_process_variable(angle, dt)
        output = control.get_control_variable()
        print(output)
        time.sleep(0.01)


if __name__ == '__main__':
    main()
