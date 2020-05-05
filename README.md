# Colinear-Balance-Bot
Git Repo for Sunkwork's Colinear Balancing Robot.

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

### Current main code:
The files that interact with the APIs in various ways.

`main.py` - loop which tries to balance the robot in place.
A good example of a non-interrupt based way of interacting with the APIs.
