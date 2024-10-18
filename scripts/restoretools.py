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
sys.path.append('./resources/python')
from cpydColours import color

sys.path.insert(0, 'scripts')

detectChoice3 = 1
latestOSName = "Ventura"
latestOSVer = "13"
runs = 0

version = open("./.version")
version = version.read()


def startup():
    global detectChoice3
    if detected == 0:
        print("\n\n  "+color.RED+color.BOLD,"RESTORE TOOLS"+color.END,"")
        print("   by",color.BOLD+"Coopydood\n"+color.END)
        print("   This menu lets you reset and restore various aspects\n   of the repository, such as"+color.BOLD,"the vNVRAM, OpenCore image, OVMF\n   firmware, and even the repo itself."+color.END+"\n"+color.RED,"\n   Most things in this menu are intentionally destructive!"+color.END)
        #print(color.BOLD+"\n"+"Profile:"+color.END,"https://github.com/Coopydood")
        #print(color.BOLD+"   Repo:"+color.END,"https://github.com/Coopydood/ultimate-macOS-KVM")
        print(color.BOLD+"\n      1. Reset vNVRAM")
        print(color.END+"         Restores the default virtual vNVRAM file.\n         This is not destructive and fixes most issues.\n")
        print(color.RED+"      2. Reset OpenCore image...")
        
        print(color.RED+"      3. Restore OVMF code files...")
        print(color.RED+"      4. Delete AutoPilot data...")
        #print(color.END+"      4. Import config file into virt-manager")
        print(color.RED+"      R. Restore all components locally...")
        print(color.RED+color.BOLD+"      X. Download and restore repository...")
        print(color.END+"      B. Back...")
        print(color.END+"      Q. Exit\n")
    detectChoice3 = str(input(color.BOLD+"Select> "+color.END))

       


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

if detectChoice3 == "1":
    os.system('python3 ./scripts/restore/nvram.py')
elif detectChoice3 == "2":
    os.system('python3 ./scripts/restore/ocimage.py')
elif detectChoice3 == "3":
    os.system('python3 ./scripts/restore/ovmf.py')

elif detectChoice3 == "4":
    os.system('python3 ./scripts/restore/apwf.py')

elif detectChoice3 == "r" or detectChoice3 == "R":
    os.system('python3 ./scripts/restore/localfull.py')
elif detectChoice3 == "x" or detectChoice3 == "X":
    os.system('python3 ./scripts/restore/obliterator.py')
elif detectChoice3 == "b" or detectChoice3 == "B":
    os.system('python3 ./scripts/extras.py')
elif detectChoice3 == "q" or detectChoice3 == "Q":
    exit