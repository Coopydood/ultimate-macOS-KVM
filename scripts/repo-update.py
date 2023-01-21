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
print("Checking for updates...")

if os.path.exists("./resources/WEBVERSION"): os.system("rm ./resources/WEBVERSION")
os.system("wget -q --output-document=./resources/WEBVERSION --no-cache --no-cookies https://raw.githubusercontent.com/Coopydood/ultimate-macOS-KVM/main/VERSION")
webVersion = open("./resources/WEBVERSION")
webVersion = webVersion.read()

time.sleep(2)
clear()


versionInt = version.replace(".","")
webVersionInt = webVersion.replace(".","")

versionInt = int(versionInt)
webVersionInt = int(webVersionInt)


if webVersionInt is str:
   webVersionInt = "UNKNOWN"

if versionInt is str:
   versionInt = "UNKNOWN"



if versionInt == webVersionInt:
   clear()
   print("\n\n   "+color.BOLD+color.GREEN+"✔  NO UPDATES AVAILABLE"+color.END,"")
   print("   You're on the latest version\n")
   print(color.BOLD+"   Current Version\n   "+color.END+"v"+version,"\n\n\n\n")

   print("   Check back periodically to ensure you're always using\n   the latest version of the project."+"\n\n")
elif versionInt > webVersionInt:# and versionInt is int and webVersionInt is int:
   clear()
   print("\n\n   "+color.BOLD+color.PURPLE+"⚛  PRE-RELEASE VERSION"+color.END,"")
   print("   You're on a newer version\n")
   print(color.BOLD+"   Current Version\n   "+color.END+"v"+version,"\n")
   print(color.BOLD+"   Public Release Version\n   "+color.END+"v"+webVersion,"\n\n\n\n")
   print("   Either you've tampered with your version number or\n   you're Coopydood and subsequently weird beyond repair."+"\n\n")
elif versionInt < webVersionInt:
   clear()
   print("\n\n   "+color.BOLD+color.BLUE+"⎋  NEW UPDATES AVAILABLE"+color.END,"")
   print("   Updates are ready to download\n")
   print(color.END+color.GRAY+"         Current Version\n   "+"          v"+version,color.END+"\n")
   print(color.BOLD+"               ⋁\n")
   print(color.BOLD+"         Latest Version\n   "+color.BOLD+"          v"+webVersion,"\n"+color.END)
   print("   Updates can introduce important fixes and new features. Downloading and\n   installing this update does not affect non-repo files, such as any\n   personal config scripts, hard disk images, ROMs, or boot files.")

   print("\n   Do you want to update now?\n"+color.END)
   print(color.BOLD+"      1. Download and Install...")
   print(color.END+"         Updates out-of-date repo files with new versions\n")
   print(color.END+"      2. Download only")
   print(color.END+"      Q. Exit without updating\n")
   detectChoice1 = str(input(color.BOLD+"Select> "+color.END))

   if detectChoice1 == "1":
      clear()
      print("Starting...")
      time.sleep(3)
      clear()
      print("\n\n   "+color.BOLD+color.BLUE+"⎋  UPDATING..."+color.END,"")
      print("   Do not terminate this script\n")
      print(color.END+color.GRAY+"         Current Version\n   "+"          v"+version,color.END+"\n")
      print(color.BOLD+"               ⋁\n")
      print(color.BOLD+"         Latest Version\n   "+color.BOLD+"          v"+webVersion,"\n"+color.END)
      print("   The update you requested is being downloaded and installed.\n   Do NOT terminate this script or close the window.\n\n\n\n")
      time.sleep(3)
      os.system("git stash")
      time.sleep(2)
      os.system("git pull")

else:
   clear()
   print("\n\n   "+color.BOLD+color.RED+"✖ FAILED TO CHECK FOR UPDATES"+color.END,"")
   print("   Something went wrong\n")
   print(color.BOLD+"   Your Reported Version\n   "+color.END+"v"+version,"\n")
   print("   I couldn't get the status of your current version, and/or the\n   remote server version's control file."+"\n\n")
   
#https://raw.githubusercontent.com/Coopydood/ultimate-macOS-KVM/main/VERSION