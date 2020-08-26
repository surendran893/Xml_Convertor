from service import node_service as node
from service import edge_service as edge
from service import route_service as route
from service import type_service as type_
from service import config_service as config
from service import net_service as net
from service import traci_service as traci

class simulation_service():

    def trigger_simulation(files):
        print("files is ", files)
        # [file_path, nodeXmlFile,edgeXmlFile,typeXmlFile,routeXmlFile,configXmlFile,netXmlFile,outputXmlFile,
        # FrameId,SequenceId,MissionMode,MissionSequence,VehicleId,DestinationLinkId]

        route1 = route.route_service
        net1 = net.net_service
        traci1 = traci.traci_service

        file_path = files[0]
        routeXmlFile = files[4]
        nodeXmlFile = files[1]
        edgeXmlFile = files[2]
        typeXmlFile = files[3]
        netXmlFile = files[6]
        configXmlFile = files[5] 
        outputXmlFile = files[7]
        nodes = [[56999,files[13]]]
        route1.route_data(routeXmlFile, nodes, files[12])
        net1.net_data(file_path, nodeXmlFile, edgeXmlFile, typeXmlFile, netXmlFile)
        traci1.main(configXmlFile, outputXmlFile, file_path, files)


