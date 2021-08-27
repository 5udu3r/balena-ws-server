import pytest
from unittest.mock import MagicMock, patch
from wshandler import WebsocketMQTTConnector

@pytest.mark.usefixtures('patch_mqtt')
@pytest.mark.asyncio
class TestWSServer:

    async def test_websocket_listens_on_correct_port(self, fake_websocket):
        expected_port = 12345
        bridge = WebsocketMQTTConnector('output', expected_port)
        await bridge.start()
        assert fake_websocket.port == expected_port

    async def test_sends_1_to_mqtt_when_receives_1(self, fake_mqtt_client, fake_websocket):
        bridge = WebsocketMQTTConnector('output', 1234)
        await bridge.start()
        await fake_websocket.send('1')
        assert fake_mqtt_client.get_publish_payload() == '1'

    async def test_sends_0_to_mqtt_when_receives_any_other_value(self, fake_mqtt_client, fake_websocket):
        bridge = WebsocketMQTTConnector('output', 1234)
        await bridge.start()
        await fake_websocket.send('0')
        assert fake_mqtt_client.get_publish_payload() == '0'
        await fake_websocket.send('xyz')
        assert fake_mqtt_client.get_publish_payload() == '0'


@pytest.fixture
def fake_websocket():

    class FakeWebsocket:
        async def serve(self, handler, host, port, *a, **kw):
            self.port = port
            self.handler = handler
        async def send(self, msg):
            async def fake_recv():
                return msg
            websocket_instance = MagicMock(recv=fake_recv)
            await self.handler(websocket_instance, None)
    
    ws = FakeWebsocket()

    with patch('wshandler.main.websockets', new=ws):
        yield ws

@pytest.fixture
def fake_mqtt_client():
    client = MagicMock()
    client.get_publish_payload = lambda: client.publish.call_args.kwargs.get('payload')
    client.get_publish_topic = lambda: client.publish.call_args.kwargs.get('topic')
    client.publish = MagicMock()
    return client

@pytest.fixture()
def patch_mqtt(fake_mqtt_client):
    fake_mqtt = MagicMock()
    fake_mqtt.Client = MagicMock(return_value=fake_mqtt_client)
    with patch('wshandler.main.mqtt', new=fake_mqtt):
        yield
