import os
import json
import logging
from datetime import datetime, timedelta, timezone

from setting import session
from models import CO2SensorEdge

import paho.mqtt.client as mqtt

from dotenv import load_dotenv

load_dotenv()
broker = os.getenv('MQTT_BROKER_IP')
port = int(os.getenv('MQTT_BROKER_PORT'))
topic = os.getenv('MQTT_TOPIC')

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

client_id = 'subscriber-k8s-server'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            logging.info("Connected to MQTT Broker!")
            mqtt_client.subscribe(topic)
        else:
            logging.error(f"Failed to connect, return code {rc}")

    def on_disconnect(client, userdata, rc):
        if rc != 0:
            logging.warning(f"Unexpected disconnection. rc: {rc}")

    def on_message(client, userdata, msg):
        try:
            payload = json.loads(msg.payload)
            payload['timestamp'] = datetime.strptime(payload['timestamp'], "%Y%m%d%H%M%S")
            
            logging.info(f"topic: {msg.topic} payload: {payload}")

            co2sensor_data = CO2SensorEdge()
            co2sensor_data.create_record(**payload)
            session.add(co2sensor_data)
            session.commit()
            logging.info(f"data commited!!")
        except Exception as e:
            logging.error(f"Error processing message: {e}")
            session.rollback()

    mqtt_client = mqtt.Client(client_id=client_id, protocol=mqtt.MQTTv311)
    # ハンドラー設定
    mqtt_client.on_message = on_message
    mqtt_client.on_disconnect = on_disconnect
    mqtt_client.on_connect = on_connect
    mqtt_client.connect(broker, port=port, keepalive=60)

    return mqtt_client


if __name__ == '__main__':
    mqtt_client = connect_mqtt()
    mqtt_client.loop_forever()

