#!/usr/bin/env python3
# pylint: disable=C0301,C0116,C0103,R0903

# Vendor         : DomTrues
# Provisioned by : Coopydood



# Import Required Modules
import os
import time
from datetime import datetime
# import subprocess
# import re 
# import json
# import sys
import argparse
# import platform


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


# Coopydoopydoo Logs
version = open("./.version")
version = version.read()
enableLog = True
parser = argparse.ArgumentParser("autopilot")
parser.add_argument("--disable-logging", dest="disableLog", help="Disables the logfile",action="store_true")
args = parser.parse_args()
global logTime
logTime = str(datetime.today().strftime('%d-%m-%Y_%H-%M-%S'))
if args.disableLog == True:
    enableLog = False
if enableLog == True: # LOG SUPPORT
    if not os.path.exists("./logs"):
        os.system("mkdir ./logs")
    logTime = str(datetime.today().strftime('%d-%m-%Y_%H-%M-%S'))
    os.system("echo ULTMOS UPTA LOG "+str(datetime.today().strftime('%d-%m-%Y %H:%M:%S'))+" > ./logs/UPTA_RUN_"+logTime+".log")
    os.system("echo ──────────────────────────────────────────────────────────────"+" >> ./logs/UPTA_RUN_"+logTime+".log")
    def cpydLog(logStatus,logMsg,*args):
        logFile = open("./logs/UPTA_RUN_"+logTime+".log","a")
        #if logStatus == "ok":      logStatus = "[ ✔ ]"
        #if logStatus == "info":    logStatus = "[ ✦ ]"
        #if logStatus == "warn":    logStatus = "[ ⚠ ]"
        #if logStatus == "error":   logStatus = "[ ✖ ]"
        #if logStatus == "fatal":   logStatus = "[ ☠ ]"
        #if logStatus == "wait":    logStatus = "[ ➜ ]"
        if logStatus == "ok":      logStatus = "[    OK ]"
        if logStatus == "info":    logStatus = "[  INFO ]"
        if logStatus == "warn":    logStatus = "[  WARN ]"
        if logStatus == "error":   logStatus = "[ ERROR ]"
        if logStatus == "fatal":   logStatus = "[ FATAL ]"
        if logStatus == "wait":    logStatus = "[  WAIT ]"
        entryTime = str(datetime.today().strftime('%H:%M:%S.%f'))
        entryTime = entryTime[:-3]
        entryLine = ("["+entryTime+"]"+str(logStatus)+":  "+str(logMsg)+"\n")
        logFile.write(entryLine)
        logFile.close()
else:
    def cpydLog(logStatus,logMsg,*args):
        None
script = "usb-menu.py"
scriptName = "USB Assistant"
scriptID = "UPTA"
scriptVendor = "DomTrues"
cpydLog("info",("ULTMOS v"+version))
cpydLog("info",(" "))
cpydLog("info",("Name       : "+scriptName))
cpydLog("info",("File       : "+script))
cpydLog("info",("Identifier : "+scriptID))
cpydLog("info",("Vendor     : "+scriptVendor))
cpydLog("info",(" "))
cpydLog("info",("Logging to ./logs/UPTA_RUN_"+logTime+".log"))



# Declare method of clearing the screen the Coopydoopydoo way.
def clear():
   os.system("clear")
   spaces = ""
   i = 0
   terminal_size = os.get_terminal_size()
   while i < terminal_size.lines:
      spaces = spaces + "\n"
      i += 1
   print(spaces)

def center(text: str):
    spaces = ""
    i = 0
    terminal_size = (os.get_terminal_size().columns / 2) - (len(text))
    while i < terminal_size:
        spaces = spaces + " "
        i += 1
    print(spaces + text)



# Declare method of "Press enter to continue", like pause on Windows...
def pause():
   input("   Press [ENTER] to continue...")



'''
This is where the fun begins.
You can thank Gigantech for simultaneously making this easier and harder
for all of us.
'''



# USB things to keep track of
usb_ids: list = []
usb_names: list = []
selected_usb_ids: list = []
qemu_flags: list = []

# Symbol for Lists (because Gigantech got us all fucked up in the first place and now we can't decide on our UI thingy)
symbol: str = "》"



# Main Menu
def preliminary():
   
    # Clear the screen, "the Coopydoopydoo way"
    clear()

    # Global Variables
    global usb_ids, usb_names

    # Logging
    print ("Detecting devices, please wait...")
    # TODO: LOGGING DEVICES BEING DETECTED

    # Get USB IDs
    usb_ids = os.popen("lsusb | sort -k6 -u | cut -b24- | grep -oP \"[0-9a-fA-F]{4}:[0-9a-fA-F]{4}\" | tr '\n' ' '").read().split(" ")
    # Remove the empty thingy
    usb_ids.pop(-1)

    # Get USB Names
    usb_names = os.popen("lsusb | sort -k6 -u | awk '{ for (i = 7; i <= NF; i++) { printf $i \" \" }; printf \"\\n\"}'").read().split("\n")
    # Remove the empty thingy
    usb_names.pop(-1)

    # If the length of either is 0, something has gone horribly, horribly wrong.
    if (len(usb_ids) == 0 or len(usb_names) == 0):
        # TODO: LOGGING SHIT GOING SOUTH
        clear()
        print(f"   \033[91m\033[1m✖ NO USB DEVICES FOUND\033[0m\n")
        print(f"   There were no USB devices detected on your computer.")
        print(f"   How did you even manage that?\n")
        pause()
        clear()
        os.system("python3 ./scripts/extras.py")
        exit()

    # If nothing has gone wrong, move on to phase 1.
    # TODO: LOG AMOUNT OF DEVICES
    phase1()



# Phase 1 - Selecting USB devices
def phase1():
    
    # Global Variables
    global usb_ids, usb_names

    # Local Variables
    user_choice: str = ""

    # Menu Loop
    while (True):

        # Clear the screen, "the Coopydoopydoo way"
        clear() 

        # Menu Text
        print("   Welcome to \033[36m\033[1mUSB Passthrough Assistant\033[0m")
        print("   Created by \033[1mDomTrues\033[0m")
        print("\n   This script simplifies the process of adding \n   your host's USB devices to your boot script.\n")
        print(f"   \033[1mThis script has detected a total of \033[32m{str(len(usb_ids))}\033[0m\033[1m USB devices.\033[0m\n")
        print("   Select an option to continue.\n")
        print("      \033[1m1. Passthrough USB devices\033[0m\n         Select the USB devices you want from\n         a list to add to your script.\n")
        print("      2. Refresh USB devices")
        print("      B. Back...")
        print("      Q. Quit\n")

        # Get User Input
        user_choice = input("\033[1mSelect>\033[0m ")

        # Menu Branching
        if (len(user_choice) == 0 or user_choice == "1"): # Passthrough USB devices
            # Goto Phase 2 and Break
            clear()
            phase2()
            break
        elif (len(user_choice) == 0 or user_choice == "2"): # Refresh USB devices
            # Restart Preliminary and Break
            clear()
            preliminary()
            break
        elif (len(user_choice) == 0 or user_choice.lower() == "b"): # Main Menu
            # Goto Extras and Break
            clear()
            os.system("./scripts/extras.py")
            break
        elif (len(user_choice) == 0 or user_choice.lower() == "q"): # Quit
            # Exit (and break just in case)
            clear()
            exit()
            break



# Phase 2 - User Selects USB Devices
def phase2():

    # Global Variables
    global usb_ids,usb_names,selected_usb_ids,symbol
    
    # Menu Loop
    while (True):

        # Clear the screen, "the Coopydoopydoo way"
        clear()

        print("\n   \033[1mSelect USB devices\033[0m")
        print("   Step 1")
        print("\n   Type in the devices you want by using their associated \n   number on the list below. To deselect a device, type its\n   number to remove it. Once you are finished selecting\n   devices, type \033[37mdone\033[0m to continue onto the next step.")

        # List the unselected USB devices.
        print("\n   \033[1mSELECTED DEVICES\033[0m\n")
        # Python has to be special, fuck me. (R.I.P. for(i = 0; i < sdgasdg; i++))
        if (len(selected_usb_ids) == 0):
            print("\033[37m       None\033[0m")
        else:
            for i in range(len(usb_ids)):
                if (i < 9):
                    if (usb_ids[i] in selected_usb_ids):
                        print(f"       \033[0m{str(i + 1)} {symbol}  {usb_names[i]}\033[0m")
                else:
                    if (usb_ids[i] in selected_usb_ids):
                        print(f"      \033[0m{str(i + 1)} {symbol}  {usb_names[i]}\033[0m")

        # List the unselected USB devices.
        print("\n   \033[1mAVAILABLE DEVICES\033[0m\n")
        # Python has to be special, fuck me. (R.I.P. for(i = 0; i < sdgasdg; i++))
        if (len(selected_usb_ids) == len(usb_ids)):
            print("\033[37m      None\033[0m")
        else:
            for i in range(len(usb_ids)):
                if (i < 9):
                    if (usb_ids[i] not in selected_usb_ids):
                        print(f"       \033[37m{str(i + 1)} {symbol}  {usb_names[i]}\033[0m")
                else:
                    if (usb_ids[i] not in selected_usb_ids):
                        print(f"      \033[37m{str(i + 1)} {symbol}  {usb_names[i]}\033[0m")
        
        # User Selection
        user_choice: str = input("\n\033[1mDevice #> \033[0m")

        # If the user has finished, continue to Phase 3
        if (user_choice == "done"):
            clear()
            phase3()
            break

        # Try to convert the input to an integer
        try:
            int_choice: int = int(user_choice)
            if (int_choice <= 0):
                continue
            if (usb_ids[int_choice - 1] not in selected_usb_ids):
                selected_usb_ids.append(usb_ids[int_choice - 1])
            else:
                selected_usb_ids.remove(usb_ids[int_choice - 1])
        except:
            # If the user is fucked up, just pretend it didn't happen.
            continue

        



# Phase 3 - Adding USB devices to QEMU
def phase3():

    # Global Variables
    global usb_ids,usb_names,selected_usb_ids,qemu_flags
    
    # If no devices were selected, return to the preliminary menu.
    if (len(selected_usb_ids) == 0):
        preliminary()

    # Menu Loop
    while (True):

        clear()

        # Display Menu
        print("\n   \033[1mValidate USB devices\033[0m")
        print("   Step 2")
        print("\n   USB entries have been generated based on your selection.\n   If this looks correct, type \033[37mY\033[0m to continue.\n   If you want to change something, type \033[37mN\033[0m to go back.\n")

        # Generate QEMU flags per device
        for i in range(len(selected_usb_ids)):
            vendor_id: str = usb_ids[i].split(":")[0]
            product_id: str = usb_ids[i].split(":")[1]
            qemu_flags.append(f"-device usb-host,vendorid=0x{vendor_id},productid=0x{product_id}")

        # Display visual flags for QEMU.
        for i in range(len(selected_usb_ids)):
            print(f"   \033[1m{usb_names[usb_ids.index(selected_usb_ids[i])]}\033[0m")
            vendor_id: str = usb_ids[i].split(":")[0]
            product_id: str = usb_ids[i].split(":")[1]
            print(f"      \033[37m{qemu_flags[i]}\033[0m")

        # Get user input
        user_choice: str = input("\n\033[1mY/N> \033[0m")

        # Branching
        if (user_choice.lower() == "n"):
            # Clear the lists and gtfo.
            usb_ids.clear()
            usb_names.clear()
            selected_usb_ids.clear()
            qemu_flags.clear()
            preliminary()
            break
        elif (user_choice.lower() == "y"):
            autoAPSelect()
            exit()
            break

def autoAPSelect():
    clear()
    if os.path.exists("./blobs/user/USR_CFG.apb"):
        apFilePath = open("./blobs/user/USR_CFG.apb")
        apFilePath = apFilePath.read()
        if os.path.exists("./"+apFilePath):
            apFile = open("./"+apFilePath,"r")
            if "APC-RUN" in apFile.read():
                print("\n\n   "+color.BOLD+color.GREEN+"✔ AUTOPILOT CONFIG AUTODETECTED"+color.END,"")
                print("   Valid AutoPilot config found\n")
                print("   An existing boot config file was found in the repo folder and\n   was generated by AutoPilot. It appears to be valid.\n")
                
                print(color.BOLD+"   "+apFile.name+color.END)
                print("\n   Do you want to use this file?\n"+color.END)
                print(color.BOLD+"      1. Add USB devices to detected file")
                print(color.END+"         Adds the generated arguments to this file\n")
                print(color.END+"      2. Select another file...")
                print(color.END+"      Q. Exit\n")
                apFile.close()
                detectChoice2 = str(input(color.BOLD+"Select> "+color.END))

                if detectChoice2 == "1":
                    #apFileR = apFile.read()
                    apFileChosen = 1
                    
                    clear()
                    if apFilePath is not None:
                        
                        print("\n\n   "+color.BOLD+color.BLUE+"⧖ APPLYING..."+color.END,"")
                        print("   Please wait\n")
                        print("   The assistant is now configuring your AutoPilot config file\n   for use with your USB devices.")
                        print(color.BOLD+"\n   This may take a few moments.\n   Your current config will be backed up.\n")
                        time.sleep(2)
                        apFilePathNoExt = apFilePath.replace(".sh","")
                        try:
                            checker = open("./"+apFilePathNoExt+"-noUSB.sh")
                            checker.close()
                        except:
                            os.system("cp ./"+apFilePath+" ./"+apFilePathNoExt+"-noUSB.sh")
                        with open("./"+apFilePath,"r") as file1:
                            apFileM = file1.read()
                            currentDispVal = len(qemu_flags) - 1
                            while currentDispVal >= 0:
                                apFileM = apFileM.replace("#USB_DEV_BEGIN","#USB_DEV_BEGIN\n"+qemu_flags[currentDispVal])
                                currentDispVal -= 1
                            clear()
                            print("\n\n   "+color.BOLD+color.GREEN+"✔ SUCCESS"+color.END,"")
                            print("   QEMU arguments have been added\n")
                            print("   The QEMU argument lines were successfully added to\n   "+color.BOLD+apFilePath+color.END+"\n\n\n\n\n\n\n")
                        file1.close

                        with open("./"+apFilePath,"w") as file:
                            file.write(apFileM)
                        
                        exit()

                if detectChoice2 == "2":
                    clear()
                    manualAPSelect()
                else:
                    clear()
                    manualAPSelect()
            else:
                clear()
                manualAPSelect()
    else:
        clear()
        manualAPSelect()

def manualAPSelect():
    clear()
    print("\n\n   "+color.BOLD+"Select AutoPilot Config File"+color.END,"")
    print("   Input a valid AutoPilot-generated config\n")
    print("   You must use a valid file generated by AutoPilot.\n   Any existing USB args will be kept.\n   AutoPilot-generated config scripts end in .sh")
        
    print(color.BOLD+"\n   Drag the *.sh file onto this window (or type the path) and hit ENTER.\n")
    apFileSelect = str(input(color.BOLD+"AutoPilot Config File> "+color.END))
    clear()
    time.sleep(1)
    if "'" in apFileSelect:
        apFileSelect = apFileSelect.replace("'","")
    if " " in apFileSelect:
        apFileSelect = apFileSelect.replace(" ","")
    if os.path.exists(apFileSelect):
        apFile = open(apFileSelect)
        if "APC-RUN" in apFile.read():
            print("\n\n   "+color.BOLD+color.GREEN+"✔ VALID AUTOPILOT CONFIG"+color.END,"")
            print("   Valid AutoPilot config found\n")
            print("   The file you selected was generated by AutoPilot.\n   It appears to be valid.\n")
            
            print(color.BOLD+"   "+apFile.name+color.END)
            print("\n   Do you want to use this file?\n   It will be copied to the repo folder.\n"+color.END)
            print(color.BOLD+"      1. Add USB devices to this file")
            print(color.END+"         Adds the generated arguments to this file\n")
            print(color.END+"      2. Select another file...")
            print(color.END+"      Q. Exit\n")
            apFile.close()
            detectChoice1 = str(input(color.BOLD+"Select> "+color.END))

            if detectChoice1 == "1":
                apFilePath = apFileSelect
                apFile = open(apFileSelect)
                apFile = apFile.read()
                apFileChosen = 1
                clear()
                #apFileR = apFile.read()
                apFileChosen = 1
                
                clear()
                if apFilePath is not None:
                        
                    print("\n\n   "+color.BOLD+color.BLUE+"⧖ APPLYING..."+color.END,"")
                    print("   Please wait\n")
                    print("   The assistant is now configuring your AutoPilot config file\n   for use with your USB devices.")
                    print(color.BOLD+"\n   This may take a few moments.\n   Your current config will be backed up.\n")
                    time.sleep(2)
                    if apFilePath[0] == "/" and apFilePath[1] == "/":
                        apFilePath = apFilePath.replace("/","",1)
                    if apFilePath[0] == "." and len(apFilePath) > 10:
                        apFilePath = apFilePath.replace(".","",1)
                    apFilePathNoExt = apFilePath.replace(".sh","")
                    os.system("cp "+apFilePath+" "+apFilePathNoExt+"-noUSB.sh")
                    with open(apFilePath,"r") as file1:
                        apFileM = file1.read()
                        '''
                        currentDispVal = len(usb_ids)
                        for y in range(len(usb_ids)):
                            
                            currentDispVal = currentDispVal - 1
                            devLineF = str(dev[currentDispVal])
                            apFileM = apFileM.replace("#VFIO_DEV_BEGIN","#VFIO_DEV_BEGIN\n"+devLineF)
                            apFileM = apFileM.replace("#-vga qxl","-vga none")
                            #apFileM = apFileM.replace("-monitor stdio","-monitor none")
                            apFileM = apFileM.replace("#-display none","-display none")
                            apFileM = apFileM.replace("REQUIRES_SUDO=0","REQUIRES_SUDO=1")
                            apFileM = apFileM.replace("VFIO_PTA=0","VFIO_PTA=1")
                            apFileM = apFileM.replace("-device qxl-vga,vgamem_mb=128,vram_size_mb=128    ","#-device qxl-vga,vgamem_mb=128,vram_size_mb=128   # DISABLED BY VFIO-PCI PASSTHROUGH ASSISTANT")
                            os.system("cp resources/ovmf/OVMF_CODE.fd ovmf/OVMF_CODE.fd")
                            os.system("cp resources/ovmf/OVMF_VARS_PT.fd ovmf/OVMF_VARS.fd")
                        '''    
                        currentDispVal = len(qemu_flags) - 1
                        while currentDispVal >= 0:
                            apFileM = apFileM.replace("#USB_DEV_BEGIN","#USB_DEV_BEGIN\n"+qemu_flags[currentDispVal])
                            currentDispVal -= 1
                        clear()
                        print("\n\n   "+color.BOLD+color.GREEN+"✔ SUCCESS"+color.END,"")
                        print("   QEMU arguments have been added\n")
                        print("   The QEMU argument lines were successfully added to\n   "+color.BOLD+apFilePath+color.END+"\n\n\n\n\n\n\n")

                    file1.close

                    with open(apFilePath,"w") as file:
                        file.write(apFileM)
                    
            if detectChoice1 == "2":
                clear()
                manualAPSelect()
    else:
        print("\n\n   "+color.BOLD+color.RED+"✖ INVALID AUTOPILOT CONFIG"+color.END,"")
        print("   Your file was not a valid AutoPilot config\n")
        print("   You must use a valid file generated by AutoPilot.\n   Any existing VFIO-based args will be kept.\n   AutoPilot-generated config scripts end in .sh")
            
        print(color.BOLD+"\n   You will be returned to the input screen.\n")
        time.sleep(8)
        clear()
        manualAPSelect()

# Start Script
preliminary()