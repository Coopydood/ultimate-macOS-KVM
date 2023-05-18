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
print("\n\n   "+color.BOLD+color.RED+"↺  DELETE AUTOPILOT DATA"+color.END,"")
print("   Please wait\n")
print(color.END+"\n\n\n   Checking data...\n\n\n\n\n")
if os.path.exists("./blobs/USR_CFG.apb"):
    integrity = 1
elif os.path.exists("./blobs/stale/USR_CFG.apb"):
    integrity = 1
else:
    integrity = 0
#time.sleep(5)


# UNCOMMENT TO FORCE INTEGRITY CHECK RESULT
#integrity = 0


clear()
print("\n\n   "+color.BOLD+color.RED+"↺  DELETE AUTOPILOT DATA"+color.END,"")
print("   Restore to default state\n")

print(color.BOLD+"   AutoPilot Data")
if integrity == 1:
   print(color.GREEN+color.BOLD+"   ●"+color.END+" FOUND")
else:
   print(color.RED+color.BOLD+"   ●"+color.END+" NOT FOUND")

if integrity == 1:
    print(color.END+color.BOLD+"\n   THIS TOOL:")
    print(color.BOLD+color.GREEN+"       WILL "+color.END+"delete all AutoPilot configuration data")
    print(color.BOLD+color.RED+"   WILL NOT "+color.END+"destroy any saved VFIO args")
    print(color.BOLD+color.RED+"   WILL NOT "+color.END+"delete scripts generated previously by AP")
    print(color.BOLD+color.RED+"   WILL NOT "+color.END+"create a backup of deleted files")

    #print(color.END+color.BOLD+"\n                 THIS TOOL")
    #print(color.BOLD+color.GREEN+"          WILL       "+color.END+"|"+color.BOLD+color.RED+"       WILL NOT"+color.END)
    #print("      DELETE AUTOPILOT DATA   |     Delete vHDDs")
    #print("      DELETE AUTOPILOT DATA   |     Delete vHDDs")
    print("\n   ARE YOU SURE YOU WANT TO DELETE?\n   This cannot be undone.\n"+color.END)
    print(color.BOLD+color.RED+"      X. DELETE")
    print(color.END+"      Q. Exit to restore tools...\n")
    detectChoice2 = str(input(color.BOLD+"Select> "+color.END))
else:
    detectChoice2 = "F"
    print("\n\n   AutoPilot could not be found or verified.\n   One or more files required to restore are damaged or missing.\n\n   The script cannot continue.\n\n")

def success():
    clear()
    print("\n\n   "+color.BOLD+color.GREEN+"✔ DELETE COMPLETE"+color.END,"")
    print("   AutoPilot working data has been deleted\n")
    print("   All user AutoPilot configuration data has been deleted.\n   AutoPilot has been rearmed for first use."+color.END+"\n\n\n\n\n\n\n")

def throwError():
    global errorMessage
    clear()
    print("\n   "+color.BOLD+color.RED+"✖ FAILED"+color.END)
    print("   Unable to continue")
    print("\n   Sorry, something happened and the restoration failed. \n   You may need to reinstall the repository.\n   If you think this was a bug, please report it on GitHub."+color.END)
    print("\n   "+color.BOLD+color.RED+"ERROR:",color.END+color.BOLD,errorMessage,color.END+"\n\n\n\n")


if detectChoice2 == "X" or detectChoice2 == "x":
    clear()
    print("\n\n   "+color.BOLD+color.RED+"↺  DELETE AUTOPILOT DATA"+color.END,"")
    print("   Processing...\n\n\n")
    print("   Please wait while the deletion process is in progress.\n   This may take a few moments.\n\n   DO NOT INTERRUPT THIS OPERATION.\n\n\n")
    time.sleep(5)
    os.system("rm ./blobs/*.apb > /dev/null 2>&1")
    os.system("rm ./blobs/stale/*.apb > /dev/null 2>&1")
    os.system("rm ./resources/config.sh > /dev/null 2>&1")
    time.sleep(2)

    
    errorMessage = "Restoration failed. You may not have sufficient\n           permissions or damaged files."

    if os.path.exists("./blobs/USR_CFG.apb") or os.path.exists("./blobs/stale/USR_CFG.apb"):
        throwError()
    else:
        success()
    
    





elif detectChoice2 == "Q" or detectChoice2 == "q":
    clear()
    os.system("./scripts/restoretools.py")
elif detectChoice2 == "F":
    time.sleep(5)