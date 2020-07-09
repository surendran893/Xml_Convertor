from Database_Connect import Database_Connect as database
from xml.etree import ElementTree as xml
from arcgis.gis import GIS
from arcgis.geocoding import reverse_geocode
import utm


def node_data(fileName):
    # query_temp = 'SELECT * from roadnode'
    query_temp = 'SELECT "id", "int_Node_ID", ST_X("geo_Position") as lattitude, ST_Y("geo_Position") as longitude    FROM "Node"'
    result = database.select_query(query_temp)
    xmlData = open(fileName, 'w')
    xmlData.write('<nodes>' + "\n")
    gis = GIS()
    x = 0

    for data in result:
        id_value = str(data[1])
        road_node_id = str(data[0])
        latitude = str(data[2])
        longitude = str(data[3])
        priority = "priority"
        x, y, c, a = utm.from_latlon(data[2], data[3])
        x_value, y_value = str(x), str(y)

        # m_location = reverse_geocode([longitude, latitude])
        # x_value = str(m_location['location']['x'])
        # y_value = str(m_location['location']['y'])
        # print("before x_value is -->> {} after x_value is -->> {} and before y_value is---->> {} and after y_value is--->>".format(latitude,x_value, longitude,y_value))
        # print("Data done for {}".format(x))
        xmlData.write('<node ' + 'id ="' +id_value+'" road_node_id= "'  + road_node_id +'" x ="' + x_value +  '" y ="' + y_value + '" type ="' +priority +'"' '/>' + "\n")
        x += 1

    xmlData.write('</nodes>' + "\n")
    xmlData.close()

def edge_data(fileName):
    # query_temp = 'SELECT * from roadlink'
    query_temp = 'SELECT "id", "int_Link_ID", "int_Node_ID_Link_Start", "int_Node_ID_Link_End"  FROM "Link"'
    result = database.select_query(query_temp)
    xmlData = open(fileName, 'w')
    xmlData.write('<edges>' + "\n")

    for data in result:
        id_value = str(data[1])
        road_link_id = str(data[0])
        source = str(data[2])
        destination = str(data[3])
        type_ = "2L50"
        # one_way = True

        # if one_way == False:
        #     xmlData.write('<edge ' + 'id ="' +id_value+'" road_link_id= "'  + road_link_id +'" from ="' + destination +  '" to ="' + source + '" type ="' +type_ +'"' '/>' + "\n")
        #     xmlData.write('<edge ' + 'id ="' +id_value+'" road_link_id= "'  + road_link_id +'" from ="' + source +  '" to ="' + destination + '" type ="' +type_ +'"' '/>' + "\n")
        # else:
            # xmlData.write('<edge ' + 'id ="' +id_value+'" road_link_id= "'  + road_link_id +'" from ="' + source +  '" to ="' + destination + '" type ="' +type_ +'"' '/>' + "\n")
        xmlData.write('<edge ' + 'id ="' +id_value+'" road_link_id= "'  + road_link_id +'" from ="' + source +  '" to ="' + destination + '" type ="' +type_ +'"' '/>' + "\n")
    xmlData.write('</edges>' + "\n")
    xmlData.close()

nodeXmlFile = "C:/WorkSpace/Renault/R_AE/Application/sumo-1.6.0/sumo/my_nodes.nod.xml"
edgeXmlFile = "C:/WorkSpace/Renault/R_AE/Application/sumo-1.6.0/sumo/my_edge.edg.xml"

# node_data(nodeXmlFile)
edge_data(edgeXmlFile)
