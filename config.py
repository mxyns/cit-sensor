import json
import sys
import paho.mqtt.client as paho

app_config_template = {
    "REMOVE_THIS": True,
    "sensor_id": "0",
    "camera": {
        "topic": "sensor/ir/%id",
        "frequency": 1.0,
        "tmp_save_path": "./tmp/capture.jpg"
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
            print(f"No configuration found at {config_target}! Template was written, please configure the module.")
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
            "frequency": camera_frequency
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
