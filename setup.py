#!/usr/bin/env python3
# pylint: disable=C0301,C0116,C0103,R0903

"""
This script was created by Coopydood as part of the ultimate-macOS-KVM project.

https://github.com/user/Coopydood
https://github.com/Coopydood/ultimate-macOS-KVM
Signature: 4CD28348A3DD016F

"""


# THIS IS THE MAIN SETUP FILE! RUN THIS FILE FIRST!
# ./setup.py


import os
import time
import subprocess
import re 
import json
import sys
import argparse

sys.path.insert(0, 'scripts')

parser = argparse.ArgumentParser("setup")
parser.add_argument("-svmc", "--skip-vm-check", dest="svmc", help="Skip the arbitrary VM check",action="store_true")

args = parser.parse_args()

global apFilePath

detectChoice = 1
latestOSName = "Ventura"
latestOSVer = "13"
runs = 0
apFilePath = ""

version = open("./VERSION")
version = version.read()

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



def startup():
    global detectChoice
    print("\n\n   Welcome to"+color.BOLD+color.CYAN,"Ultimate macOS KVM"+color.END,"(v"+version+")")
    print("   Created by",color.BOLD+"Coopydood\n"+color.END)
    if isVM == True:
        print(color.YELLOW+"   ⚠  Virtual machine detected, functionality may be limited\n"+color.END)
    if os.path.exists("blobs/USR_CFG.apb"):
            tainted = 1
    else:
        print("   This script can assist you in some often-tedious setup, including\n   processes like"+color.BOLD,"checking your GPU, getting vfio-ids, downloading macOS,\n   "+color.END+"and more. Think of it like your personal KVM swiss army knife.\n")
    #print(color.BOLD+"\n"+"Profile:"+color.END,"https://github.com/Coopydood")
    #print(color.BOLD+"   Repo:"+color.END,"https://github.com/Coopydood/ultimate-macOS-KVM")
    print("   Select an option to continue.")
    if os.path.exists("./blobs/USR_CFG.apb"):
            global apFilePath
            apFilePath = open("./blobs/USR_CFG.apb")
            apFilePath = apFilePath.read()
            macOSVer = open("./blobs/USR_TARGET_OS.apb")
            macOSVer = macOSVer.read()
            macOSVer = str(int(macOSVer) / 100)
            if os.path.exists("./"+apFilePath):
                apFile = open("./"+apFilePath,"r")
            
                if "APC-RUN" in apFile.read():
                    print(color.BOLD+"\n      B. Boot macOS "+macOSVer+"")
                    print(color.END+"         Start macOS using the detected "+apFilePath+" script.")
                    print(color.END+"\n      1. AutoPilot")

                else:
                    print(color.BOLD+"\n      1. AutoPilot (Experimental)")
                    print(color.END+"         Quickly and easily set up a macOS VM in just a few steps\n")

            else:
                print(color.BOLD+"\n      1. AutoPilot (Experimental)")
                print(color.END+"         Quickly and easily set up a macOS VM in just a few steps\n")
    else:
        print(color.BOLD+"\n      1. AutoPilot (Experimental)")
        print(color.END+"         Quickly and easily set up a macOS VM in just a few steps\n")
    if isVM == True:
        
        print(color.END+"      2. Download and convert macOS image")
        print(color.END+"      3. Check GPU compatibility"+color.YELLOW,"⚠")
        print(color.END+"      4. Check IOMMU grouping"+color.YELLOW,"⚠")
        print(color.END+"      5. Get and display vfio-pci IDs"+color.YELLOW,"⚠")
        print(color.END+"      6. Verify devices bound to vfio-pci"+color.YELLOW,"⚠")
    else:
        print(color.END+"      2. Download and convert macOS image")
        print(color.END+"      3. Check GPU compatibility")
        print(color.END+"      4. Check IOMMU grouping")
        print(color.END+"      5. Get and display vfio-pci IDs")
        print(color.END+"      6. Verify devices bound to vfio-pci")
    
    print(color.END+"      E. Extras...")
    print(color.END+"      U. Check for updates...")
    print(color.END+"      Q. Exit\n")
    detectChoice = str(input(color.BOLD+"Select> "+color.END))

       


def clear(): print("\n" * 150)



os.system("chmod +x scripts/*.py")
os.system("chmod +x scripts/*.sh")
os.system("chmod +x resources/dmg2img")



output_stream = os.popen('lspci')
vmc1 = output_stream.read()

detected = 0

global isVM

isVM = False

if "VMware" in vmc1:
   detected = 1

if "VirtualBox" in vmc1 or "Oracle" in vmc1:
   detected = 1

if "Redhat" in vmc1 or "RedHat" in vmc1 or "QEMU" in vmc1:
   detected = 1

if "Bochs" in vmc1 or "Sea BIOS" in vmc1 or "SeaBIOS" in vmc1:
   detected = 1

clear()

if detected == 1:
    if args.svmc == True:
        clear()
        startup()
    else:
        isVM = True
        print("\n   "+color.BOLD+color.YELLOW+"⚠ VIRTUAL MACHINE DETECTED"+color.END)
        print("   Virtualized devices detected")
        print("\n   I've determined that it's more than likely that \n   you're using a virtual machine to run this. I won't\n   stop you, but there really isn't much point in continuing."+color.END)
        
        print("\n   "+color.BOLD+color.YELLOW+"PROBLEM:",color.END+"Virtual hardware detected"+color.END)
        print(color.BOLD+"\n      1. Exit")
        print(color.END+"      2. Continue anyway\n")
        stageSelect = str(input(color.BOLD+"Select> "+color.END))
   
        if stageSelect == "1":
            sys.exit

        elif stageSelect == "2": 
            clear()
            startup()
else:
    clear()
    startup()










if detectChoice == "1":
    os.system('./scripts/autopilot.py')
elif detectChoice == "2":
    os.system('./scripts/dlosx.py')

elif detectChoice == "3":
    clear()
    os.system('./scripts/gpu-check.py')
elif detectChoice == "4":
    clear()
    os.system('./scripts/iommu.sh')
elif detectChoice == "5":
    clear()
    os.system('./scripts/vfio-ids.py')
elif detectChoice == "6":
    clear()
    os.system('./scripts/vfio-pci.py')
elif detectChoice == "e" or detectChoice == "E":
    clear()
    os.system('./scripts/extras.py')
elif detectChoice == "u" or detectChoice == "U":
    clear()
    os.system('./scripts/repo-update.py')
elif detectChoice == "q" or detectChoice == "Q":
    exit
elif detectChoice == "b" or detectChoice == "B":
    clear()
    os.system("./"+apFilePath)