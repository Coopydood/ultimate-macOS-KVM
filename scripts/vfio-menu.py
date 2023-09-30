#!/usr/bin/env python3
# pylint: disable=C0301,C0116,C0103,R0903

"""
This script was created by Coopydood as part of the ultimate-macOS-KVM project.

https://github.com/user/Coopydood
https://github.com/Coopydood/ultimate-macOS-KVM
Signature: 4CD28348A3DD016F

"""

# This script should NOT be run directly, but instead from the main "main.py" script.


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

version = open("./.version")
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
    print("\n\n   Welcome to"+color.BOLD+color.PURPLE,"VFIO-PCI Tools"+color.END,"")
    print("   Created by",color.BOLD+"Coopydood\n"+color.END)
    print("   This menu includes some advanced tools to help prepare\n   and configure"+color.BOLD,"PCI passthrough, IOMMU grouping, "+color.END+"and the\n  "+color.BOLD,"VFIO-PCI kernel driver.\n"+color.END)
    #print(color.BOLD+"\n"+"Profile:"+color.END,"https://github.com/Coopydood")
    #print(color.BOLD+"   Repo:"+color.END,"https://github.com/Coopydood/ultimate-macOS-KVM")
    print("   Select an option to continue.")
    print(color.BOLD+"\n      1. VFIO-PCI passthrough assistant")
    print(color.END+"         Automatically configure PCI passthrough with ease\n         using an existing AutoPilot config file\n")
    print(color.END+"      2. Check if your system is ready...")
    print(color.END+"      3. Display system IOMMU grouping")
    print(color.END+"      4. Get and display vfio-pci device IDs")
    print(color.END+"      5. Verify devices bound to vfio-pci driver")
    #print(color.END+"      6. Dump VBIOS to ROM file")
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
    os.system('./scripts/extras/vfio-passthrough.py')
elif detectChoice == "2":
    os.system('./scripts/extras/vfio-check.py')

elif detectChoice == "3":
    os.system('./scripts/iommu.sh')
elif detectChoice == "4":
    os.system('./scripts/vfio-ids.py')
elif detectChoice == "5":
    os.system('./scripts/vfio-pci.py')
elif detectChoice == "6":
    os.system('./scripts/extras/vbios-dump.py')

elif detectChoice == "r" or detectChoice == "R":
    os.system('./scripts/vifo-pci.py')
elif detectChoice == "b" or detectChoice == "B":
    os.system('./main.py')
elif detectChoice == "q" or detectChoice == "Q":
    exit