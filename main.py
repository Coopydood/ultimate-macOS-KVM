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
import datetime
sys.path.append('./resources/python')
from cpydColours import color
try:
    from pypresence import Presence
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
global baseSystemNotifArmed

detectChoice = 1
latestOSName = "Sequoia"
latestOSVer = "15"
runs = 0
apFilePath = ""
procFlow = 1
discordRPC = 1

baseSystemNotifArmed = False

version = open("./.version")
version = version.read()

versionDash = version.replace(".","-")

if args.rpcDisable == True:
    discordRPC = 0
else:
    discordRPC = 1 # DEBUGGG

projectVer = "Powered by ULTMOS v"+version

# We don't need these files anymore. If they're here, get rid
if os.path.exists("./UPGRADEPATH"): os.system("rm ./UPGRADEPATH")
if os.path.exists("./VERSION"): os.system("rm ./VERSION") 
if os.path.exists("./resources/WEBVERSION"): os.system("rm ./resources/WEBVERSION")

def startup():
    global detectChoice
    global apFile
    global apFilePath
    detectChoice = None

    if not os.path.exists("resources/script_store/main.py"): # BACKUP ORIGINAL FILES TO STORE
        os.system("cp -R ./scripts/* ./resources/script_store/")
        os.system("cp ./main.py ./resources/script_store/")
        os.system("cp ./.version ./resources/script_store/")


    def fts():
        clear()
        print("\n\n   "+color.BOLD+color.BLUE+"                WELCOME TO"+color.CYAN+" ULTMOS"+color.BLUE+color.BOLD+""+color.END)
        print("                First time setup wizard\n")
        print("   Welcome! As this is your first time using ULTMOS, you\n   must select how you'd like to use the project.\n   The project can be run in 2 modes.")
        print(color.BOLD+"\n      1. Standard mode (recommended)")
        print(color.END+"         This mode is the default, and sets up the repo to\n         use a traditional folder structure; designed for \n         use with one virtual machine at a time. Making a\n         new VM would replace the old one.")
        #print(color.BOLD+"\n      2. Create a new XML file using AutoPilot...")
        #print(color.END+"         Use this option if you do not have an AutoPilot config file.\n         This script will take you through the AutoPilot steps before\n         generating an XML file based on your answers. No existing\n         data, such as vHDDs, can be used with this method.")
        print(color.BOLD+color.GRAY+"\n      2. Dynamic mode (BETA)"+color.END)
        print(color.GRAY+"         This mode is intended to replace standard mode. It\n         instead allows you to create many VMs under one\n         repo, sharing project resources. This means you can\n         easily move and copy VMs to other computers.")
        print(color.RED+"         This feature is currently unavailable.\n"+color.END)
        print("   Please select a mode to begin.\n")
    
        #print(color.YELLOW+color.BOLD+"\n   ⚠ "+color.END+color.BOLD+"WARNING"+color.END+"\n   This action requires superuser permissions.\n"+color.END)
        detectChoiceMode = str(input(color.BOLD+"Select> "+color.END))

        if detectChoiceMode == detectChoiceMode:
            clear()
            nrsblob = open("./resources/.nrsMode","w")
            nrsblob.write("1")
            nrsblob.close()
        else:
            fts()
    
    #print(color.BOLD+"\n"+"Profile:"+color.END,"https://github.com/Coopydood")
    #print(color.BOLD+"   Repo:"+color.END,"https://github.com/Coopydood/ultimate-macOS-KVM")
    #print("   Select an option to continue.")

    if not os.path.exists("./resources/.nrsMode"):
        fts()

    if isVM == True:
        print(color.YELLOW+"\n   ⚠  Virtual machine detected, functionality may be limited\n"+color.END)
    if os.path.exists("blobs/user/USR_CFG.apb"):
            print(color.BOLD+"\n\n  "+color.CYAN,"ULTMOS"+color.END+color.GRAY,"v"+version+color.END)
            print("   by Coopydood"+color.END)
            tainted = 1
    else:
        print(color.BOLD+"\n\n   Welcome to"+color.CYAN,"ULTMOS"+color.END+color.GRAY,"v"+version+color.END)
        print("   by Coopydood"+color.END)
        print("\n   This project can assist you in some often-tedious setup, including\n   processes like"+color.BOLD,"checking your GPU, checking your system, downloading macOS,\n   "+color.END+"and more. Think of it like your personal KVM swiss army knife.")



    

    if os.path.exists("./blobs/USR_TARGET_OS.apb") and not os.path.exists("./blobs/user/USR_TARGET_OS.apb"):  # Rescue live blobs if coming from older repo version
        os.system("mv ./blobs/*.apb ./blobs/user")


    if os.path.exists("./blobs/user/USR_CFG.apb"):
            global apFilePath
            global apFilePathNoPT
            global apFile
            global apFilePathNoUSB
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
                global VALID_FILE_NOPT
                global VALID_FILE_NOUSB
                global baseSystemNotifArmed
                VALID_FILE = 0
                VALID_FILE_NOPT = 0
                VALID_FILE_NOUSB = 0
                

                apFile = open("./"+apFilePath,"r")

                

                if "REQUIRES_SUDO=1" in apFile.read():
                    REQUIRES_SUDO = 1
                else:
                    REQUIRES_SUDO = 0

                apFile.close()

                apFile = open("./"+apFilePath,"r")

                apFilePathNoPT = apFilePath.replace(".sh","-noPT.sh")
                apFilePathNoUSB = apFilePath.replace(".sh","-noUSB.sh")
                
                apFileM = apFile.read()

                if "APC-RUN" in apFileM:
                    VALID_FILE = 1

                    if "#-drive id=BaseSystem,if=none,file=\"$VM_PATH/BaseSystem.img\",format=raw" not in apFileM and "-drive id=BaseSystem,if=none,file=\"$VM_PATH/BaseSystem.img\",format=raw" in apFileM and "HDD_PATH=\"/dev/disk/" not in apFileM:
                        if os.path.exists("./blobs/user/USR_HDD_PATH.apb"):
                            hddPath = open("./blobs/user/USR_HDD_PATH.apb")
                            hddPath = hddPath.read()
                            hddPath = hddPath.replace("$VM_PATH",os.path.realpath(os.curdir))
                        if (os.path.getsize(hddPath)) > 22177079296 and not os.path.exists("./blobs/user/.noBaseSystemReminder"):
                            baseSystemNotifArmed = True
                    #REQUIRES_SUDO = 1 # UNCOMMENT FOR DEBUGGING

                    if REQUIRES_SUDO == 1:
                        print(color.BOLD+"\n      B. Boot",mOSString,macOSVer+color.YELLOW,"⚠"+color.END)
                        print(color.END+"         Start",mOSString,"using the detected\n         "+apFilePath+" script file."+color.YELLOW,"Requires superuser."+color.END)
                    else:
                        print(color.BOLD+"\n      B. Boot",mOSString,macOSVer+"")
                        print(color.END+"         Start",mOSString,"using the detected\n         "+apFilePath+" script file.")
                    
                    if os.path.exists("./"+apFilePathNoPT):
                        VALID_FILE_NOPT = 1
                    
                    if os.path.exists("./"+apFilePathNoUSB):
                        VALID_FILE_NOUSB = 1
                        
                    if VALID_FILE_NOPT == 1 or VALID_FILE_NOUSB == 1:
                        print(color.BOLD+"\n      O. Other boot options...") 


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

def baseSystemAlert():
    global apFilePath
    clear()
    print("\n\n   "+color.BOLD+color.GREEN+"FINISHED INSTALLING MACOS?"+color.END,"")
    print("   Finished install detected\n")
    print("   The assistant has detected that your macOS installation \n   may be complete. Would you like me to remove the install\n   media from your config file for you?\n\n   This stops the \"macOS Base System\" boot entry from appearing.\n")
    #print(color.YELLOW+color.BOLD+"\n   ⚠ "+color.END+color.BOLD+"WARNING"+color.END+"\n   This action requires superuser permissions.\n"+color.END)
    print(color.BOLD+"      1. Remove BaseSystem"+color.END)
    print(color.END+"         Detaches the macOS installer\n         from the",apFilePath+" file\n")
    print(color.END+"      2. Not now")
    print(color.END+"      3. Don't remind me again\n")
    detectChoice5 = str(input(color.BOLD+"Select> "+color.END))

    if detectChoice5 == "1":
        with open("./"+apFilePath,"r") as apFile:
            apFileM = apFile.read()
            apFileM = apFileM.replace("-drive id=BaseSystem,if=none,file=\"$VM_PATH/BaseSystem.img\",format=raw\n-device ide-hd,bus=sata.4,drive=BaseSystem","#-drive id=BaseSystem,if=none,file=\"$VM_PATH/BaseSystem.img\",format=raw\n#-device ide-hd,bus=sata.4,drive=BaseSystem")
            apFile.close()
        time.sleep(1)
        with open("./"+apFilePath,"w") as apFile:
            apFile.write(apFileM)
            apFile.close()
        clear()
        print("\n\n   "+color.BOLD+color.GREEN+"DONE"+color.END,"")
        print("   BaseSystem removed successfully\n\n\n\n\n\n\n\n")
        time.sleep(3)
        clear()
    elif detectChoice5 == "3":
        with open("./blobs/user/.noBaseSystemReminder","w") as remindFile:
            remindFile.write(" ")
            remindFile.close()
        clear()
    else:
        clear()

os.system("chmod +x -R scripts/*.py")
os.system("chmod +x -R scripts/extras/*.py")
#os.system("chmod +x -R scripts/extras/*.sh")
os.system("chmod +x -R scripts/restore/*.py")
os.system("chmod +x -R scripts/*.sh")
os.system("chmod +x resources/dmg2img")
os.system("chmod +x scripts/hyperchromiac/*.py")




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
        
        print("\n   "+color.BOLD+color.RED+"PROBLEM:",color.END+"well... not Linux... ¯\\_(ツ)_/¯"+color.END)
        print("\n\n\n")
        time.sleep(5)
        sys.exit

        
else:
    clear()
    
    startup()
    #baseSystemAlert() # uncomment to always trigger notification
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
elif detectChoice == "b" and VALID_FILE == 1 or detectChoice == "B" and VALID_FILE == 1:
    clear()

    if not os.path.exists("./ovmf/OVMF_VARS.df"):   # AUTO REPAIR OVMF
        if os.path.exists("./ovmf/user_store/OVMF_VARS.fd"):
            os.system("cp ./ovmf/user_store/OVMF_VARS.fd ./ovmf/OVMF_VARS.fd")
        else:
            os.system("cp ./resources/ovmf/OVMF_VARS.fd ./ovmf/OVMF_VARS.fd")

    if discordRPC == 1:

        # Discord rich presence routine
        client_id = "1149434759152422922"
        try:
            RPC = Presence(client_id)
        except:
            None

        if os.path.exists("./blobs/user/USR_VFIO_DEVICES.apb"):
            vfioDevs = open("./blobs/user/USR_VFIO_DEVICES.apb")
            vfioDevs = vfioDevs.read()
            subprocess.Popen(["python3","./scripts/drpc.py","--os",macOSVer,"--pt",vfioDevs])
        else:
            subprocess.Popen(["python3","./scripts/drpc.py","--os",macOSVer])
    if REQUIRES_SUDO == 1:
        print(color.YELLOW+color.BOLD+"\n   ⚠ "+color.END+color.BOLD+"SUPERUSER PRIVILEGES"+color.END+"\n   This script uses physical device passthrough,\n   and needs superuser privileges to run.\n\n   Press CTRL+C to cancel.\n"+color.END)
        if baseSystemNotifArmed == True:
            baseSystemAlert()
        if discordRPC == 0:
            os.system("sudo ./"+apFilePath+" -d 0")
        else:
            os.system("sudo ./"+apFilePath)
        

    else:
        if baseSystemNotifArmed == True:
            baseSystemAlert()
        if discordRPC == 0:
            os.system("./"+apFilePath+" -d 0")
        else:
            os.system("./"+apFilePath)
elif detectChoice == "o" and VALID_FILE_NOPT == 1 or detectChoice == "o" and VALID_FILE_NOUSB == 1 or detectChoice == "O" and VALID_FILE_NOPT == 1 or detectChoice == "O" and VALID_FILE_NOUSB == 1:
    # Spawn boot options menu
    clear()
    print(color.BOLD+color.BLUE+"\n\n   BOOT OPTIONS FOR",mOSString.upper(),macOSVer.upper()+""+color.END)
    print("   The following boot options are available:")

    if REQUIRES_SUDO == 1:
        print(color.BOLD+"\n      1. Boot",mOSString,macOSVer+color.YELLOW,"⚠"+color.END)
        print(color.END+"         Start",mOSString,"using the detected\n         "+apFilePath+" script file."+color.YELLOW,"Requires superuser."+color.END)
    else:
        print(color.BOLD+"\n      1. Boot",mOSString,macOSVer+"")
        print(color.END+"         Start",mOSString,"using the detected\n         "+apFilePath+" script file.")
                    
    

    if VALID_FILE_NOPT == 1:
        
        apFile = open("./"+apFilePathNoPT,"r")

        if "REQUIRES_SUDO=1" in apFile.read():
            REQUIRES_SUDO = 1
        else:
            REQUIRES_SUDO = 0

        if REQUIRES_SUDO == 1:
            print(color.BOLD+"\n      2. Boot",mOSString,macOSVer+" without PCI passthrough"+color.YELLOW+" ⚠"+color.END)
            print(color.END+"         Start",mOSString,"using "+apFilePathNoPT+", with\n         no passthrough devices enabled."+color.YELLOW,"Requires superuser."+color.END)
        else:
            print(color.BOLD+"\n      2. Boot",mOSString,macOSVer+" without PCI passthrough")
            print(color.END+"         Start",mOSString,"using "+apFilePathNoPT+", with\n         no passthrough devices enabled.")

    
    if VALID_FILE_NOUSB == 1:
        
        apFile = open("./"+apFilePathNoUSB,"r")

        if "REQUIRES_SUDO=1" in apFile.read():
            REQUIRES_SUDO = 1
        else:
            REQUIRES_SUDO = 0

        if REQUIRES_SUDO == 1:
            print(color.BOLD+"\n      3. Boot",mOSString,macOSVer+" without host USB devices"+color.YELLOW+" ⚠"+color.END)
            print(color.END+"         Start",mOSString,"using "+apFilePathNoUSB+", with\n         no host USB devices."+color.YELLOW,"Requires superuser."+color.END)
        else:
            print(color.BOLD+"\n      3. Boot",mOSString,macOSVer+" without host USB devices")
            print(color.END+"         Start",mOSString,"using "+apFilePathNoUSB+", with\n         no host USB devices.")

    print(color.END+"\n      B. Back...")
    print(color.END+"      Q. Exit\n")
    detectChoice3 = str(input(color.BOLD+"Select> "+color.END))

    if detectChoice3 == "1" and VALID_FILE == 1:  # REGULAR BOOT
        clear()

        if not os.path.exists("./ovmf/OVMF_VARS.df"):   # AUTO REPAIR OVMF
            if os.path.exists("./ovmf/user_store/OVMF_VARS.fd"):
                os.system("cp ./ovmf/user_store/OVMF_VARS.fd ./ovmf/OVMF_VARS.fd")
            else:
                os.system("cp ./resources/ovmf/OVMF_VARS.fd ./ovmf/OVMF_VARS.fd")

        if discordRPC == 1:
            # Discord rich presence routine
            client_id = "1149434759152422922"
            try:
                RPC = Presence(client_id)
            except:
                None
            if os.path.exists("./blobs/user/USR_VFIO_DEVICES.apb"):
                vfioDevs = open("./blobs/user/USR_VFIO_DEVICES.apb")
                vfioDevs = vfioDevs.read()
                subprocess.Popen(["python3","./scripts/drpc.py","--os",macOSVer,"--pt",vfioDevs])
            else:
                subprocess.Popen(["python3","./scripts/drpc.py","--os",macOSVer])
        if REQUIRES_SUDO == 1:
            print(color.YELLOW+color.BOLD+"\n   ⚠ "+color.END+color.BOLD+"SUPERUSER PRIVILEGES"+color.END+"\n   This script uses physical device passthrough,\n   and needs superuser privileges to run.\n\n   Press CTRL+C to cancel.\n"+color.END)
            if baseSystemNotifArmed == True:
                baseSystemAlert()   
            if discordRPC == 0:
                os.system("sudo ./"+apFilePath+" -d 0")
            else:
                os.system("sudo ./"+apFilePath)
        else:
            if baseSystemNotifArmed == True:
                baseSystemAlert()
            if discordRPC == 0:
                os.system("./"+apFilePath+" -d 0")
            else:
                os.system("./"+apFilePath)
    
    if detectChoice3 == "2" and VALID_FILE_NOPT == 1:  # NO PASSTHROUGH BOOT
        clear()

        apFile = open("./"+apFilePathNoPT,"r")

                

        if "REQUIRES_SUDO=1" in apFile.read():
            REQUIRES_SUDO = 1
        else:
            REQUIRES_SUDO = 0

        if not os.path.exists("./ovmf/OVMF_VARS.df"):   # AUTO REPAIR OVMF
            if os.path.exists("./ovmf/user_store/OVMF_VARS.fd"):
                os.system("cp ./ovmf/user_store/OVMF_VARS.fd ./ovmf/OVMF_VARS.fd")
            else:
                os.system("cp ./resources/ovmf/OVMF_VARS.fd ./ovmf/OVMF_VARS.fd")

        if discordRPC == 1:
            # Discord rich presence routine
            client_id = "1149434759152422922"
            try:
                RPC = Presence(client_id)
            except:
                None
            subprocess.Popen(["python3","./scripts/drpc.py","--os",macOSVer])
        if REQUIRES_SUDO == 1:
            print(color.YELLOW+color.BOLD+"\n   ⚠ "+color.END+color.BOLD+"SUPERUSER PRIVILEGES"+color.END+"\n   This script uses physical device passthrough,\n   and needs superuser privileges to run.\n\n   Press CTRL+C to cancel.\n"+color.END)
            if baseSystemNotifArmed == True:
                baseSystemAlert()
            if discordRPC == 0:
                os.system("sudo ./"+apFilePathNoPT+" -d 0")
            else:
                os.system("sudo ./"+apFilePathNoPT)
        else:
            if baseSystemNotifArmed == True:
                baseSystemAlert()
            if discordRPC == 0:
                os.system("./"+apFilePathNoPT+" -d 0")
            else:
                os.system("./"+apFilePathNoPT)
    
    if detectChoice3 == "3" and VALID_FILE_NOUSB == 1:  # NO USB BOOT
        clear()

        apFile = open("./"+apFilePathNoUSB,"r")

                

        if "REQUIRES_SUDO=1" in apFile.read():
            REQUIRES_SUDO = 1
        else:
            REQUIRES_SUDO = 0

        if not os.path.exists("./ovmf/OVMF_VARS.df"):   # AUTO REPAIR OVMF
            if os.path.exists("./ovmf/user_store/OVMF_VARS.fd"):
                os.system("cp ./ovmf/user_store/OVMF_VARS.fd ./ovmf/OVMF_VARS.fd")
            else:
                os.system("cp ./resources/ovmf/OVMF_VARS.fd ./ovmf/OVMF_VARS.fd")

        if discordRPC == 1:
            # Discord rich presence routine
            client_id = "1149434759152422922"
            try:
                RPC = Presence(client_id)
            except:
                None
            subprocess.Popen(["python3","./scripts/drpc.py","--os",macOSVer])
        if REQUIRES_SUDO == 1:
            print(color.YELLOW+color.BOLD+"\n   ⚠ "+color.END+color.BOLD+"SUPERUSER PRIVILEGES"+color.END+"\n   This script uses physical device passthrough,\n   and needs superuser privileges to run.\n\n   Press CTRL+C to cancel.\n"+color.END)
            if baseSystemNotifArmed == True:
                baseSystemAlert()
            if discordRPC == 0:
                os.system("sudo ./"+apFilePathNoUSB+" -d 0")
            else:
                os.system("sudo ./"+apFilePathNoUSB)
        else:
            if baseSystemNotifArmed == True:
                baseSystemAlert()
            if discordRPC == 0:
                os.system("./"+apFilePathNoUSB+" -d 0")
            else:
                os.system("./"+apFilePathNoUSB)
    
    elif detectChoice3 == "b" or detectChoice3 == "B":
        os.system('./main.py --skip-vm-check')
        
    elif detectChoice3 == "q" or detectChoice3 == "Q":
        exit
    else:
        startup()
elif detectChoice == "q" or detectChoice == "Q":
    clear()
    print(color.BOLD+"\n\n   "+color.PURPLE+"GOODBYE!"+color.END)
    print("   Thanks for using ULTMOS!"+color.END)
    print("\n   This project was created with "+color.RED+color.BOLD+"❤"+color.END+" by Coopydood\n   and a growing list of awesome contributors.\n\n   Have feedback, issues, or want to contribute?\n   I'd love to hear from you!\n\n   "+color.BOLD+"https://github.com/Coopydood/ultimate-macOS-KVM\n   https://discord.gg/WzWkSsT\n"+color.END)
    hr = datetime.datetime.now().time().hour
    if hr > 3 and hr < 12:
        print("   Have a nice day! :]\n\n\n")
    elif hr >= 12 and hr < 17:
        print("   Have a nice rest of your afternoon! :]\n\n\n")
    elif hr >= 17 and hr < 21:
        print("   Have a nice evening! :]\n\n\n")
    else:
        print("   Have a nice night - "+color.CYAN+"and remember to sleep!"+color.END+" :]\n\n\n")
    exit(0)

elif detected != 2:
    clear()
    os.system('./main.py')