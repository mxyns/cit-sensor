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
    parser.add_argument('-c', '--config', default="config.json",
                        help="Path to the configuration file")
    args = parser.parse_args()

    config = config_helper.load_app_config(args.config)
    mqtt_config = config["mqtt"]
    camera_config = config["camera"]

    print(config)

    with mqtt.MqttClient(config=mqtt_config) as client:
        with sensor.Camera() as camera:
            while True:
                loop_start = time.time()
                image = camera.still_capture_sync(resize=(
                    camera_config["length"], camera_config["width"]), format=camera_config["image_format"], save=camera_config["tmp_save_path"])

                buffered = BytesIO()
                image = image.convert(camera_config["image_mode"])
                image.save(buffered, format=camera_config["image_format"])
                img_b64 = base64.b64encode(buffered.getvalue())

                client.publish(camera_config["topic"], img_b64.decode(
                    "ascii"), camera_config["qos"])

                loop_duration = time.time() - loop_start
                need_to_sleep = camera_config["frequency"] - loop_duration
                time.sleep(max(0, need_to_sleep))
                if need_to_sleep <= 0:
                    print(
                        f"Warning, capture is taking too long to match the configured frequency of {camera_config['frequency']}s")


if __name__ == '__main__':
    main()
