import random
import paho.mqtt.client as mqtt
import threading
import os
class MqttServer:
    MQTT_BROKER_HOST = "213.202.219.45"
    MQTT_BROKER_PORT = 1883
    MQTT_TOPIC = "lazys_epaper_byte_stream"
    
    def publish_file(self):
        with open("./uploads/byte_stream.txt", "rb") as file:
            print("MQTT 更新中")
            data = file.read()
            # for i in range(1, 101):
            #     print(i, "->")
            #     data_chunk = bytes([i]) + data[(i-1) * 1920: i * 1920]
            #     self.client.publish("lazys_epaper_byte_stream", payload=data_chunk, qos=2, retain=False)

            self.client.publish("lazys_epaper_byte_stream", payload=data, qos=2, retain=False)
        
    def on_connect(client, userdata, flags, rc):
        print("Connected to MQTT Broker")


    client = mqtt.Client("E-Paper-Server")
    client.on_connect = on_connect
    client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 60)

    def mqtt_thread(self):
        self.client.loop_forever()

