import pygame


class RemoteController:
    def __init__(self):
        print("Controller init.")
        self.screen = pygame.display.set_mode([10, 10])  # Piece of shit nightmare thing
        pygame.joystick.init()
        self.joy = pygame.joystick.Joystick(0)
        self.joy.init()

        self.lerp_axis = [0] * 10
        self.interpolant = 0.6
        self.scaling_factor = 0.5 # Must be between 0-1

    def lerp(self, a, b):
        '''Linear Interpolation form a to b'''
        #TODO Multiply interpolant with delta time
        return (self.interpolant * a) + ((1 - self.interpolant) * b)

    def expo(self, input):
        return self.scaling_factor * input ** 3 + (1-self.scaling_factor)*input

    def get_axis(self, axis):
        pygame.event.get()
        self.lerp_axis[axis] = self.lerp(self.lerp_axis[axis], self.joy.get_axis(axis))
        return self.expo(self.lerp_axis[axis])

    def get_ly_axis(self):
        return -self.get_axis(1)

    def get_lx_axis(self):
        return self.get_axis(0)

    def get_ry_axis(self):
        return -self.get_axis(4)

    def get_rx_axis(self):
        return self.get_axis(3)


def main():
    from matplotlib import pyplot as plt
    import matplotlib.animation as animation

    def xyPlot(i):
        sx = remote.get_lx_axis()
        sy = remote.get_ly_axis()
        rx = remote.get_rx_axis()
        ry = remote.get_ry_axis()

        print("SX:", sx)
        print("SY:", sy)
        ax.clear()
        plt.axis([-1, 1, -1, 1])
        ax.scatter(sx, sy)
        ax.scatter(rx, ry)

    remote = RemoteController()
    print(remote.joy.get_numaxes())
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ani = animation.FuncAnimation(fig, xyPlot, interval=50)
    plt.show()


if __name__ == '__main__':
    main()
