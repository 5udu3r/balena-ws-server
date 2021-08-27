import asyncio
import os
from wshandler import WebsocketMQTTConnector

if __name__ == '__main__':
    topic = os.environ.get('OUTPUT', 'output')
    bridge = WebsocketMQTTConnector(mqtt_topic=topic, wsport=8765)
    asyncio.get_event_loop().run_until_complete(bridge.start())
    asyncio.get_event_loop().run_forever()
