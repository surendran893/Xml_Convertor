from Database_Connect import Database_Connect as database
from xml.etree import ElementTree as xml


class route_service():

    def route_data(fileName, desitinationLinkID, vehicleId):

        try:
            accel = "1.0"
            decel = "5.0"
            length = "15.0"
            maxSpeed = "5.0"
            sigma = "0.0"
            depart = 0
            id_ = "ZoeEV"

            obj = []

            # obj.append([56999,44611])
            # obj.append([44611,56999])
            # obj.append([56999,57035])
            # obj.append([57035,56999])
            # obj.append([57035,50194])
            # obj.append([50194,56999])
            # obj.append([30351,57051])
            # obj.append([57050,30351])
            # obj.append([57050,57068])
            # obj.append([50166,57068])
            # obj.append([57068,50175])
            # obj.append([44611,57069])
            # obj.append([57068,57050])
            # obj.append([50175,57050])
            # obj.append([50175,44611])
            # obj.append([49814,57050])
            # obj.append([57050,44611])
            # obj.append([50175,30989])
            # obj.append([50175,30351])
            # obj.append([30351,50175])

            
            count = 10
            xmlData = open(fileName, 'w')
            xmlData.write('<routes>' + "\n")
            xmlData.write("\n")
            xmlData.write('<vType ' + 'accel = "' +accel +'" decel = "'  + decel +'" id = "' + id_ +  '" length = "' + length + '" maxSpeed = "' +maxSpeed + '" sigma = "' + sigma +'"' '/>' + "\n")
            xmlData.write("\n")

            for node in desitinationLinkID:
                count  += 1
                route_id = "route"+ str(count)
                # veh_id = "adccsim"+ str(count)
                veh_id = vehicleId

                query_temp = "select array_to_string(array(SELECT edge FROM pgr_dijkstra ('SELECT \"int_Link_ID\" as id, \"int_Node_ID_Link_Start\" as source, \"int_Node_ID_Link_End\" as target, \"real_Link_Length\" as cost, reverse_cost FROM  \"Link\" where \"int_Link_ID\" not in (20341,20342,20330,20334,27727,27726,21141,21145,27989,30405,24353,24348,28139,28165,21089,21090,21069,21068,20984,20985,29562,29563,29553,29650,29734,29735,28852,28868,29311,29307,22299,22300,30338,30337,23822,23762,23821,23763,28068,28067,22491,22490,41353,41372,23639,23635,22525,22526,41371,22674,35012,21399,21396,22390,22389,34606,34668,34667,22432,22433,34730,34757,34937,34922,34982,22394,34874,34884)',%s,%s)),' ')"
                parameters = (node[0], node[1])
                result = database.select_query_with_param(query_temp, parameters)
                edge_route  = str(result[0]).replace("('","").replace("',)","").replace("-1", "")
                
                xmlData.write('<route ' + 'id = "' +route_id+'" edges = "'  + edge_route +'"' '/>' + "\n")
                xmlData.write('<vehicle ' + 'depart = "' +str(depart)+'" id = "'  + veh_id +'" route = "' + route_id +  '" type = "' + id_ + '" class = "' + "taxi" +'"' '>' + "\n")
                xmlData.write('<stop ' + 'lane = "' +edge_route[-6:-1]+"_0"+'" parking = "'  + "true" +'"' '/>' + "\n")
                xmlData.write("</vehicle>" + "\n")
                xmlData.write("\n")
                depart += 10
            xmlData.write('</routes>' + "\n")
            xmlData.close()
        except Exception as e:
            print("Error in Route File Generation is -->>>>>", e)
        