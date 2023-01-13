import json
import sys

import PIL.Image
import paho.mqtt.client as paho

app_config_template = {
    "REMOVE_THIS": True,
    "sensor_id": "0",
    "camera": {
        "topic": "sensor/ir/%id",
        "tmp_save_path": "/tmp/camera_tmp.jpg",
        "frequency": 10.0,
        "qos": 1,
        "length": 640,
        "width": 360,
        "format": "JPEG",
        "image_mode": "RGB"
    },
    "mqtt": {
        "broker_hostname": "26630c3dc9f043aea09a7154577a5bba.s2.eu.hivemq.cloud",
        "broker_port": 8883,
        "username": "lebongrosnoeud",
        "password": "noeudnoeud",
        "clientid": "",
        "version": "MQTTv5"
    }
}


def load_or_template(config_target, config_template):
    try:
        with open(config_target) as file:
            config = json.load(file)
    except FileNotFoundError:
        with open(config_target, "w") as file:
            print(
                f"No configuration found at {config_target}! Template was written, please configure the module.")
            json.dump(config_template, file)
        sys.exit(1)

    if config.get("REMOVE_THIS") is not None:
        print("Please configure the app and remove the \"REMOVE_THIS\" field form the configuration!")
        sys.exit(1)

    return config


def load_app_config(config_target):
    config = load_or_template(config_target, app_config_template)

    try:
        sensor_id = str(config["sensor_id"])
        camera_topic = str(config["camera"]["topic"].replace("%id", sensor_id))
        camera_frequency = int(config["camera"]["frequency"])
        camera_qos = int(config["camera"]["qos"])
        assert 0 <= camera_qos <= 2
        camera_length = int(config["camera"]["length"])
        camera_width = int(config["camera"]["width"])
        assert camera_length > 0
        assert camera_width > 0
        camera_format = str(config["camera"]["format"])
        assert camera_format in PIL.Image.registered_extensions().keys() or camera_format in PIL.Image.registered_extensions().values()
        camera_image_mode = str(config["camera"]["mode"])
        assert camera_image_mode in PIL.Image.MODES

        camera_tmp_save_path = str(config["camera"]["tmp_save_path"])
        mqtt_broker_hostname = str(config["mqtt"]["broker_hostname"])
        mqtt_broker_port = int(config["mqtt"]["broker_port"])
        mqtt_username = str(config["mqtt"]["username"])
        mqtt_password = str(config["mqtt"]["password"])
        mqtt_clientid = str(config["mqtt"]["clientid"])
        mqtt_version = int(getattr(paho, config["mqtt"]["version"]))
    except RuntimeError:
        print("Configuration is missing parameters")
        sys.exit(1)

    return {
        "sensor_id": sensor_id,
        "camera": {
            "tmp_save_path": camera_tmp_save_path,
            "topic": camera_topic,
            "frequency": camera_frequency,
            "qos": camera_qos,
            "length": camera_length,
            "width": camera_width,
            "image_format": camera_format,
            "image_mode": camera_image_mode
        },
        "mqtt": {
            "broker_hostname": mqtt_broker_hostname,
            "broker_port": mqtt_broker_port,
            "username": mqtt_username,
            "password": mqtt_password,
            "clientid": mqtt_clientid,
            "version": mqtt_version
        }
    }
