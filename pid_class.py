import math
import os
from multiprocessing import Process

class PID:
    def __init__(self):
        self.file_name = "PID.txt"
        self.kP = 160
        self.kI = 0
        self.kD = 3

        self.max_I_val = 25.0
        self.P = 0
        self.I = 0
        self.D = 0
        self.setpoint = math.radians(0)
        self.process_variable = 0
        self.dt = 0

        self.last_error = 0
        self.error_val = 0
        self.y = 0
        self.need_to_calc_y = True #prevents having to calculate the y_val more often than needed

    def update_constants(self):
        print(os.listdir())
        with open(self.file_name, 'r') as infile:
            kP, kI, kD, max_I = (float(infile.readline()) for i in range(4))
            if kP != self.kP or kI != self.kI or kD != self.kD or max_I != self.max_I_val:
                print("New constants fixed. resetting I-val.")
                self.I = 0
                self.kP = kP
                self.kI = kI
                self.kD = kD
                self.max_I_val = max_I

    def set_setpoint(self, new_setpoint):
        """ changes the setpoint to a new value.
        new_setpoint: the new setpoint, in radians """
        # TODO: reset other values?
        print(f"old setpoint: {self.setpoint}\tnew: {new_setpoint}")
        self.setpoint = new_setpoint

    def set_process_variable(self, measurement, dt):
        """ measurement: the latest measured value
        dt: the time between this measurement and the last one """
        self.need_to_calc_y = True
        self.process_variable = measurement
        self.dt = dt

    def calculate_error_val(self):
        self.last_error = self.error_val
        self.error_val = self.setpoint - self.process_variable

    def calc_deriviate(self):
        self.D = (self.error_val - self.last_error) / self.dt

    def calc_proportional(self):
        self.P = self.error_val

    def calc_integral(self):
        # TODO: add min and max-val
        # Resets the integral term when passing the top position
        #if (self.last_error < 0 < self.error_val) or \
        #        (self.last_error > 0 > self.error_val):
        #    self.I = 0
        self.I += self.error_val
        if self.I > self.max_I_val:
            self.I = self.max_I_val
        elif self.I < -self.max_I_val:
            self.I = -self.max_I_val

    def get_control_variable(self):
        if not self.need_to_calc_y:
            return self.y
        self.calculate_error_val()
        self.calc_proportional()
        self.calc_integral()
        self.calc_deriviate()
        # TODO: try with squared P value
        self.y = self.P * self.kP + self.I * self.kI + self.D * self.kD
        self.need_to_calc_y = False
        return self.y

    #   How to use:
    #      Set control variable val + time between measurements
    #      use get_control_variable to get output value
"""

processes = []

for i in range(os.cpu_count()):
    print('registering process %d' % i)
    processes.append(Process(target=update_constants, args=(self)))
 processes.append(Process(target=set_setpoint))
    processes.append(Process(target=set_process_variable))
    processes.append(Process(target=calculate_error_val))
    processes.append(Process(target=calc_deriviate))
    processes.append(Process(target=calc_proportional))
    processes.append(Process(target=calc_integral))
    processes.append(Process(target=get_control_variable)) 


for process in processes:
	process.start()

for process in processes:
	process.join()


    """