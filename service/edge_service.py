from Database_Connect import Database_Connect as database
from xml.etree import ElementTree as xml


class edge_service():

    def edge_data(fileName):

        try:
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
                xmlData.write('<edge ' + 'id ="' +id_value+'" road_link_id= "'  + road_link_id +'" from ="' + source +  '" to ="' + destination + '" type ="' +type_ +'"' '/>' + "\n")
            xmlData.write('</edges>' + "\n")
            xmlData.close()
        except Exception as e:
            print("Error in Edge File Generation is -->>>>>", e)
        