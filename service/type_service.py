from Database_Connect import Database_Connect as database
from xml.etree import ElementTree as xml

class type_service():

    def type_data(fileName):

        try:
            xmlData = open(fileName, 'w')
            xmlData.write('<types>' + "\n")

            type_ = "2L50"
            priority_Lanes = "2"
            speed = "50"

            xmlData.write('<type ' + 'id ="' +type_+'" priority= "'  + priority_Lanes +'" numLanes ="' + priority_Lanes +  '" speed ="' + speed  +'" ' '/>' + "\n")
            xmlData.write('</types>' + "\n")
            xmlData.close()
        except Exception as e:
            print("Error in Type File Generation is -->>>>>", e)
        