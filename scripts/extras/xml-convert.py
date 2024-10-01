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
import pathlib
sys.path.append('./resources/python')
from cpydColours import color

global apFileSelect
global autodetect
global useBlobs
global domainTitle
global apFilePath


detectChoice = "1"
detectChoiceM = ""
latestOSName = "Sequoia"
latestOSVer = "15"
runs = 0
nrsdir = None

global cpydPassthrough
cpydPassthrough = 0

version = open("./.version")
version = version.read()

parser = argparse.ArgumentParser("xml-convert")
parser.add_argument("-i", "--import", dest="importfile", help="Import existing XML domain file",metavar="<file>", type=str)
parser.add_argument("-c", "--convert", dest="convert", help="Convert existing config script to XML", metavar="<file>", type=str)
parser.add_argument("-q", "--quiet", dest="quiet", help="Silences any UI output, must be used with  --convert", action="store_true")
parser.add_argument("-ni", "--no-import", dest="noimport", help="Don't offer import when conversion is finished", action="store_true")
parser.add_argument("--no-blobs", dest="noblobs", help="Blocks the initialisation of arrays using AP blobs", action="store_true")
parser.add_argument("--mark-ap", dest="markap", help="Internal use only", action="store_true")
parser.add_argument("--nrs-dir", dest="nrsdir", help="Internal use only", type=str)
#parser.add_argument("-f", "--force", dest="forceModel", metavar="<model>", help="Override auto-detected GPU with a custom model. Pretty useless, mostly for debugging.", type=str)
args = parser.parse_args()
if args.nrsdir is not None:
    nrsdir = args.nrsdir
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
    detectChoice = str(input(color.BOLD+"Select> "+color.END))


def startup():
    clear()
    global detectChoiceM
    print("\n\n  "+color.PURPLE+color.BOLD,"XML CONVERSION TOOL"+color.END,"")
    print("   by",color.BOLD+"Coopydood"+color.END)
    print("   "+"\n   This tool can use both an existing AutoPilot file, or even\n   assist you in creating a new one. Please read and choose\n   from the options below."+color.END)#print(color.BOLD+"\n"+"Profile:"+color.END,"https://github.com/Coopydood")
    #print(color.BOLD+"   Repo:"+color.END,"https://github.com/Coopydood/ultimate-macOS-KVM")
    print(color.BOLD+"\n      1. Convert AutoPilot config to XML... (recommended)")
    print(color.END+"         This option allows you to convert a previously-created AutoPilot\n         config file into an XML file for use with virsh. Your AutoPilot\n         settings, data, and ROMs will be preserved and will be used with\n         virsh / virt-manager, including any VFIO-PCI passthrough settings.")
    #print(color.BOLD+"\n      2. Create a new XML file using AutoPilot...")
    #print(color.END+"         Use this option if you do not have an AutoPilot config file.\n         This script will take you through the AutoPilot steps before\n         generating an XML file based on your answers. No existing\n         data, such as vHDDs, can be used with this method.")
    print(color.BOLD+"\n      2. Import XML file...")
    print(color.END+"         Use this option if you already have an XML file.\n         This option lets you import a previously-created XML file\n         into virsh for use with virt-manager.\n")
  
    print(color.END+"      ?. Help...")
    print(color.END+"      M. Back to menu...")
    print(color.END+"      Q. Exit\n")
    detectChoiceM = str(input(color.BOLD+"Select> "+color.END))

       


def clear(): print("\n" * 150)

def importXML():
    global cpydPassthrough
    clear()
    if cpydPassthrough != 1:
        if not os.path.exists("./ovmf/OVMF_VARS.fd"):
            if os.path.exists("./ovmf/user_store/OVMF_VARS.fd"): # Might be tainted?
                os.system("cp ./ovmf/user_store/OVMF_VARS.fd ./ovmf/OVMF_VARS.fd")
            else:
                os.system("cp ./resources/ovmf/OVMF_VARS.fd ./ovmf/OVMF_VARS.fd")

        print("\n\n   "+color.BOLD+color.BLUE+"IMPORT XML FILE"+color.END,"")
        print("   For use with virsh / virt-manager\n")
        global apFile
        global apFilePath
        print("   You must use a valid domain XML file.\n   AutoPilot-generated XML files end in .xml")
        
        print(color.BOLD+"\n   Drag the *.xml file onto this window (or type the path) and hit ENTER.\n")
        apFileSelect = str(input(color.BOLD+"XML File> "+color.END))
    elif cpydPassthrough == 1:
        apFileSelect = args.importfile
    clear()
    time.sleep(1)
    apFilePath = apFileSelect
    apFilePathNoExt = apFilePath.replace(".xml","")
    if os.path.exists(apFileSelect):
        apFile = open(apFileSelect)
        print("\n\n   "+color.BOLD+color.BLUE+"IMPORT XML FILE"+color.END,"")
        print("   For use with virsh / virt-manager\n")
        print("   You can now import your XML domain file into\n   virt-manager for GUI-based usage.")
        print(color.YELLOW+color.BOLD+"\n   ⚠ "+color.END+color.BOLD+"WARNING"+color.END+"\n   This stage requires superuser permissions.\n   You can also run the following command manually if you wish:\n\n    "+color.BOLD+"$ sudo virsh define "+apFilePathNoExt+".xml\n"+color.END)
        print(color.BOLD+"      1. Import "+apFilePathNoExt+".xml"+color.YELLOW,"⚠"+color.END)
        print(color.END+"         Use virsh to define the domain\n")
        print(color.END+"      2. Select another file...")
        print(color.END+"      Q. Exit\n")
        apFile.close()
        detectChoice1 = str(input(color.BOLD+"Select> "+color.END))

        if detectChoice1 == "1":
            clear()
            print(color.YELLOW+color.BOLD+"\n   ⚠ "+color.END+color.BOLD+"SUPERUSER PRIVILEGES"+color.END+"\n   To define the domain, virsh needs superuser to continue.\n\n   Press CTRL+C to cancel.\n"+color.END)
            os.system("sudo virsh define "+apFilePathNoExt+".xml")
            time.sleep(4)
            clear()
            print("\n\n   "+color.BOLD+color.GREEN+"SUCCESS"+color.END,"")
            print("   XML domain has been defined\n")
            print("   The requested XML file has been successfully defined\n   using virsh, and is now available in virt-manager.\n"+color.END+"\n\n\n\n\n\n\n") 
            time.sleep(5)

        elif detectChoice1 == "2":
            importXML()


    else:
            print("\n\n   "+color.BOLD+color.RED+"INVALID XML FILE"+color.END,"")
            print("   Your file was not a valid domain XML file\n")
            print("   You must use a valid file generated by AutoPilot.\n   Any existing VFIO-based args will be kept.\n   AutoPilot-generated config scripts end in .sh")
            
            print(color.BOLD+"\n   You will be returned to the input screen.\n")
            cpydPassthrough = 0   # KILL PASSTHROUGH AS IT WAS DESTROYED BY USER
            time.sleep(8)
            clear()
def convertBrains():
    global apFile
    global apFilePath
    
    if apFilePath is not None:
        if args.quiet != True:
            clear()
            print("\n\n   "+color.BOLD+color.BLUE+"⧖ CONVERTING..."+color.END,"")
            print("   Please wait\n")
            print("   The assistant is now converting your AutoPilot config file\n   into a valid domain XML file for use with virsh.")
            print(color.BOLD+"\n   This may take a few moments.\n   Your source config won't be modified.\n")
        time.sleep(2)
        with open(""+apFilePath,"r") as source:
            global apVars
            global useBlobs
            apFileS = source.read()
            apVars = ["macOS","macOS",apFilePath,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            
            
            if autodetect == False or args.noblobs is True:
                apVars = (re.findall(r'"([^"]*)"', apFileS))
                useBlobs = False
                USR_BOOT_FILE = 0
            else:
                # NEW BLOB MODE yay

                # We are only substituting what is needed. This is done to add backwards compatibility with < v0.9.2
                # This makes the array look fragmented, but hard-coded and expected values are pre-entered into the array before these assignments
                # Even if they're assigned a place in the array below, there's no guarantee they'll be used

                # HOWEVER, because this method relies on blob existence, there's no guarantee of a APC lineup
                # Therefore, this will only be used if the APC was autodetected and user authorises this
                sourceDir = "."+os.curdir

                if nrsdir is not None:
                    os.chdir(nrsdir)
                #with open("./blobs/user/USR_NAME.apb") as blob: apVars[0] = str(blob.read())
                with open("./blobs/user/USR_TARGET_OS.apb") as blob: macOSVer = int(blob.read())
                with open("./blobs/user/USR_TARGET_OS.apb") as blob: apVars[1] = ""+str(blob.read())
                with open("./blobs/user/USR_TARGET_OS_NAME.apb") as blob: apVars[18] = ""+str(blob.read())
                with open("./blobs/user/USR_ALLOCATED_RAM.apb") as blob: apVars[4] = str(blob.read())
                with open("./blobs/user/USR_CPU_CORES.apb") as blob: apVars[6] = str(blob.read())
                with open("./blobs/user/USR_CPU_THREADS.apb") as blob: apVars[7] = str(blob.read())
                with open("./blobs/user/USR_CPU_MODEL.apb") as blob: apVars[8] = str(blob.read())
                with open("./blobs/user/USR_CPU_FEATURE_ARGS.apb") as blob: apVars[9] = str(blob.read())
                with open("./blobs/user/USR_NETWORK_DEVICE.apb") as blob: apVars[16] = str(blob.read())
                with open("./blobs/user/USR_MAC_ADDRESS.apb") as blob: apVars[17] = str(blob.read())
                with open("./blobs/user/USR_BOOT_FILE.apb") as blob: apVars[21] = str(blob.read())


                # REQUIRES FL 7
                if os.path.exists("./blobs/user/USR_HDD_ISPHYSICAL.apb"):
                    with open("./blobs/user/USR_HDD_ISPHYSICAL.apb") as blob: apVars[22] = str(blob.read())
                    USR_HDD_ISPHYSICAL = apVars[22]
                else: USR_HDD_ISPHYSICAL = False

                # REQUIRES FL 6
                if os.path.exists("./blobs/user/USR_HDD_TYPE.apb"):
                    with open("./blobs/user/USR_HDD_TYPE.apb") as blob: apVars[20] = str(blob.read())
                    USR_HDD_TYPE = apVars[20]
                else: USR_HDD_TYPE == "HDD"

                # REQUIRES FL 5
                if os.path.exists("./blobs/user/USR_HDD_PATH.apb"):
                    with open("./blobs/user/USR_HDD_PATH.apb") as blob: apVars[19] = str(blob.read())
                else:
                    apVars[19] = "$VM_PATH/HDD.qcow2"
                    apVars[19] = apVars[19].replace("$VM_PATH",workdir)
                useBlobs = True

                if int(macOSVer) <= 110 and int(macOSVer) > 99:
                    apVars[18] = apVars[18].replace("macOS","Mac OS X")
                

                if os.path.exists("./blobs/user/USR_TARGET_OS_NAME.apb"):
                    macOSVer = open("./blobs/user/USR_TARGET_OS_NAME.apb")
                    macOSVer = macOSVer.read()
            
                USR_BOOT_FILE = apVars[21]


                
                
                




            if "-device vfio-pci" in apFileS:
                vfioargs = apFileS.split("#VFIO_DEV_BEGIN",1)[1]
                vfioargs = vfioargs.replace("\n","",1)
                vfioargs = vfioargs.split("#VFIO_DEV_END",1)[0]
                vfioargsN = vfioargs.count('\n')
                #print(vfioargs,vfioargsN)

                vfioargsBlock = []

                #vfioargs = io.StringIO(vfioargs)

                vfioargsBlock = vfioargs.splitlines()

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





            if "-device usb-host" in apFileS:
                usbargs = apFileS.split("#USB_DEV_BEGIN",1)[1]
                usbargs = usbargs.replace("\n","",1)
                usbargs = usbargs.split("#USB_DEV_END",1)[0]
                usbargsN = usbargs.count('\n')
                #print(usbargs,usbargsN)

                usbargsBlock = []

                #usbargs = io.StringIO(usbargs)

                usbargsBlock = usbargs.splitlines()

            #    <hostdev mode="subsystem" type="pci" managed="yes">
            #        <source>                     ##  usbVendor ##        ##  usbFunctions ##  
            #                                            \/                         \/
            #            <address domain="0x0000" bus="0x04" slot="0x00" function="0x0"/>
            #        </source>                          ##  busDrivers  ##
            #                                                   \/
            #        <address type="pci" domain="0x0000" bus="0x02" slot="0x00" function="0x0"/>
            #    </hostdev>

                busDrivers = 1

                usbVendor = []
                usbProduct = []
                usbConstructor = []
                usbXML = []

                # ESTABLISH ARRAYS
                for x in range(usbargsN):
                    usbargsBlock[x] = usbargsBlock[x].replace("-device usb-host,vendorid=","")
                    usbargsBlock[x] = usbargsBlock[x].replace("productid=","")
                    usbargsBlock[x] = usbargsBlock[x].replace(",","")
                    #usbargsBlock[x] = usbargsBlock[x].split(",",1)[0]

                    usbVendor.append(usbargsBlock[x].split("0x")[1])
                    usbProduct.append(usbargsBlock[x].split("0x")[2])

                # FEED THE XML!
                for x in range(usbargsN):
                    usbXML.append("<hostdev mode=\"subsystem\" type=\"usb\" managed=\"yes\">\n      <source>\n        <vendor id=\"0x"+usbVendor[x]+"\"/>\n        <product id=\"0x"+usbProduct[x]+"\"/>\n      </source>\n    </hostdev>")
                    


        apFilePathNoExt = apFilePath.replace(".sh","")
        apFilePathNoExt = r"{}".format(apFilePathNoExt)
        if ".." in sourceDir:
            sourceDir = sourceDir.replace("..",".") # fix sourcing paths
        os.system("cp "+sourceDir+"/resources/baseDomain"+" "+apFilePathNoExt+".xml")
        with open(""+apFilePathNoExt+".xml","r") as file1:
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

            
            # Decide whether or not to probe array for VHD type
            if apVars[20] != 0 and useBlobs == False:
                USR_HDD_TYPE = apVars[20]
            elif useBlobs == False:
                USR_HDD_TYPE = "HDD" # Couldn't determine, fallback to regular HDD

            # Decide whether or not to probe array for physical disk
            if apVars[21] != 0 and useBlobs == False:
                USR_HDD_ISPHYSICAL = apVars[21]
            elif useBlobs == False:
                USR_HDD_ISPHYSICAL = False # Couldn't determine, fallback to regular HDD


            apVars[1] = apVars[1].replace("macOS ","")
            apVars[1] = apVars[1].replace("Mac OS X ","")

            macOSVer = int(apVars[1].replace(".",""))


            if int(macOSVer) <= 999 and int(macOSVer) > 99:
                apFileM = apFileM.replace("$USR_NAME","Mac OS X "+apVars[18]+"")
                domainTitle = "Mac OS X "+apVars[18]
            else:
                apFileM = apFileM.replace("$USR_NAME","macOS "+apVars[18]+"")
                domainTitle = "macOS "+apVars[18]

            apFileM = apFileM.replace("$USR_NAME",apVars[18]+"")
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
            #apThreadsCvt = round(apThreadsCvt / 2)

            # CONVERT VCPUS TO VIRSH FORMAT
            apTotalCvt = apVars[6]
            apTotalCvt = int(apTotalCvt)
            apTotalCvt = round(apTotalCvt * apThreadsCvt)

            # CONVERT OS VERSION TO VIRSH FORMAT
            apOSCvt = apVars[1]
            apOSCvt = apOSCvt.replace("macOS ","")
            apOSCvt = apOSCvt.replace("Mac OS X ","")
            apOSCvt = apOSCvt.replace(".","")

            if USR_HDD_ISPHYSICAL == "True":
                apFileM = apFileM.replace("    <disk type=\"file\" device=\"disk\"> <!-- HDD HEADER -->\n      <driver name=\"qemu\" type=\"qcow2\"/>\n      <source file=\"$USR_HDD_PATH\"/>\n      <target dev=\"sdb\" bus=\"sata\" rotation_rate=\"7200\"/>\n      <address type=\"drive\" controller=\"0\" bus=\"0\" target=\"0\" unit=\"1\"/>\n    </disk> <!-- HDD FOOTER -->","    <disk type=\"block\" device=\"disk\"> <!-- HDD HEADER -->\n      <driver name=\"qemu\" type=\"raw\"/>\n      <source dev=\"$USR_HDD_PATH\"/>\n      <target dev=\"sdb\" bus=\"sata\" rotation_rate=\"7200\"/>\n      <address type=\"drive\" controller=\"0\" bus=\"0\" target=\"0\" unit=\"1\"/>\n    </disk> <!-- HDD FOOTER -->")

            if USR_HDD_TYPE == "HDD":       # DISK TYPE ROUTINE; REQUIRES CONFIG FL 6!
                    None
            elif USR_HDD_TYPE == "SSD":
                apFileM = apFileM.replace("rotation_rate=\"7200\"","rotation_rate=\"1\"")
            elif USR_HDD_TYPE == "NVMe":
                apFileM = apFileM.replace("<!-- NVME HEADER -->","<qemu:arg value=\"-drive\"/>\n    <qemu:arg value=\"file=$USR_HDD_PATH,format=qcow2,if=none,id=HDD\"/>\n    <qemu:arg value=\"-device\"/>\n    <qemu:arg value=\"nvme,drive=HDD,serial=ULTMOS,bus=pcie.0,addr=10\"/>")
                apFileM = apFileM.replace("<disk type=\"file\" device=\"disk\"> <!-- HDD HEADER -->","<!-- <disk type=\"file\" device=\"disk\">")
                apFileM = apFileM.replace("</disk> <!-- HDD FOOTER -->","</disk> -->")

            if USR_BOOT_FILE != "-2":
                apFileM = apFileM.replace("<!-- BASESYSTEM HEADER -->","<!--############# REMOVE THESE LINES AFTER MACOS INSTALLATION #############-->\n\n    <disk type=\"file\" device=\"disk\"> \n      <driver name=\"qemu\" type=\"raw\"/>\n      <source file=\"$VM_PATH/BaseSystem.img\"/>\n      <target dev=\"sdc\" bus=\"sata\"/>\n      <address type=\"drive\" controller=\"0\" bus=\"0\" target=\"0\" unit=\"2\"/>\n	  </disk> \n\n<!--#######################################################################-->")


            if USR_BOOT_FILE == "-2" and useBlobs == True:       # DISABLE THE DETACHED BASESYSTEM; REQUIRES BLOB METHOD!
                apFileM = apFileM.replace("<!--############# REMOVE THESE LINES AFTER MACOS INSTALLATION #############-->","<!--############# REMOVE THESE LINES AFTER MACOS INSTALLATION #############")
                apFileM = apFileM.replace("<!--#######################################################################-->","    #######################################################################-->")
                apFileM = apFileM.replace("<!-- BASESYSTEM HEADER -->","")
                apFileM = apFileM.replace("<!-- BASESYSTEM FOOTER -->","")

            
            apFileM = apFileM.replace("$USR_MEMORY",str(apMemCvt))
            apFileM = apFileM.replace("$USR_CPU_CORES",apVars[6])
            apFileM = apFileM.replace("$USR_CPU_TOTAL",str(apTotalCvt))
            apFileM = apFileM.replace("$USR_CPU_THREADS",str(apThreadsCvt))
            apFileM = apFileM.replace("$USR_CPU_MODEL",apVars[8])
            apFileM = apFileM.replace("$OVMF_DIR","ovmf")
            
            apFileM = apFileM.replace("$USR_CPU_ARGS",apVars[9])
            apFileM = apFileM.replace("$USR_CPU_CORES",apVars[6])
            apFileM = apFileM.replace("$USR_NETWORK_ADAPTER",apVars[16])
            apFileM = apFileM.replace("$USR_MAC_ADDRESS",apVars[17])
            if apVars[19] == 0:
                apFileM = apFileM.replace("$USR_HDD_PATH","$VM_PATH/HDD.qcow2")
            else:
                apFileM = apFileM.replace("$USR_HDD_PATH",apVars[19])
            apFileM = apFileM.replace("$VM_PATH",workdir)
            apFileM = apFileM.replace("$USR_OS_VERSION",apOSCvt)
            apFileM = apFileM.replace("$USR_OS_NAME",apVars[18])
            apFileM = apFileM.replace("$USR_HEADER","Converted from "+apFilePath)
            apFileM = apFileM.replace("$REPO_VERSION",version)
            apFileM = apFileM.replace("$XML_FILE",apFilePathNoExt+".xml")
            apFileM = apFileM.replace("$AP_FILE",apFilePath)
            apFileM = apFileM.replace("$AP_RUNTIME",str(datetime.today().strftime('%H:%M:%S %d/%m/%Y')))
            
            if "-device vfio-pci" in apFileS: # DISABLE VGA VIDEO OUT IF PASSTHROUGH DETECTED
                apFileM = apFileM.replace("    <video>\n      <model type=\"vga\" vram=\"16384\" heads=\"1\" primary=\"yes\"/>\n      <address type=\"pci\" domain=\"0x0000\" bus=\"0x09\" slot=\"0x01\" function=\"0x0\"/>\n    </video>","    <video>\n		<model type=\"none\"/>\n    </video>")
            
            
            if autodetect == True:
                apFileM = apFileM.replace("$AP_AUTO","Yes")
            else:
                apFileM = apFileM.replace("$AP_AUTO","No")
            if useBlobs == True:
                apFileM = apFileM.replace("$AP_BLOB","Yes")
            else:
                apFileM = apFileM.replace("$AP_BLOB","No")

            if args.markap == True:
                apFileM = apFileM.replace("$AP_FLOW","Yes")
            else:
                apFileM = apFileM.replace("$AP_FLOW","No")

            if "-device vfio-pci" in apFileS:
                apFileM = apFileM.replace("<!-- VFIO-PCI HEADER -->",('\n    '.join(vfioXML)))

            if "-device usb-host" in apFileS:
                apFileM = apFileM.replace("<!-- USB HEADER -->",('\n    '.join(usbXML)))
        # apFileM = apFileM.replace("$USR_",apVars[])
        
        file1.close

        with open(""+apFilePathNoExt+".xml","w") as file:
            file.write(apFileM)
        time.sleep(2)

        os.chdir(sourceDir)         



    apFile = open(""+apFilePathNoExt+".xml","r")
    if "APC-RUN" in apFile.read():
        if args.quiet != True:
            clear()
            print("\n\n   "+color.BOLD+color.GREEN+"SUCCESS"+color.END,"")
            print("   AutoPilot config file converted\n")
            print("   The config file was converted successfully into\n   "+color.BOLD+""+apFilePathNoExt+".xml"+color.END+"\n\n\n\n\n   Please wait...\n\n") 
        time.sleep(3)
        if args.noimport != True:
            clear()
            print("\n\n   "+color.BOLD+color.BLUE+"IMPORT XML FILE"+color.END,"")
            print("   For use with virsh / virt-manager\n")
            print("   You can now import your XML domain file into\n   virt-manager for GUI-based usage.")
            print(color.YELLOW+color.BOLD+"\n   ⚠ "+color.END+color.BOLD+"WARNING"+color.END+"\n   This stage requires superuser permissions.\n   You can also run the following command manually if you wish:\n\n    "+color.BOLD+"$ sudo virsh define "+apFilePathNoExt+".xml\n"+color.END)
            print(color.BOLD+"      1. Import "+apFilePathNoExt+".xml"+color.YELLOW,"⚠"+color.END)
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
                os.system("cp resources/ovmf/OVMF_VARS.fd ovmf/OVMF_VARS.fd")
                clear()
                print("\n\n   "+color.BOLD+color.GREEN+"✔ SUCCESS"+color.END,"")
                print("   XML domain has been defined\n")
                print("   The requested XML file has been successfully defined\n   using virsh, and is now available in virt-manager.\n   The name is displayed below.\n\n   "+color.BOLD+domainTitle+" (ULTMOS)"+color.END+"\n\n\n\n\n\n\n") 
                time.sleep(5)
def manualAPSelect():
        global apFile
        global apFilePath
        global cpydPassthrough
        if cpydPassthrough != 1:
            print("\n\n   "+color.BOLD+"Select AutoPilot Config File"+color.END,"")
            print("   Input a valid AutoPilot-generated config\n")
            print("   You must use a valid file generated by AutoPilot.\n   Any existing VFIO-based args will be kept.\n   AutoPilot-generated config scripts end in .sh")
            
            print(color.BOLD+"\n   Drag the *.sh file onto this window (or type the path) and hit ENTER.\n")
            apFileSelect = str(input(color.BOLD+"AutoPilot Config File> "+color.END))
        elif cpydPassthrough == 1:
            apFileSelect = args.convert
        clear()
        time.sleep(1)
        if os.path.exists(apFileSelect):
            apFile = open(apFileSelect)
            if "APC-RUN" in apFile.read() and ".sh" in apFileSelect:
                global autodetect
                autodetect = False
                print("\n\n   "+color.BOLD+color.GREEN+"VALID AUTOPILOT CONFIG"+color.END,"")
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
                    if apFilePath[0] == "/" and apFilePath[1] == "/":
                            apFilePath = apFilePath.replace("/","",1)
                    if apFilePath[0] == "." and len(apFilePath) > 10:
                        apFilePath = apFilePath.replace(".","",1)
                    
                    cleanPath = r"{}".format(apFilePath)
                    apFilePath = cleanPath


                    
                    apFile = open(apFilePath,"r")
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
                print("\n\n   "+color.BOLD+color.RED+"INVALID AUTOPILOT CONFIG"+color.END,"")
                print("   Your file was not a valid AutoPilot config\n")
                print("   You must use a valid file generated by AutoPilot.\n   Any existing VFIO-based args will be kept.\n   AutoPilot-generated config scripts end in .sh")
                
                print(color.BOLD+"\n   You will be returned to the input screen.\n")
                cpydPassthrough = 0   # KILL PASSTHROUGH AS IT WAS DESTROYED BY USER
                time.sleep(8)
                clear()
                manualAPSelect()
        else:
            print("\n\n   "+color.BOLD+color.RED+"INVALID AUTOPILOT CONFIG"+color.END,"")
            print("   Your file was not a valid AutoPilot config\n")
            print("   You must use a valid file generated by AutoPilot.\n   Any existing VFIO-based args will be kept.\n   AutoPilot-generated config scripts end in .sh")
            
            print(color.BOLD+"\n   You will be returned to the input screen.\n")
            cpydPassthrough = 0   # KILL PASSTHROUGH AS IT WAS DESTROYED BY USER
            time.sleep(8)
            clear()
            manualAPSelect()

if args.importfile is not None or args.convert is not None:
    if args.importfile is not None:
        apFileSelect = args.importfile
        cpydPassthrough = 1
        importXML()
    elif args.convert is not None:
        apFileSelect = args.convert
        apFilePath = args.convert
        autodetect = True
        cpydPassthrough = 1
        convertBrains()
else:
    startup()

if detectChoiceM == "1":
    clear()
    global apFile
    if not os.path.exists("blobs/user/USR_CFG.apb"):
        os.system("cp blobs/*.apb blobs/user/")
    if os.path.exists("./blobs/user/USR_CFG.apb"):
            apFilePath = open("./blobs/user/USR_CFG.apb")
            apFilePath = apFilePath.read()
            if os.path.exists("./"+apFilePath):
                apFile = open("./"+apFilePath,"r")
                if "APC-RUN" in apFile.read():
                    print("\n\n   "+color.BOLD+color.GREEN+"AUTOPILOT CONFIG AUTODETECTED"+color.END,"")
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
                        os.system("cp resources/ovmf/OVMF_VARS.fd ovmf/OVMF_VARS.fd")
                        apFileChosen = 1
                        apFile = open("./"+apFilePath,"r")
                        autodetect = True
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
elif detectChoiceM == "3":
    os.system('./scripts/dlosx.py')
elif detectChoiceM == "2":
    clear()
    importXML()
elif (len(detectChoiceM) == "M" or detectChoiceM.lower() == "m"): # Main Menu
            # Goto Extras and Break
            clear()
            os.system("./scripts/vfio-menu.py")
            
elif detectChoiceM == "?":
    clear()
    print("\n\n   "+color.BOLD+color.GREEN+"OPENING HELP PAGE IN DEFAULT BROWSER"+color.END,"")
    print("   Continue in your browser\n")
    print("\n   I have attempted to open the XML Converter help page in\n   your default browser. Please be patient.\n\n   You will be returned to the last screen in 5 seconds.\n\n\n\n\n")
    os.system('xdg-open https://github.com/Coopydood/ultimate-macOS-KVM/wiki/XML-Converter > /dev/null 2>&1')
    time.sleep(6)
    clear()
    startup()


#https://github.com/Coopydood/ultimate-macOS-KVM/wiki/XML-Converter