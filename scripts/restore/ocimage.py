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
sys.path.append('./resources/python')
from cpydColours import color

detectChoice = 1
latestOSName = "Ventura"
latestOSVer = "13"
runs = 0
global errorMessage

version = open("./.version")
version = version.read()

def clear(): print("\n" * 150)


clear()
print("\n\n   "+color.BOLD+color.RED+"↺  RESET OPENCORE AND vNVRAM"+color.END,"")
print("   Please wait\n")
print(color.END+"\n\n\n   Checking integrity...\n\n\n\n\n")
if os.path.exists("./resources/oc_store/compat_new/OpenCore.qcow2") and os.path.exists("./resources/oc_store/compat_old/OpenCore.qcow2") and os.path.exists("./resources/ovmf/OVMF_CODE.fd") and os.path.exists("./resources/ovmf/OVMF_VARS.fd") and os.path.exists("./resources/ovmf/OVMF_VARS_1280x720.fd"):
    integrity = 1
else:
    integrity = 0
#time.sleep(5)


# UNCOMMENT TO FORCE INTEGRITY CHECK RESULT
#integrity = 0


clear()
print("\n\n   "+color.BOLD+color.RED+"↺  RESET OPENCORE AND vNVRAM"+color.END,"")
print("   Restore to default state\n")

print(color.BOLD+"   Integrity")
if integrity == 1:
   print(color.GREEN+color.BOLD+"   ●"+color.END+" PASSED")
else:
   print(color.RED+color.BOLD+"   ●"+color.END+" DAMAGED")

if integrity == 1:
    print(color.END+color.BOLD+"\n   THIS TOOL:")
    print(color.BOLD+color.GREEN+"       WILL "+color.END+"reset the virtual NVRAM")
    print(color.BOLD+color.GREEN+"       WILL "+color.END+"reset the OpenCore image back to default")
    print(color.BOLD+color.YELLOW+"      MIGHT "+color.END+"fix common boot issues")
    print(color.BOLD+color.RED+"   WILL NOT "+color.END+"replace the OVMF code with a new copy")
    print(color.BOLD+color.RED+"   WILL NOT "+color.END+"delete your configs or vHDD files")
    print(color.BOLD+color.RED+"   WILL NOT "+color.END+"create a backup of reset files")

    #print(color.END+color.BOLD+"\n                 THIS TOOL")
    #print(color.BOLD+color.GREEN+"          WILL       "+color.END+"|"+color.BOLD+color.RED+"       WILL NOT"+color.END)
    #print("      Reset vNVRAM   |     Delete vHDDs")
    #print("      Reset vNVRAM   |     Delete vHDDs")
    print("\n   ARE YOU SURE YOU WANT TO RESET?\n   This cannot be undone.\n"+color.END)
    print(color.BOLD+color.RED+"      X. RESET")
    print(color.END+"      Q. Exit to restore tools...\n")
    detectChoice2 = str(input(color.BOLD+"Select> "+color.END))
else:
    detectChoice2 = "F"
    print("\n\n   The repo integrity could not be verified.\n   One or more files required to restore are damaged or missing.\n\n   The script cannot continue.\n\n")

def success():
    clear()
    print("\n\n   "+color.BOLD+color.GREEN+"✔ RESTORE COMPLETE"+color.END,"")
    print("   OpenCore and vNVRAM has been reset\n")
    print("   The OpenCore image and vNVRAM file have been reset.\n   You can safely use the new files."+color.END+"\n\n\n\n\n\n\n")

def throwError():
    global errorMessage
    clear()
    print("\n   "+color.BOLD+color.RED+"✖ FAILED"+color.END)
    print("   Unable to continue")
    print("\n   Sorry, something happened and the restoration failed. \n   You may need to reinstall the repository.\n   If you think this was a bug, please report it on GitHub."+color.END)
    print("\n   "+color.BOLD+color.RED+"ERROR:",color.END+color.BOLD,errorMessage,color.END+"\n\n\n\n")


if detectChoice2 == "X" or detectChoice2 == "x":
    
    clear()
    print("\n\n   "+color.BOLD+color.RED+"↺  RESET OPENCORE AND vNVRAM"+color.END,"")
    print("   Restoring...\n\n\n")
    print("   Please wait while the restore process is in progress.\n   This may take a few moments.\n\n   DO NOT INTERRUPT THIS OPERATION.\n\n\n")
    time.sleep(5)
    os.system("rm ./boot/OpenCore.qcow2 > /dev/null 2>&1")
    os.system("rm ./boot/config.plist > /dev/null 2>&1")
    os.system("rm -rf ./boot/EFI > /dev/null 2>&1")

    global USR_TARGET_OS

    blob = open("./blobs/user/USR_TARGET_OS.apb","r")
    USR_TARGET_OS = blob.read()
    USR_TARGET_OS = int(USR_TARGET_OS)
    if USR_TARGET_OS < 999:
        USR_TARGET_OS = USR_TARGET_OS * 100
    blob.close()

    time.sleep(2)
    if USR_TARGET_OS <= 1015:
        os.system("cp resources/oc_store/compat_old/OpenCore.qcow2 boot/OpenCore.qcow2")
    else:
        os.system("cp resources/oc_store/compat_new/OpenCore.qcow2 boot/OpenCore.qcow2")

    
    errorMessage = "Restoration failed. You may not have sufficient\n           permissions or damaged files."

    if os.path.exists("boot/OpenCore.qcow2"):
        success()
    else:
        throwError()
    
    





elif detectChoice2 == "Q" or detectChoice2 == "q":
    clear()
    os.system("./scripts/restoretools.py")
elif detectChoice2 == "F":
    time.sleep(5)