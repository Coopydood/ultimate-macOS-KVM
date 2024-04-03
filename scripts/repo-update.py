#!/usr/bin/env python3
# pylint: disable=C0301,C0116,C0103,R0903

"""
This script was created by Coopydood as part of the ultimate-macOS-KVM project.
It will not work outside of this project.

It CAN be used manually from the root ultimate-macOS-KVM repo folder.
See     $ ./scripts/repo-update.py --help     for further assistance.

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
import argparse
import http.client as httplib
global noDelta

detectChoice = 1
latestOSName = "Sonoma"
latestOSVer = "14"
runs = 0
noDelta = 0

global version

# INTERNAL VERSION OF THIS UTILITY
# May be used in the future
updaterVersion = "2.4"

if os.path.exists("./.version"):
   version = open("./.version")
else:
   version = open("./VERSION") # COMPATIBILITY WITH LEGACY VERSIONS

version = version.read()


global webVersion
global versionDash

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

parser = argparse.ArgumentParser("repo-update")
parser.add_argument("-a", "--auto", dest="install", help="Automatically download and install available updates without asking",action="store_true")
parser.add_argument("-d", "--download", dest="download", help="Automatically download (but not install) available updates without asking",action="store_true")
parser.add_argument("-v", "--version", dest="version", help="Upgrade/downgrade to a specific version. Must be used with --force.", metavar="<X.X.X>", type=str)
parser.add_argument("-f", "--force", dest="force", help="Force install the latest version, even if it is already installed. Use only to skip ahead to latest commit", action="store_true")
parser.add_argument("--targetBranch", dest="switchBranch", help="Select the target branch for update search", action="store")
parser.add_argument("--forceDelta", dest="forceDelta", help="Skip the delta update compatibility check and allow upgrading forcefully. THIS IS UNSAFE!", action="store_true")
parser.add_argument("--noDelta", dest="noDelta", help="For debugging only. Flags all updates as incompatible even if they aren't", action="store_true")
parser.add_argument("--menuFlow", dest="menuFlow", help="To be used by other internal scripts only", action="store_true")

args = parser.parse_args()


#args.version = "0.8.5"   # UNCOMMENT TO DEBUG ARGS

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


clear()

if integrity == 1 and args.version is None:
   print("Checking for updates...")
elif integrity == 1 and args.version is not None:
   print("Searching for update...")

targetBranch = "main"

if args.switchBranch is not None:
   targetBranch = args.switchBranch


#print("wget -q --output-document=./resources/.webversion --no-cache --no-cookies https://raw.githubusercontent.com/Coopydood/ultimate-macOS-KVM/"+str(targetBranch)+"/.version")

if integrity == 1:
   if os.path.exists("./resources/.webversion"): os.system("rm ./resources/.webversion")
   #os.system("wget -q --output-document=./resources/.webversion --no-cache --no-cookies https://raw.githubusercontent.com/Coopydood/ultimate-macOS-KVM/"+str(targetBranch)+"/VERSION")
   os.system("wget -q --output-document=./resources/.webversion --no-cache --no-cookies https://raw.githubusercontent.com/Coopydood/ultimate-macOS-KVM/"+str(targetBranch)+"/.version")
   if os.path.exists("./resources/.upgrade"): os.system("rm ./resources/.upgrade")
   os.system("wget -q --output-document=./resources/.upgrade --no-cache --no-cookies https://raw.githubusercontent.com/Coopydood/ultimate-macOS-KVM/"+str(targetBranch)+"/resources/.upgrade")

   # COMPATIBILITY MODE
   if os.path.exists("./resources/WEBVERSION"): os.system("rm ./resources/WEBVERSION")
   if os.path.exists("./resources/UPGRADEPATH"): os.system("rm ./resources/UPGRADEPATH")



   webVersion = open("./resources/.webversion")
   webVersion = webVersion.read()


   time.sleep(2)
   clear()



   webVersion = webVersion.replace("*","")

   version = version.replace("\n","")
   webVersion = webVersion.replace("\n","")

   versionInt = version.replace(".","")
   webVersionInt = webVersion.replace(".","")

   if args.version is not None:
    argsVersionInt = args.version.replace(".","")
    argsVersionInt = int(argsVersionInt)

   if os.path.exists("./resources/.upgrade"):
      deltaSupport = open("./resources/.upgrade")
      deltaSupport = deltaSupport.read()
      deltaSupport = deltaSupport.replace("\n"," ")
      # print(deltaSupport)    # Uncomment to display supported upgrade versions
      if version not in deltaSupport:
         noDelta = 1
   elif os.path.exists("./resources/UPGRADEPATH"):
      deltaSupport = open("./resources/UPGRADEPATH")
      deltaSupport = deltaSupport.read()
      deltaSupport = deltaSupport.replace("\n"," ")
      # print(deltaSupport)    # Uncomment to display supported upgrade versions
      if version not in deltaSupport:
         noDelta = 1

   if "*" in webVersion:
         noDelta = 1


   # HONOUR USER ARGUMENTS
   if args.noDelta == True:
      noDelta = 1
   if args.forceDelta == True:
      noDelta = 0

   if args.menuFlow == True:
      menuFlow = 1
   else:
      menuFlow = 0


   if args.version is not None:
      targetVersion = args.version
      if argsVersionInt < 100: argsVersionInt = argsVersionInt * 10

   versionInt = int(versionInt)
   webVersionInt = int(webVersionInt)

   if versionInt < 100: versionInt = versionInt * 10
   if webVersionInt < 100: webVersionInt = webVersionInt * 10
   
   
   if versionInt > 7000: versionInt = versionInt / 10

   if webVersionInt is str:
      webVersionInt = "UNKNOWN"

   if versionInt is str:
      versionInt = "UNKNOWN"


   def updateBrains():

      global webVersion
      global versionDash
      global version

      if detectChoice1 == "1" and noDelta == 0:
         if args.version is not None:
            webVersion = args.version
            
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
         
         os.system("git stash -q > /dev/null 2>&1")
         #os.system("git clean -f -q > /dev/null 2>&1")
         clear()
         clear()
         print("\n\n   "+color.BOLD+color.BLUE+"⧖  UPDATING..."+color.END,"")
         print("   Do not terminate this script\n")
         print(color.END+color.GRAY+"         Current Version\n   "+"          v"+version,color.END+"\n")
         print(color.BOLD+"               ⋁\n")
         print(color.BOLD+"         Target Version\n   "+color.BOLD+"          v"+webVersion,"\n"+color.END)
         print("   The update you requested is being downloaded and installed.\n   Do NOT terminate this script or close the window.\n\n")
         time.sleep(2)
         if args.version is not None and targetBranch == "main":
            targetVersion = args.version
            os.system("git reset --hard tags/v"+targetVersion)
         elif targetBranch != "main":
            os.system("git switch "+str(targetBranch)+" > /dev/null 2>&1")
            os.system("git fetch --all -q > /dev/null 2>&1")
            os.system("git merge --autostash origin/"+str(targetBranch)+" > /dev/null 2>&1")
         else:
            #os.system("git reset --hard HEAD")
            #os.system("git clean -xffd > /dev/null 2>&1")
            os.system("git fetch --all -q > /dev/null 2>&1")
            os.system("git branch -q backup-main > /dev/null 2>&1")
            os.system("git reset --hard -q origin/main > /dev/null 2>&1")
         clear()
         clear()
         print("\n\n   "+color.BOLD+color.BLUE+"⧖  UPDATING..."+color.END,"")
         print("   Do not terminate this script\n")
         print(color.END+color.GRAY+"         Current Version\n   "+"          v"+version,color.END+"\n")
         print(color.BOLD+"               ⋁\n")
         print(color.BOLD+"         Target Version\n   "+color.BOLD+"          v"+webVersion,"\n"+color.END)
         print("   The update you requested is being downloaded and installed.\n   Do NOT terminate this script or close the window.\n\n")
         time.sleep(3)
         os.system("git maintenance run --auto --quiet > /dev/null 2>&1")
         os.system("chmod +x scripts/*.py > /dev/null 2>&1")
         os.system("chmod +x scripts/*.sh > /dev/null 2>&1")
         os.system("chmod +x *.sh > /dev/null 2>&1")
         os.system("chmod +x *.py > /dev/null 2>&1")
         os.system("chmod +x scripts/extras/*.py > /dev/null 2>&1")
         os.system("chmod +x scripts/extras/*.sh > /dev/null 2>&1")
         os.system("chmod +x resources/dmg2img > /dev/null 2>&1")
         clear()


         
         if os.path.exists("./.version"):
            versionNew = open("./.version")
         else:
            versionNew = open("./VERSION") # LEGACY VERSION SUPPORT
         versionNew = versionNew.read()


         if versionNew == webVersion:
            print("\n\n   "+color.BOLD+color.GREEN+"✔  UPDATE COMPLETE"+color.END,"")
            print("   The update was installed\n")
            print(color.END+color.GRAY+"         Previous Version\n   "+"          v"+version,color.END+"\n")
            print(color.BOLD+"               ✔\n")
            print(color.BOLD+"         Current Version\n   "+color.BOLD+"          v"+webVersion,"\n"+color.END)
            print("   You can now use this version.\n   It is safe to exit this window.\n")
            versionDash = webVersion.replace(".","-")
            if menuFlow == 1:
               print(color.BOLD+"      W. What's new?")
               print(color.END+"         Open the changelog of v"+webVersion+" in your browser\n")
               print(color.END+"      M. Main menu")
               print(color.END+"      Q. Exit\n")
               detectChoice3 = str(input(color.BOLD+"Select> "+color.END))

               if detectChoice3 == "W" or detectChoice3 == "w":
                  clear()
                  print("\n\n   "+color.BOLD+color.GREEN+"✔  OPENING RELEASE NOTES IN DEFAULT BROWSER"+color.END,"")
                  print("   Continue in your browser\n")
                  print("\n   I have attempted to open the release notes in\n   your default browser. Please be patient.\n\n   You will be returned to the main menu in 5 seconds.\n\n\n\n\n")
                  os.system('xdg-open https://github.com/Coopydood/ultimate-macOS-KVM/blob/"+str(targetBranch)+"/docs/changelogs/v'+versionDash+".md > /dev/null 2>&1")
                  time.sleep(6)
                  clear()
                  os.system('./main.py')
               elif detectChoice3 == "M" or detectChoice3 == "m":
                  clear()
                  os.system("./main.py")
               elif detectChoice3 == "Q" or detectChoice3 == "q":
                  exit
         else:
            print("\n\n   "+color.BOLD+color.RED+"✖  UPDATE FAILED"+color.END,"")
            print("   The update could not be installed\n")
            print(color.END+color.GRAY+"         Current Version\n   "+"          v"+version,color.END+"\n")
            print(color.BOLD+"               ✖\n")
            print(color.BOLD+"         Target Version\n   "+color.BOLD+"          v"+webVersion,"\n"+color.END)
            print("   Something went wrong during the update and it was\n   not completed. Try updating manually.\n\n")  

      elif detectChoice1 == "2" and noDelta == 0 or detectChoice1 and noDelta == 1:
         if args.version is not None:
            webVersion = args.version
         
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
         os.system("mkdir ./updates > /dev/null 2>&1")
         os.system("mkdir ./updates/"+webVersion+" > /dev/null 2>&1")
         clear()
         clear()
         print("\n\n   "+color.BOLD+color.BLUE+"➔  DOWNLOADING UPDATE..."+color.END,"")
         print("   Download to update folder only\n")
         print(color.END+color.GRAY+"         Current Version\n   "+"          v"+version,color.END+"\n")
         print(color.BOLD+"               ✚\n")
         print(color.BOLD+"         Target Version\n   "+color.BOLD+"          v"+webVersion,"\n"+color.END)
         print("   The update you requested is being downloaded.\n   It will be in the \"<repo>/updates/"+webVersion+"\" folder.\n\n")
         time.sleep(2)
         if args.version is not None:
            targetVersion = webVersion
            os.system("git clone -q -b v"+webVersion+" --depth 1 https://github.com/Coopydood/ultimate-macOS-KVM ./updates/"+webVersion+"/ > /dev/null 2>&1")         
         else:
            os.system("git clone -q --depth 1 https://github.com/Coopydood/ultimate-macOS-KVM ./updates/"+webVersion+"/")
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
         os.system("chmod +x ./updates/"+webVersion+"/scripts/*.py > /dev/null 2>&1")
         os.system("chmod +x ./updates/"+webVersion+"/scripts/*.sh > /dev/null 2>&1")
         os.system("chmod +x ./updates/"+webVersion+"/*.sh > /dev/null 2>&1")
         os.system("chmod +x ./updates/"+webVersion+"/*.py > /dev/null 2>&1")
         os.system("chmod +x ./updates/"+webVersion+"/scripts/extras/*.py > /dev/null 2>&1")
         os.system("chmod +x ./updates/"+webVersion+"/scripts/extras/*.sh > /dev/null 2>&1")
         os.system("chmod +x ./updates/"+webVersion+"/resources/dmg2img > /dev/null 2>&1")
         clear()
         if os.path.exists("./updates/"+webVersion+"/.version"):
            versionNew = open("./updates/"+webVersion+"/.version")
         else:
            versionNew = open("./updates/"+webVersion+"/VERSION") # LEGACY VERSION SUPPORT

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

   if versionInt == webVersionInt and args.force is not True and args.version is None:
      clear()
     
      print("\n\n   "+color.BOLD+color.GREEN+"✔  NO UPDATES AVAILABLE"+color.END,"")
      print("   You're on the latest version\n")
      print(color.BOLD+"   Current Version\n   "+color.END+"v"+version,"\n")
      
      print("   Check back periodically to ensure you're always using\n   the latest version of the project."+"\n")
      versionDash = webVersion.replace(".","-")
      if menuFlow == 1:
         print(color.BOLD+"      M. Main menu")
         print(color.END+"         Return to the ULTMOS main menu\n")
         print(color.END+"      W. What's new?")
         print(color.END+"      Q. Exit\n")
         detectChoice3 = str(input(color.BOLD+"Select> "+color.END))

         if detectChoice3 == "W" or detectChoice3 == "w":
            clear()
            print("\n\n   "+color.BOLD+color.GREEN+"✔  OPENING RELEASE NOTES IN DEFAULT BROWSER"+color.END,"")
            print("   Continue in your browser\n")
            print("\n   I have attempted to open the release notes in\n   your default browser. Please be patient.\n\n   You will be returned to the main menu in 5 seconds.\n\n\n\n\n")
            os.system('xdg-open https://github.com/Coopydood/ultimate-macOS-KVM/blob/"+str(targetBranch)+"/docs/changelogs/v'+versionDash+".md > /dev/null 2>&1")
            time.sleep(6)
            clear()
            os.system('./main.py')
         elif detectChoice3 == "M" or detectChoice3 == "m":
            clear()
            os.system("./main.py")
         elif detectChoice3 == "Q" or detectChoice3 == "q":
            exit
      else:
         print("\n\n\n")
   elif versionInt > webVersionInt and args.version is None:# and versionInt is int and webVersionInt is int:
      clear()
      print("\n\n   "+color.BOLD+color.PURPLE+"⚛  PRE-RELEASE VERSION"+color.END,"")
      print("   You're on a newer version\n")
      print(color.BOLD+"   Current Version\n   "+color.END+"v"+version,"\n")
      print(color.BOLD+"   Public Release Version\n   "+color.END+"v"+webVersion,"\n\n\n\n")
      print("   Either you've tampered with your version number or\n   you're Coopydood and subsequently weird beyond repair."+"\n\n")
   elif versionInt < webVersionInt and noDelta == 1 and args.version is None or args.force == True and noDelta == 1 and args.version is None: #or args.version is not None and argsVersionInt > versionInt and noDelta == 1:
      clear()
      if args.version is not None:
            print("\n\n   "+color.BOLD+color.YELLOW+"⚠  TARGET UPDATE INCOMPATIBLE"+color.END,"")
      else:
         print("\n\n   "+color.BOLD+color.YELLOW+"⚠  MANUAL UPDATE REQUIRED"+color.END,"")
      print("   Automatic updating is unavailable\n")
      print(color.BOLD+"         Current Version\n   "+"          v"+version,color.END+"\n")
      print(color.END+"               ⊘\n")
      
      if args.version is not None:
         print(color.BOLD+"         Target Version\n   "+color.BOLD+"          v"+args.version,"\n"+color.END)
      else:
         print(color.BOLD+"         Latest Version\n   "+color.BOLD+"          v"+webVersion,"\n"+color.END)
      print("   Your version is incompatible with the latest version.\n   To protect your data, auto-update is unavailable.\n\n   This happens when your version is too old,\n   or a major update has been released. You can\n   manually download and install it.\n")
      
      print(color.BOLD+"      1. Download only")
      print(color.END+"      Q. Exit without updating\n")
      detectChoice1 = str(input(color.BOLD+"Select> "+color.END))
      if detectChoice1 == "1":
         detectChoice1 == "2"
         updateBrains()
      elif detectChoice1 == "q" or detectChoice1 == "Q":
         exit
      
   elif versionInt < webVersionInt and noDelta == 0 and args.version is None or args.force == True and noDelta == 0 and args.version is None or args.version is not None and argsVersionInt > versionInt:
      clear()
      if args.install is not True and args.download is not True:
         if args.version is not None:
            print("\n\n   "+color.BOLD+color.BLUE+"⎋  TARGET UPDATE FOUND"+color.END,"")
            print("   User specified update found\n")
         elif targetBranch != "main":
            print("\n\n   "+color.BOLD+color.PURPLE+"⥂  SWITCH TO "+str(targetBranch.upper())+" BRANCH"+color.END,"")
            print("   Update to a development version\n")
         else:
            print("\n\n   "+color.BOLD+color.BLUE+"⎋  UPDATE AVAILABLE"+color.END,"")
            print("   Updates are ready to download and install\n")
         print(color.END+color.GRAY+"         Current Version\n   "+"          v"+version,color.END+"\n")
         print(color.BOLD+"               ⋁\n")
         if args.version is not None:
            print(color.BOLD+"         Target Version\n   "+color.BOLD+"          v"+args.version,"\n"+color.END)
            print("   No support is available for this update because it was\n   specifically chosen by you. Compatibility with your\n   current version is not guaranteed or verified.")
         elif targetBranch != "main":
            print(color.BOLD+"         Target Version\n   "+color.BOLD+"         v"+webVersion,color.PURPLE+"⚛\n"+color.END)
            print("   No support is available for this update because it is\n   on an unsupported branch. Compatibility with your\n   current version is not guaranteed or verified.")
         
         else:
            print(color.BOLD+"         Latest Version\n   "+color.BOLD+"          v"+webVersion,"\n"+color.END)
            print("   Updates can introduce important fixes and new features. Downloading and\n   installing this update does not affect non-repo files, such as any\n   personal config scripts, hard disk images, ROMs, or boot files.")

         print("\n   Do you want to update now?\n"+color.END)
         print(color.BOLD+"      1. Download and Install...")
         print(color.END+"         Updates out-of-date repo files with new versions\n")
         print(color.END+"      2. Download only")
         print(color.END+"      Q. Exit without updating\n")
         detectChoice1 = str(input(color.BOLD+"Select> "+color.END))
         updateBrains()
   elif args.version is not None and argsVersionInt < versionInt:
      clear()
      if args.install is not True and args.download is not True:
         print("\n\n   "+color.BOLD+color.YELLOW+"⚠  DOWNGRADE DETECTED"+color.END,"")
         print("   The target version is an older version\n")
         print(color.END+color.GRAY+"         Current Version\n   "+"          v"+version,color.END+"\n")
         print(color.BOLD+"               ⋁\n")
         print(color.BOLD+"         Target Version\n   "+color.BOLD+"          v"+args.version,color.END+color.YELLOW+"⚠\n"+color.END)
         print("   The updater is currently targeting an older version.\n   There are risks involved and incompatibilities may arise.\n   No support is provided for downgrades.")

         print("\n   Do you want to continue anyway?\n"+color.END)
         print(color.BOLD+"      1. Download and Install..."+color.END,color.YELLOW+"⚠"+color.END)
         print(color.END+"         Restores the repo to the target version\n")
         print(color.END+"      2. Download only")
         print(color.END+"      Q. Exit without changes\n")
         detectChoice1 = str(input(color.BOLD+"Select> "+color.END))
         os.system("cp ./scripts/repo-update.py ./scripts/repo-update.py.newest > /dev/null 2>&1")
         updateBrains()
      

   else:
      clear()
      print("\n\n   "+color.BOLD+color.RED+"✖ FAILED TO CHECK FOR UPDATES"+color.END,"")
      print("   Something went wrong\n")
      print(color.BOLD+"   Your Reported Version\n   "+color.END+"v"+version,"\n")
      print("   The updater couldn't get the status of your current version, and/or the\n   remote server version's control file."+"\n\n")
      
   
else:
   clear()
   print("\n\n   "+color.BOLD+color.RED+"✖ CONNECTION FAILED"+color.END,"")
   print("   Unable to connect to server\n")
   print(color.BOLD+"   Your Reported Version\n   "+color.END+"v"+version,"\n")
   print("   The updater cannot connect to the update server.\n   Check your internet connection status."+"\n\n")

   #https://raw.githubusercontent.com/Coopydood/ultimate-macOS-KVM/"+str(targetBranch)+"/.version
