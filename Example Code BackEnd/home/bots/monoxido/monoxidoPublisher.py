import paho.mqtt.publish as publish
import random
import time
import json

from paho.mqtt import client as mqtt_client

with open("./home/bots/config.json") as config_file:
    config = json.load(config_file)

mqtt_config = config["mqtt"]

broker_address = mqtt_config["broker"]
broker_tcp_port = mqtt_config["tcpPort"]
broker_websocket_port = mqtt_config["webSocketPort"]
topic="/casa/interior/sensores/monoxido"
topicLuz="/casa/interior/actuadores/luces"
topicAlarm="/casa/interior/actuadores/alarma"
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = mqtt_config["username"]
password = mqtt_config["password"]

def connect_mqtt():
    def on_connect(client, userdata, flags, returnCode):
        if returnCode == 0:
            print("Connected to MQQT Broker!")
        else:
            print("Failed to connect %d\n", returnCode)

    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker_address, broker_tcp_port)
    return client

def publish(client):
    while True:
        time.sleep(60)
        #msg = "0"
        msg = random.randint(900,1500)
        #value = random.randint(0, 100)
        if msg>1200:
            client.publish(topicAlarm,1)
            client.publish(topicLuz,1) 
        else:
            client.publish(topicAlarm,0)
            client.publish(topicLuz,0) 
        client.publish(topic,msg)



def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)

if __name__ == '__main__':
    run()