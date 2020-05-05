import pygame


class RemoteController:
    def __init__(self):
        print("Controller init.")
        self.screen = pygame.display.set_mode([10, 10])  # Piece of shit nightmare thing
        pygame.joystick.init()
        self.joy = pygame.joystick.Joystick(0)
        self.joy.init()

    def get_axis(self, axis):
        pygame.event.get()
        return self.joy.get_axis(axis)

    def get_y_axis(self):
        return self.get_axis(1)

    def get_x_axis(self):
        return self.get_axis(0)


def main():
    from matplotlib import pyplot as plt
    import matplotlib.animation as animation

    def xyPlot(i, axis1, axis2):
        sx = remote.get_axis(axis1)
        sy = -remote.get_axis(axis2)
        print("SX:", sx)
        print("SY:", sy)
        ax.clear()
        plt.axis([-1, 1, -1, 1])
        ax.scatter(sx, sy)

    remote = RemoteController()
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ani = animation.FuncAnimation(fig, xyPlot, fargs=(0, 1, remote), interval=50)
    plt.show()


if __name__ == '__main__':
    main()
