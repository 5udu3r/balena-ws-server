### Balena Blocks: Websocket binary server

Listens to websocket messages and passes them on to internal MQTT server. Ideally used with a reverse-proxy block.
Only accepts '1' and '0' as input messages, everything else will be sent as '0' to MQTT.

___Usage a block___

Add the following to your `docker-compose.yaml`:

```yaml
  ws-server:
    build: ./ws-server
    restart: always
    ports:
      - "8765:8765"
    environment: 
      - OUTPUT=button_1
```

___Available variables___

- `OUTPUT`: topic, under which to publish the output

___Environment variables defaults___

- `OUTPUT`: output

___Tests___

```bash
$ PIPENV_VENV_IN_PROJECT=1 pipenv install --dev
$ pipenv shell
$ pytest -vs
```

___Standalone usage___

```python
import asyncio
import os
from wshandler import WebsocketMQTTConnector

if __name__ == '__main__':
    topic = os.environ.get('OUTPUT', 'output')
    bridge = WebsocketMQTTConnector(mqtt_topic=topic, wsport=8765)
    asyncio.get_event_loop().run_until_complete(bridge.start())
    asyncio.get_event_loop().run_forever()
```

> N.B. mqtt connects to host 'mqtt' on port 1883
