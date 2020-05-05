import pygame


class remoteController:
    def __init__(self):
        print("Controller init.")
        self.screen = pygame.display.set_mode([10, 10])  # Piece of shit nightmare thing
        pygame.joystick.init()
        self.joy = pygame.joystick.Joystick(0)
        self.joy.init()

    def update(self):
        pygame.event.get()

    def getAxis(self, axis):
        return round(self.joy.get_axis(axis), 2)


def main():
    from matplotlib import pyplot as plt
    import matplotlib.animation as animation
    def xyPlot(i, axis1, axis2):
        pygame.event.get()
        remote.update()
        sx = remote.getAxis(axis1)
        sy = -remote.getAxis(axis2)
        print("SX:", sx)
        print("SY:", sy)
        ax.clear()
        plt.axis([-1, 1, -1, 1])
        ax.scatter(sx, sy)

    remote = remoteController()
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ani = animation.FuncAnimation(fig, xyPlot, fargs=(0, 1, remote), interval=50)
    plt.show()


if __name__ == '__main__':
    main()
