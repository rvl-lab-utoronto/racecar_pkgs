# racecar_pkgs
ROS Packages and software build instructions to setup the MIT race car used for teaching CSC477- Intro to Mobile Robotics

## Dependencies
- Ubuntu 20.04 
- ROS noetic (refer: install_ROS.sh)
- VSCode (optional)(referP: install_VSCode.sh)
- TP-link ([wifi dongle drivers](https://github.com/morrownr/8821au-20210708))

Use install_dependcencies.sh script to install ROS dependencies for the source code. 

## Build Instructions
```
mkdir -p racecar_ws/src && cd racecar_ws/src 
catkin_init_workspace 
git clone https://github.com/rvl-lab-utoronto/racecar_pkgs
````
Build the packages 
```
catkin_make 
```
or 
```
catkin_make_isolated
```


run teleop 
```
./launch_teleop.sh
```
