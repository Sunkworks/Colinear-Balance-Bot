import math

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

    def update_constants(self):
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
        if abs(self.I) > self.max_I_val:
            self.I = self.max_I_val
        #print(self.I)

    def get_control_variable(self):
        self.calculate_error_val()
        self.calc_proportional()
        self.calc_integral()
        self.calc_deriviate()
        # TODO: try with squared P value
        y = self.P * self.kP + self.I * self.kI + self.D * self.kD
        return y

    #   How to use:
    #      Set control variable val + time between measurements
    #      use get_control_variable to get output value
