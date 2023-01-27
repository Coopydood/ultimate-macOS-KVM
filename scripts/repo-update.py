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

noDelta = 0

if os.path.exists("./resources/WEBVERSION"): os.system("rm ./resources/WEBVERSION")
os.system("wget -q --output-document=./resources/WEBVERSION --no-cache --no-cookies https://raw.githubusercontent.com/Coopydood/ultimate-macOS-KVM/main/VERSION")
webVersion = open("./resources/WEBVERSION")
webVersion = webVersion.read()

time.sleep(2)
clear()

if "*" in webVersion:
   noDelta = 1

webVersion = webVersion.replace("*","")

version = version.replace("\n","")
webVersion = webVersion.replace("\n","")

versionInt = version.replace(".","")
webVersionInt = webVersion.replace(".","")



versionInt = int(versionInt)
webVersionInt = int(webVersionInt)

if versionInt < 100: versionInt = versionInt * 10
if webVersionInt < 100: webVersionInt = webVersionInt * 10

if webVersionInt is str:
   webVersionInt = "UNKNOWN"

if versionInt is str:
   versionInt = "UNKNOWN"

def updateBrains():
   if detectChoice1 == "1" and noDelta == 0:
      clear()
      print("Starting...")
      time.sleep(3)
      clear()
      print("\n\n   "+color.BOLD+color.BLUE+"⧖  UPDATING..."+color.END,"")
      print("   Do not terminate this script\n")
      print(color.END+color.GRAY+"         Current Version\n   "+"          v"+version,color.END+"\n")
      print(color.BOLD+"               ⋁\n")
      print(color.BOLD+"         Target Version\n   "+color.BOLD+"          v"+webVersion,"\n"+color.END)
      print("   The update you requested is being downloaded and installed.\n   Do NOT terminate this script or close the window.\n\n")
      time.sleep(3)
      os.system("git stash -q")
      os.system("git clean -f -q")
      clear()
      clear()
      print("\n\n   "+color.BOLD+color.BLUE+"⧖  UPDATING..."+color.END,"")
      print("   Do not terminate this script\n")
      print(color.END+color.GRAY+"         Current Version\n   "+"          v"+version,color.END+"\n")
      print(color.BOLD+"               ⋁\n")
      print(color.BOLD+"         Target Version\n   "+color.BOLD+"          v"+webVersion,"\n"+color.END)
      print("   The update you requested is being downloaded and installed.\n   Do NOT terminate this script or close the window.\n\n")
      time.sleep(2)
      os.system("git pull -f -q")
      clear()
      clear()
      print("\n\n   "+color.BOLD+color.BLUE+"⧖  UPDATING..."+color.END,"")
      print("   Do not terminate this script\n")
      print(color.END+color.GRAY+"         Current Version\n   "+"          v"+version,color.END+"\n")
      print(color.BOLD+"               ⋁\n")
      print(color.BOLD+"         Target Version\n   "+color.BOLD+"          v"+webVersion,"\n"+color.END)
      print("   The update you requested is being downloaded and installed.\n   Do NOT terminate this script or close the window.\n\n")
      time.sleep(3)
      os.system("git maintenance run --auto --quiet")
      os.system("chmod +x scripts/*.py")
      os.system("chmod +x scripts/*.sh")
      os.system("chmod +x *.sh")
      os.system("chmod +x *.py")
      os.system("chmod +x scripts/extras/*.py")
      os.system("chmod +x scripts/extras/*.sh")
      os.system("chmod +x resources/dmg2img")
      clear()


      
      versionNew = open("./VERSION")
      versionNew = versionNew.read()


      if versionNew == webVersion:
         print("\n\n   "+color.BOLD+color.GREEN+"✔  UPDATE COMPLETE"+color.END,"")
         print("   The update was installed\n")
         print(color.END+color.GRAY+"         Previous Version\n   "+"          v"+version,color.END+"\n")
         print(color.BOLD+"               ✔\n")
         print(color.BOLD+"         Current Version\n   "+color.BOLD+"          v"+webVersion,"\n"+color.END)
         print("   You can now use this version.\n   It is safe to exit this window.\n\n")
      else:
         print("\n\n   "+color.BOLD+color.RED+"✖  UPDATE FAILED"+color.END,"")
         print("   The update could not be installed\n")
         print(color.END+color.GRAY+"         Current Version\n   "+"          v"+version,color.END+"\n")
         print(color.BOLD+"               ✖\n")
         print(color.BOLD+"         Target Version\n   "+color.BOLD+"          v"+webVersion,"\n"+color.END)
         print("   Something went wrong during the update and it was\n   not completed. Try updating manually.\n\n")  

   elif detectChoice1 == "2":
      clear()
      print("Starting...")
      time.sleep(3)
      clear()
      print("\n\n   "+color.BOLD+color.BLUE+"➔  DOWNLOADING UPDATE..."+color.END,"")
      print("   Download to update folder only\n")
      print(color.END+color.GRAY+"         Current Version\n   "+"          v"+version,color.END+"\n")
      print(color.BOLD+"               ✚\n")
      print(color.BOLD+"         Target Version\n   "+color.BOLD+"          v"+webVersion,"\n"+color.END)
      print("   The update you requested is being downloaded.\n   It will be in the \"<repo>/updates/"+webVersion+"\" folder.\n\n")
      time.sleep(3)
      os.system("mkdir ./updates")
      os.system("mkdir ./updates/"+webVersion)
      clear()
      clear()
      print("\n\n   "+color.BOLD+color.BLUE+"➔  DOWNLOADING UPDATE..."+color.END,"")
      print("   Download to update folder only\n")
      print(color.END+color.GRAY+"         Current Version\n   "+"          v"+version,color.END+"\n")
      print(color.BOLD+"               ✚\n")
      print(color.BOLD+"         Target Version\n   "+color.BOLD+"          v"+webVersion,"\n"+color.END)
      print("   The update you requested is being downloaded.\n   It will be in the \"<repo>/updates/"+webVersion+"\" folder.\n\n")
      time.sleep(2)
      os.system("git clone -q https://github.com/Coopydood/ultimate-macOS-KVM ./updates/"+webVersion+"/")
      clear()
      clear()
      print("\n\n   "+color.BOLD+color.BLUE+"➔  DOWNLOADING UPDATE..."+color.END,"")
      print("   Download to update folder only\n")
      print(color.END+color.GRAY+"         Current Version\n   "+"          v"+version,color.END+"\n")
      print(color.BOLD+"               ✚\n")
      print(color.BOLD+"         Target Version\n   "+color.BOLD+"          v"+webVersion,"\n"+color.END)
      print("   The update you requested is being downloaded.\n   It will be in the \"<repo>/updates/"+webVersion+"\" folder.\n\n")
      time.sleep(3)
      os.system("git maintenance run --auto --quiet")
      os.system("chmod +x ./updates/"+webVersion+"/scripts/*.py")
      os.system("chmod +x ./updates/"+webVersion+"/scripts/*.sh")
      os.system("chmod +x ./updates/"+webVersion+"/*.sh")
      os.system("chmod +x ./updates/"+webVersion+"/*.py")
      os.system("chmod +x ./updates/"+webVersion+"/scripts/extras/*.py")
      os.system("chmod +x ./updates/"+webVersion+"/scripts/extras/*.sh")
      os.system("chmod +x ./updates/"+webVersion+"/resources/dmg2img")
      clear()
      versionNew = open("./updates/"+webVersion+"/VERSION")
      versionNew = versionNew.read()


      if versionNew == webVersion:
         print("\n\n   "+color.BOLD+color.GREEN+"✔  UPDATE DOWNLOADED"+color.END,"")
         print("   The update was downloaded\n")
         print(color.END+color.GRAY+"         Current Version\n   "+"          v"+version,color.END+"\n")
         print(color.BOLD+"               ✔\n")
         print(color.BOLD+"       Downloaded Version\n   "+color.BOLD+"          v"+webVersion,"\n"+color.END)
         print("   This version has NOT been installed and\n   current version files have not been modified.\n\n   It is available in the following directory:\n   "+color.BOLD+"<repo>/updates/"+webVersion+color.END+"\n\n")
      else:
         print("\n\n   "+color.BOLD+color.RED+"✖  UPDATE FAILED"+color.END,"")
         print("   The update could not be installed\n")
         print(color.END+color.GRAY+"         Current Version\n   "+"          v"+version,color.END+"\n")
         print(color.BOLD+"               ✖\n")
         print(color.BOLD+"         Target Version\n   "+color.BOLD+"          v"+webVersion,"\n"+color.END)
         print("   Something went wrong during the update and it was\n   not completed. Try updating manually.\n\n")  

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
elif versionInt < webVersionInt and noDelta == 1:
   clear()
   print("\n\n   "+color.BOLD+color.YELLOW+"⚠  MANUAL UPDATE REQUIRED"+color.END,"")
   print("   Automatic updating is unavailable\n")
   print(color.BOLD+"         Current Version\n   "+"          v"+version,color.END+"\n")
   print(color.END+"               ⊘\n")
   print(color.END+color.GRAY+"         Latest Version\n   "+"          v"+webVersion,"\n"+color.END)
   print("   Your version is incompatible with the latest version.\n   To protect your data, auto-update is unavailable.\n\n   This happens when your version is very old,\n   or a major update has been released. You can\n   manually download and install it.\n")
   print(color.GRAY+"      1. Download and Install..."+color.END)
   print(color.BOLD+"      2. Download only")
   print(color.END+"      Q. Exit without updating\n")
   detectChoice1 = str(input(color.BOLD+"Select> "+color.END))
   updateBrains()
elif versionInt < webVersionInt and noDelta == 0:
   clear()
   print("\n\n   "+color.BOLD+color.BLUE+"⎋  UPDATE AVAILABLE"+color.END,"")
   print("   Updates are ready to download and install\n")
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
   updateBrains()
   

else:
   clear()
   print("\n\n   "+color.BOLD+color.RED+"✖ FAILED TO CHECK FOR UPDATES"+color.END,"")
   print("   Something went wrong\n")
   print(color.BOLD+"   Your Reported Version\n   "+color.END+"v"+version,"\n")
   print("   I couldn't get the status of your current version, and/or the\n   remote server version's control file."+"\n\n")
   
#https://raw.githubusercontent.com/Coopydood/ultimate-macOS-KVM/main/VERSION