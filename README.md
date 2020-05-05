# Colinear Balance Bot
Git Repo for Sunkworks' Colinear Balancing Robot.

## Code flow
### APIs that have to be used:
`mpu.py` - gets data from IMU and filters it, usage: `Sensor.get_angle()`,
returns estimated angle and time since last call.

`pid_class.py` - reads pid parameters from `PID.txt` every once in a while (when told to).
Main task is to return an output value to be fed into the odrives.
Angle values have to be fed in every run through the loop.  
`PID.txt` - stores PID parameters and `I_max` value.

`drive.py` - API that interacts with the odrives. Currently used through setting same speed on all motors.  
Planned feature: set rpm offset to the rest of the motors, to drive collinearly and turn.

`config.yml` - odrive config file. **Note:** When changing, make sure to also change `newConfig` to `true`.


##### Not yet finished:
`remote.py` - **TODO**: turn into API for dualshock controller


### Examples / Working implementations:
`manual_navigator.py` and `main.py` - An middleware and matching main loop.
Allows the user to control the robot manually with a DualShock (PlayStation) 4 controller.
Note: Due to the usage of `time.sleep()` in the main loop,
the delay between iterations isn't very precise (1ms ±0.5ms).
