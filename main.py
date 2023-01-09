import argparse
import base64
import time
from io import BytesIO

import config as config_helper
import mqtt
import sensor


def main():

    parser = argparse.ArgumentParser(
        prog='SensorCIT',
        description='Capture images from a PiCamera and publish it to a MQTT Broker',
        epilog='Hi DevOps Team!')
    parser.add_argument('-c', '--config', default="config.json", help="Path to the configuration file")
    args = parser.parse_args()

    config = config_helper.load_app_config(args.config)
    mqtt_config = config["mqtt"]
    camera_config = config["camera"]

    with mqtt.MqttClient(config=mqtt_config) as client:
        with sensor.Camera() as camera:
            image = camera.still_capture_sync(resize=(640, 360), save=camera_config["tmp_save_path"])

            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            img_b64 = base64.b64encode(buffered.getvalue())

            client.publish(camera_config["topic"], img_b64.decode("ascii"))

            time.sleep(camera_config["frequency"])


if __name__ == '__main__':
    main()
