
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

Your running container would be called **vrx_ros2** and based on the **dockerwater:humble image**

If instead you have already started the container in a terminal and want to open another terminal in the container, run the command
```
docker exec -u 0 -it vrx_ros2 bash
```

Now navigate inside your docker container to the ROS2 workspace, inside the workspace, you have to source ROS2 and build your repo:

```
source /opt/ros/humble/setup.bash
colcon build --merge-install
source install/setup.bash

```

By now you have everything set to run the launch scripts or work within your environment.

Try running the following laucnh file from docker in your vrx_ws

```
ros2 launch vrx_gz competition.launch.py world:=sydney_regatta
```

This would take some time to execute and open gazebo, but if it works then congratulations.

# Useful Docker tips?

if the container is running but you used `ctrl+d` and you want to reopen, then you type 

```
docker start vrx_ros2
docker attach vrx_ros2
```

To display running containers type:

```
docker ps -a
```

To remove a container

```
docker rm [container_name]
```
To delete images

```
docker images
docker rmi $[image_id]
```

To check logs of the container and changes

```
docker logs <container_id>
```

When needed to install some requiremnts in docker, then you can do it with `pip` or `apt-get` but it is necessary to build your image again, so

```
#Navigate to you Dockerfile
cd ../dockwater/humble/
#run the following to build the same docker image with same docker name
docker build -t dockwater:humble .
```
You don't need to exit the current container, changes take place even if you open another container instance

Also another technique especially works well to install python packages and dependencies is by creating a `requirements.txt` in the same directory of the `Dockerfile` with adding these to lines to `Dockfile`

```
# Copy the requirements file into the container Dockfile
COPY requirements.txt .

# Install the specific version and other dependencies in Dockfile
RUN pip install --no-cache-dir -r requirements.txt

```

Rebuild the image, the changes are saved in the image under same name

```
docker build -t dockwater:humble .

# docker commit could be used as well to save minor changes to the bash 

docker commit <container-id> dockwater:humble

```

# How to configure Visual Code with the container?

From Visual code extensions install `Dev Containers` and `Docker`. You can run `code .` from your workspace outside the container to open VS and then from the command palette `shift + ctrl + p` you can type `Dev Containers` and attach a running container

# How to open pycharm with the container?

You need to Navigate to `setting` and under `plugins` install `docker`. Then you can navigate to services `add service` and configure your docker. You always should be able to run from your workplace pycharm outside the container by `pycharm-community .`


# Useful links

[OceanAI](https://oceanai.mit.edu/moos-ivp/pmwiki/pmwiki.php?n=Main.HomePage)

[VRX_solved](https://github.com/Tinker-Twins/SINGABOAT-VRX/tree/main)


# How to build a new ROS2 pkg?

In your `ws` write in the terminal the following, while doing a `pkg` for dynamic positioning 

```
ros2 pkg create --build-type ament_python dynamic_positioning
```

Navigate the `pkg`

```
cd ~/ros2_ws/src/dynamic_positioning/dynamic_positioning
```

Create the file for your node

```
touch dynamic_positioning_node.py
chmod +x dynamic_positioning_node.py
```

Edit your node to publish and subscribe to topics, then update the `setup.py` file in the root of your `pkg` to register the executable node in the `entry_points` as follows:

```
entry_points={
    'console_scripts': [
        'dynamic_positioning_node = dynamic_positioning.dynamic_positioning_node:main',
    ],
},

```
Now you can build and run the `pkg` by using `ros2 run` as follows

```
cd ~/ros2_ws
colcon build --merge-install --packages-select dynamic_positioning
source install/setup.bash
ros2 run dynamic_positioning dynamic_positioning_node

```

To listen to topics:

```
ros2 topic list

```

To make a launch file inside the `pkg` do the following and generate the launch describtion

```
mkdir launch
touch launch/dynamic_positioning.launch.py
```

And thus one call the new launch file by: 

```
ros2 launch dynamic_positioning dynamic_positioning.launch.py

```
However, make sure that `setup.py` is set correctly where `pkg` should be added to the `data_files` entry and then sourced and build before use.




## Authors
Ali Srour <br>


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
