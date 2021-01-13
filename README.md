# marvelmind-localization
This repo is used for tracking object via marvelmind indoor GPS

A nice tutorials: https://github.com/methylDragon/marvelmind-indoor-gps-tutorial/blob/master/01%20-%20Marvelmind%20Indoor%20GPS%20Tutorial.md

## Step 1: launch marvelmind indoor GPS
Please refer the official tutorials to setup device:
- section 4.2: https://marvelmind.com/pics/marvelmind_navigation_system_manual.pdf
- video tutorials: https://www.youtube.com/watch?v=sOce7B2_6Sk

## Step 2: receive localization information with ROS
1. Pre-requirements:
    - Ubuntu 20.04: https://releases.ubuntu.com/20.04/
    - ROS Noetic
      - http://wiki.ros.org/noetic/Installation/Ubuntu
      - http://wiki.ros.org/ROS/Tutorials
    - Anaconda: https://www.anaconda.com/products/individual#Downloads

2. Create a ROS workspace for marvelmind device
    - reference: https://marvelmind.com/pics/marvelmind_ROS.pdf
    - setup pipeline:
      - setup others:
        ```shell script
        sudo apt install git net-tools
        sudo apt install ros-noetic-rosbridge-server ros-noetic-rosbridge-suite
        ```
      - clone this repo:
        ```shell script
        cd ~
        git clone https://github.com/KuangHaofei/marvelmind-localization.git
        cd marvelmind-localization
        
        conda env create -f ./ros_env.yaml
        ``` 
      - setup conda & ROS environments:
        ```shell script
        cd ~
        conda activate ros_env
        git clone https://bitbucket.org/marvelmind_robotics/ros_marvelmind_package.git
        mkdir -p catkin_ws/src && cd catkin_ws/src
        mkdir marvelmind_nav
        
        mv ~/ros_marvelmind_package/* .
        mv ~/marvelmind-localization/launch ~/marvelmind-localization/scripts ./marvelmind_nav/
        sudo chmod -R 777 ./marvelmind_nav/scripts
        cd ~/catkin_ws
        catkin_make
        catkin_make install
        ```
            
3. Tracking & Communication with Robot Arm
    - Tracking
      - launch all device, please make sure the modem or a mobile beacon connect to your PC through usb.
      - start tracking:
        ```shell script
        sudo chmod 777 /dev/ttyACM0
        
        conda activate ros_env
        cd ~/catkin_ws
        source devel/setup.bash
        roslauch marvelmind_nav tracking.launch
        ```
      - open ros_bridge for Unity:
        ```shell script
        roslaunch rosbridge_server rosbridge_websocket.launch
        ``` 
    - Communication with Arm:  
      Open another terminator:
      ```shell script
      conda activate ros_env
      cd ~/catkin_ws
      source devel/setup.bash
      
      rosrun marvelmind_nav message_arm_server.py
      ```
