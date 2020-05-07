import pygame
import time
import os


class RemoteController:
    def __init__(self):
        print("Controller init.")
        self.screen = pygame.display.set_mode([10, 10])  # Piece of shit nightmare thing

        pygame.joystick.init()
        self.joy = pygame.joystick.Joystick(0)
        self.joy.init()

        self.last_axis_state = [0] * self.joy.get_numaxes()
        self.interpolant = 0
        self.scaling_factor = 0.0 # Must be between 0-1
        self.timestamp = time.time()

    def lerp(self, a, b):
        '''Linear Interpolation form a to b'''
        return (self.interpolant * a) + ((1 - self.interpolant) * b)

    def expo(self, input):
        return self.scaling_factor * input ** 3 + (1-self.scaling_factor)*input

    def get_axis(self, axis):
        pygame.event.get()
        self.last_axis_state[axis] = self.lerp(self.last_axis_state[axis], self.joy.get_axis(axis))
        return self.expo(self.last_axis_state[axis])

    def get_ly_axis(self):
        return -self.get_axis(1)

    def get_lx_axis(self):
        return self.get_axis(0)

    def get_ry_axis(self):
        return -self.get_axis(5)

    def get_rx_axis(self):
        return self.get_axis(2)


def main():
    remote = RemoteController()
    print(remote.joy.get_numaxes())
    for i in range(100):
        lx = remote.get_lx_axis()
        ly = remote.get_ly_axis()
        rx = remote.get_rx_axis()
        ry = remote.get_ry_axis()
        print("SX:", lx)
        print("SY:", ly)
        print("RX:", rx)
        print("RY:", ry)
        time.sleep(0.1)


if __name__ == '__main__':
    main()
