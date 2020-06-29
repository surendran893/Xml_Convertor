from Database_Connect import Database_Connect as database
from xml.etree import ElementTree as xml

def node_data(fileName):
    query_temp = 'SELECT * from roadnode'
    result = database.select_query(query_temp)
    xmlData = open(fileName, 'w')
    xmlData.write('<nodes>' + "\n")

    for data in result:
        id_value = str(data[0])
        road_node_id = str(data[1])
        latitude = str(data[2])
        longitude = str(data[3])
        priority = "priority"

        xmlData.write('<node ' + 'id ="' +id_value+'" road_node_id= "'  + road_node_id +'" x ="' + latitude +  '" y ="' + longitude + '" type ="' +priority +'"' '/>' + "\n")

    xmlData.write('</nodes>' + "\n")
    xmlData.close()

def edge_data(fileName):
    query_temp = 'SELECT * from roadlink'
    result = database.select_query(query_temp)
    xmlData = open(fileName, 'w')
    xmlData.write('<edges>' + "\n")

    for data in result:
        id_value = str(data[0])
        road_link_id = str(data[1])
        source = str(data[3])
        destination = str(data[4])
        type_ = "2L50"

        xmlData.write('<edge ' + 'id ="' +id_value+'" road_link_id= "'  + road_link_id +'" from ="' + source +  '" to ="' + destination + '" type ="' +type_ +'"' '/>' + "\n")

    xmlData.write('</edges>' + "\n")
    xmlData.close()

nodeXmlFile = "C:/WorkSpace/Renault/R_AE/my_nodes.nod.xml"
edgeXmlFile = "C:/WorkSpace/Renault/R_AE/my_edge.edg.xml"

node_data(nodeXmlFile)
edge_data(edgeXmlFile)