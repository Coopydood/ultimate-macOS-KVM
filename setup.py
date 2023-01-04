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

parser = argparse.ArgumentParser("gpu-check")
parser.add_argument("-a", "--auto", dest="auto", help="Detect GPU(s) automatically",action="store_true")
parser.add_argument("-m", "--manual", dest="manual", help="Enter GPU model manually", metavar="<model>", type=str)
parser.add_argument("-f", "--force", dest="forceModel", metavar="<model>", help="Override auto-detected GPU with a custom model. Pretty useless, mostly for debugging.", type=str)

args = parser.parse_args()

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

os.system('./scripts/vmcheck.py')

def startup():
    global detectChoice
    print("\n\n   Welcome to"+color.BOLD+color.YELLOW,"Ultimate macOS KVM Setup"+color.END,"(BETA)")
    print("   Created by",color.BOLD+"Coopydood\n"+color.END)
    print("   This script can assist you in some often-tedious setup, including\n   processes like"+color.BOLD,"checking your GPU, getting vfio-ids, downloading macOS,\n   "+color.END+"and more. Think of it like your personal KVM swiss army knife.\n")
    #print(color.BOLD+"\n"+"Profile:"+color.END,"https://github.com/Coopydood")
    #print(color.BOLD+"   Repo:"+color.END,"https://github.com/Coopydood/ultimate-macOS-KVM")
    print("   Select an option to continue.")
    print(color.BOLD+"\n      1. AutoPilot config wizard (Experimental)")
    print(color.END+"         Quickly and easily set up a macOS VM in just a few steps\n")
    print(color.END+"      2. Download and convert macOS image")
    print(color.END+"      3. Check GPU compatibility")
    print(color.END+"      4. Check IOMMU grouping")
    print(color.END+"      5. Get and display vfio-pci IDs")
    print(color.END+"      6. Verify devices bound to vfio-pci")
    print(color.END+"      E. Extras...")
    print(color.END+"      Q. Exit\n")
    detectChoice = int(input(color.BOLD+"Select> "+color.END))

       


def clear(): print("\n" * 150)

os.system("chmod +x scripts/*.py")
os.system("chmod +x scripts/*.sh")
os.system("chmod +x resources/dmg2img")

startup()
clear()

if detectChoice == 1:
    os.system('./scripts/autopilot.py')
elif detectChoice == 2:
    os.system('./scripts/dlosx.py')

elif detectChoice == 3:
    os.system('./scripts/gpu-check.py')
elif detectChoice == 4:
    os.system('./scripts/iommu.sh')
elif detectChoice == 5:
    os.system('./scripts/vfio-ids.py')
elif detectChoice == 6:
    os.system('./scripts/vfio-pci.py')
elif detectChoice == "e" or detectChoice == "E":
    os.system('./scripts/extras.py')
elif detectChoice == "q" or detectChoice == "Q":
    exit