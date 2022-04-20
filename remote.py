import pygame #Used for controller
import time #Delay
from indicator import * #Indication for LED not in use
import os # for mp and other stuff
from multiprocessing import Process #mp=multiproccessing

class RemoteController:
    def __init__(self):
        print("Controller init.") #Trying to find for controller
        self.screen = pygame.display.set_mode([10, 10])  # Piece of shit nightmare thing
        
        pygame.joystick.init()
        self.joy = pygame.joystick.Joystick(0)
        self.joy.init()
        print("Controller found!")

        self.last_axis_state = [0] * self.joy.get_numaxes()
        self.interpolant = 0
        self.scaling_factor = 0.5 # Must be between 0-1
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
    
    def get_button(self, button):
        pygame.event.get()
        return self.joy.get_button(button)


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
    ani = animation.FuncAnimation(fig, xyPlot, interval=1)
    plt.show()


if __name__ == '__main__':
    main()

processes = [] #Creates multiple processes so the CPU can use all of the cores

for i in range(os.cpu_count()):
	print('registering process %d' % i)
	processes.append(Process(target=main))

for process in processes:
	process.start()

for process in processes:
	process.join()