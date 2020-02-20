class PID:
    def __init__(self):
        self.kP = 1
        self.kI = 1
        self.kD = 1

        self.P = 0
        self.I = 0
        self.D = 0
        self.setpoint = 0
        self.process_variable = 0
        self.dt = 0

        self.last_error = 0
        self.error_val = 0

    def set_setpoint(self, new_setpoint):
        """ changes the setpoint to a new value.
        new_setpoint: the new setpoint, in radians """
        # TODO: reset other values?
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
        # Resets the integral term when passing the top position
        if (self.last_error < 0 < self.error_val) or \
                (self.last_error > 0 > self.error_val):
            self.I = 0
        self.I += self.error_val

    def get_control_variable(self):
        self.calculate_error_val()
        self.calc_proportional()
        self.calc_integral()
        self.calc_deriviate()
        y = self.P * self.kP + self.I * self.kI + self.D * self.kD
        return y

    #   How to use:
    #      Set control variable val + time between measurements
    #      use get_control_variable to get output value
