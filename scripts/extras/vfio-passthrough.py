#!/usr/bin/env python3
# pylint: disable=C0301,C0116,C0103,R0903

"""
This script was created by Coopydood as part of the ultimate-macOS-KVM project.

https://github.com/user/Coopydood
https://github.com/Coopydood/ultimate-macOS-KVM
Signature: 4CD28348A3DD016F

"""

# This script should NOT be run directly, but instead from the main "setup.py" script.


import os
import time
import subprocess
import re 
import json
import sys
import argparse

sys.path.insert(0, 'scripts')

detectChoice = 1
latestOSName = "Ventura"
latestOSVer = "13"
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

def startup():
    global detectChoice
    print("\n\n   Welcome to"+color.BOLD+color.PURPLE,"VFIO-PCI Passthrough Assistant"+color.END,"")
    print("   Created by",color.BOLD+"Coopydood\n"+color.END)
    print("   This script will attempt to guide you through the process\n   of passing through your host's physical PCI devices for use\n   within the guest. This is advanced and requires patience. Seriously.\n")
    #print(color.BOLD+"\n"+"Profile:"+color.END,"https://github.com/Coopydood")
    #print(color.BOLD+"   Repo:"+color.END,"https://github.com/Coopydood/ultimate-macOS-KVM")
    print("   Select an option to continue.")
    print(color.BOLD+"\n      1. Start")
    print(color.END+"         Continue to requirements list and prepare your sanity\n")
    print(color.END+"      2. Check GPU compatibility")
    print(color.END+"      B. Back...")
    print(color.END+"      Q. Exit\n")
    detectChoice = str(input(color.BOLD+"Select> "+color.END))

       


def clear(): print("\n" * 150)



def stage2():
    clear()
    print("Detecting devices, please wait...")
    time.sleep(0.5)

    output_stream = os.popen('lspci -k | grep -B 2 "vfio-pci"')
    vgaGrep = output_stream.read()

    output_stream1 = os.popen('lspci -k | awk \'/vfio-pci/ {print a} {a=b;b=$0}\'')
    vgaGrepIDOnly = output_stream1.read()

    vfioCount = vgaGrep.count("vfio-pci")
    #vfioCount = 0 #<--- uncomment to force-disable detection for error debugging
    clear()
    if vfioCount >= 1:
        print("\n\n   "+color.BOLD+color.GREEN+"VFIO-PCI Devices Detected!"+color.END,"")
        print("   The following devices are ready for passthrough\n")
        print("   The devices listed below have been correctly configured to use\n   VFIO-PCI and are ready for full passthrough.\n")

        outputStyle = ("\n   "+vgaGrep)
        outputStyle = outputStyle.replace("--\n","\n   ")
        outputStyle = outputStyle.replace("Audio device: ","")
        outputStyle = outputStyle.replace("Multimedia controller: ","")
        outputStyle = outputStyle.replace("VGA compatible controller: ","")

        print(outputStyle)
        print("   You can now choose how many virtual PCI slots you need.\n   Each entry you want to use needs its own slot. Type the\n   number of slots you want below now, or \"-1\" to exit.\n"+color.END)

        slotCount = int(input(color.BOLD+"Value> "+color.END))
        clear()

        global slotContainer
        slotContainer = []

        #print(slotContainer)

        for x in range(slotCount):
            #global slotContainer
            xF = str(x)

         
                

            clear()
            print("\n\n   "+color.BOLD+"Assign Device to Slot #"+xF+color.END,"")
            print("   Choose a listed device to assign\n")
            print("   Type the 5-digit ID now. Do NOT include punctuation.\n   Example: 04:00.1 -> 04001")

            outputStyle = ("\n"+vgaGrepIDOnly)
            outputStyle = outputStyle.replace("\n","\n   ")
            outputStyle = outputStyle.replace("Audio device: ","")
            outputStyle = outputStyle.replace("Multimedia controller: ","")
            outputStyle = outputStyle.replace("VGA compatible controller: ","")

            print(outputStyle)
            print("   You should only enter one entry consisting of 5 digits.\n"+color.END)
            thisSlot = str(input(color.BOLD+"Assign ID to Slot>  "+color.END))
            slotContainer.append(thisSlot)

            #print(slotContainer)
        
        clear()
        print("\n\n   "+color.BOLD+"Slot Configuration Summary",color.END,"")
        print("   Check your slot allocations\n")
        print("   The slots listed below will be used with their assigned devices.\n   For each, you'll be asked what kind of device it is.\n")
        slotContainerPT = []
        currentSlotEdit = -1
        for i in slotContainer:
            currentSlotEdit = currentSlotEdit + 1
            editValue = str(slotContainer[currentSlotEdit])
            #print(editValue)
            editValue = editValue.replace(editValue[:2],(editValue[:2]+":"),1)
            editValue = editValue.replace(editValue[:5],(editValue[:5]+"."),1)
            #print(editValue)


            slotContainerPT.append(editValue)
            #print("slotContainerPT is now",slotContainerPT)


        currentSlotDisplay = -1
        
        for y in range(slotCount):

            currentSlotDisplay = currentSlotDisplay + 1
            print("   ",color.BOLD+"SLOT #"+str(y)+":",color.END+slotContainerPT[currentSlotDisplay])
        print("\n   Continue when you're ready, or you can change slots and IDs.\n"+color.END)

        print(color.BOLD+"\n      1. Continue")
        print(color.END+"      2. Reconfigure...")
        print(color.END+"      Q. Exit\n")
        detectChoice1 = str(input(color.BOLD+"Select> "+color.END))
        if detectChoice1 == "1":
            stage3()
        elif detectChoice1 == "2":
            stage2()
        elif detectChoice1 == "q" or detectChoice1 == "Q":
            exit
        
    
    
    
    else:
        print("\n\n   "+color.BOLD+color.RED+"No VFIO-PCI Devices Found"+color.END,"")
        print("   There are no devices ready for passthrough\n")
        print("   No devices have been configured for use with VFIO-PCI. You must \n   consult the guide on how to do this. Until then, this\n   tool can't be used just yet.")
        #print("\n")
        #print("   \n   Type the VFIO-ID of the device now. (XX:XX.XX)\n"+color.END)
        print(color.BOLD+"\n      1. Try again")
        print(color.END+"      B. Back...")
        print(color.END+"      Q. Exit\n")
        detectChoice1 = str(input(color.BOLD+"Select> "+color.END))
        if detectChoice1 == "1":
            stage2()
        elif detectChoice1 == "B" or detectChoice1 == "b":
            stage1()
        elif detectChoice1 == "q" or detectChoice1 == "Q":
            exit


def stage1():
    clear()
    
    print("\n\n   "+color.BOLD+"System Requirements"+color.END,"")
    print("   Check your system meets this list\n")
    print("   Okay, so you're committed. Fair enough. But first, you need to make\n   sure your system is ready to even begin this nonsense.\n")
    #print(color.BOLD+"\n"+"Profile:"+color.END,"https://github.com/Coopydood")
    #print(color.BOLD+"   Repo:"+color.END,"https://github.com/Coopydood/ultimate-macOS-KVM")
    print(color.BOLD+"   1. Modern hardware"+color.END)
    print("      You must have a fairly modern PC to do this.")
    print(color.BOLD+"   2. BIOS configured correctly"+color.END)
    print("      Virtualisation and IOMMU *MUST* be enabled.")
    print(color.BOLD+"   3. UEFI"+color.END)
    print("      ...and more UEFI. Everything must be using it.")
    print(color.BOLD+"   4. vfio-pci kernel driver stubbing"+color.END)
    print("      The PCI devices in question must be stubbed correctly.")
    print(color.BOLD+"   5. Unwavering patience"+color.END)
    print("      You NEED to expect a LOT of trial and error. No I'm serious.")
    print(color.BOLD+"\n      1. Continue and detect devices")
    print(color.END+"      B. Back...")
    print(color.END+"      Q. Exit\n")
    detectChoice1 = str(input(color.BOLD+"Select> "+color.END))
    if detectChoice1 == "1":
        stage2()
    elif detectChoice1 == "B" or detectChoice1 == "b":
        startup()
    elif detectChoice1 == "q" or detectChoice1 == "Q":
        exit


startup()


if detectChoice == "1":
    clear()
    time.sleep(1)
    stage1()
elif detectChoice == "2":
    clear()
    os.system('./scripts/gpu-check.py')

elif detectChoice == "B" or detectChoice == "b":
    os.system('./scripts/extras.py')
elif detectChoice == "q" or detectChoice == "Q":
    exit