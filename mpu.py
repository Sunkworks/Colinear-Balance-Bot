#!/usr/bin/python

import time
import math
from enum import Enum

from smbus2 import SMBus


# A class for representing a 3D vector of some kind:
# eg. a velocity, an acceleration, a coordinate etc.
class Vector:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0

    def downscale_values(self, scale_factor):
        self.x = 1.0 * self.x / scale_factor
        self.y = 1.0 * self.y / scale_factor
        self.z = 1.0 * self.z / scale_factor

    def to_radians(self):
        self.x = math.radians(self.x)
        self.y = math.radians(self.y)
        self.z = math.radians(self.z)

    def __str__(self):
        return "{}, {}, {}".format(self.x, self.y, self.z)


# For register numbers, see MPU-9250 register map
class ACC_REGISTER(Enum):
    X = 0x3b
    Y = 0x3d
    Z = 0x3f


class GYRO_REGISTER(Enum):
    X = 67
    Y = 69
    Z = 71


def twos_complement(val, bits):
    """ Converts an unsigned number from sensor into a signed number,
        with what used to be the most significant bit signifying signedness"""
    if val >> (bits - 1) & 0b1:
        val = val - (1 << bits)
    return val


class Sensors:
    def __init__(self, channel, addr):
        print("HWLLO")
        self.channel = channel
        self.address = addr
        self.bus = SMBus(self.channel)
        self.a = 0.98  # Complimentary filter coefficient
        self.gyro_LSB = 131  # From datasheet
        self.timestamp = time.time()  # Time of last measurement
        self.reset_angle()

    def reset_angle(self):
        # Call when robot is stationary, calcs current angle entirely from accelerometer
        self.angle = self.calc_accel_angle()

    def twobyte_merge(self, register):
        """ Returns: numerical value from high and low byte
            register: the register for the high byte
            assumption: the low byte is stored in the subsequent register
            """
        #raw_data = self.bus.read_i2c_block_data(self.address, register.value, 2)
        time.sleep(0.0001)
        raw_data = [0, 0]
        for i in range(2):
            try:
                raw_data[0] = self.bus.read_byte_data(self.address, register.value)
                time.sleep(0.0001)
                raw_data[1] = self.bus.read_byte_data(self.address, register.value)
                break
            except OSError:
                time.sleep(0.0001)
                continue
        unsigned_val = (raw_data[0] << 8) + raw_data[1]
        return twos_complement(unsigned_val, 16)

    def read_sensor(self, REGISTER):
        """ Returns: Vector with vals from sensor
            REGISTER: Enum with x, y and z addresses."""
        output = Vector()
        #bus = SMBus(self.channel)  # TODO: have bus permanently open instead
        time.sleep(0.0001)
        output.x = self.twobyte_merge(REGISTER.X)
        time.sleep(0.0001)
        output.y = self.twobyte_merge(REGISTER.Y)
        time.sleep(0.0001)
        output.z = self.twobyte_merge(REGISTER.Z)
        time.sleep(0.0001)
        #bus.close()
        return output

    def read_accelerometer(self):
        """ Returns: Vector with vals from sensor"""
        return self.read_sensor(ACC_REGISTER)

    def calc_accel_angle(self):
        reading = self.read_accelerometer()
        if reading.x == 0:
            raise ValueError
        return -math.atan(1.0 * reading.y / reading.x)

    def read_gyroscope(self):
        """ Supposed to return: change of angle in radians/s"""
        measurement = self.read_sensor(GYRO_REGISTER)
        #print(measurement)
        measurement.downscale_values(self.gyro_LSB)
        #print(measurement)
        measurement.to_radians()
        #print(measurement)
        return measurement

    # TODO:
    # Add variables for point values
    # Add method called "update sensors", which reads both gyro and accelerometer,
    # and returns a new angle
    def get_angle(self):
        """ Returns current angle and dt"""
        gyro_z = self.read_gyroscope().z
        # print(gyro_z)
        angle_xy = self.calc_accel_angle()
        # print(math.degrees(angle_xy))
        dt = time.time() - self.timestamp
        #y_n = (1 - self.a) * angle_xy + self.a * self.angle
        self.angle = self.a * (self.angle + gyro_z * dt) + (1 - self.a) * angle_xy
        #self.angle = angle_xy
        self.timestamp = time.time()
        return self.angle, dt


def main():
    channel = 1
    address = 0x68
    sensors = Sensors(channel, address)
    reading = sensors.read_accelerometer()
    print(reading)
    print(sensors.read_gyroscope())


def test_filter():
    channel = 1
    address = 0x68
    sensors = Sensors(channel, address)
    current_angle, dt = sensors.get_angle()
    print(math.degrees(current_angle))
    for x in range(10000):
        current_angle, dt = sensors.get_angle()
        if x % 10:
            print(math.degrees(current_angle))
        time.sleep(0.01)


def test_gyro():
    channel = 1
    address = 0x68
    sensors = Sensors(channel, address)
    print(sensors.read_gyroscope())


def test_accel():
    channel = 1
    address = 0x68
    sensors = Sensors(channel, address)
    print(sensors.calc_accel_angle())


if __name__ == '__main__':
    test_filter()
    # test_gyro()
