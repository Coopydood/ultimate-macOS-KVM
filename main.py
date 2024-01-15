#!/usr/bin/env python3
# pylint: disable=C0301,C0116,C0103,R0903

"""
This script was created by Coopydood as part of the ultimate-macOS-KVM project.

https://github.com/user/Coopydood
https://github.com/Coopydood/ultimate-macOS-KVM
Signature: 4CD28348A3DD016F

"""

#    WELCOME TO ULTMOS! *waves like an idiot*

##################################################
#   THIS IS THE MAIN FILE! RUN THIS FILE FIRST!  #
#                                                #
#                  $ ./main.py                   #
##################################################


import os
import time
import subprocess
import re 
import json
import sys
import argparse
import platform
try:
    import pypresence
except:
    None

sys.path.insert(0, 'scripts')

parser = argparse.ArgumentParser("main")
parser.add_argument("--skip-vm-check", dest="svmc", help="Skip the arbitrary VM check",action="store_true")
parser.add_argument("--skip-os-check", dest="sosc", help="Skip the OS platform check",action="store_true")
parser.add_argument("--disable-rpc", dest="rpcDisable", help="Disable Discord Rich Presence integration",action="store_true")

args = parser.parse_args()

global apFilePath
global VALID_FILE
global REQUIRES_SUDO
global discordRPC

detectChoice = 1
latestOSName = "Sonoma"
latestOSVer = "14"
runs = 0
apFilePath = ""
procFlow = 1
discordRPC = 1

version = open("./.version")
version = version.read()

versionDash = version.replace(".","-")


# Discord rich presence routine
client_id = "1149434759152422922"
try:
    RPC = Presence(client_id)
except:
    None

if args.rpcDisable == True:
    discordRPC = 0
else:
    discordRPC = 1 # DEBUGGG

projectVer = "Powered by ULTMOS v"+version

# We don't need these files anymore. If they're here, get rid
if os.path.exists("./UPGRADEPATH"): os.system("rm ./UPGRADEPATH")
if os.path.exists("./VERSION"): os.system("rm ./VERSION") 
if os.path.exists("./resources/WEBVERSION"): os.system("rm ./resources/WEBVERSION")

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



def startup():
    global detectChoice
    print(color.BOLD+"\n\n   Welcome to"+color.CYAN,"ULTMOS"+color.END+color.GRAY,"v"+version+color.END)
    print("   by Coopydood"+color.END)

    if not os.path.exists("resources/script_store/main.py"): # BACKUP ORIGINAL FILES TO STORE
        os.system("cp -R ./scripts/* ./resources/script_store/")
        os.system("cp ./main.py ./resources/script_store/")
        os.system("cp ./.version ./resources/script_store/")

    if isVM == True:
        print(color.YELLOW+"\n   ⚠  Virtual machine detected, functionality may be limited\n"+color.END)
    if os.path.exists("blobs/user/USR_CFG.apb"):
            tainted = 1
    else:
        print("\n   This project can assist you in some often-tedious setup, including\n   processes like"+color.BOLD,"checking your GPU, checking your system, downloading macOS,\n   "+color.END+"and more. Think of it like your personal KVM swiss army knife.")
    #print(color.BOLD+"\n"+"Profile:"+color.END,"https://github.com/Coopydood")
    #print(color.BOLD+"   Repo:"+color.END,"https://github.com/Coopydood/ultimate-macOS-KVM")
    #print("   Select an option to continue.")


    if os.path.exists("./blobs/USR_TARGET_OS.apb") and not os.path.exists("./blobs/user/USR_TARGET_OS.apb"):  # Rescue live blobs if coming from older repo version
        os.system("mv ./blobs/*.apb ./blobs/user")


    if os.path.exists("./blobs/user/USR_CFG.apb"):
            global apFilePath
            global macOSVer
            global mOSString
            apFilePath = open("./blobs/user/USR_CFG.apb")
            apFilePath = apFilePath.read()
            if os.path.exists("./blobs/user/USR_TARGET_OS_NAME.apb"):
                macOSVer = open("./blobs/user/USR_TARGET_OS_NAME.apb")
                macOSVer = macOSVer.read()
           
            macOSVer = open("./blobs/user/USR_TARGET_OS.apb")
            macOSVer = macOSVer.read()
            if int(macOSVer) <= 999 and int(macOSVer) > 99:
                macOSVer = str(int(macOSVer) / 100)
                mOSString = "Mac OS X"
            else:
                mOSString = "macOS"
            if os.path.exists("./blobs/user/USR_TARGET_OS_NAME.apb"):
                macOSVer = open("./blobs/user/USR_TARGET_OS_NAME.apb")
                macOSVer = macOSVer.read()
            if os.path.exists("./"+apFilePath):
                global REQUIRES_SUDO
                global VALID_FILE
                
                apFile = open("./"+apFilePath,"r")

                

                if "REQUIRES_SUDO=1" in apFile.read():
                    REQUIRES_SUDO = 1
                else:
                    REQUIRES_SUDO = 0

                apFile.close()

                apFile = open("./"+apFilePath,"r")
                
                if "APC-RUN" in apFile.read():
                    VALID_FILE = 1
                    
                    #REQUIRES_SUDO = 1 # UNCOMMENT FOR DEBUGGING

                    if REQUIRES_SUDO == 1:
                        print(color.BOLD+"\n      B. Boot",mOSString,macOSVer+color.YELLOW,"⚠"+color.END)
                        print(color.END+"         Start",mOSString,"using the detected\n         "+apFilePath+" script file."+color.YELLOW,"Requires superuser."+color.END)
                    else:
                        print(color.BOLD+"\n      B. Boot",mOSString,macOSVer+"")
                        print(color.END+"         Start",mOSString,"using the detected\n         "+apFilePath+" script file.")
                    print(color.END+"\n      1. AutoPilot")

                else:
                    print(color.BOLD+"\n      1. AutoPilot")
                    print(color.END+"         Quickly and easily set up a macOS\n         virtual machine in just a few steps\n")

            else:
                print(color.BOLD+"\n      1. AutoPilot")
                print(color.END+"         Quickly and easily set up a macOS\n         virtual machine in just a few steps\n")
    else:
        print(color.BOLD+"\n      1. AutoPilot")
        print(color.END+"         Quickly and easily set up a macOS\n         virtual machine in just a few steps\n")
    

    #print(color.END+"      2. Download and convert macOS image")
    #print(color.END+"      3. Check GPU compatibility")
    #print(color.END+"      4. Check IOMMU grouping")
    #print(color.END+"      5. Get and display vfio-pci IDs")
    #print(color.END+"      6. Verify devices bound to vfio-pci")
    
    print(color.END+"      2. Download macOS...")
    print(color.END+"      3. Compatibility checks...")
    print(color.END+"      4. Passthrough tools...\n")
    
    
    print(color.END+"      E. Extras...")
    print(color.END+"      W. What's new?")
    print(color.END+"      U. Check for updates")
    print(color.END+"      Q. Exit\n")
    detectChoice = str(input(color.BOLD+"Select> "+color.END))

       


def clear(): print("\n" * 150)



os.system("chmod +x -R scripts/*.py")
os.system("chmod +x -R scripts/extras/*.py")
#os.system("chmod +x -R scripts/extras/*.sh")
os.system("chmod +x -R scripts/restore/*.py")
os.system("chmod +x -R scripts/*.sh")
os.system("chmod +x resources/dmg2img")
os.system("chmod +x scripts/domtrues/*.py")




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

if platform.system() != "Linux":
    detected = 2


clear()

#detected = 2    # FORCE DETECTION OF INCOMPATIBLE OS FOR DEBUG

if detected == 1:
    if args.svmc == True:
        clear()
        startup()
    else:
        isVM = True
        print("\n   "+color.BOLD+color.YELLOW+"⚠ VIRTUAL MACHINE DETECTED"+color.END)
        print("   Virtualized devices detected")
        print("\n   I've determined that it's more than likely that \n   you're using a virtual machine to run this. I won't\n   stop you, but there really isn't much point in continuing."+color.END)
        
        print("\n   "+color.BOLD+color.YELLOW+"PROBLEM:",color.END+"Virtual hardware detected"+color.END)
        print(color.BOLD+"\n      1. Exit")
        print(color.END+"      2. Continue anyway\n")
        stageSelect = str(input(color.BOLD+"Select> "+color.END))
   
        if stageSelect == "1":
            sys.exit

        elif stageSelect == "2": 
            clear()
            startup()
elif detected == 2:
    if args.sosc == True:
        clear()
        startup()
    else:
        print("\n   "+color.BOLD+color.RED+"✖ INCOMPATIBLE OPERATING SYSTEM"+color.END)
        print("   "+platform.system()+" detected")
        print("\n   I've determined that you're using "+platform.system()+". \n   Put simply, this project won't work on here.\n   To save you further disappointment, I'm instead\n   throwing you this error.\n\n   Sorry :/"+color.END)
        
        print("\n   "+color.BOLD+color.RED+"PROBLEM:",color.END+"well... not Linux... ¯\_(ツ)_/¯"+color.END)
        print("\n\n\n")
        time.sleep(5)
        sys.exit

        
else:
    clear()
    startup()










if detectChoice == "1":
    os.system('./scripts/autopilot.py')
elif detectChoice == "2":
    os.system('./scripts/dlosx.py')

elif detectChoice == "3":
    clear()
    os.system('./scripts/compatchecks.py')
elif detectChoice == "4":
    clear()
    os.system('./scripts/vfio-menu.py')
elif detectChoice == "e" or detectChoice == "E":
    clear()
    os.system('./scripts/extras.py')
elif detectChoice == "w" or detectChoice == "W":
    clear()
    print("\n\n   "+color.BOLD+color.GREEN+"✔  OPENING RELEASE NOTES IN DEFAULT BROWSER"+color.END,"")
    print("   Continue in your browser\n")
    print("\n   I have attempted to open the release notes in\n   your default browser. Please be patient.\n\n   You will be returned to the main menu in 5 seconds.\n\n\n\n\n")
    os.system('xdg-open https://github.com/Coopydood/ultimate-macOS-KVM/blob/main/docs/changelogs/v'+versionDash+".md > /dev/null 2>&1")
    time.sleep(6)
    clear()
    os.system('./main.py')
elif detectChoice == "u" or detectChoice == "U":
    clear()
    os.system('./scripts/repo-update.py --menuFlow')
elif detectChoice == "q" or detectChoice == "Q":
    exit
elif detectChoice == "b" and VALID_FILE == 1 or detectChoice == "B" and VALID_FILE == 1:
    clear()

    if not os.path.exists("./ovmf/OVMF_VARS.df"):   # AUTO REPAIR OVMF
        if os.path.exists("./ovmf/user_store/OVMF_VARS.fd"):
            os.system("cp ./ovmf/user_store/OVMF_VARS.fd ./ovmf/OVMF_VARS.fd")
        else:
            os.system("cp ./resources/ovmf/OVMF_VARS.fd ./ovmf/OVMF_VARS.fd")

    if discordRPC == 1:
        subprocess.Popen(["python","./scripts/drpc.py","--os",macOSVer])
    if REQUIRES_SUDO == 1:
        print(color.YELLOW+color.BOLD+"\n   ⚠ "+color.END+color.BOLD+"SUPERUSER PRIVILEGES"+color.END+"\n   This script uses physical device passthrough,\n   and needs superuser priviledges to run.\n\n   Press CTRL+C to cancel.\n"+color.END)
        if discordRPC == 0:
            os.system("sudo ./"+apFilePath+" -d 0")
        else:
            os.system("sudo ./"+apFilePath)
    else:
        if discordRPC == 0:
            os.system("./"+apFilePath+" -d 0")
        else:
            os.system("./"+apFilePath)
else:
    startup()