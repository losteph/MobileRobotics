#!/bin/bash

xhost +
docker run -it --rm --net host --ipc host --privileged \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v ~/.Xauthority:/root/.Xauthority \
    -e DISPLAY=$DISPLAY \
    -e XAUTHORITY=$XAUTHORITY \
    #--gpus all \ # scommentare se avete una scheda grafica esterna
    #--env="NVIDIA_DRIVER_CAPABILITIES=all" \ # e non la legge
    #--env="QT_X11_NO_MITSHM=1" \
    -v "$(pwd)/ros_ws/:/root/ros_workspace" \
    --name project_container \
    ros:project bash
