from xml.etree import ElementTree as xml
import os
import sys
import subprocess

class net_service():

    def net_data(file_path, node_fileName, eddge_fileName, type_fileName,net_fileName ):

        try:
            
            file1 = 'C:/WorkSpace/Renault/R_AE/Application/sumo-1.6.0/sumo'
            home_dir = os.system("cd %s" % file_path)
            if home_dir == 0:
                print("Direcrtory has been changed to ",file_path)
            else:
                print("Direcrtory has not been changed to ",file_path)
                raise EnvironmentError

            try:
                net_file = "netconvert --node-files " + node_fileName + " --edge-files " + eddge_fileName +" --type-files "+ type_fileName + " --o "+net_fileName
                net_command_file = subprocess.call(net_file, shell=True)
                if net_command_file == 0:
                    print("Net File creation is success ")

            except Exception as e:
                print("Net File creation is Failed --> ", e)
        except Exception as e:
            print("Error in Net File Generation is -->>>>>", e)
        