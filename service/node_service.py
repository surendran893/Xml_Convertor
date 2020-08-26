from Database_Connect import Database_Connect as database
from xml.etree import ElementTree as xml
from arcgis.gis import GIS
from arcgis.geocoding import reverse_geocode
import utm
import os
import sys
import subprocess

class node_service():

    def node_data(fileName):

        try:
            query_temp = 'select a."id",a."int_Node_ID", ST_X(a."geo_Position")  as lattitude, ST_Y(a."geo_Position") as longitude,  c."str_Node_IntersectionTrafficSign_Name" as trafficSign ,b."int_Intersection_ID" from "Node" a left Join "IntersectionArea" b on ST_Intersects(a."geo_Position", b."geo_Position") inner join "IntersectionTrafficSign" c on a."int_Node_IntersectionTrafficSign_ID" = c."int_Node_IntersectionTrafficSign_ID"'
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
                priority = "priority" if data[4] == 'GiveWay' else "traffic_light" if data[4] == 'TrafficLight' else "priority_stop" if data[4] == 'Stop' else "unregulated"
                x, y, c, a = utm.from_latlon(data[2], data[3])
                x_value, y_value = str(x), str(y)

                xmlData.write('<node ' + 'id ="' +id_value+'" road_node_id= "'  + road_node_id +'" x ="' + y_value +  '" y ="' + x_value + '" type ="' +priority +'"' '/>' + "\n")
                x += 1

            xmlData.write('</nodes>' + "\n")
            xmlData.close()
        except Exception as e:
            print("Error in Node File Generation is -->>>>>", e)
        