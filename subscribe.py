import paho.mqtt.client as mqtt
import time
import json
from threading import Thread
from simulation_service import simulation_service as mt

from service import node_service as node
from service import edge_service as edge
from service import route_service as route
from service import type_service as type_
from service import config_service as config
from service import net_service as net
from service import traci_service as traci


def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    m_decode=str(message.payload.decode("utf-8","ignore"))
    m_in=json.loads(m_decode)
    print (type(m_in))
    print (m_in)
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
    initlization_.append(m_in['Header']['FrameId'])
    initlization_.append(m_in['Header']['SequenceId'])
    initlization_.append(m_in['MissionMode'])
    initlization_.append(m_in['MissionSequence'])
    initlization_.append(m_in['VehicleId'])
    initlization_.append(m_in['DestinationLinkId'])
    Thread(target = mt.trigger_simulation(initlization_)).start()

def stop_client(client):
    client.loop_stop()
    print("Client Loop Stopped")

def publish_data(client1, vehicle_status, topic="/vehicles_fleet/SIM_vehicle_status/adccsim11"):
    print("Publishing message to topic","/vehicles_fleet/SIM_vehicle_status/adccsim11")
    client1.publish(topic, vehicle_status)

def subscribe_data(client, topic="/vehicles_fleet/SIM_mission_request/adccsim11"):
    # /mission_request/adccsim11
    print("Subscribing to topic","/vehicles_fleet/SIM_mission_request/adccsim11")
    client.subscribe(topic)

def initlization():
    node1 = node.node_service
    edge1 = edge.edge_service
    type1 = type_.type_service
    route1 = route.route_service
    config1 = config.config_service
    net1 = net.net_service
    traci1 = traci.traci_service


    file_path = "C:/WorkSpace/Renault/R_AE/Application/sumo-1.6.0/sumo/"
    route_fileName = "my_route.rou.xml"
    net_fileName = "my_net.net.xml"
    node_fileName = "my_nodes.nod.xml"
    edge_fileName = "my_edge.edg.xml"
    type_fileName = "my_type.type.xml"
    config_fileName = "test_maptry.sumocfg"
    output_fileName = "tripinfo.xml"
    gui_fileName = "guiInfo.xml"


    nodeXmlFile = file_path + node_fileName
    edgeXmlFile = file_path + edge_fileName
    typeXmlFile = file_path + type_fileName
    routeXmlFile =  file_path + route_fileName
    configXmlFile = file_path + config_fileName
    netXmlFile = file_path + net_fileName
    outputXmlFile = file_path + output_fileName

    node1.node_data(nodeXmlFile)
    edge1.edge_data(edgeXmlFile)
    type1.type_data(typeXmlFile)
    config1.config_data(configXmlFile, net_fileName, route_fileName, gui_fileName)

    return [file_path, nodeXmlFile,edgeXmlFile,typeXmlFile,routeXmlFile,configXmlFile,netXmlFile,outputXmlFile]

global  initlization_
initlization_ = initlization()   
broker_address="10.8.0.1" 
print("creating new instance")
client = mqtt.Client("P1-test")
client.username_pw_set("adccISIT", "3Q8eaKGAHl9T1MR8N9C7VKRfQfpzDIMumIxmh3LOfKw6kd2YasVW0B1HGf67LGrX")
print("connecting to broker")
client.on_message=on_message
client.connect(broker_address, 1883, 60)

client.loop_start()
subscribe = subscribe_data(client)
while True:
    if subscribe != None:
        print("Subscribed data is ",subscribe)
        