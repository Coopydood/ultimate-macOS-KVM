#!/usr/bin/env python3
# pylint: disable=C0301,C0116,C0103,R0903

"""
This script was created by Coopydood as part of the ultimate-macOS-KVM project.
It will not work outside of this project.

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

detectChoice = 1
latestOSName = "Ventura"
latestOSVer = "13"
runs = 0

version = open("./VERSION")
version = version.read()

def clear(): print("\n" * 150)

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
   GRAY = '\u001b[38;5;245m'


clear()
print("\n\n   "+color.BOLD+color.RED+"↺  RESET OPENCORE AND vNVRAM"+color.END,"")
print("   Please wait\n")
print(color.END+"\n\n\n   Checking integrity...\n\n\n\n\n")
if os.path.exists("./resources/oc_store/compat_new/OpenCore.qcow2") and os.path.exists("./resources/oc_store/compat_old/OpenCore.qcow2") and os.path.exists("./ovmf/var/OVMF_CODE.fd") and os.path.exists("./ovmf/var/OVMF_VARS.fd") and os.path.exists("./ovmf/var/OVMF_VARS-1280x720.fd") and os.path.exists("./resources/oc_store/compat_new/config.plist"):
    integrity = 1
else:
    integrity = 0
#time.sleep(5)


# UNCOMMENT TO FORCE INTEGRITY CHECK RESULT
#integrity = 0


clear()
print("\n\n   "+color.BOLD+color.RED+"↺  RESET OPENCORE AND vNVRAM"+color.END,"")
print("   Restore to default state\n")

print(color.BOLD+"   Integrity Check")
if integrity == 1:
   print(color.GREEN+color.BOLD+"   ●"+color.END+" PASSED")
else:
   print(color.RED+color.BOLD+"   ●"+color.END+" DAMAGED")

if integrity == 1:
    print(color.END+color.BOLD+"\n   THIS TOOL:")
    print(color.BOLD+color.GREEN+"       WILL "+color.END+"reset the virtual NVRAM")
    print(color.BOLD+color.GREEN+"       WILL "+color.END+"reset the OpenCore image back to default")
    print(color.BOLD+color.GREEN+"       WILL "+color.END+"replace the OVMF code with a new copy")
    print(color.BOLD+color.YELLOW+"      MIGHT "+color.END+"fix common boot issues")
    print(color.BOLD+color.RED+"   WILL NOT "+color.END+"delete your configs or vHDD files")
    print(color.BOLD+color.RED+"   WILL NOT "+color.END+"create a backup of reset files")

    #print(color.END+color.BOLD+"\n                 THIS TOOL")
    #print(color.BOLD+color.GREEN+"          WILL       "+color.END+"|"+color.BOLD+color.RED+"       WILL NOT"+color.END)
    #print("      Reset vNVRAM   |     Delete vHDDs")
    #print("      Reset vNVRAM   |     Delete vHDDs")
    print("\n   ARE YOU SURE YOU WANT TO RESET?\n   This cannot be undone.\n"+color.END)
    print(color.BOLD+color.RED+"      X. RESET")
    print(color.END+"      Q. Exit to extras menu\n")
    detectChoice2 = str(input(color.BOLD+"Select> "+color.END))
else:
    print("\n\n   The repo integrity could not be verified.\n   One or more files required to restore are damaged or missing.\n\n   The script cannot continue.\n\n")

if detectChoice2 == "X" or detectChoice2 == "x":
    clear()
    print("\n\n   "+color.BOLD+color.RED+"↺  RESET OPENCORE AND vNVRAM"+color.END,"")
    print("   Restoring...\n\n\n")
    print("   Please wait while the restore process is in progress.\n   This may take a few moments.\n\n   DO NOT INTERRUPT THIS OPERATION.\n\n\n")
    time.sleep(5)
elif detectChoice2 == "Q" or detectChoice2 == "q":
    clear()
    os.system("./scripts/extras.py")