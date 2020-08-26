from Database_Connect import Database_Connect as database
from xml.etree import ElementTree as xml


class config_service():

    def config_data(fileName, net_file, route_file, gui_file):

        try:
            xmlData = open(fileName, 'w')
            xmlData.write('<configuration>' + "\n")
            xmlData.write("\n")
            xmlData.write('<input>' + "\n")
            xmlData.write('<net-file ' + 'value ="' +net_file+ '" ' '/>' + "\n")
            xmlData.write('<route-files ' + 'value ="' +route_file+ '" ' '/>' + "\n")
            xmlData.write('<gui-settings-file ' + 'value ="' +gui_file+ '" ' '/>' + "\n")
            xmlData.write('</input>' + "\n")
            xmlData.write('<time>' + "\n")
            xmlData.write('<begin ' + 'value ="' +str(0)+ '" ' '/>' + "\n")
            xmlData.write('<end ' + 'value ="' +str(2000)+ '" ' '/>' + "\n")
            xmlData.write('</time>' + "\n")
            xmlData.write("\n")
            xmlData.write('</configuration>' + "\n")
        except Exception as e:
            print("Error in Config File Generation is -->>>>>", e)
        