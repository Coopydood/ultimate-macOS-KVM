#!/usr/bin/env python3
# pylint: disable=C0301,C0116,C0103,R0903

# Vendor         : Hyperchromiac and Coopydood
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
    os.system("echo ULTMOS VPTA LOG "+str(datetime.today().strftime('%d-%m-%Y %H:%M:%S'))+" > ./logs/VPTA_RUN_"+logTime+".log")
    os.system("echo ──────────────────────────────────────────────────────────────"+" >> ./logs/VPTA_RUN_"+logTime+".log")
    def cpydLog(logStatus,logMsg,*args):
        logFile = open("./logs/VPTA_RUN_"+logTime+".log","a")
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
script = "vfio-passthrough.py"
scriptName = "VFIO Passthrough Assistant"
scriptID = "VPTA"
scriptVendor = "Hyperchromiac, Coopydood"
cpydLog("info",("ULTMOS v"+version))
cpydLog("info",(" "))
cpydLog("info",("Name       : "+scriptName))
cpydLog("info",("File       : "+script))
cpydLog("info",("Identifier : "+scriptID))
cpydLog("info",("Vendor     : "+scriptVendor))
cpydLog("info",(" "))
cpydLog("info",("Logging to ./logs/VPTA_RUN_"+logTime+".log"))



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
   input("   Press [ENTER] to continue...\n")



'''
This is where the fun begins.
You can thank Gigantech for simultaneously making this easier and harder
for all of us.
'''



# VFIO-PCI things to keep track of
vfio_ids: list = []
pci_ids: list = []
gpu_ids: list = []
vfio_names: list = []
selected_vfio_ids: list = []
qemu_flags: list = []
gpuDetected = 0
naviDetected = 0
# Symbol for Lists (because Gigantech got us all f*cked up in the first place and now we can't decide on our UI thingy)
symbol: str = "》"

def usbOffer():
    time.sleep(3)
    clear()
    print("\n\n   "+color.BOLD+color.YELLOW+"⚠  VIRTUAL INPUT DEVICES REMOVED"+color.END,"")
    print("   Virtual monitor was removed\n")
    print("   The assistant has detected that you "+color.BOLD+"passed through a GPU."+color.END+"\n   To accommodate this, the virtual guest monitor had to be\n   removed. This also means you can't use the virtual input\n   devices that utilise the monitor.\n\n   To send input to the guest, you may want to passthrough\n   USB input devices attached to your host. This project\n   can do this for you. You don't need this if you also\n   passed through a host USB controller.\n")
    #print(color.YELLOW+color.BOLD+"\n   ⚠ "+color.END+color.BOLD+"WARNING"+color.END+"\n   This action requires superuser permissions.\n"+color.END)
    print(color.BOLD+"      1. Run USB Passthrough Assistant"+color.YELLOW,""+color.END)
    print(color.END+"         Starts the USB passthrough assistant\n")
    print(color.END+"      2. Skip and Exit\n")
    detectChoice4 = str(input(color.BOLD+"Select> "+color.END))

    if detectChoice4 == "1":
        clear()
        os.system('./scripts/hyperchromiac/usb-passthrough.py')
    elif detectChoice4 == "2":
        clear()
        exit
    else:
        usbOffer()
        
# Main Menu
def preliminary():
   
    # Clear the screen, "the Coopydoopydoo way"
    clear()

    # Global Variables
    global vfio_ids, vfio_names, pci_ids, gpu_ids

    # Logging
    print (color.BOLD+"Detecting devices, please wait...")
    print(color.END+"\n  "+color.YELLOW+"⚠ "+color.END+" If you have been stuck on this screen for\n     at least 30 seconds, make sure the devices\n     are not currently in use by the system.")
    # TODO: LOGGING DEVICES BEING DETECTED
    cpydLog("wait", "Detecting VFIO-PCI devices...")

    # Get VFIO-PCI IDs      # why is dom so good at awk???
    vfio_ids = os.popen("lspci -nnk | grep -B2 \"vfio-pci\" | grep -P \"[0-9a-fA-F]{2}:[0-9a-fA-F]{2}\.[0-9A-Fa-f]\" | grep -oP \"[0-9A-Fa-f]{4}:[0-9A-Fa-f]{4}\" | sort -u | tr '\n' ' '").read().split(" ")
    # Remove the empty thingy
    vfio_ids.pop(-1)

    # Get PCI IDs
    pci_ids = os.popen("lspci -nnk | grep -B2 \"vfio-pci\" | grep -P \"[0-9a-fA-F]{2}:[0-9a-fA-F]{2}\.[0-9A-Fa-f]\" | awk '{print $1}' | sort -u | tr '\n' ' '").read().split(" ")
    # Remove the empty thingy
    pci_ids.pop(-1)

    # Get GPU IDs
    gpu_ids = os.popen("lspci -nnk | grep -B2 \"vfio-pci\" | grep \"VGA compatible controller\" | grep -P \"[0-9a-fA-F]{2}:[0-9a-fA-F]{2}\.[0-9A-Fa-f]\" | awk '{print $1}' | sort -u | tr '\n' ' '").read().split(" ")
    # Remove the empty thingy
    gpu_ids.pop(-1)

    # Get PCI Names
    vfio_names = os.popen("lspci -nnk | grep -B2 \"vfio-pci\" | grep -P \"[0-9a-fA-F]{2}:[0-9a-fA-F]{2}\.[0-9A-Fa-f]\" | sort -u | sed -E 's/[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}\.[0-9A-Fa-f] ((\w|-)+( )?)* \[[0-9A-Fa-f]*\]: //' | sed -E 's/\[[0-9A-Fa-f]{4}:[0-9A-Fa-f]{4}\]( \(.*\))?//' | sed 's/Advanced Micro Devices, Inc. \[AMD\/ATI\] //g' | tr '\n' '@'").read().split("@")
    # Remove the empty thingy
    vfio_names.pop(-1)

    # If the length of either is 0, something has gone horribly, horribly wrong.
    if (len(vfio_ids) == 0 or len(vfio_names) == 0 or len(pci_ids) == 0):
        # TODO: LOGGING SHIT GOING SOUTH
        clear()
        print(f"   \033[91m\033[1m✖ NO VFIO-PCI DEVICES FOUND\033[0m\n")
        print(f"   The script couldn't find any stubbed PCI devices")
        print(f"   to use with VFIO. Check your boot arguments!!!\n")
        cpydLog("fatal", "User's machine does not have any stubbed VFIO-PCI devices.")
        pause()
        clear()
        os.system("./scripts/vfio-menu.py")
        exit()

    # If nothing has gone wrong, move on to phase 1.
    # TODO: LOG AMOUNT OF DEVICES
    cpydLog("info", f"Detected {len(vfio_ids)} VFIO-PCI devices")
    phase1()



# Phase 1 - Selecting VFIO-PCI devices
def phase1():
    
    # Global Variables
    global vfio_ids, vfio_names, pci_ids

    # Local Variables
    user_choice: str = ""

    # Menu Loop
    while (True):

        # Clear the screen, "the Coopydoopydoo way"
        clear() 
        cpydLog("wait", "Main Menu >> Awaiting input from user")

        # Menu Text
        print(f"   {color.PURPLE}\033[1mVFIO-PCI PASSTHROUGH ASSISTANT\033[0m")
        print("   by \033[1mHyperchromiac\033[0m and \033[1mCoopydood\033[0m")
        print("\n   This script simplifies the process of adding your host's\n   stubbed VFIO devices to your boot script in an attempt to \n   simplify the end user experience.")
        print(f"\n   \033[1mDetected a total of {color.GREEN}{str(len(vfio_ids))}\033[0m\033[1m VFIO-PCI devices.\033[0m\n")
        print("   Select an option to continue.\n")
        print("      \033[1m1. Passthrough VFIO-PCI devices\033[0m\n         Select the stubbed PCI devices you want from\n         a list to add to your script.\n")
        #print("      2. Refresh VFIO-PCI devices")
        print("      M. Main Menu")
        print("      Q. Quit\n")

        # Get User Input
        user_choice = input("\033[1mSelect>\033[0m ")

        # Menu Branching
        if (len(user_choice) == 0 or user_choice == "1"): # Passthrough VFIO-PCI devices
            # Goto Phase 2 and Break
            clear()
            cpydLog("info", "User has selected 'Passthrough VFIO-PCI devices'")
            phase2()
            break
        elif (len(user_choice) == 0 or user_choice == "2"): # Refresh VFIO-PCI devices
            # Restart Preliminary and Break
            clear()
            cpydLog("info", "User has selected 'Refresh VFIO-PCI devices'")
            preliminary()
            break
        elif (len(user_choice) == 0 or user_choice.lower() == "m"): # Main Menu
            # Goto Extras and Break
            clear()
            cpydLog("info", "User has selected 'Main Menu'")
            os.system("python3 ./scripts/extras.py")
            break
        elif (len(user_choice) == 0 or user_choice.lower() == "q"): # Quit
            # Exit (and break just in case)
            clear()
            cpydLog("info", "User has selected 'Quit'")
            exit()
            break



# Phase 2 - User Selects VFIO-PCI Devices
def phase2():

    # Global Variables
    global vfio_ids,vfio_names,selected_vfio_ids,symbol,pci_ids
    
    # Menu Loop
    while (True):

        # Clear the screen, "the Coopydoopydoo way"
        clear()
        cpydLog("wait", "Select VFIO-PCI devices >> Awaiting input from user")

        print("\n   \033[1mSelect VFIO-PCI devices\033[0m")
        print("   Step 1")
        print("\n   Type in the devices you want by using their associated \n   number on the list below. To deselect a device, type its\n   number to remove it. Once you are finished selecting\n   devices, type  \033[1mdone\033[0m  to continue onto the next step.")

        # List the unselected VFIO-PCI devices.
        print("\n   \033[1mSELECTED DEVICES\033[0m\n")
        # Python has to be special, f*ck me. (R.I.P. for(i = 0; i < sdgasdg; i++))
        if (len(selected_vfio_ids) == 0):
            print("\033[37m       None\033[0m")
        else:
            for i in range(len(pci_ids)):
                if (i < 9):
                    if (pci_ids[i] in selected_vfio_ids):
                        print(f"       \033[0m{str(i + 1)} {symbol}{pci_ids[i]} {symbol}{vfio_names[i]}\033[0m")
                else:
                    if (pci_ids[i] in selected_vfio_ids):
                        print(f"      \033[0m{str(i + 1)} {symbol}{pci_ids[i]} {symbol}{vfio_names[i]}\033[0m")

        # List the unselected VFIO-PCI devices.
        print("\n   \033[1mAVAILABLE DEVICES\033[0m\n")
        # Python has to be special, f*ck me. (R.I.P. for(i = 0; i < sdgasdg; i++))
        if (len(selected_vfio_ids) == len(pci_ids)):
            print("\033[37m      None\033[0m")
        else:
            for i in range(len(pci_ids)):
                if (i < 9):
                    if (pci_ids[i] not in selected_vfio_ids):
                        print(f"       \033[37m{str(i + 1)} {symbol}{pci_ids[i]} {symbol}{vfio_names[i]}\033[0m")
                else:
                    if (pci_ids[i] not in selected_vfio_ids):
                        print(f"      \033[37m{str(i + 1)} {symbol}{pci_ids[i]} {symbol}{vfio_names[i]}\033[0m")
        
        # User Selection
        user_choice: str = input("\n\033[1mDevice #> \033[0m")

        # If the user has finished, continue to Phase 3
        if (user_choice == "done"):
            clear()
            cpydLog("info", "User has finished selecting VFIO-PCI devices")
            phase3()
            break

        # Try to convert the input to an integer
        try:
            int_choice: int = int(user_choice)
            if (int_choice <= 0):
                continue
            if (pci_ids[int_choice - 1] not in selected_vfio_ids):
                selected_vfio_ids.append(pci_ids[int_choice - 1])
                cpydLog("info", f"User has selected ID {pci_ids[int_choice - 1]}")
            else:
                selected_vfio_ids.remove(pci_ids[int_choice - 1])
                cpydLog("info", f"User has deselected ID {pci_ids[int_choice - 1]}")
        except:
            # If the user is f*cked up, just pretend it didn't happen.
            continue

        



# Phase 3 - Adding VFIO-PCI devices to QEMU
def phase3():

    # Global Variables
    global vfio_ids,vfio_names,selected_vfio_ids,qemu_flags,pci_ids,naviDetected,gpuDetected
    
    # If no devices were selected, return to the preliminary menu.
    if (len(selected_vfio_ids) == 0):
        cpydLog("info", f"No devices selected, returning to original menu...")
        preliminary()

    cpydLog("info", f"{len(gpu_ids)} GPU detected." if len(gpu_ids) == 1 else f"{len(gpu_ids)} GPUs detected.")

    # Generate QEMU flags per device
    for i in range(len(selected_vfio_ids)):
        if selected_vfio_ids[i] in gpu_ids:
            if "Navi" in vfio_names[pci_ids.index(selected_vfio_ids[i])]:
                naviDetected = 1
            else:
                naviDetected = 0
            gpuDetected = 1
            clear()
            print(f"   {color.BOLD}{color.BLUE}❖  GPU DETECTED{color.END}")
            print(f"   VBIOS ROM file selection{color.END}\n")
            print(f"   {color.BOLD}{vfio_names[pci_ids.index(selected_vfio_ids[i])]}{color.END}\n")
            print(f"   Some GPUs need a romfile to function in a VM, others do not.\n   Please specify the direct path to a VBIOS romfile below,\n   or type \"skip\" if you don't need one.")
            cpydLog("wait", f"Awaiting for user input on GPU romfile for {selected_vfio_ids[i]}")
            user_input: str = input(f"{color.BOLD}\nAbsolute Path of VBIOS>{color.END} ")
            if (user_input == "" or user_input == None):
                qemu_flags.append(f"-device vfio-pci,host=\"{selected_vfio_ids[i]}\",multifunction=on,bus=pcie.0")
                cpydLog("info", f"User has opted out of selecting a romfile")
            if (user_input != "skip"):
                os.system(f"cp {user_input} ./roms/")
                filename = user_input.split("/")[-1]
                cpydLog("info", f"User has selected a romfile from {user_input}")
                qemu_flags.append(f"-device vfio-pci,host=\"{selected_vfio_ids[i]}\",romfile=\"./roms/{filename}\",multifunction=on,bus=pcie.0")
            else:
                cpydLog("info", f"User has opted out of selecting a romfile")
                qemu_flags.append(f"-device vfio-pci,host=\"{selected_vfio_ids[i]}\",multifunction=on,bus=pcie.0")
        else:
            qemu_flags.append(f"-device vfio-pci,host=\"{selected_vfio_ids[i]}\",bus=pcie.0")
    if naviDetected == 1:
        clear()
        print("\n\n   "+color.BOLD+color.YELLOW+"⚠  BOOT PATCH AVAILABLE"+color.END,"")
        print("   You may need to apply a fix to boot macOS\n")
        print("   The assistant has detected that you may have a"+color.BOLD+" Navi-based"+color.END+" GPU. \n   A patch is available to fix the macOS boot process. I can add\n   this patch for you automatically just now, or you can do it\n   later using the macOS Boot Argument Assistant.")
        print(color.YELLOW+color.BOLD+"\n   ⚠ "+color.END+color.BOLD+"WARNING"+color.END+"\n   This action requires superuser permissions.\n"+color.END)
        print(color.BOLD+"      1. Apply Patch"+color.YELLOW,"⚠"+color.END)
        print(color.END+"         Mounts your OpenCore image and applies\n         the patch automatically\n")
        print(color.END+"      2. Skip\n")
        detectChoice5 = str(input(color.BOLD+"Select> "+color.END))

        if detectChoice5 == "1":
            os.system("./scripts/extras/boot-args.py --autopatch \"navi\"")
        else:
            None

    cpydLog("info", f"Validate VFIO-PCI devices >> User has selected a total of {len(selected_vfio_ids)} VFIO-PCI devices")

    # Menu Loop
    while (True):

        clear()
        cpydLog("wait", f"Validate VFIO-PCI devices >> Awaiting input from user...")

        # Display Menu
        print("\n   \033[1mValidate VFIO-PCI devices\033[0m")
        print("   Step 2")
        print("\n   VFIO-PCI entries have been generated based on your selection.\n   Does this look correct?\n")

        # Display visual flags for QEMU.
        for i in range(len(selected_vfio_ids)):
            print(f"\033[1m   {selected_vfio_ids[i]} {vfio_names[pci_ids.index(selected_vfio_ids[i])]}\n\033[0m      {qemu_flags[i]}")

        # Get user input
        user_choice: str = input("\n\033[1mY/N> \033[0m")

        # Branching
        if (user_choice.lower() == "n"):
            # Clear the lists and gtfo.
            vfio_ids.clear()
            pci_ids.clear()
            vfio_names.clear()
            selected_vfio_ids.clear()
            qemu_flags.clear()
            cpydLog("info", f"User has opted to not follow through with their current VFIO-PCI devices")
            preliminary()
            break
        elif (user_choice.lower() == "y"):
            # TODO: implement appending flags
            cpydLog("info", f"User has opted to follow through with their current VFIO-PCI devices")
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
                print(color.BOLD+"      1. Add VFIO-PCI devices to detected file")
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
                        print("   The assistant is now configuring your AutoPilot config file\n   for use with your VFIO-PCI devices.")
                        print(color.BOLD+"\n   This may take a few moments.\n   Your current config will be backed up.\n")
                        time.sleep(2)
                        apFilePathNoExt = apFilePath.replace(".sh","")
                        try:
                            checker = open("./"+apFilePathNoExt+"-noPT.sh")
                            checker.close()
                        except:
                            os.system("cp ./"+apFilePath+" ./"+apFilePathNoExt+"-noPT.sh")
                        with open("./"+apFilePath,"r") as file1:
                            apFileM = file1.read()
                            currentDispVal = len(qemu_flags) - 1
                            while currentDispVal >= 0:
                                apFileM = apFileM.replace("#VFIO_DEV_BEGIN","#VFIO_DEV_BEGIN\n"+qemu_flags[currentDispVal])
                                currentDispVal -= 1
                            apFileM = apFileM.replace("#-vga qxl","-vga none")
                            #apFileM = apFileM.replace("-monitor stdio","-monitor none")
                            apFileM = apFileM.replace("#-display none","-display none")
                            apFileM = apFileM.replace("REQUIRES_SUDO=0","REQUIRES_SUDO=1")
                            apFileM = apFileM.replace("VFIO_PTA=0","VFIO_PTA=1")

                            totalVD = apFileM.split("VFIO_DEVICES=",1)[1]
                            totalVD = totalVD[0:1]

                            totalVD = int(totalVD)

                            currentAmount = totalVD

                            newAmount = len(selected_vfio_ids)

                            totalVD = int(newAmount) + currentAmount

                            apFileM = apFileM.replace("VFIO_DEVICES="+str(currentAmount),"VFIO_DEVICES="+str(totalVD))
                            
                            blob = open("./blobs/user/USR_VFIO_DEVICES.apb","w")
                            blob.write(str(totalVD))
                            blob.close()

                            apFileM = apFileM.replace("-device qxl-vga,vgamem_mb=128,vram_size_mb=128    ","#-device qxl-vga,vgamem_mb=128,vram_size_mb=128   # DISABLED BY VFIO-PCI PASSTHROUGH ASSISTANT")
                            apFileM = apFileM.replace("/OVMF_VARS.fd","/OVMF_VARS_PT.fd")
                            os.system("cp resources/ovmf/OVMF_CODE.fd ovmf/OVMF_CODE.fd")
                            os.system("cp resources/ovmf/OVMF_VARS.fd ovmf/OVMF_VARS.fd")
                            os.system("cp resources/ovmf/OVMF_VARS_PT.fd ovmf/OVMF_VARS_PT.fd")
                            clear()
                            print("\n\n   "+color.BOLD+color.GREEN+"✔ SUCCESS"+color.END,"")
                            print("   QEMU arguments have been added\n")
                            print("   The QEMU argument lines were successfully added to\n   "+color.BOLD+apFilePath+color.END+"\n\n\n\n\n\n\n")
                        file1.close

                        with open("./"+apFilePath,"w") as file:
                            file.write(apFileM)

                        if gpuDetected == 1:
                            usbOffer()

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
    print("   You must use a valid file generated by AutoPilot.\n   Any existing VFIO-PCI args will be kept.\n   AutoPilot-generated config scripts end in .sh")
        
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
            print(color.BOLD+"      1. Add VFIO-PCI devices to this file")
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
                    print("   The assistant is now configuring your AutoPilot config file\n   for use with your VFIO-PCI devices.")
                    print(color.BOLD+"\n   This may take a few moments.\n   Your current config will be backed up.\n")
                    time.sleep(2)
                    if apFilePath[0] == "/" and apFilePath[1] == "/":
                        apFilePath = apFilePath.replace("/","",1)
                    if apFilePath[0] == "." and len(apFilePath) > 10:
                        apFilePath = apFilePath.replace(".","",1)
                    apFilePathNoExt = apFilePath.replace(".sh","")
                    os.system("cp "+apFilePath+" "+apFilePathNoExt+"-noPT.sh")
                    with open(apFilePath,"r") as file1:
                        apFileM = file1.read()
                        '''
                        currentDispVal = len(vfio_ids)
                        for y in range(len(vfio_ids)):
                            
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
                            apFileM = apFileM.replace("#VFIO_DEV_BEGIN","#VFIO_DEV_BEGIN\n"+qemu_flags[currentDispVal])
                            currentDispVal -= 1
                        apFileM = apFileM.replace("#-vga qxl","-vga none")
                        #apFileM = apFileM.replace("-monitor stdio","-monitor none")
                        apFileM = apFileM.replace("#-display none","-display none")
                        apFileM = apFileM.replace("REQUIRES_SUDO=0","REQUIRES_SUDO=1")
                        apFileM = apFileM.replace("VFIO_PTA=0","VFIO_PTA=1")
                        apFileM = apFileM.replace("-device qxl-vga,vgamem_mb=128,vram_size_mb=128    ","#-device qxl-vga,vgamem_mb=128,vram_size_mb=128   # DISABLED BY VFIO-PCI PASSTHROUGH ASSISTANT")
                        os.system("cp resources/ovmf/OVMF_CODE.fd ovmf/OVMF_CODE.fd")
                        os.system("cp resources/ovmf/OVMF_VARS_PT.fd ovmf/OVMF_VARS.fd")
                        clear()
                        print("\n\n   "+color.BOLD+color.GREEN+"✔ SUCCESS"+color.END,"")
                        print("   QEMU arguments have been added\n")
                        print("   The QEMU argument lines were successfully added to\n   "+color.BOLD+apFilePath+color.END+"\n\n\n\n\n\n\n")

                    file1.close

                    with open(apFilePath,"w") as file:
                        file.write(apFileM)
                    
                    if gpuDetected == 1:
                            usbOffer()
                    
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
