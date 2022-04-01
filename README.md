# Colinear Balance Bot
Git Repo for Sunkworks' Colinear Balancing Robot.

## Basic operation
To operate the robot two criteria must be met: 
The battery must be charged to at least 17v or 3.4v/cell, and the user must have a dualshock 4 remote.

The robot is powered on by connecting the XT60-connector and flicking the switch, the booting procedure will then commence. Booting takes a while since DHCP has not been disabled, be patient. One of the indicator LEDs on top of the robot will briefly turn green, indicating that the first script is running.

White-blue alternating flashing indicates that Bluetooth pairing is about to begin. Press and hold the SHARE and PS buttons on the dualShock remote until the remote begins to flash white and then release. Pairing may take some time but once it is complete an indicator on the robot will illuminate in solid blue and so will the remote.

For the next step, to calibrate the ODrives the robot must be placed in a way so the wheels do NOT touch the ground. Preferably prop the axel ends up on boxes or books. The calibration procedure is then started by pressing the TRIANGLE button on the remote. An indicator LED will turn yellow signifying that the robot is searching for & connecting to the ODrives. This also takes time. If the yellow indicator starts flashing red the battery voltage is too low and it will not proceed. If the battery is charged well enough another indicator will light up showing the current charge. It ranges from green (100%, 21v) to red (0%, 17v). The yellow indicator turns pink to signify that the calibration procedure has begun. A loud beep will be emitted and the motors will turn, this is normal.

Once the calibration procedure has finished an indicator will illuminate in white. Place the robot on the running surface and hold it as straight as possible, then press the X button on the remote for it to start balancing. The robot may jerk at this stage so hold it firm while allowing it to move and gain its balance. The heartbeat will flash indicating code execution.

Once balancing the left joystick controls forward and reverse motion in addition to the collinear motion. The right stick controls rotation. To stop the robot hold down the SQUARE button, it will go lame so make sure to hold it still. The heartbeat indicator will turn red indicating a stop. The X button on the remote can now be pressed to start balancing again, make sure to hold it upright.

The robot will automatically stop if the angle is to great i.e. in a fall. This is also indicated by the heartbeat indicator turning red and can be reset with the X button on the remote. If all indicators turn solid red an unhandled error has been thrown and all code execution stops. The only way to reset this without ssh or keyboard & mouse is through a reboot.

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

Install guide Raspberry Pi OS
----------------

Install required packages for Raspberry Pi OS

```
# apt install libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev python-dev
```
Install pip packages

```
# pip3 install -r requirements.txt
```
