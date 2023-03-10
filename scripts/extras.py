#!/usr/bin/env python3
# pylint: disable=C0301,C0116,C0103,R0903

"""
This script was created by Coopydood as part of the ultimate-macOS-KVM project.

https://github.com/user/Coopydood
https://github.com/Coopydood/ultimate-macOS-KVM
Signature: 4CD28348A3DD016F

"""

# This script should NOT be run directly, but instead from the main "setup.py" script.


import os
import time
import subprocess
import re 
import json
import sys
import argparse

sys.path.insert(0, 'scripts')

detectChoice = 1
latestOSName = "Ventura"
latestOSVer = "13"
runs = 0

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
    if detected == 0:
        print("\n\n   Welcome to"+color.BOLD+color.BLUE,"Ultimate macOS KVM Extras"+color.END,"")
        print("   Created by",color.BOLD+"Coopydood\n"+color.END)
        print("   This script can assist you in more advanced post-install\n   processes like"+color.BOLD,"PCI/GPU passthrough, dumping your VBIOS,\n   "+color.END+"and"+color.BOLD,"importing your VM into virt-manager.\n"+color.END)
        #print(color.BOLD+"\n"+"Profile:"+color.END,"https://github.com/Coopydood")
        #print(color.BOLD+"   Repo:"+color.END,"https://github.com/Coopydood/ultimate-macOS-KVM")
        print("   Select an option to continue.")
        print(color.BOLD+"\n      1. Create and import XML file")
        print(color.END+"         Auto generate an XML file from your boot script and\n         import it into virsh / virt-manager\n")
        print(color.END+"      2. VFIO-PCI passthrough assistant")
        
        print(color.END+"      3. Create a backup of config files")
        print(color.END+"      4. Dump VBIOS to ROM file")
        #print(color.END+"      4. Import config file into virt-manager")
        print(color.RED+"      R. Reset OpenCore image and vNVRAM")
        print(color.RED+"      X. Download and restore all")
        print(color.END+"      B. Back...")
        print(color.END+"      Q. Exit\n")
    else:
        print("\n\n   Welcome to"+color.BOLD+color.BLUE,"Ultimate macOS KVM Extras"+color.END,"")
        print("   Created by",color.BOLD+"Coopydood\n"+color.END)
        if detected == True:
            print(color.YELLOW+"   ???  Virtual machine detected, functionality may be limited\n"+color.END)
        print("   This script can assist you in more advanced post-install\n   processes like"+color.BOLD,"PCI/GPU passthrough, dumping your VBIOS,\n   "+color.END+"and"+color.BOLD,"importing your VM into virt-manager.\n"+color.END)
        #print(color.BOLD+"\n"+"Profile:"+color.END,"https://github.com/Coopydood")
        #print(color.BOLD+"   Repo:"+color.END,"https://github.com/Coopydood/ultimate-macOS-KVM")
        print("   Select an option to continue.")
        print(color.BOLD+"\n      1. Create and import XML file"+color.END+color.YELLOW,"???")
        print(color.END+"         Auto generate an XML file from your boot script and\n         import it into virsh / virt-manager\n")
        print(color.END+"      2. VFIO-PCI passthrough assistant"+color.YELLOW,"???")
        print(color.END+"      3. "+color.YELLOW,"")
        print(color.END+"      4. Create a backup of config files")
        print(color.END+"      5. Dump VBIOS to ROM file"+color.YELLOW,"???")
        #print(color.END+"      4. Import config file into virt-manager")
        print(color.RED+"      R. Reset OpenCore image and vNVRAM")
        print(color.RED+"      X. Download and restore all")
        print(color.END+"      B. Back...")
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


startup()
clear()

if detectChoice == "1":
    os.system('./scripts/autopilot.py')
elif detectChoice == "2":
    os.system('./scripts/extras/vfio-passthrough.py')
elif detectChoice == "2":
    os.system('./scripts/extras/smbios.py')

elif detectChoice == "4":
    os.system('./scripts/extras/backupassist.py')

elif detectChoice == "r" or detectChoice == "R":
    os.system('./scripts/extras/ocreset.py')
elif detectChoice == "x" or detectChoice == "X":
    os.system('./scripts/extras/obliterator.py')
elif detectChoice == "q" or detectChoice == "Q":
    exit