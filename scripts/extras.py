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

detectChoice = 1
latestOSName = "Sonoma"
latestOSVer = "14"
runs = 0

version = open("./.version")
version = version.read()


def startup():
    global detectChoice
    if detected == 0:
        print("\n\n  "+color.BOLD+color.BLUE,"EXTRAS"+color.END,"")
        print("   by",color.BOLD+"Coopydood\n"+color.END)
        print("   These tools can assist you in post-install processes,\n   such as"+color.BOLD,"importing your VM into virt-manager, backing up\n   your data, "+color.END+"and"+color.BOLD,"restore options for troubleshooting.\n"+color.END)
        #print(color.BOLD+"\n"+"Profile:"+color.END,"https://github.com/Coopydood")
        #print(color.BOLD+"   Repo:"+color.END,"https://github.com/Coopydood/ultimate-macOS-KVM")
        #print("   Select an option to continue.")
        print(color.BOLD+"      1. Convert and import XML file")
        print(color.END+"         Auto generate an XML file from your boot script and\n         import it into virsh / virt-manager\n")
        #print(color.END+"      2. Passthrough tools...")
        print(color.END+"      2. OpenCore Configuration Assistant...")
        print(color.END+"      3. macOS Boot Argument Editor...")
        print(color.END+"      4. GRUB Argument Editor...")
        print(color.END+"      5. Generate SMBIOS / Serial Number...\n")
        print(color.RED+"      R. Restore tools...")
        print(color.END+"      I. Report an issue...")
        print(color.END+"      B. Back...")
        print(color.END+"      Q. Exit\n")  
    detectChoice = str(input(color.BOLD+"Select> "+color.END))

       


def clear(): print("\n" * 150)

os.system("chmod +x scripts/*.py")
os.system("chmod +x scripts/*.sh")
os.system("chmod +x resources/dmg2img")

detected = 0





startup()
clear()

if detectChoice == "1":
    os.system('./scripts/extras/xml-convert.py')
elif detectChoice == "99":
    os.system('./scripts/vfio-menu.py')
elif detectChoice == "2":
    os.system('./scripts/hyperchromiac/nbdassistant.py')
#elif detectChoice == "3":
#    
#    print("\n\n   "+color.BOLD+color.GREEN+"✔  OPENING PROJECT IN DEFAULT BROWSER"+color.END,"")
#    print("   Continue in your browser\n")
#    print("\n   I have attempted to open the project page in\n   your default browser. Please be patient.\n\n   You will be returned to the extras menu in 5 seconds.\n\n\n\n\n")
#    os.system('xdg-open https://github.com/Coopydood/ultimate-macOS-KVM > /dev/null 2>&1')
#    time.sleep(6)
#    clear()
#    os.system('./scripts/extras.py')
elif detectChoice == "3":
    os.system('./scripts/extras/boot-args.py')
elif detectChoice == "4":
    os.system('./scripts/hyperchromiac/grub-args.py')
elif detectChoice == "5":
    os.system('./resources/python/smbios/GenSMBIOS.py')
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
