import paho.mqtt.client as mqtt
import websockets

class WebsocketMQTTConnector:

    def __init__(self, mqtt_topic, wsport):
        self.__mqtt = mqtt.Client()
        self.__topic = mqtt_topic
        self.__wsport = wsport

    async def start(self):
        await websockets.serve(self.__handle_websocket_msg, '0.0.0.0', self.__wsport, ping_interval=None)

    async def __handle_websocket_msg(self, websocket, path):
        try:
            user_input = await websocket.recv()
            message = sanitize_input(user_input)
            self.__mqtt_publish(message)
        except:
            self.__mqtt_publish('0')

    def __mqtt_publish(self, msg):
        self.__mqtt.connect('mqtt', 1883)
        self.__mqtt.publish(topic=self.__topic, payload=msg)
        self.__mqtt.disconnect()


def sanitize_input(message):
    if message == '1':
        return '1'
    return '0'
