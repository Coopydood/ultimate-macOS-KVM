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
    print("\n\n   Welcome to"+color.BOLD+color.PURPLE,"VFIO-PCI Passthrough Assistant"+color.END,"")
    print("   Created by",color.BOLD+"Coopydood\n"+color.END)
    print("   This script will attempt to guide you through the process\n   of passing through your host's physical PCI devices for use\n   within the guest. This is advanced and requires patience. Seriously.\n")
    #print(color.BOLD+"\n"+"Profile:"+color.END,"https://github.com/Coopydood")
    #print(color.BOLD+"   Repo:"+color.END,"https://github.com/Coopydood/ultimate-macOS-KVM")
    print("   Select an option to continue.")
    print(color.BOLD+"\n      1. Start")
    print(color.END+"         Continue to requirements list and prepare your sanity\n")
    print(color.END+"      2. Check GPU compatibility")
    print(color.END+"      B. Back...")
    print(color.END+"      Q. Exit\n")
    detectChoice = int(input(color.BOLD+"Select> "+color.END))

       


def clear(): print("\n" * 150)


def stage1():
    clear()
    
    print("\n\n   "+color.BOLD+"System Requirements"+color.END,"")
    print("   Check your system meets this list\n")
    print("   Okay, so you're committed. Fair enough. But first, you need to make\n   sure your system is ready to even begin this nonsense.\n")
    #print(color.BOLD+"\n"+"Profile:"+color.END,"https://github.com/Coopydood")
    #print(color.BOLD+"   Repo:"+color.END,"https://github.com/Coopydood/ultimate-macOS-KVM")
    print(color.BOLD+"   1. Modern hardware"+color.END)
    print("      You must have a fairly modern PC to do this.")
    print(color.BOLD+"   2. BIOS configured correctly"+color.END)
    print("      Virtualisation and IOMMU *MUST* be enabled.")
    print(color.BOLD+"   3. UEFI"+color.END)
    print("      ...and more UEFI. Everything must be using it.")
    print(color.BOLD+"   4. vfio-pci kernel driver stubbing"+color.END)
    print("      The PCI devices in question must be stubbed correctly.")
    print(color.BOLD+"   5. Unwavering patience"+color.END)
    print("      You NEED to expect a LOT of trial and error. No I'm serious.")
    print(color.BOLD+"\n      1. Continue")
    print(color.END+"      B. Back...")
    print(color.END+"      Q. Exit\n")
    detectChoice1 = int(input(color.BOLD+"Select> "+color.END))
    if detectChoice1 == 1:
        stage2()
    elif detectChoice1 == "B" or detectChoice == "b":
        startup()
    elif detectChoice1 == "q" or detectChoice == "Q":
        exit


startup()


if detectChoice == 1:
    clear()
    time.sleep(1)
    stage1()
elif detectChoice == 2:
    os.system('./scripts/gpu-check.py')

elif detectChoice == "B" or detectChoice == "b":
    os.system('./scripts/extras.py')
elif detectChoice == "q" or detectChoice == "Q":
    exit