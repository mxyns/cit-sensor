# cit-sensor

## instructions

requires: Python3 + pip3
```
    apt install libtiff5 libopenjp2-7
```

install python dependencies
```
    python3 -m pip install -r requirements.txt
```

user running the script needs to be in the `video` usergroup
```
     sudo usermod -aG video $USER
```

ensure camera is enabled on the rpi with `raspi-config` (needs reboot to work)
or try https://raspberrypi.stackexchange.com/a/14247
mount the camera peripheral with docker
```
    https://www.losant.com/blog/how-to-access-the-raspberry-pi-camera-in-docker
```

run the script once to generate the template configuration
run with `-c <config_path>` to change the config file path 
```
    python3 main.py
```

configure the app
remove the `REMOVE_THIS` line in the configuration file
run the app