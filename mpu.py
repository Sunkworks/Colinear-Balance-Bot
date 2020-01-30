#!/usr/bin/python

import time
import math
from enum import Enum

from smbus import SMBus


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

    def __str__(self):
        return "{}, {}, {}".format(self.x, self.y, self.z)
        #return "x: {:06}\ty: {:06}\tz:{:06}".format(self.x, self.y, self.z)



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
        self.channel = channel
        self.address = addr
        self.reset_angle()
        self.timestamp = time.time()  # Time of last measurement
        self.a = 0.98  # Complimentary filter coefficient
        self.gyro_LSB = 131  # From datasheet

    def reset_angle(self):
        # Call when robot is stationary, calcs current angle entirely from accelerometer
        self.angle = self.calc_accel_angle()

    def twobyte_merge(self, bus, register):
        """ Returns: numerical value from high and low byte
            register: the register for the high byte
            assumption: the low byte is stored in the subsequent register
            """
        raw_data = bus.read_i2c_block_data(self.address, register.value, 2)
        unsigned_val = (raw_data[0] << 8) + raw_data[1]
        return twos_complement(unsigned_val, 16)

    def read_sensor(self, REGISTER):
        """ Returns: Vector with vals from sensor
            REGISTER: Enum with x, y and z addresses."""
        output = Vector()
        bus = SMBus(self.channel)  # TODO: have bus permanently open instead
        output.x = self.twobyte_merge(bus, REGISTER.X)
        output.y = self.twobyte_merge(bus, REGISTER.Y)
        output.z = self.twobyte_merge(bus, REGISTER.Z)
        bus.close()
        return output

    def read_accelerometer(self):
        """ Returns: Vector with vals from sensor"""
        return self.read_sensor(ACC_REGISTER)

    def calc_accel_angle(self):
        reading = self.read_accelerometer()
        if reading.x == 0:
            return math.pi  # Or maybe -pi, depending on z val?
        return math.atan(reading.y / -reading.x)

    def read_gyroscope(self):
        """ Supposed to return: change of angle in radians/s"""
        measurement = self.read_sensor(GYRO_REGISTER)
        measurement.downscale_values(self.gyro_LSB)
        return measurement

    # TODO:
    # Add variables for point values
    # Add method called "update sensors", which reads both gyro and accelerometer,
    # and returns a new angle
    def get_angle(self):
        """ Returns current angle using complimentary filter"""
        gyro_z = self.read_gyroscope().z
        angle_xy = self.calc_accel_angle()
        dt = time.time() - self.timestamp
        y_n = (1 - self.a) * angle_xy + self.a * self.angle
        self.angle = (1 - self.a) * (self.angle + gyro_z * dt) + (self.a) * angle_xy
        self.timestamp = time.time()
        return self.angle


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
    current_angle = sensors.get_angle()
    print(math.degrees(current_angle))
    for x in range(100):
        current_angle = sensors.get_angle()
        if not x % 10:
            print(math.degrees(current_angle))
        time.sleep(0.1)
    

def test_gyro():
    channel = 1
    address = 0x68
    sensors = Sensors(channel, address)
    print(sensors.read_gyroscope())



if __name__ == '__main__':
    test_filter()
    #test_gyro()
