#!/usr/bin/env python3
# pylint: disable=C0301,C0116,C0103,R0903

"""
This script was created by Coopydood as part of the ultimate-macOS-KVM project.

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
from datetime import datetime


detectChoice = 1
latestOSName = "Sonoma"
latestOSVer = "14"
runs = 0

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
    clear()
    print("\n\n  "+color.BOLD+color.PURPLE,"BOOT ARGUMENT EDITOR"+color.END,"")
    print("   by",color.BOLD+"Coopydood and DomTrues\n"+color.END)
    print("   This script can automatically mount your OpenCore image\n   and modify its boot arguments without booting macOS."+color.END)
    #print(color.BOLD+"\n"+"Profile:"+color.END,"https://github.com/Coopydood")
    #print(color.BOLD+"   Repo:"+color.END,"https://github.com/Coopydood/ultimate-macOS-KVM")
    print("\n   "+color.YELLOW,"⚠  "+color.END+color.BOLD+"Requires superuser privileges."+color.END)

    print(color.BOLD+"\n      1. AutoPatch..."+color.YELLOW,"⚠"+color.END)
    print(color.END+"         This option lists a set of available\n         boot argument related fixes and instantly applies them.\n")
    print(color.BOLD+"      2. View or Change..."+color.YELLOW,"⚠"+color.END)
    print(color.END+"         This option will allow you to enter new\n         boot arguments to be used.\n")
    
    print(color.BOLD+"      X. Restore Default..."+color.YELLOW,"⚠"+color.END)
    print(color.END+"         This option will restore the default boot\n         arguments that originally came with the image.\n")
    print(color.END+"      M. Main menu")
    print(color.END+"      ?. Help")
    print(color.END+"      Q. Exit\n")
    detectChoice = str(input(color.BOLD+"Select> "+color.END))
    clear()
    os.system("./scripts/domtrues/nbdassistant.py -u -q") # Ensure no stale mounts
       


def clear(): print("\n" * 150)

startup()

if detectChoice == "1":
    clear()
    print(color.YELLOW+color.BOLD+"\n   ⚠ "+color.END+color.BOLD+"SUPERUSER PRIVILEGES"+color.END+"\n   To mount the OpenCore image,\n   the script needs superuser to continue.\n\n   Press CTRL+C to cancel.\n"+color.END)
    os.system("./scripts/domtrues/nbdassistant.py -m -q")
    # NOTE: IMPLEMENT ERROR CATCH HERE
    clear()
    plistFile = open("./boot/mnt/EFI/OC/config.plist","r")
    plist = plistFile.read()
    plistFile.close()
    plistSplit = plist.split("<key>boot-args</key>",1)[1]
    plistSplit = plistSplit.split("</string>",1)[0]
    bootArgs = plistSplit.split("<string>",1)[1]
    
    print("   "+"\n   "+color.BOLD+"AutoPatch"+color.END)
    print("   "+"Choose an available patch")
    print("   "+"\n   A list of predefined patches are listed below.\n   The patch will be appended to your existing arguments."+color.END)#print(color.BOLD+"\n"+"Profile:"+color.END,"https://github.com/Coopydood")
    print("\n   "+color.BOLD+color.CYAN+"CURRENT:"+color.END+color.BOLD,bootArgs+color.END)
    
    #print(color.BOLD+"   Repo:"+color.END,"https://github.com/Coopydood/ultimate-macOS-KVM")
    print(color.BOLD+"\n      1. Fix black screen or reset on Navi GPUs")
    print(color.END+"         Fixes the post-install blackout on AMD RX 5xxx / 6xxx (Navi) GPUs")
    print(color.BOLD+"\n      2. Fix GPU initialisation on HD 7000 / R7 GPUs")
    print(color.END+"         Fixes the initialisation of AMD Radeon HD 7000 and R7 series GPUs")
  
    #print(color.END+"\n      ?. Help...")
    print(color.END+"\n      M. Main menu")
    print(color.END+"      Q. Exit\n")
    detectChoice1 = str(input(color.BOLD+"Select> "+color.END))

    if detectChoice1 == "1": # Navi Patch
        clear()

        if "agdpmod=pikera" in bootArgs:
            print("   "+"\n   "+color.BOLD+color.RED+"✖  BOOT ARGUMENT PATCH FAILED"+color.END)
            print("   "+"Boot arguments were not updated")
            print("   "+"\n   Your changes could not be saved.\n"+color.END)#print(color.BOLD+"\n"+"Profile:"+color.END,"https://github.com/Coopydood")
        
            print("   "+color.BOLD+color.RED+"ERROR:"+color.END+color.BOLD,"The selected patch is already applied."+color.END+"\n\n\n\n\n")
            time.sleep(3)



        else:
            bootArgsNew = bootArgs+" agdpmod=pikera"
            print("   "+"\n   "+color.BOLD+"Confirm Patch"+color.END)
            print("   "+"Ready to apply")
            print("   "+"\n   The selected patch has been added to your existing\n   boot arguments. Would you like to apply it?"+color.END)#print(color.BOLD+"\n"+"Profile:"+color.END,"https://github.com/Coopydood")
            print("\n   "+color.BOLD+color.CYAN+"CURRENT:"+color.END+color.BOLD,bootArgs+color.END)
            #print("     "+color.BOLD+"   ▼")
            print("   "+color.BOLD+color.GREEN+"    NEW:"+color.END+color.BOLD,bootArgsNew+color.END)
            #print(color.BOLD+"   Repo:"+color.END,"https://github.com/Coopydood/ultimate-macOS-KVM")
            print(color.BOLD+"\n      1. Apply")
            print(color.END+"         Add the patch and unmount the OpenCore image")
            
            #print(color.END+"         Use this option if you already have an XML file.\n         This option lets you import a previously-created XML file\n         into virsh for use with virt-manager.\n")
            print(color.END+"\n      B. Back...")
            #print(color.END+"      ?. Help...")
            print(color.END+"      Q. Exit\n")
            detectChoice2 = str(input(color.BOLD+"Select> "+color.END))

            if detectChoice2 == "1":
                backupOCPath = str(datetime.today().strftime('%d-%m-%Y_%H-%M-%S'))
                os.system("mkdir boot/"+backupOCPath)
                os.system("cp boot/*.qcow2 boot/"+backupOCPath+"/")
                plistFile = open("./boot/mnt/EFI/OC/config.plist","w")
                updatedPlist = plist.replace(bootArgs,bootArgsNew)
                plistFile.write(updatedPlist)
                plistFile.close()
                time.sleep(3)
                clear()
                print("   "+"\n   "+color.BOLD+color.GREEN+"✔  BOOT ARGUMENT PATCH APPLIED"+color.END)
                print("   "+"Boot arguments updated")
                print("   "+"\n   Your changes have been saved.\n   The new boot arguments are ready to use."+color.END)#print(color.BOLD+"\n"+"Profile:"+color.END,"https://github.com/Coopydood")
                print("\n   "+color.BOLD+color.GRAY+"    OLD:"+color.END,bootArgs+color.END)
                #print("     "+color.BOLD+"   ▼")
                print("   "+color.BOLD+color.GREEN+"CURRENT:"+color.END+color.BOLD,bootArgsNew+color.END+"\n\n\n\n\n")
                os.system("./scripts/domtrues/nbdassistant.py -u -q")
                time.sleep(3)
            
            elif detectChoice2 == "B" or detectChoice2 == "b":
                os.system("./scripts/extras/boot-args.py")
            elif detectChoice == "Q" or detectChoice == "q":
                exit
    
    if detectChoice1 == "2": # R7 HD Patch
        clear()

        if "radpg=15" in bootArgs:
            print("   "+"\n   "+color.BOLD+color.RED+"✖  BOOT ARGUMENT PATCH FAILED"+color.END)
            print("   "+"Boot arguments were not updated")
            print("   "+"\n   Your changes could not be saved.\n"+color.END)#print(color.BOLD+"\n"+"Profile:"+color.END,"https://github.com/Coopydood")
        
            print("   "+color.BOLD+color.RED+"ERROR:"+color.END+color.BOLD,"The selected patch is already applied."+color.END+"\n\n\n\n\n")
            time.sleep(3)



        else:
            bootArgsNew = bootArgs+" radpg=15"
            print("   "+"\n   "+color.BOLD+"Confirm Patch"+color.END)
            print("   "+"Ready to apply")
            print("   "+"\n   The selected patch has been added to your existing\n   boot arguments. Would you like to apply it?"+color.END)#print(color.BOLD+"\n"+"Profile:"+color.END,"https://github.com/Coopydood")
            print("\n   "+color.BOLD+color.CYAN+"CURRENT:"+color.END+color.BOLD,bootArgs+color.END)
            #print("     "+color.BOLD+"   ▼")
            print("   "+color.BOLD+color.GREEN+"    NEW:"+color.END+color.BOLD,bootArgsNew+color.END)
            #print(color.BOLD+"   Repo:"+color.END,"https://github.com/Coopydood/ultimate-macOS-KVM")
            print(color.BOLD+"\n      1. Apply")
            print(color.END+"         Add the patch and unmount the OpenCore image")
            
            #print(color.END+"         Use this option if you already have an XML file.\n         This option lets you import a previously-created XML file\n         into virsh for use with virt-manager.\n")
            print(color.END+"\n      B. Back...")
            #print(color.END+"      ?. Help...")
            print(color.END+"      Q. Exit\n")
            detectChoice2 = str(input(color.BOLD+"Select> "+color.END))

            if detectChoice2 == "1":
                backupOCPath = str(datetime.today().strftime('%d-%m-%Y_%H-%M-%S'))
                os.system("mkdir boot/"+backupOCPath)
                os.system("cp boot/*.qcow2 boot/"+backupOCPath+"/")
                plistFile = open("./boot/mnt/EFI/OC/config.plist","w")
                updatedPlist = plist.replace(bootArgs,bootArgsNew)
                plistFile.write(updatedPlist)
                plistFile.close()
                time.sleep(3)
                clear()
                print("   "+"\n   "+color.BOLD+color.GREEN+"✔  BOOT ARGUMENT PATCH APPLIED"+color.END)
                print("   "+"Boot arguments updated")
                print("   "+"\n   Your changes have been saved.\n   The new boot arguments are ready to use."+color.END)#print(color.BOLD+"\n"+"Profile:"+color.END,"https://github.com/Coopydood")
                print("\n   "+color.BOLD+color.GRAY+"    OLD:"+color.END,bootArgs+color.END)
                #print("     "+color.BOLD+"   ▼")
                print("   "+color.BOLD+color.GREEN+"CURRENT:"+color.END+color.BOLD,bootArgsNew+color.END+"\n\n\n\n\n")
                os.system("./scripts/domtrues/nbdassistant.py -u -q")
                time.sleep(3)
            
            elif detectChoice2 == "B" or detectChoice2 == "b":
                os.system("./scripts/extras/boot-args.py")
            elif detectChoice == "Q" or detectChoice == "q":
                exit
   

    elif detectChoice == "M" or detectChoice == "m":
        startup()

    elif detectChoice == "Q" or detectChoice == "q":
        exit

elif detectChoice == "2":
    clear()
    print(color.YELLOW+color.BOLD+"\n   ⚠ "+color.END+color.BOLD+"SUPERUSER PRIVILEGES"+color.END+"\n   To mount the OpenCore image,\n   the script needs superuser to continue.\n\n   Press CTRL+C to cancel.\n"+color.END)
    os.system("./scripts/domtrues/nbdassistant.py -m -q")
    # NOTE: IMPLEMENT ERROR CATCH HERE
    clear()
    plistFile = open("./boot/mnt/EFI/OC/config.plist","r")
    plist = plistFile.read()
    plistFile.close()
    plistSplit = plist.split("<key>boot-args</key>",1)[1]
    plistSplit = plistSplit.split("</string>",1)[0]
    bootArgs = plistSplit.split("<string>",1)[1]
    
    print("   "+"\n   "+color.BOLD+"Boot Argument Editor"+color.END)
    print("   "+"View or change your boot arguments")
    print("   "+"\n   You can view your current boot arguments below,\n   and edit them if you wish to."+color.END)#print(color.BOLD+"\n"+"Profile:"+color.END,"https://github.com/Coopydood")
    print("\n   "+color.BOLD+color.CYAN+"CURRENT:"+color.END+color.BOLD,bootArgs+color.END)
    
    #print(color.BOLD+"   Repo:"+color.END,"https://github.com/Coopydood/ultimate-macOS-KVM")
    print(color.BOLD+"\n      1. Enter new boot arguments...")
    print(color.END+"         Manually write the OpenCore boot arguments")

    print(color.END+"\n      M. Main menu")
    print(color.END+"      Q. Exit\n")
    detectChoice1 = str(input(color.BOLD+"Select> "+color.END))

    if detectChoice1 == "1":
        
        clear()
        def enterArgs():
            global bootArgsNew
            print("   "+"\n   "+color.BOLD+"Boot Argument Editor"+color.END)
            print("   "+"Type boot arguments")
            print("   "+"\n   Type the boot arguments the OpenCore image\n   should use. Seperate arguments with spaces."+color.END)#print(color.BOLD+"\n"+"Profile:"+color.END,"https://github.com/Coopydood")
            print("\n   "+color.BOLD+color.CYAN+"CURRENT:"+color.END+color.BOLD,bootArgs+color.END+"\n\n\n\n")
            bootArgsNew = str(input(color.BOLD+"Boot Arguments> "+color.END))
            time.sleep(1)
        
            clear()
            print("   "+"\n   "+color.BOLD+"Confirm Update"+color.END)
            print("   "+"Ready to apply")
            print("   "+"\n   The entered boot arguments have been processed.\n   Confirm or edit? A backup will be created."+color.END)#print(color.BOLD+"\n"+"Profile:"+color.END,"https://github.com/Coopydood")
            print("\n   "+color.BOLD+color.CYAN+"CURRENT:"+color.END+color.BOLD,bootArgs+color.END)
            #print("     "+color.BOLD+"   ▼")
            print("   "+color.BOLD+color.GREEN+"    NEW:"+color.END+color.BOLD,bootArgsNew+color.END)
            #print(color.BOLD+"   Repo:"+color.END,"https://github.com/Coopydood/ultimate-macOS-KVM")
            print(color.BOLD+"\n      1. Apply")
            print(color.END+"         Set the boot arguments and unmount the OpenCore image")
            print(color.BOLD+"\n      2. Edit...")
            print(color.END+"         Re-enter the boot arguments")
            print(color.END+"\n      B. Back...")
            #print(color.END+"      ?. Help...")
            print(color.END+"      Q. Exit\n")
            detectChoice2 = str(input(color.BOLD+"Select> "+color.END))

            if detectChoice2 == "1":
                backupOCPath = str(datetime.today().strftime('%d-%m-%Y_%H-%M-%S'))
                os.system("mkdir boot/"+backupOCPath)
                os.system("cp boot/*.qcow2 boot/"+backupOCPath+"/")
                plistFile = open("./boot/mnt/EFI/OC/config.plist","w")
                updatedPlist = plist.replace(bootArgs,bootArgsNew)
                plistFile.write(updatedPlist)
                plistFile.close()
                time.sleep(3)
                clear()
                print("   "+"\n   "+color.BOLD+color.GREEN+"✔  BOOT ARGUMENTS APPLIED"+color.END)
                print("   "+"Boot arguments updated")
                print("   "+"\n   Your changes have been saved.\n   The new boot arguments are ready to use."+color.END)#print(color.BOLD+"\n"+"Profile:"+color.END,"https://github.com/Coopydood")
                print("\n   "+color.BOLD+color.GRAY+"    OLD:"+color.END,bootArgs+color.END)
                #print("     "+color.BOLD+"   ▼")
                print("   "+color.BOLD+color.GREEN+"CURRENT:"+color.END+color.BOLD,bootArgsNew+color.END+"\n\n\n\n\n")
                os.system("./scripts/domtrues/nbdassistant.py -u -q")
                time.sleep(3)
            
            elif detectChoice2 == "2":
                clear()
                enterArgs()
            
            elif detectChoice2 == "B" or detectChoice2 == "b":
                os.system('./scripts/extras/boot-args.py')
            elif detectChoice == "Q" or detectChoice == "q":
                exit
        enterArgs()
    
    elif detectChoice == "M" or detectChoice == "m":
        os.system('./scripts/extras/boot-args.py')

    elif detectChoice == "Q" or detectChoice == "q":
        exit

elif detectChoice == "X" or detectChoice == "x":
    clear()
    print(color.YELLOW+color.BOLD+"\n   ⚠ "+color.END+color.BOLD+"SUPERUSER PRIVILEGES"+color.END+"\n   To mount the OpenCore image,\n   the script needs superuser to continue.\n\n   Press CTRL+C to cancel.\n"+color.END)
    os.system("./scripts/domtrues/nbdassistant.py -m -q")
    # NOTE: IMPLEMENT ERROR CATCH HERE
    clear()
    plistFile = open("./boot/mnt/EFI/OC/config.plist","r")
    plist = plistFile.read()
    plistFile.close()
    plistSplit = plist.split("<key>boot-args</key>",1)[1]
    plistSplit = plistSplit.split("</string>",1)[0]
    bootArgs = plistSplit.split("<string>",1)[1]
    bootArgsNew = "-v keepsyms=1 tlbto_us=0 vti=9"
    print("   "+"\n   "+color.BOLD+"Restore to Default"+color.END)
    print("   "+"Reset OpenCore boot arguments")
    print("   "+"\n   Your boot arguments will be reset to the defaults.\n   EXISTING BOOT ARGUMENTS WILL BE LOST.\n\n   A backup will be made.\n   No other user-made OpenCore modifications will be affected."+color.END)#print(color.BOLD+"\n"+"Profile:"+color.END,"https://github.com/Coopydood")
    print("\n   "+color.BOLD+color.CYAN+"CURRENT:"+color.END+color.BOLD,bootArgs+color.END)
    #print("     "+color.BOLD+"   ▼")
    print("   "+color.BOLD+color.BLUE+"DEFAULT:"+color.END+color.BOLD,bootArgsNew+color.END)
    #print(color.BOLD+"   Repo:"+color.END,"https://github.com/Coopydood/ultimate-macOS-KVM")
    print(color.BOLD+"\n      X. Reset")
    print(color.END+"         Reset the boot arguments to defaults")
    
    #print(color.END+"         Use this option if you already have an XML file.\n         This option lets you import a previously-created XML file\n         into virsh for use with virt-manager.\n")
    print(color.END+"\n      B. Back...")
    #print(color.END+"      ?. Help...")
    print(color.END+"      Q. Exit\n")
    detectChoice2 = str(input(color.BOLD+"Select> "+color.END))

    if detectChoice2 == "X" or detectChoice2 == "x":
        backupOCPath = str(datetime.today().strftime('%d-%m-%Y_%H-%M-%S'))
        os.system("mkdir boot/"+backupOCPath)
        os.system("cp boot/*.qcow2 boot/"+backupOCPath+"/")
        plistFile = open("./boot/mnt/EFI/OC/config.plist","w")
        updatedPlist = plist.replace(bootArgs,bootArgsNew)
        plistFile.write(updatedPlist)
        plistFile.close()
        time.sleep(3)
        clear()
        print("   "+"\n   "+color.BOLD+color.GREEN+"✔  BOOT ARGUMENTS RESET"+color.END)
        print("   "+"Boot arguments reset")
        print("   "+"\n   Your changes have been saved.\n   The original boot arguments are ready to use."+color.END)#print(color.BOLD+"\n"+"Profile:"+color.END,"https://github.com/Coopydood")
        print("\n   "+color.BOLD+color.GRAY+"    OLD:"+color.END,bootArgs+color.END)
        #print("     "+color.BOLD+"   ▼")
        print("   "+color.BOLD+color.GREEN+"CURRENT:"+color.END+color.BOLD,bootArgsNew+color.END+"\n\n\n\n\n")
        os.system("./scripts/domtrues/nbdassistant.py -u -q")
        time.sleep(3)
    
    elif detectChoice2 == "B" or detectChoice2 == "b":
        os.system("./scripts/extras/boot-args.py")
    elif detectChoice == "Q" or detectChoice == "q":
        exit
    
    elif detectChoice == "M" or detectChoice == "m":
        startup()

    elif detectChoice == "Q" or detectChoice == "q":
        exit

elif detectChoice == "?":
    clear()
    print("\n\n   "+color.BOLD+color.GREEN+"✔  OPENING HELP PAGE IN DEFAULT BROWSER"+color.END,"")
    print("   Continue in your browser\n")
    print("\n   I have attempted to open this script's help page in\n   your default browser. Please be patient.\n\n   You will be returned to the last screen in 5 seconds.\n\n\n\n\n")
    os.system('xdg-open https://github.com/Coopydood/ultimate-macOS-KVM/wiki/Boot-Argument-Editor > /dev/null 2>&1')
    time.sleep(6)
    #clear()
    startup()

elif detectChoice == "M" or detectChoice == "m":
    clear()
    os.system("./scripts/extras.py")

elif detectChoice == "Q" or detectChoice == "q":
    exit

else:
    startup()