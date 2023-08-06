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
global errorMessage

version = open("./.version")
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
print("\n\n   "+color.BOLD+color.RED+"↺  RESET ALL COMPONENTS LOCALLY"+color.END,"")
print("   Please wait\n")
print(color.END+"\n\n\n   Checking integrity...\n\n\n\n\n")
if os.path.exists("./resources/oc_store/compat_new/OpenCore.qcow2") and os.path.exists("./resources/oc_store/compat_old/OpenCore.qcow2") and os.path.exists("./resources/ovmf/OVMF_CODE.fd") and os.path.exists("./resources/ovmf/OVMF_VARS.fd") and os.path.exists("./resources/ovmf/OVMF_VARS_1280x720.fd") and os.path.exists("./resources/oc_store/compat_new/config.plist") and os.path.exists("./resources/script_store/extras.py") and os.path.exists("./resources/script_store/main.py"):
    integrity = 1
else:
    integrity = 0
#time.sleep(5)


# UNCOMMENT TO FORCE INTEGRITY CHECK RESULT
#integrity = 0


clear()
print("\n\n   "+color.BOLD+color.RED+"↺  RESET ALL COMPONENTS LOCALLY"+color.END,"")
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
    #print(color.BOLD+color.GREEN+"       WILL "+color.END+"delete AutoPilot configuration data")
    print(color.BOLD+color.GREEN+"       WILL "+color.END+"replace the OVMF code with a new copy")
    print(color.BOLD+color.GREEN+"       WILL "+color.END+"fix permissions on resources")
    print(color.BOLD+color.YELLOW+"      MIGHT "+color.END+"fix some quirky issues")
    print(color.BOLD+color.YELLOW+"      MIGHT "+color.END+"downgrade repository files to older versions")
    print(color.BOLD+color.RED+"   WILL NOT "+color.END+"delete your configs or vHDD files")
    print(color.BOLD+color.RED+"   WILL NOT "+color.END+"create a backup of reset files")

    #print(color.END+color.BOLD+"\n                 THIS TOOL")
    #print(color.BOLD+color.GREEN+"          WILL       "+color.END+"|"+color.BOLD+color.RED+"       WILL NOT"+color.END)
    #print("      Reset vNVRAM   |     Delete vHDDs")
    #print("      Reset vNVRAM   |     Delete vHDDs")
    print("\n   ARE YOU SURE YOU WANT TO RESTORE?\n   This cannot be undone.\n"+color.END)
    print(color.BOLD+color.RED+"      X. RESTORE")
    print(color.END+"      Q. Exit to restore tools...\n")
    detectChoice2 = str(input(color.BOLD+"Select> "+color.END))
else:
    detectChoice2 = "F"
    print("\n\n   The repo integrity could not be verified.\n   One or more files required to restore are damaged or missing.\n\n   The script cannot continue.\n\n")

def success():
    clear()
    print("\n\n   "+color.BOLD+color.GREEN+"✔ RESTORE COMPLETE"+color.END,"")
    print("   All local components have been reset\n")
    print("   The project files have been restored from the local project store.\n   You can safely use these files.\n\n   REMEMBER: Do not tamper with files in the /resources folder."+color.END+"\n\n\n\n\n\n\n")

def throwError():
    global errorMessage
    clear()
    print("\n   "+color.BOLD+color.RED+"✖ FAILED"+color.END)
    print("   Unable to continue")
    print("\n   Sorry, something happened and the restoration failed. \n   You may need to reinstall the repository.\n   If you think this was a bug, please report it on GitHub."+color.END)
    print("\n   "+color.BOLD+color.RED+"ERROR:",color.END+color.BOLD,errorMessage,color.END+"\n\n\n\n")


if detectChoice2 == "X" or detectChoice2 == "x":
    
    clear()

    version = open("./.version")
    version = version.read()

    versionStore = open("./resources/script_store/.version")
    versionStore = versionStore.read()

    versionInt = version.replace(".","")
    versionStoreInt = versionStore.replace(".","")

    versionInt = int(versionInt)
    versionStoreInt = int(versionStoreInt)

    if versionStoreInt < versionInt:
        print("\n\n   "+color.BOLD+color.YELLOW+"⚠ RISK OF DOWNGRADE DETECTED"+color.END,"")
        print("   Version data does not match local store\n")
        print("   The version data of the repository files in the local project store\n   do not match those of your current files. As a result, restoring locally\n   may downgrade your repository to an older version.\n"+color.END+"")
        print("\n   Would you like to continue?\n"+color.END)
        print(color.BOLD+"      1. Continue anyway...")
        print(color.END+"      Q. Exit to restore tools...\n")
        detectChoice3 = str(input(color.BOLD+"Select> "+color.END))
        if detectChoice3 == 1:
            clear()
        elif detectChoice3 == "q" or detectChoice3 == "Q":
            clear()
            os.system('./scripts/restoretools.py')



    print("\n\n   "+color.BOLD+color.RED+"↺  RESET ALL COMPONENTS LOCALLY"+color.END,"")
    print("   Restoring...\n\n\n")
    print("   Please wait while the restore process is in progress.\n   This may take a few moments.\n\n   DO NOT INTERRUPT THIS OPERATION.\n\n\n")
    time.sleep(5)
    os.system("rm ./boot/OpenCore.qcow2 > /dev/null 2>&1")
    os.system("rm ./boot/config.plist > /dev/null 2>&1")
    os.system("rm -rf ./boot/EFI > /dev/null 2>&1")
    os.system("rm ./ovmf/OVMF_VARS.fd > /dev/null 2>&1")
    os.system("rm ./ovmf/OVMF_CODE.fd > /dev/null 2>&1")
    #os.system("rm ./blobs/*.apb > /dev/null 2>&1")
    #os.system("rm ./blobs/stale/*.apb > /dev/null 2>&1")
    os.system("rm ./resources/config.sh > /dev/null 2>&1")
    os.system("rm ./main.py > /dev/null 2>&1")
    os.system("rm ./.version > /dev/null 2>&1")
    os.system("rm ./scripts/* > /dev/null 2>&1")
    os.system("rm ./scripts/restore/* > /dev/null 2>&1")
    os.system("rm ./scripts/extras/* > /dev/null 2>&1")
    time.sleep(4)

    global USR_TARGET_OS

    if os.path.exists("./blobs/USR_TARGET_OS.apb"):
        blob = open("./blobs/USR_TARGET_OS.apb","r")
        USR_TARGET_OS = blob.read()
        USR_TARGET_OS = int(USR_TARGET_OS)
        if USR_TARGET_OS < 999:
            USR_TARGET_OS = USR_TARGET_OS * 100
        blob.close()
    else:
        USR_TARGET_OS = 9999

    time.sleep(2)
    if USR_TARGET_OS <= 1015:
        os.system("cp resources/oc_store/compat_old/OpenCore.qcow2 boot/OpenCore.qcow2")
        os.system("cp resources/oc_store/compat_old/config.plist boot/config.plist")
        os.system("cp -R resources/oc_store/compat_old/EFI boot/EFI")
    else:
        os.system("cp resources/oc_store/compat_new/OpenCore.qcow2 boot/OpenCore.qcow2")
        os.system("cp resources/oc_store/compat_new/config.plist boot/config.plist")
        os.system("cp -R resources/oc_store/compat_new/EFI boot/EFI")


    os.system("cp -R ./resources/script_store/* ./scripts/")
    os.system("mv ./scripts/main.py ./main.py")
    os.system("mv ./scripts/.version ./.version")
    os.system("cp ./resources/ovmf/OVMF_CODE.fd ./ovmf/OVMF_CODE.fd")
    os.system("cp ./ovmf/var/OVMF_VARS.fd ./ovmf/OVMF_VARS.fd")

    
    errorMessage = "Restoration failed. You may not have sufficient\n           permissions or damaged files."

    if os.path.exists("boot/OpenCore.qcow2"):
        if os.path.exists("ovmf/OVMF_CODE.fd"):
            if os.path.exists("boot/EFI/"):
                if os.path.exists("scripts/extras.py"):
                    success()
                else:
                    throwError()
            else:
                throwError()
        else:
            throwError()
    else:
        throwError()
    
    





elif detectChoice2 == "Q" or detectChoice2 == "q":
    clear()
    os.system("./scripts/restoretools.py")
elif detectChoice2 == "F":
    time.sleep(5)