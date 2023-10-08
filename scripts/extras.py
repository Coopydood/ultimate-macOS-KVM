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
latestOSName = "Sonoma"
latestOSVer = "14"
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
    if detected == 0:
        print("\n\n   Welcome to"+color.BOLD+color.BLUE,"Ultimate macOS KVM Extras"+color.END,"")
        print("   Created by",color.BOLD+"Coopydood\n"+color.END)
        print("   This script can assist you in post-install processes,\n   such as"+color.BOLD,"importing your VM into virt-manager, backing up\n   your data, "+color.END+"and"+color.BOLD,"restore options for troubleshooting.\n"+color.END)
        #print(color.BOLD+"\n"+"Profile:"+color.END,"https://github.com/Coopydood")
        #print(color.BOLD+"   Repo:"+color.END,"https://github.com/Coopydood/ultimate-macOS-KVM")
        print("   Select an option to continue.")
        print(color.BOLD+"\n      1. Convert and import XML file")
        print(color.END+"         Auto generate an XML file from your boot script and\n         import it into virsh / virt-manager\n")
        print(color.END+"      2. VFIO-PCI passthrough assistant")
        
        #print(color.END+"      . Create a backup of config files")
        print(color.END+"      3. Open GitHub project page")
        print(color.END+"      4. VFIO-PCI tools...")
        print(color.END+"      5. OpenCore configuration assistant...")
        print(color.END+"      6. Boot Argument Editor...")
        print(color.RED+"      R. Restore tools...")
        print(color.END+"      I. Report an issue...")
        print(color.END+"      B. Back...")
        print(color.END+"      Q. Exit\n")
    else:
        print("\n\n   Welcome to"+color.BOLD+color.BLUE,"Ultimate macOS KVM Extras"+color.END,"")
        print("   Created by",color.BOLD+"Coopydood\n"+color.END)
        if detected == True:
            print(color.YELLOW+"   ⚠  Virtual machine detected, functionality may be limited\n"+color.END)
        print("   This script can assist you in more advanced post-install\n   processes like"+color.BOLD,"PCI/GPU passthrough, dumping your VBIOS,\n   "+color.END+"and"+color.BOLD,"importing your VM into the virt-manager GUI.\n"+color.END)
        #print(color.BOLD+"\n"+"Profile:"+color.END,"https://github.com/Coopydood")
        #print(color.BOLD+"   Repo:"+color.END,"https://github.com/Coopydood/ultimate-macOS-KVM")
        print("   Select an option to continue.")
        print(color.BOLD+"\n      1. Convert and import XML file"+color.END+color.YELLOW,"⚠")
        print(color.END+"         Auto generate an XML file from your boot script and\n         import it into virsh / virt-manager\n")
        print(color.END+"      2. VFIO-PCI passthrough assistant"+color.YELLOW,"⚠")
        #print(color.END+"      3. Create a backup of config files")
        print(color.END+"      3. Open GitHub project page")
        print(color.END+"      4. VFIO-PCI tools...")
        print(color.END+"      5. OpenCore configuration assistant...")
        print(color.END+"      6. Boot Argument Editor...")
        print(color.RED+"      R. Restore tools...")
        print(color.END+"      I. Report an issue...")
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
    os.system('./scripts/extras/xml-convert.py')
elif detectChoice == "2":
    os.system('./scripts/extras/vfio-passthrough.py')
#elif detectChoice == "3":
 #   os.system('./scripts/extras/smbios.py')
elif detectChoice == "3":
    
    print("\n\n   "+color.BOLD+color.GREEN+"✔  OPENING PROJECT IN DEFAULT BROWSER"+color.END,"")
    print("   Continue in your browser\n")
    print("\n   I have attempted to open the project page in\n   your default browser. Please be patient.\n\n   You will be returned to the extras menu in 5 seconds.\n\n\n\n\n")
    os.system('xdg-open https://github.com/Coopydood/ultimate-macOS-KVM > /dev/null 2>&1')
    time.sleep(6)
    clear()
    os.system('./scripts/extras.py')
elif detectChoice == "4":
    os.system('./scripts/vfio-menu.py')
elif detectChoice == "5":
    os.system('./scripts/domtrues/nbdassistant.py')
elif detectChoice == "6":
    os.system('./scripts/extras/boot-args.py')

elif detectChoice == "i" or detectChoice == "I":
    
    print("\n\n   "+color.BOLD+color.GREEN+"✔  OPENING ISSUE CREATOR IN DEFAULT BROWSER"+color.END,"")
    print("   Continue in your browser\n")
    print("\n   I have attempted to open the new issue form in\n   your default browser. Please be patient.\n\n   You will be returned to the extras menu in 5 seconds.\n\n\n\n\n")
    os.system('xdg-open https://github.com/Coopydood/ultimate-macOS-KVM/issues/new > /dev/null 2>&1')
    time.sleep(6)
    clear()
    os.system('./scripts/extras.py')


elif detectChoice == "r" or detectChoice == "R":
    os.system('./scripts/restoretools.py')
elif detectChoice == "b" or detectChoice == "B":
    os.system('./main.py')
elif detectChoice == "q" or detectChoice == "Q":
    exit