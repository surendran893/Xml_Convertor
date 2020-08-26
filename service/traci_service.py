from __future__ import print_function
from __future__ import absolute_import
import os
import sys
import optparse
from sumolib import checkBinary  # Checks for the binary in environ vars
import traci
import sumolib

import datetime as date
import re
import json

import paho.mqtt.client as mqtt
import time
import utm


class traci_service():

    def get_options():
        opt_parser = optparse.OptionParser()
        opt_parser.add_option("--nogui", action="store_true",
                            default=False, help="run the commandline version of sumo")
        options, args = opt_parser.parse_args()
        return options

    def run(file_path):
        step=0
        json_output = []
        while traci.simulation.getMinExpectedNumber() > 0:
            print("step", step)
            
            traci.simulationStep()
            typeID = "ZoeEV"
            ID = "adcc1"
            
            print("vehicle", traci.vehicle.getIDList())
            
            if len(traci.vehicle.getIDList()) > 0:
                regex_remove = str(traci.vehicle.getIDList())
                ID = re.sub('[\W\_]','', regex_remove)
                print("vehicletypes", traci.vehicletype.getIDList())
                print("vehicletype count", traci.vehicletype.getIDCount())
                print("vehicle count", traci.vehicle.getIDCount())
                print("examining", typeID)
                print("Vehicle ID : ", traci.vehicle.getTypeID(ID))
                print("Speed : ", traci.vehicle.getMaxSpeed(ID))
                # print("ROUTE : ", traci.vehicle.getRoute(ID))
                print("Mode Status : ", traci.vehicle.isStopped(ID))
                print("lane position : ", traci.vehicle.getLanePosition(ID))
                print("location : ", traci.vehicle.getPosition(ID))
                # print("TAXI : ", traci.vehicle.getTaxiFleet(ID))
                print("MotionStatus :  ", traci.vehicle.getRoutingMode(ID))
                print("DestinationLinkID :  ", traci.vehicle.getRoadID(ID))
                print("Heading :  ", traci.vehicle.getAngle(ID))
                heading = traci.vehicle.getAngle(ID)
                Speed = traci.vehicle.getMaxSpeed(ID)
                DestinationLinkId =  traci.vehicle.getRoadID(ID)
                MissionSequence = 123
                MissionAcknowledgement = 12
                MissionMode =1
                FrameId = 1
                SequenceId = ID[4: len(ID)] 
                ArrivalStatus = 1
                MotionStatus = traci.vehicle.getRoutingMode(ID)
                Availability = 2
                utc = date.datetime.now()
                ModeStatus = traci.vehicle.isStopped(ID)

                if len(traci.vehicle.getIDList()) > 0:
                    lon, lat = traci.vehicle.getPosition(ID)
                    # lon, lat = traci.simulation.convertGeo(x, y)
                    print("Lattitude is {} and Longiture is {}".format(lat, lon))
                    x2, y2 = traci.simulation.convertGeo(lon, lat, fromGeo=True)

                header = { "UtcTimestamp" : str(utc) , "FrameId" : FrameId, "SequenceId": SequenceId}
                Location = {"Latitude" : lat, "Longitude" : lon}

                output = { 
                
                "Header": header, "VehicleId" : ID.upper(), "ArrivalStatus" : ArrivalStatus, "MotionStatus": MotionStatus,
                "ModeStatus" : ModeStatus, "Location" :  Location, "Heading" : heading, "Speed" : Speed, "Availability" : Availability,
                "DestinationLinkId" : DestinationLinkId, "MissionSequence" : MissionSequence,
                "MissionMode" : MissionMode, "MissionAcknowledgement" : MissionAcknowledgement
                }
                json_output.append(output)

                step+=1
        
        fileName = file_path+"addc1.txt"
        with open(fileName, 'w', encoding='utf-8') as jsonfile:
            json.dump(json_output, jsonfile, ensure_ascii=False, indent=4)

        print("simulation complted")
        traci.simulationStep()
        print("simulation not stoped")
        traci.close()
        print("simulation stopped")

    
    def run_temp(file_path):
        step=0
        json_output = []
        json_dict = {}
        while traci.simulation.getMinExpectedNumber() > 0:

            traci.simulationStep()

            if len(traci.vehicle.getIDList()) > 0:

                split_veh_id = str(traci.vehicle.getIDList()).replace("(","").replace(")","").replace("'","").split(",")
                for veh_id in split_veh_id:
                    if veh_id is not '':
                        regex_remove = str(veh_id)
                        ID = re.sub('[\W\_]','', regex_remove)

                        heading = traci.vehicle.getAngle(ID)
                        Speed = traci.vehicle.getMaxSpeed(ID)
                        DestinationLinkId =  traci.vehicle.getRoadID(ID)
                        SequenceId = ID[4: len(ID)] 
                        MotionStatus = traci.vehicle.getRoutingMode(ID) # 0- Forward, 1- reverse, 2- Unavailable
                        utc = date.datetime.now()
                        ModeStatus = 1 #0-Manaul , 1 - Automatic, 2-Helpome , 3, Safety Mode
                        lon, lat = traci.vehicle.getPosition(ID)
                        FrameId = 1 # Default
                        MissionMode =1 #  1- Robo Taxi, 2-Stop Mission, 3-Valet service, 4- Telop Mission

                        MissionSequence = 123
                        # MissionAcknowledgement = int(traci.vehicle.isStopped(ID) == False) # 0- refused, 1-accepted , 3- unavilable
                        MissionAcknowledgement = 3 if traci.vehicle.isStopped(ID) == False else 1 if traci.vehicle.isStopped(ID) == True else 0

                        #Unavaialble will be send while in idle state
                        ArrivalStatus = int(traci.vehicle.isStopped(ID) == True) # 0- Not Arrived, 1- Arrived, 2- Arival unavailable 

                        Availability = 1 if traci.vehicle.isStopped(ID) == False else 2 if traci.vehicle.isStopped(ID) == True else 3# 1- Vehicle is In Mission, 2- Available, 3 - Unavailable.

                        header = { "UtcTimestamp" : str(utc) , "FrameId" : FrameId, "SequenceId": SequenceId}
                        Location = {"Latitude" : lat, "Longitude" : lon}

                        output = { 
                        
                        "Header": header, "VehicleId" : ID.upper(), "ArrivalStatus" : ArrivalStatus, "MotionStatus": MotionStatus,
                        "ModeStatus" : ModeStatus, "Location" :  Location, "Heading" : heading, "Speed" : Speed, "Availability" : Availability,
                        "DestinationLinkId" : DestinationLinkId, "MissionSequence" : MissionSequence,
                        "MissionMode" : MissionMode, "MissionAcknowledgement" : MissionAcknowledgement
                        }
                        # json_output.append(output)
                        # publish_data = json.dumps(vehicle_status)

                        if ID in json_dict:
                            json_dict[ID].append(output)
                        else:
                            json_dict[ID] = [output]

                        step+=1
        
        for key, value in json_dict.items():
            fileName = file_path+ "json_output/" + str(key) + ".json"
            with open(fileName, 'w', encoding='utf-8') as jsonfile:
                json.dump(value, jsonfile, ensure_ascii=False, indent=4)



        print("simulation complted")
        traci.simulationStep()
        print("simulation not stoped")
        traci.close()
        print("simulation stopped")

    
    def start_client():

        def on_message(client, userdata, message):
            print("message received " ,str(message.payload.decode("utf-8")))
            m_decode=str(message.payload.decode("utf-8","ignore"))
            m_in=json.loads(m_decode)
            print (type(m_in))
            print (m_in)
            print("message topic=",message.topic)
            print("message qos=",message.qos)
            print("message retain flag=",message.retain)

        broker_address="10.8.0.1" 
        print("creating new instance")
        client = mqtt.Client("P1") #create new instance
        client.username_pw_set("adccISIT", "3Q8eaKGAHl9T1MR8N9C7VKRfQfpzDIMumIxmh3LOfKw6kd2YasVW0B1HGf67LGrX")
        print("connecting to broker")
        client.on_message=on_message #attach function to callback
        client.connect(broker_address, 1883, 60)

        return client

    def stop_client(client1):
        client1.loop_stop()
        print("Client Loop Stopped")

    def publish_data(client1, vehicle_status, topic="/vehicles_fleet/SIM_vehicle_status/adccsim11"):
        print("Publishing message to topic","/vehicles_fleet/SIM_vehicle_status/adccsim11")
        client1.publish(topic, vehicle_status)

    def subscribe_data(client, topic="/vehicles_fleet/SIM_vehicle_status/adccsim11"):

        print("Subscribing to topic","/vehicles_fleet/SIM_vehicle_status/adccsim11")
        client.subscribe(topic)

    def publish_mqtt_data(file_path,vehData):
        step=0
        json_output = []
        json_dict = {}
        
        # [file_path, nodeXmlFile,edgeXmlFile,typeXmlFile,routeXmlFile,configXmlFile,netXmlFile,outputXmlFile,
        # FrameId,SequenceId,MissionMode,MissionSequence,VehicleId,DestinationLinkId]
        
        #Starting MQTT Client
        client = traci_service.start_client()

        while traci.simulation.getMinExpectedNumber() > 0:

            traci.simulationStep()
            
            if len(traci.vehicle.getIDList()) > 0:

                split_veh_id = str(traci.vehicle.getIDList()).replace("(","").replace(")","").replace("'","").split(",")
                for veh_id in split_veh_id:
                    if veh_id is not '':
                        regex_remove = str(veh_id)
                        ID = re.sub('[\W\_]','', regex_remove)

                        heading = traci.vehicle.getAngle(ID)
                        Speed = traci.vehicle.getMaxSpeed(ID)
                        DestinationLinkId =  traci.vehicle.getRoadID(ID)
                        SequenceId = int(ID[7: len(ID)]) 
                        MotionStatus = traci.vehicle.getRoutingMode(ID) # 0- Forward, 1- reverse, 2- Unavailable
                        utc = date.datetime.now()
                        ModeStatus = 1 #0-Manaul , 1 - Automatic, 2-Helpome , 3, Safety Mode
                        x, y = traci.vehicle.getPosition(ID)
                        lon, lat = traci.simulation.convertGeo(x, y)
                        lon, lat = utm.to_latlon(lat, lon, 39, 'N')
                        # print(lat, lon)
                        FrameId = 1 # Default
                        MissionMode =1 #  1- Robo Taxi, 2-Stop Mission, 3-Valet service, 4- Telop Mission

                        MissionSequence = 123
                        # MissionAcknowledgement = int(traci.vehicle.isStopped(ID) == False) # 0- refused, 1-accepted , 3- unavilable
                        MissionAcknowledgement = 3 if traci.vehicle.isStopped(ID) == False else 1 if traci.vehicle.isStopped(ID) == True else 0

                        #Unavaialble will be send while in idle state
                        ArrivalStatus = int(traci.vehicle.isStopped(ID) == True) # 0- Not Arrived, 1- Arrived, 2- Arival unavailable 

                        Availability = 1 if traci.vehicle.isStopped(ID) == False else 2 if traci.vehicle.isStopped(ID) == True else 3# 1- Vehicle is In Mission, 2- Available, 3 - Unavailable.

                        header = { "UtcTimestamp" : str(utc) , "FrameId" : FrameId, "SequenceId": SequenceId}
                        Location = {"Latitude" : lat, "Longitude" : lon}

                        output = { 
                        "Header": header, "VehicleId" : ID.lower(), "ArrivalStatus" : ArrivalStatus, "MotionStatus": MotionStatus,
                        "ModeStatus" : ModeStatus, "Location" :  Location, "Heading" : heading, "Speed" : Speed, "Availability" : Availability,
                        "DestinationLinkId" : DestinationLinkId, "MissionSequence" : MissionSequence,
                        "MissionMode" : MissionMode, "MissionAcknowledgement" : MissionAcknowledgement
                        }

                        vehicle_status = json.dumps(output)
                        time.sleep(1)
                        traci_service.publish_data(client, vehicle_status)


        #Starting MQTT Client
        traci_service.stop_client(client)


        print("simulation complted")
        traci.simulationStep()
        print("simulation not stoped")
        traci.close()
        print("simulation stopped")


    def main(configXmlFile, outputfileName, file_path, vehData):

        if 'SUMO_HOME' in os.environ:
            tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
            sys.path.append(tools)
        else:
            sys.exit("please declare environment variable 'SUMO_HOME'")

        options = traci_service.get_options()

        # check binary
        if options.nogui:
            sumoBinary = checkBinary('sumo')
        else:
            sumoBinary = checkBinary('sumo-gui')

        traci.start([sumoBinary, "-c", configXmlFile,
                                "--tripinfo-output", outputfileName])
        traci_service.publish_mqtt_data(file_path, vehData)