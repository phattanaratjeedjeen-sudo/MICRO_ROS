## Overview
This package is built for implementing micro ros in ESP32 with platformIO to control hardware using CAN BUS propocal.
>note: 
>Test environment: ros2 jazzy with ubuntu 24.04 

**Reference**
- [MKS-SERVO45D-57D](https://github.com/makerbase-motor/MKS-SERVO42D-57D)
- [micro-ROS](https://github.com/micro-ROS)

**File Structure**
```bash
~/uros_ws/firmware
.
├── COLCON_IGNORE
└── Hardware_control    --> Project
    ├── include
    │   ├── header.h
    ├── lib
    ├── platformio.ini
    ├── src
        └── main.cpp    --> Microcontroller firmware
```
## Micro ros setup
```bash
source /opt/ros/jazzy/setup.bash
```

Ceate workspace
```bash
mkdir uros_ws && cd uros_ws
```

```bash
git clone -b jazzy https://github.com/micro-ROS/micro_ros_setup.git src/micro_ros_setup
```

Install rosdep
```bash
sudo apt update
sudo apt install python3-rosdep
sudo rosdep init
```

```bash
rosdep update && rosdep install --from-paths src --ignore-src -y
```

```bash
colcon build
source install/setup.bash
```

Build micro ros agent
```bash
ros2 run micro_ros_setup create_agent_ws.sh
ros2 run micro_ros_setup build_agent.sh
source install/local_setup.sh
```

## Install platformIO for vscode

platform installation stuck because `"PlatformIO: Can not find working Python 3.6+ Interpreter"` to fix this

```bash
sudo apt update
sudo apt install python3-venv
```
then restart vscode

link the command so it works everywhere
```bash
mkdir -p /usr/local/bin
sudo ln -s ~/.platformio/penv/bin/platformio /usr/local/bin/platformio
sudo ln -s ~/.platformio/penv/bin/pio /usr/local/bin/pio
sudo ln -s ~/.platformio/penv/bin/piodebuggdb /usr/local/bin/piodebuggdb
```

```bash
# check platformIO version ( 6.1.0 or greater)
pio --version
```

```bash
sudo apt update
sudo apt install -y git cmake python3-pip
```

## Micro ros for arduino

create directory to store firmware for esp32
```bash
cd ~/uros_ws
mkdir firmware
cd firmware

# prevent build this directory
touch COLCON_IGNORE
```

Open VS Code, go to the PlatformIO Home, click "New Project", and when it asks for the location, uncheck "Use Default Location" and select your new `~/uros_ws/firmware` folder.

update .gitignore
```bash
echo ".pio/" >> .gitignore
```

check point
```bash
cd ~/uros_ws && ls -a
# .  ..  build  firmware  .gitignore  install  log  README.md  src
```

```bash
cd firmware
# .  ..  COLCON_IGNORE  Hardware_control
```

edit `platformio.ini` inside platformIO project

to check
```bash
cd Hardware_control
cat platformio.ini
```

must get output like this
```bash
; PlatformIO Project Configuration File
;
;   Build options: build flags, source filter
;   Upload options: custom upload port, speed and extra flags
;   Library options: dependencies, extra library storages
;   Advanced options: extra scripting
;
; Please visit documentation for the other options and examples
; https://docs.platformio.org/page/projectconf.html

[env:esp32dev]
platform = espressif32
board = esp32dev
framework = arduino

; 1. Add the micro-ROS library dependency
lib_deps =
    https://github.com/micro-ROS/micro_ros_platformio


; 2. Set the ROS 2 distribution (match your Ubuntu ROS 2 version)
board_microros_distro = jazzy

; 3. Set the transport (serial is easiest for getting started)
board_microros_transport = serial

; 4. Optional: Increase the monitor speed for debugging
monitor_speed = 115200
```

Now to proceed with the PlatformIO workflow:
```bash
cd Hardware_control
pio lib install
```

```bash
pio run
```

you will get
```bash
Processing esp32dev (platform: espressif32; board: esp32dev; framework: arduino)
-------------------------------------------------------------------------------------------------------------
Verbose mode can be enabled via `-v, --verbose` option
CONFIGURATION: https://docs.platformio.org/page/boards/espressif32/esp32dev.html
PLATFORM: Espressif 32 (6.13.0) > Espressif ESP32 Dev Module
HARDWARE: ESP32 240MHz, 320KB RAM, 4MB Flash
DEBUG: Current (cmsis-dap) External (cmsis-dap, esp-bridge, esp-prog, iot-bus-jtag, jlink, minimodule, olimex-arm-usb-ocd, olimex-arm-usb-ocd-h, olimex-arm-usb-tiny-h, olimex-jtag-tiny, tumpa)
PACKAGES: 
 - framework-arduinoespressif32 @ 3.20017.241212+sha.dcc1105b 
 - tool-esptoolpy @ 2.41100.0 (4.11.0) 
 - toolchain-xtensa-esp32 @ 8.4.0+2021r2-patch5
LDF: Library Dependency Finder -> https://bit.ly/configure-pio-ldf
LDF Modes: Finder ~ chain, Compatibility ~ soft
Installing importlib-resources with pip at PlatformIO environment
/home/wa/.platformio/penv/bin/python -m pip install importlib-resources
Requirement already satisfied: importlib-resources in /home/wa/.platformio/penv/lib/python3.12/site-packages (6.5.2)
Installing pyyaml with pip at PlatformIO environment
/home/wa/.platformio/penv/bin/python -m pip install pyyaml
Requirement already satisfied: pyyaml in /home/wa/.platformio/penv/lib/python3.12/site-packages (6.0.3)
Installing markupsafe==2.0.1 with pip at PlatformIO environment
/home/wa/.platformio/penv/bin/python -m pip install markupsafe==2.0.1
Requirement already satisfied: markupsafe==2.0.1 in /home/wa/.platformio/penv/lib/python3.12/site-packages (2.0.1)
Installing empy==3.3.4 with pip at PlatformIO environment
/home/wa/.platformio/penv/bin/python -m pip install empy==3.3.4
Requirement already satisfied: empy==3.3.4 in /home/wa/.platformio/penv/lib/python3.12/site-packages (3.3.4)
Configuring esp32dev with transport serial
Downloading micro-ROS dev dependencies
ament_cmake pull failed: 
From https://github.com/ament/ament_cmake
 * branch            jazzy      -> FETCH_HEAD
hint: You have divergent branches and need to specify how to reconcile them.
hint: You can do so by running one of the following commands sometime before
hint: your next pull:
hint: 
hint:   git config pull.rebase false  # merge
hint:   git config pull.rebase true   # rebase
hint:   git config pull.ff only       # fast-forward only
hint: 
hint: You can replace "git config" with "git config --global" to set a default
hint: preference for all repositories. You can also pass --rebase, --no-rebase,
hint: or --ff-only on the command line to override the configured default per
hint: invocation.
fatal: Need to specify how to reconcile divergent branches.

======================================== [FAILED] Took 4.08 seconds ========================================
```

solve by
```bash
git config --global pull.rebase false
```

then clean the broken state
```bash
rm -rf .pio/libdeps/esp32dev/micro_ros_platformio
```

build again
```bash
pio run
```

plug ESP32
```bash
# list usb connected device
ls /dev/ttyUSB*
```

enable permission permanent
```bash
sudo usermod -a -G dialout $USER
```
- `usermod` : Short for User Modify. This is the utility used to change a user's account settings.
- `-a` : Stands for **Append**, It tells Ubuntu to add you to a new group 
- `G` : Stands for **Groups**. It tells the command that the following word `dialout` is the name of the group you want to join.
- `dialout` : This is a specific system group in Linux that "owns" serial port
- `$USER` : This is a shortcut (an environment variable) that automatically fills in your username

```bash
# active it
newgrp dialout
# recheck
groups
# output should have "dialout"
```

```bash
# flash the firmware
pio run --target upload
```

## Run agent

```bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyUSB0
```

>note: 
>must flash firmware before run agent