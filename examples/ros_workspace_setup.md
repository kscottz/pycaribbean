== Setting up the ROS workspace

This assumes you have already installed ROS indigo and associated packages following [this tutorial](http://wiki.ros.org/indigo/Installation/Ubuntu). You will also need to install the [OpenNI drivers from occipital](https://github.com/occipital/OpenNI2).


This is a raw history dump of building ROS:
```
mkdir -p ./pycaribbean_ws/src/
cd pycaribbean_ws/src/
source /opt/ros/indigo/setup.bash 
catkin_init_workspace 
cd ..
catkin_make
source ./devel/setup.bash
wstool init
wstool set openni2_camera --git https://github.com/ros-drivers/openni2_camera
wstool update openni2_camera
wstool set openni2_launch --git git@github.com:ros-drivers/openni2_launch.git
wstool update openni2_launch
wstool set structure_sensor_processing --git git@github.com:kscottz/structure_sensor_processing.git
wstool update structure_sensor_processing
cd ..
catkin_make
```

To run the structure sensor.
```
cd cd Code/pycaribbean_ws/src/openni2_launch/launch/
roslaunch openni2.launch
rosrun image_view image_view image:=/camera/depth/image_rect
```
