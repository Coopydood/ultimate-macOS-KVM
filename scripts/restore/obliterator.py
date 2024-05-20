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
import http.client as httplib

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
print("\n\n   "+color.BOLD+color.RED+"↺  DOWNLOAD AND RESTORE REPOSITORY"+color.END,"")
print("   Please wait\n")
print(color.END+"\n\n\n   Checking integrity...\n\n\n\n\n")


global integrity

def have_internet() -> bool:
    global integrity
    conn = httplib.HTTPSConnection("8.8.8.8", timeout=5)
    try:
        conn.request("HEAD", "/")
        return True
    except Exception:
        return False
    finally:
        conn.close()

if have_internet() == True:
    integrity = 1
else:
    integrity = 0


# UNCOMMENT TO FORCE INTEGRITY CHECK RESULT
#integrity = 0


clear()
print("\n\n   "+color.BOLD+color.RED+"↺  DOWNLOAD AND RESTORE REPOSITORY"+color.END,"")
print("   Online full repository restore\n")

print(color.BOLD+"   Connection")
if integrity == 1:
   print(color.GREEN+color.BOLD+"   ●"+color.END+" ONLINE")
else:
   print(color.RED+color.BOLD+"   ●"+color.END+" OFFLINE")

if integrity == 1:
    print(color.END+color.BOLD+"\n   THIS TOOL:")
    print(color.BOLD+color.BLUE+"   DOWNLOADS "+color.END+"a full copy of the latest repository")
    print(color.BOLD+color.GREEN+"        WILL "+color.END+color.BOLD+"reset ALL non-user repository files")
    print(color.BOLD+color.GREEN+"        WILL "+color.END+"fix permissions on resources")
    print(color.BOLD+color.GREEN+"        WILL "+color.END+"repair any component corruption")
    print(color.BOLD+color.GREEN+"        WILL "+color.END+"remove older project version files")
    print(color.BOLD+color.RED+"       RISKS "+color.END+"deleting your configs or vHDD files")
    print(color.BOLD+color.RED+"    WILL NOT "+color.END+"create a backup of anything")

    #print(color.END+color.BOLD+"\n                 THIS TOOL")
    #print(color.BOLD+color.GREEN+"          WILL       "+color.END+"|"+color.BOLD+color.RED+"       WILL NOT"+color.END)
    #print("      Reset vNVRAM   |     Delete vHDDs")
    #print("      Reset vNVRAM   |     Delete vHDDs")
    print("\n   ARE YOU SURE YOU WANT TO DOWNLOAD AND RESTORE?\n   This cannot be undone.\n"+color.END)
    print(color.BOLD+color.RED+"      X. DOWNLOAD AND RESTORE...")
    print(color.END+"      Q. Exit to restore tools...\n")
    detectChoice2 = str(input(color.BOLD+"Select> "+color.END))
else:
    detectChoice2 = "F"
    print("\n\n   A connection to the internet could not be established.\n   To perform a full repository restore, you must be online.\n\n   The script cannot continue.\n\n")

def success():
    clear()
    print("\n\n   "+color.BOLD+color.GREEN+"✔ RESTORE COMPLETE"+color.END,"")
    print("   Repository has been fully restored\n")
    print("   All repository components were downloaded and restored.\n   You can safely use these files.\n\n   You can disconnect from the internet if needed."+color.END+"\n\n\n\n\n\n\n")

def throwError():
    global errorMessage
    clear()
    print("\n   "+color.BOLD+color.RED+"✖ FAILED"+color.END)
    print("   Unable to continue")
    print("\n   Sorry, something happened and the restoration failed. \n   You may need to reinstall the repository.\n   If you think this was a bug, please report it on GitHub."+color.END)
    print("\n   "+color.BOLD+color.RED+"ERROR:",color.END+color.BOLD,errorMessage,color.END+"\n\n\n\n")


if detectChoice2 == "X" or detectChoice2 == "x":
    
    clear()
    print("\n\n   "+color.BOLD+color.RED+"↺  DOWNLOAD AND RESTORE REPOSITORY"+color.END,"")
    print("   Restoring...\n\n\n")
    print("   Please wait while the restore process is in progress.\n   This may take a few moments.\n\n   DO NOT INTERRUPT THIS OPERATION.\n\n\n")
    os.system("mkdir ./RESTORE")
    time.sleep(5)
    os.system("rm ./boot/OpenCore.qcow2 > /dev/null 2>&1")
    os.system("rm ./boot/config.plist > /dev/null 2>&1")
    os.system("rm -rf ./boot/EFI > /dev/null 2>&1")
    os.system("rm -rf ./resources/script_store/ > /dev/null 2>&1")
    os.system("rm ./ovmf/OVMF_VARS.fd > /dev/null 2>&1")
    os.system("rm ./ovmf/OVMF_CODE.fd > /dev/null 2>&1")
    os.system("rm ./resources/dmg2img > /dev/null 2>&1")
    os.system("rm ./resources/baseConfig > /dev/null 2>&1")
    os.system("rm -rf ./resources > /dev/null 2>&1")
    os.system("rm -rf ./scripts > /dev/null 2>&1")
    os.system("rm -rf ./ovmf > /dev/null 2>&1")
    os.system("rm -rf ./blobs > /dev/null 2>&1")
    #os.system("rm ./blobs/*.apb > /dev/null 2>&1")
    #os.system("rm ./blobs/stale/*.apb > /dev/null 2>&1")
    os.system("rm ./resources/config.sh > /dev/null 2>&1")
    os.system("rm ./main.py > /dev/null 2>&1")
    os.system("rm ./.version > /dev/null 2>&1")
    os.system("rm ./README.md > /dev/null 2>&1")

    time.sleep(4)

    os.system("git clone -q https://github.com/Coopydood/ultimate-macOS-KVM ./RESTORE")
    time.sleep(4)
    os.system("git maintenance run --auto --quiet")
    os.system("chmod +x ./RESTORE/scripts/*.py")
    os.system("chmod +x ./RESTORE/scripts/*.sh")
    os.system("chmod +x ./RESTORE/*.py")
    os.system("chmod +x ./RESTORE/scripts/extras/*.py")
    os.system("chmod +x ./RESTORE/resources/dmg2img")
    time.sleep(4)
    os.system("cp -R ./RESTORE/scripts ./scripts")
    os.system("cp -R ./RESTORE/resources ./resources")
    os.system("cp -R ./RESTORE/ovmf ./ovmf")
    os.system("cp -R ./RESTORE/blobs ./blobs")
    os.system("cp ./RESTORE/.version ./.version")
    os.system("cp ./RESTORE/README.md ./README.md")
    os.system("cp ./RESTORE/main.py ./main.py")
    os.system("cp ./RESTORE/* ./ > /dev/null 2>&1")
    os.system("rm -rf ./RESTORE")
    os.system("mkdir ./boot > /dev/null 2>&1")
    time.sleep(2)
    clear()








    global USR_TARGET_OS

    if os.path.exists("./blobs/user/USR_TARGET_OS.apb"):
        blob = open("./blobs/user/USR_TARGET_OS.apb","r")
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
        #os.system("cp -R resources/oc_store/compat_old/EFI boot/EFI")
    else:
        os.system("cp resources/oc_store/compat_new/OpenCore.qcow2 boot/OpenCore.qcow2")
        os.system("cp resources/oc_store/compat_new/config.plist boot/config.plist")
        #os.system("cp -R resources/oc_store/compat_new/EFI boot/EFI")



    os.system("cp ./resources/ovmf/OVMF_CODE.fd ./ovmf/OVMF_CODE.fd")
    os.system("cp ./resources/ovmf/OVMF_VARS.fd ./ovmf/OVMF_VARS.fd")

    
    errorMessage = "Restoration failed. You may not have sufficient\n           permissions or damaged files."

    if os.path.exists("boot/OpenCore.qcow2"):
        if os.path.exists("ovmf/OVMF_CODE.fd"):
            success()
        else:
            throwError()
    else:
        throwError()

    





elif detectChoice2 == "Q" or detectChoice2 == "q":
    clear()
    os.system("./scripts/restoretools.py")

elif detectChoice2 == "F":
    time.sleep(5)