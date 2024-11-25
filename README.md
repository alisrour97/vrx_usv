
# How to install Docker on your host machine?

There is a convinient script that facilitate everything
```
curl -fsSL get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```
We suggest to use docker as a non-root user, that way your build folder won't be owned by root after using docker. In a new terminal run
```
# Create docker group (may not be required)
sudo groupadd docker
# Add your user to the docker group.
sudo usermod -aG docker $USER
```
**Now log out and in again before using docker!!**

# Docker Image?

Inorder to have all the necessary dependencies from linux version, python packages etc.. You need to create a docker image. Luckily on [Docker Hub](https://hub.docker.com/) there is already an image that contains the dependencies, so clone and run:

```
git clone https://github.com/Field-Robotics-Lab/dockwater.git
cd dockwater
./build.bash humble

```
**Now you have the image installed, you can attach it to your cloned repo in ROS2 work space and do your work inside a container**

# Setup your ROS2 

```
mkdir -p vrx_ws/src
cd vrx_ws/src
git clone http://gitlab.sts.seaowl.com:9004/asr/vrx.git
```
You dont have to build your project yet. We need to start a docker container and source/build the project there so

```
cd ..
cat> create_vrx_ros2.sh
```
In the created shell script type the following:

```
# enable access to xhost from the container
xhost +

# Run docker and open bash shell
docker run -it --privileged \
--env=LOCAL_USER_ID="$(id -u)" \
--env "DISPLAY" \
-v $(pwd):/home/user/vrx_ws:rw \
--network host \
--workdir="/home/user/" \
--name=vrx_ros2 dockwater:humble
```

This will enable you to start a docker container for your workspace. This script can be called from terminal as follows:

```
./create_vrx_ros2.sh
```

Your running container would be called **vrx_ros2** and based on the dockerwater:humble image








## Tutorials from the OSRF-VRX
# Virtual RobotX (VRX)
This repository is the home to the source code and software documentation for the VRX simulation environment, which supports simulation of unmanned surface vehicles in marine environments.
* Designed in coordination with RobotX organizers, this project provides arenas and tasks similar to those featured in past and future RobotX competitions, as well as a description of the WAM-V platform.
* For RobotX competitors this simulation environment is intended as a first step toward developing tools prototyping solutions in advance of physical on-water testing.
* We also welcome users with simulation needs beyond RobotX. As we continue to improve the environment, we hope to offer support to a wide range of potential applications.

## Now supporting Gazebo Sim and ROS 2 by default
We're happy to announce with release 2.0 VRX has transitioned from Gazebo Classic to the newer Gazebo simulator (formerly [Ignition Gazebo](https://www.openrobotics.org/blog/2022/4/6/a-new-era-for-gazebo)). 
* Gazebo Garden and ROS 2 are now default prerequisites for VRX.
* This is the recommended configuration for new users.
* Users who wish to continue running Gazebo Classic and ROS 1 can still do so using the `gazebo_classic` branch of this repository. 
  * Tutorials for VRX Classic will remain available on our Wiki.
  * VRX Classic will transition from an officially supported branch to a community supported branch by Spring 2023.

## The VRX Competition
The VRX environment is also the "virtual venue" for the [VRX Competition](https://github.com/osrf/vrx/wiki). Please see our Wiki for tutorials and links to registration and documentation relevant to the virtual competition. 

![VRX](images/sydney_regatta_gzsim.png)
![Ubuntu CI](https://github.com/osrf/vrx/workflows/Ubuntu%20CI/badge.svg)

## Getting Started

 * Watch the [Release 2.3 Highlight Video](https://vimeo.com/851696025).
 * The [VRX Wiki](https://github.com/osrf/vrx/wiki) provides documentation and tutorials.
 * The instructions assume a basic familiarity with the ROS environment and Gazebo.  If these tools are new to you, we recommend starting with the excellent [ROS Tutorials](http://wiki.ros.org/ROS/Tutorials)
 * For technical problems, please use the [project issue tracker](https://github.com/osrf/vrx/issues) to describe your problem or request support. 
