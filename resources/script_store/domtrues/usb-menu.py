#!/usr/bin/env python3
# pylint: disable=C0301,C0116,C0103,R0903

# Vendor         : DomTrues
# Provisioned by : Coopydood



# Import Required Modules
import os
# import time
from datetime import datetime
# import subprocess
# import re 
# import json
# import sys
import argparse
# import platform



# Coopydoopydoo Logs
version = open("./.version")
version = version.read()
enableLog = True
parser = argparse.ArgumentParser("autopilot")
parser.add_argument("--disable-logging", dest="disableLog", help="Disables the logfile",action="store_true")
parser.add_argument("-m","--mount", dest="mount", help="Immediately mount detected OC image",action="store_true")
parser.add_argument("-u","--unmount", dest="unmount", help="Immediately unmount detected OC image",action="store_true")
parser.add_argument("-q","--quiet", dest="quiet", help="Don't print any verbose information",action="store_true")
args = parser.parse_args()
global logTime
logTime = str(datetime.today().strftime('%d-%m-%Y_%H-%M-%S'))
if args.disableLog == True:
    enableLog = False
if enableLog == True: # LOG SUPPORT
    if not os.path.exists("./logs"):
        os.system("mkdir ./logs")
    logTime = str(datetime.today().strftime('%d-%m-%Y_%H-%M-%S'))
    os.system("echo ULTMOS DTUM LOG "+str(datetime.today().strftime('%d-%m-%Y %H:%M:%S'))+" > ./logs/DTUM_RUN_"+logTime+".log")
    os.system("echo ──────────────────────────────────────────────────────────────"+" >> ./logs/DTUM_RUN_"+logTime+".log")
    def cpydLog(logStatus,logMsg,*args):
        logFile = open("./logs/DTGE_RUN_"+logTime+".log","a")
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
scriptName = "USB Menu"
scriptID = "DTUM"
scriptVendor = "DomTrues"
cpydLog("info",("ULTMOS v"+version))
cpydLog("info",(" "))
cpydLog("info",("Name       : "+scriptName))
cpydLog("info",("File       : "+script))
cpydLog("info",("Identifier : "+scriptID))
cpydLog("info",("Vendor     : "+scriptVendor))
cpydLog("info",(" "))
cpydLog("info",("Logging to ./logs/DTYN_RUN_"+logTime+".log"))



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
        print(f"   \033[91m\033[1mSHIT A BRICK.\033[0m\n")
        print(f"   No, seriously. Your computer is a literal brick. Call your friendly")
        print(f"   neighborhood tech support scammer, perhaps?\n")
        print(f"   I legitimately don't even know how you've even got here, I hope it's")
        print(f"   because you modified the script, otherwise, your USB situation is fucked.\n")
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
        print("\n   This script abstracts the process of adding your host's\n   USB devices to your ULTMOS KVM in an attempt to simplify\n   the end user experience. If you made it this far, your")
        print("   computer is more mentally sound than a sleep-deprived\n   cabbage, congratulations.\n")
        print(f"   \033[1mThis script has detected a total of \033[36m{str(len(usb_ids))}\033[0m\033[1m USB devices.\033[0m\n")
        print("   Select an option to continue.\n")
        print("      \033[1m1. Passthrough USB devices\033[0m\n         Select the USB devices you want from\n         a list to load into QEMU.\n")
        print("      2. Refresh USB devices")
        print("      M. Main Menu")
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
        elif (len(user_choice) == 0 or user_choice.lower() == "m"): # Main Menu
            # Goto Extras and Break
            clear()
            os.system("python3 ./scripts/extras.py")
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
        print("\n   Type in the devices you want by their associated number on\n   the list below. If you added a device by mistake, type its\n   number to take it off. Once you are finished with selecting\n   devices, type \033[37mdone\033[0m and you will continue onto the next step.")

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
        print("\n   QEMU flags have been generated based on your devices selected.\n   If these are correct, type \033[37mY\033[0m to add them to your QEMU config.\n   If there is an inconsistency, or you've changed your mind, you\n   can type \033[37mN\033[0m to return.\n")

        # Generate QEMU flags per device
        for i in range(len(selected_usb_ids)):
            vendor_id: str = usb_ids[i].split(":")[0]
            product_id: str = usb_ids[i].split(":")[1]
            qemu_flags.append(f"-device usb-host,vendorid=0x{vendor_id},productid=0x{product_id}")

        # Display visual flags for QEMU.
        for i in range(len(selected_usb_ids)):
            print(f"   {usb_names[usb_ids.index(selected_usb_ids[i])]}")
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
        elif (user_choice.lower() == "y"):
            # TODO: implement appending flags
            clear()
            for i in range(len(qemu_flags)):
                print(f"\033[37m{qemu_flags[i]}\033[0m")
            print("")
            exit()
            break


# Start Script
preliminary()