#!/usr/bin/env python3
# pylint: disable=C0301,C0116,C0103,R0903

"""
This script was created by Coopydood as part of the ultimate-macOS-KVM project.

https://github.com/user/Coopydood
https://github.com/Coopydood/ultimate-macOS-KVM
Signature: 4CD28348A3DD016F

"""





import os
import time
import subprocess
import re 
import json
import sys
import argparse
from datetime import datetime
import timeit
import uuid
import random
import io

detectChoice = 1
latestOSName = "Ventura"
latestOSVer = "13"
runs = 0

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

version = open("./.version")
version = version.read()

def choiceMenu(): # UNUSED FOR NOW

    print("\n   This script can assist you in converting (or creating) an AutoPilot config\n   into an XML file for use with virsh. This script can then optionally\n   define and import the XML file into virt-manager for you."+color.END)
    #print(color.BOLD+"\n"+"Profile:"+color.END,"https://github.com/Coopydood")
    #print(color.BOLD+"   Repo:"+color.END,"https://github.com/Coopydood/ultimate-macOS-KVM")
    print("\n   Select what you'd like to do when you're ready.")
    print(color.BOLD+"\n      1. Next...")
    print(color.END+"         Continue to the choice selection screen \n")
    print(color.END+"      2. Help...")
    print(color.END+"      3. Main menu")
    print(color.END+"      4. Exit\n")
    detectChoice = int(input(color.BOLD+"Select> "+color.END))


def startup():
    global detectChoice
    print("   "+"\n   "+color.BOLD+"XML creation type"+color.END)
    print("   "+"Choose a method to use")
    print("   "+"\n   This tool can use both an existing AutoPilot file, or even\n   assist you in creating a new one. Please read and choose\n   from the options below."+color.END)#print(color.BOLD+"\n"+"Profile:"+color.END,"https://github.com/Coopydood")
    #print(color.BOLD+"   Repo:"+color.END,"https://github.com/Coopydood/ultimate-macOS-KVM")
    print(color.BOLD+"\n      1. Convert AutoPilot config to XML... (recommended)")
    print(color.END+"         This option allows you to convert a previously-created AutoPilot\n         config file into an XML file for use with virsh. Your AutoPilot\n         settings, data, and ROMs will be preserved and will be used with\n         virsh / virt-manager, including any VFIO-PCI passthrough settings.")
    #print(color.BOLD+"\n      2. Create a new XML file using AutoPilot...")
    #print(color.END+"         Use this option if you do not have an AutoPilot config file.\n         This script will take you through the AutoPilot steps before\n         generating an XML file based on your answers. No existing\n         data, such as vHDDs, can be used with this method.")
    print(color.BOLD+"\n      2. Import XML file...")
    print(color.END+"         Use this option if you already have an XML file.\n         This option lets you import a previously-created XML file\n         into virsh for use with virt-manager.\n")
  
    print(color.END+"      ?. Help...")
    print(color.END+"      M. Main menu")
    print(color.END+"      Q. Exit\n")
    detectChoice = str(input(color.BOLD+"Select> "+color.END))

       


def clear(): print("\n" * 150)

startup()

def importXML():
    clear()
    print("\n\n   "+color.BOLD+color.BLUE+"❖  IMPORT XML FILE"+color.END,"")
    print("   For use with virsh / virt-manager\n")
    global apFile
    global apFilePath
    print("   You must use a valid domain XML file.\n   AutoPilot-generated XML files end in .xml")
    
    print(color.BOLD+"\n   Drag the *.xml file onto this window (or type the path) and hit ENTER.\n")
    apFileSelect = str(input(color.BOLD+"XML File> "+color.END))
    clear()
    time.sleep(1)
    apFilePath = apFileSelect
    apFilePathNoExt = apFilePath.replace(".xml","")
    if os.path.exists(apFileSelect):
        apFile = open(apFileSelect)
        print("\n\n   "+color.BOLD+color.BLUE+"❖  IMPORT XML FILE"+color.END,"")
        print("   For use with virsh / virt-manager\n")
        print("   You can now import your XML domain file into\n   virt-manager for GUI-based usage.")
        print(color.YELLOW+color.BOLD+"\n   ⚠ "+color.END+color.BOLD+"WARNING"+color.END+"\n   This stage requires superuser permissions.\n   You can also run the following command manually if you wish:\n\n    "+color.BOLD+"$ sudo virsh define "+apFilePathNoExt+".xml\n"+color.END)
        print(color.BOLD+"      1. Import "+apFilePathNoExt+".xml")
        print(color.END+"         Use virsh to define the domain\n")
        print(color.END+"      2. Select another file...")
        print(color.END+"      Q. Exit\n")
        apFile.close()
        detectChoice1 = str(input(color.BOLD+"Select> "+color.END))

        if detectChoice1 == "1":
            clear()
            print(color.YELLOW+color.BOLD+"\n   ⚠ "+color.END+color.BOLD+"SUPERUSER PRIVILEGES"+color.END+"\n   To define the domain, virsh needs superuser to continue.\n"+color.END)
            os.system("sudo virsh define "+apFilePathNoExt+".xml")
            time.sleep(4)
            clear()
            print("\n\n   "+color.BOLD+color.GREEN+"✔ SUCCESS"+color.END,"")
            print("   XML domain has been defined\n")
            print("   The requested XML file has been successfully defined\n   using virsh, and is now available in virt-manager.\n"+color.END+"\n\n\n\n\n\n\n") 
            time.sleep(5)

        elif detectChoice1 == "2":
            importXML()


    else:
            print("\n\n   "+color.BOLD+color.RED+"✖ INVALID XML FILE"+color.END,"")
            print("   Your file was not a valid domain XML file\n")
            print("   You must use a valid file generated by AutoPilot.\n   Any existing VFIO-based args will be kept.\n   AutoPilot-generated config scripts end in .sh")
            
            print(color.BOLD+"\n   You will be returned to the input screen.\n")
            time.sleep(8)
            clear()
def convertBrains():
    global apFile
    global apFilePath
    clear()
    if apFilePath is not None:
        print("\n\n   "+color.BOLD+color.BLUE+"⧖ CONVERTING..."+color.END,"")
        print("   Please wait\n")
        print("   The assistant is now converting your AutoPilot config file\n   into a valid domain XML file for use with virsh.")
        print(color.BOLD+"\n   This may take a few moments.\n   Your source config won't be modified.\n")
        time.sleep(2)
        with open("./"+apFilePath,"r") as source:
            apFileS = source.read()
            apVars = (re.findall(r'"([^"]*)"', apFileS))
            if "-device vfio-pci" in apFileS:
                vfioargs = apFileS.split("#VFIO_DEV_BEGIN",1)[1]
                vfioargs = vfioargs.replace("\n","",1)
                vfioargs = vfioargs.split("#VFIO_DEV_END",1)[0]
                vfioargsN = vfioargs.count('\n')
                #print(vfioargs,vfioargsN)

                vfioargsBlock = []

                #vfioargs = io.StringIO(vfioargs)

                vfioargsBlock = vfioargs.splitlines()

               

                # TO GET QEMU COMMAND LINE ARGS ONLY, DEPRECATED :/

                #for x in range(vfioargsN):
                #    vfioargsBlock[x] = vfioargsBlock[x].replace("-device ","")
                #    vfioargsBlock[x] = "<qemu:arg value=\"-device\"/>\n<qemu:arg value=\""+vfioargsBlock[x]+"\"/>"





            #    <hostdev mode="subsystem" type="pci" managed="yes">
            #        <source>                     ##  vfioBuses ##        ##  vfioFunctions ##  
            #                                            \/                         \/
            #            <address domain="0x0000" bus="0x04" slot="0x00" function="0x0"/>
            #        </source>                          ##  busDrivers  ##
            #                                                   \/
            #        <address type="pci" domain="0x0000" bus="0x02" slot="0x00" function="0x0"/>
            #    </hostdev>

                busDrivers = 1

                vfioBuses = []
                vfioFunctions = []
                vfioAddresses = []

                vfioXML = []

                # ESTABLISH ARRAYS
                for x in range(vfioargsN):
                    vfioargsBlock[x] = vfioargsBlock[x].replace("-device vfio-pci,host=\"","")
                    vfioargsBlock[x] = vfioargsBlock[x].split("\",",1)[0]

                    vfioBuses.append(vfioargsBlock[x].split(":",1)[0])
                    vfioFunctions.append(int(vfioargsBlock[x].split(".")[1]))

                    busDrivers = busDrivers + 1
                    vfioAddresses.append(busDrivers)

                # FEED THE XML!
                for x in range(vfioargsN):
                    vfioXML.append("<hostdev mode=\"subsystem\" type=\"pci\" managed=\"yes\">\n      <source>\n        <address domain=\"0x0000\" bus=\"0x"+vfioBuses[x]+"\" slot=\"0x00\" function=\"0x"+str(vfioFunctions[x])+"\"/>\n      </source>\n      <address type=\"pci\" domain=\"0x0000\" bus=\"0x0"+str(vfioAddresses[x])+"\" slot=\"0x00\" function=\"0x0\"/>\n    </hostdev>")


                

                #print('\n'.join(vfioargsBlock))

                #print("__________  RESULTS!  ___________")
                #print('\n'.join(vfioXML))







        apFilePathNoExt = apFilePath.replace(".sh","")
        os.system("cp ./resources/baseDomain"+" ./"+apFilePathNoExt+".xml")
        with open("./"+apFilePathNoExt+".xml","r") as file1:
            apFileM = file1.read()
            apFileM = apFileM.replace("baseDomain",str(apFilePathNoExt+".xml"))
            apFileM = apFileM.replace("#    THIS DOMAIN FILE SHOULD NOT BE EDITED BY THE USER!    #","    APC-RUN_"+str(datetime.today().strftime('%d-%m-%Y_%H-%M-%S'))+"\n \n    THIS FILE WAS GENERATED USING AUTOPILOT.")
            apFileM = apFileM.replace("#                                                          #\n","")
            apFileM = apFileM.replace("	#    It is intended to be used by the XML import wizard.   #\n","")
            apFileM = apFileM.replace("#    To use the wizard, run the included \"main.py\" file;   #\n","")
            apFileM = apFileM.replace("#                                                          #"," ")
            apFileM = apFileM.replace("#                       $ ./main.py                        #"," \n     To be used with virsh / virt-manager.")
            apFileM = apFileM.replace("#    ./main.py","")
            apFileM = apFileM.replace("############################################################."," ")


            apFileM = apFileM.replace("$USR_NAME",apVars[1]+"")
            apFileM = apFileM.replace("$USR_UUID",str(uuid.uuid4()))

            # CONVERT MEMORY TO VIRSH FORMAT
            apMemCvt = apVars[4].replace("G","")
            apMemCvt = int(apMemCvt)
            apMemCvt = apMemCvt * 1048576

            # GET WD
            workdir = os.getcwd()

            # CONVERT THREADS TO VIRSH FORMAT
            apThreadsCvt = apVars[7]
            apThreadsCvt = int(apThreadsCvt)
            apThreadsCvt = round(apThreadsCvt / 2)

            # CONVERT VCPUS TO VIRSH FORMAT
            apTotalCvt = apVars[6]
            apTotalCvt = int(apTotalCvt)
            apTotalCvt = round(apTotalCvt * apThreadsCvt)

            # CONVERT OS VERSION TO VIRSH FORMAT
            apOSCvt = apVars[1]
            apOSCvt = apOSCvt.replace("macOS ","")
            apOSCvt = apOSCvt.replace(".","")

            apFileM = apFileM.replace("$USR_MEMORY",str(apMemCvt))
            apFileM = apFileM.replace("$USR_CPU_CORES",apVars[6])
            apFileM = apFileM.replace("$USR_CPU_TOTAL",str(apTotalCvt))
            apFileM = apFileM.replace("$USR_CPU_THREADS",str(apThreadsCvt))
            apFileM = apFileM.replace("$USR_CPU_MODEL",apVars[8])
            apFileM = apFileM.replace("$OVMF_DIR","ovmf")
            apFileM = apFileM.replace("$REPO_DIR",workdir)
            apFileM = apFileM.replace("$USR_CPU_ARGS",apVars[9])
            apFileM = apFileM.replace("$USR_CPU_CORES",apVars[6])
            apFileM = apFileM.replace("$USR_NETWORK_ADAPTER",apVars[16])
            apFileM = apFileM.replace("$USR_MAC_ADDRESS",apVars[17])
            apFileM = apFileM.replace("$USR_OS_VERSION",apOSCvt)
            apFileM = apFileM.replace("$USR_OS_NAME",apVars[1])
            apFileM = apFileM.replace("$USR_HEADER","Converted from "+apFilePath)
            apFileM = apFileM.replace("$REPO_VERSION",version)
            apFileM = apFileM.replace("$XML_FILE",apFilePathNoExt+".xml")
            apFileM = apFileM.replace("$AP_FILE",apFilePath)
            apFileM = apFileM.replace("$AP_RUNTIME",str(datetime.today().strftime('%H:%M:%S %d/%m/%Y')))


            if "-device vfio-pci" in apFileS:
                apFileM = apFileM.replace("<!-- VFIO-PCI HEADER -->",('\n    '.join(vfioXML)))
        # apFileM = apFileM.replace("$USR_",apVars[])
        
        file1.close

        with open("./"+apFilePathNoExt+".xml","w") as file:
            file.write(apFileM)
        time.sleep(5)

    apFile = open("./"+apFilePathNoExt+".xml","r")
    if "APC-RUN" in apFile.read():
        clear()
        print("\n\n   "+color.BOLD+color.GREEN+"✔ SUCCESS"+color.END,"")
        print("   AutoPilot config file converted\n")
        print("   The config file was converted successfully into\n   "+color.BOLD+"./"+apFilePathNoExt+".xml"+color.END+"\n\n\n\n\n   Please wait...\n\n") 
        time.sleep(3)
        clear()
        print("\n\n   "+color.BOLD+color.BLUE+"❖  IMPORT XML FILE"+color.END,"")
        print("   For use with virsh / virt-manager\n")
        print("   You can now import your XML domain file into\n   virt-manager for GUI-based usage.")
        print(color.YELLOW+color.BOLD+"\n   ⚠ "+color.END+color.BOLD+"WARNING"+color.END+"\n   This stage requires superuser permissions.\n   You can also run the following command manually if you wish:\n\n    "+color.BOLD+"$ sudo virsh define "+apFilePathNoExt+".xml\n"+color.END)
        print(color.BOLD+"      1. Import "+apFilePathNoExt+".xml")
        print(color.END+"         Use virsh to define the domain\n")
        print(color.END+"      2. Select another file...")
        print(color.END+"      Q. Exit\n")
        apFile.close()
        detectChoice1 = str(input(color.BOLD+"Select> "+color.END))

        if detectChoice1 == "1":
            clear()
            print(color.YELLOW+color.BOLD+"\n   ⚠ "+color.END+color.BOLD+"SUPERUSER PRIVILEGES"+color.END+"\n   To define the domain, virsh needs superuser to continue.\n"+color.END)
            os.system("sudo virsh define "+apFilePathNoExt+".xml")
            time.sleep(4)
            clear()
            print("\n\n   "+color.BOLD+color.GREEN+"✔ SUCCESS"+color.END,"")
            print("   XML domain has been defined\n")
            print("   The requested XML file has been successfully defined\n   using virsh, and is now available in virt-manager.\n   The name is displayed below.\n\n   "+color.BOLD+apVars[1]+" (ultimate-macOS-KVM)"+color.END+"\n\n\n\n\n\n\n") 
            time.sleep(5)
def manualAPSelect():
        global apFile
        global apFilePath
        print("\n\n   "+color.BOLD+"Select AutoPilot Config File"+color.END,"")
        print("   Input a valid AutoPilot-generated config\n")
        print("   You must use a valid file generated by AutoPilot.\n   Any existing VFIO-based args will be kept.\n   AutoPilot-generated config scripts end in .sh")
        
        print(color.BOLD+"\n   Drag the *.sh file onto this window (or type the path) and hit ENTER.\n")
        apFileSelect = str(input(color.BOLD+"AutoPilot Config File> "+color.END))
        clear()
        time.sleep(1)
        if os.path.exists(apFileSelect):
            apFile = open(apFileSelect)
            if "APC-RUN" in apFile.read():
                print("\n\n   "+color.BOLD+color.GREEN+"✔ VALID AUTOPILOT CONFIG"+color.END,"")
                print("   Valid AutoPilot config found\n")
                print("   The file you selected was generated by AutoPilot.\n   It appears to be valid.\n")
                
                print(color.BOLD+"   "+apFile.name+color.END)
                print("\n   Do you want to use this file?\n   It will be copied to the repo folder.\n"+color.END)
                print(color.BOLD+"      1. Convert file to XML and import")
                print(color.END+"         Converts this file into a domain XML and imports it\n")
                print(color.END+"      2. Select another file...")
                print(color.END+"      Q. Exit\n")
                apFile.close()
                detectChoice1 = str(input(color.BOLD+"Select> "+color.END))

                if detectChoice1 == "1":
                    apFilePath = apFileSelect
                    apFile = open("./"+apFilePath,"r")
                    apFile = apFile.read()
                    apFileChosen = 1
                    clear()
                    #apFileR = apFile.read()
                    apFileChosen = 1
                    convertBrains()
                    
                if detectChoice1 == "2":
                    clear()
                    manualAPSelect()
        else:
            print("\n\n   "+color.BOLD+color.RED+"✖ INVALID AUTOPILOT CONFIG"+color.END,"")
            print("   Your file was not a valid AutoPilot config\n")
            print("   You must use a valid file generated by AutoPilot.\n   Any existing VFIO-based args will be kept.\n   AutoPilot-generated config scripts end in .sh")
            
            print(color.BOLD+"\n   You will be returned to the input screen.\n")
            time.sleep(8)
            clear()
            manualAPSelect()



if detectChoice == "1":
    clear()
    global apFile
    global apFilePath
    if not os.path.exists("blobs/user/USR_CFG.apb"):
        os.system("cp blobs/*.apb blobs/user/")
    if os.path.exists("./blobs/user/USR_CFG.apb"):
            apFilePath = open("./blobs/user/USR_CFG.apb")
            apFilePath = apFilePath.read()
            if os.path.exists("./"+apFilePath):
                apFile = open("./"+apFilePath,"r")
                if "APC-RUN" in apFile.read():
                    print("\n\n   "+color.BOLD+color.GREEN+"✔ AUTOPILOT CONFIG AUTODETECTED"+color.END,"")
                    print("   Valid AutoPilot config found\n")
                    print("   An existing boot config file was found in the repo folder and\n   was generated by AutoPilot. It appears to be valid.\n")
                    
                    print(color.BOLD+"   "+apFile.name+color.END)
                    print("\n   Do you want to use this file?\n"+color.END)
                    print(color.BOLD+"      1. Convert",apFilePath,"to XML and import")
                    print(color.END+"         Converts this file into a domain XML and imports it\n")
                    print(color.END+"      2. Select another file...")
                    print(color.END+"      Q. Exit\n")
                    apFile.close()
                    detectChoice2 = str(input(color.BOLD+"Select> "+color.END))

                    if detectChoice2 == "1":
                        #apFileR = apFile.read()
                        apFileChosen = 1
                        apFile = open("./"+apFilePath,"r")

                        apFile = apFile.read()
                        apFileChosen = 1
                        clear()
                        clear()
                        convertBrains()

                    if detectChoice2 == "2":
                        clear()
                        manualAPSelect()
                else:
                    clear()
                    manualAPSelect()
            else:
                clear()
                manualAPSelect()
elif detectChoice == "3":
    os.system('./scripts/dlosx.py')
elif detectChoice == "2":
    clear()
    importXML()
elif detectChoice == "?":
    clear()
    print("\n\n   "+color.BOLD+color.GREEN+"✔  OPENING HELP PAGE IN DEFAULT BROWSER"+color.END,"")
    print("   Continue in your browser\n")
    print("\n   I have attempted to open the XML Converter help page in\n   your default browser. Please be patient.\n\n   You will be returned to the last screen in 5 seconds.\n\n\n\n\n")
    os.system('xdg-open https://github.com/Coopydood/ultimate-macOS-KVM/wiki/XML-Converter > /dev/null 2>&1')
    time.sleep(6)
    clear()
    startup()


#https://github.com/Coopydood/ultimate-macOS-KVM/wiki/XML-Converter