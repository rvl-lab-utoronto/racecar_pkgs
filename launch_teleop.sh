#!/bin/bash

sudo chmod 777 /dev/ttyACM* /dev/input/js*
source ../../devel_isolated/setup.bash
roslaunch racecar teleop.launch
