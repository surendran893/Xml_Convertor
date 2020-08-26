import paho.mqtt.client as mqClient
import time
import datetime as date

def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
    print("Message string ", str(message.payload))

def on_disconnect(client, userdata, flags, rc=0):
    m="DisConnected flags"+"result code "+str(rc)
    print(m)

def on_connect(client, userdata, flags, rc):
    print("Connected flags ",str(flags),"result code ",str(rc))
    client.subscribe('/vehicle_status/adccsim1')

def on_publish(client,userdata,result):
    print("data published \n", result)
    pass

def on_subscribe(client, userdata, mid, granted_qos):
    client.subscribe(self._topic_sub)

broker_address="10.8.0.1"

client = mqClient.Client("digi_mqtt_test")
client.username_pw_set(username="adccISIT",password="3Q8eaKGAHl9T1MR8N9C7VKRfQfpzDIMumIxmh3LOfKw6kd2YasVW0B1HGf67LGrX")
client.connect(broker_address, 1883)

client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
# client.on_log = on_log
client.on_subscribe = on_subscribe

# client.loop_start()
# print("Loop Started")
# time.sleep(1)
# # client.subscribe('/vehicle_status/adccsim1')
# for i in range(1, 100):
#     client.subscribe(topic="/vehicle_status/adccsim1" , qos=0)
#     time.sleep(2)

# client.loop_stop()
# client.on_disconnect()

client.loop_forever()