import paho.mqtt.client as paho
from paho import mqtt


class MqttClient:

    def __init__(self, config):
        self._paho = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)

        self._paho.on_connect = default_on_connect
        self._paho.on_subscribe = default_on_subscribe
        self._paho.on_message = default_on_message
        self._paho.on_publish = default_on_publish

        # enable TLS for secure connection
        self._paho.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        # set username and password
        self._paho.username_pw_set(config.get("username") or "username", config.get("password") or "password")
        # connect to HiveMQ Cloud on port 8883 (default for MQTT)
        self._paho.connect(config.get("broker_hostname") or "127.0.0.1", config.get("broker_port") or 8883)

    def set_callback(self, name, callback):
        if hasattr(self, name):
            setattr(self._paho, name, callback)
        else:
            raise AttributeError()

    def subscribe(self, topic: str, qos: int = 1):
        self._paho.subscribe(topic=topic, qos=qos)

    def publish(self, topic: str, payload: str, qos: int = 1):
        self._paho.publish(topic=topic, payload=payload, qos=qos)

    def start(self):
        self._paho.loop_start()

    def stop(self):
        self._paho.loop_stop()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()


# setting callbacks for different events to see if it works, print the message etc.
def default_on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)


# with this callback you can see if your publish was successful
def default_on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))


# print which topic was subscribed to
def default_on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


# print message, useful for checking if it was successful
def default_on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
