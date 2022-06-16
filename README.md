# racecar_pkgs
ROS Packages and software build instructions to setup the MIT race car used for teaching CSC477- Intro to Mobile Robotics

## Build Instructions
Once you have ubuntu 18.04 installed on  the Jetson, we can begin to setup ROS and build all the requuired packages. 
```
mkdir -p racecar_ws/src && cd racecar_ws/src 
catkin_init_workspace 
git clone https://github.com/rvl-lab-utoronto/racecar_pkgs
````
Build the packages 
```
catkin_make_isolated 
```
