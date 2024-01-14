#!/usr/bin/env python3
# pylint: disable=C0301,C0116,C0103,R0903

# Vendor         : Hyperchromatic
# Provisioned by : Coopydood

# Import Required Modules
import os
import time
from datetime import datetime
import subprocess
import re 
# import json
# import sys
import argparse
import platform

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
   os.system("echo ULTMOS DTGE LOG "+str(datetime.today().strftime('%d-%m-%Y %H:%M:%S'))+" > ./logs/DTGE_RUN_"+logTime+".log")
   os.system("echo ──────────────────────────────────────────────────────────────"+" >> ./logs/DTGE_RUN_"+logTime+".log")

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

script = "grub-args.py"
scriptName = "Grub Editor"
scriptID = "DTGE"
scriptVendor = "Hyperchromatic"

cpydLog("info",("ULTMOS v"+version))
cpydLog("info",(" "))
cpydLog("info",("Name       : "+scriptName))
cpydLog("info",("File       : "+script))
cpydLog("info",("Identifier : "+scriptID))
cpydLog("info",("Vendor     : "+scriptVendor))
cpydLog("info",(" "))
cpydLog("info",("Logging to ./logs/DTGE_RUN_"+logTime+".log"))


# Right, so we want to be able to check for existing boot arguments, and add other arguments at the user's discretion.
# We also want to check for what platform the user is on in order to add 
# intel_iommu=on | amd_iommu=on
# iommu=pt
# pcie_acs_override=downstream,multifunction
# video=efifb:off
# vfio-pci.ids=xxxx:xxxx

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

# Declare method of "Press enter to continue", like pause on Windows...
def pause():
   input("   Press [ENTER] to continue...")

# Script Variables
detectchoice = 0
cpu_vendor = ""
cpu_model = ""
cpu_iommu = "intel_iommu=on"
iommu = "iommu=pt"
pcie_acs = "pcie_acs_override=downstream,multifunction"
video_efifb = "video=efifb:off"
vfio_stub = []
vfio_stub_str = ""

# Target GRUB file.
targetfile = "./grub"

# Get CPU Vendor Information
clear()
cpydLog("wait", "Getting CPU information...")
print("   Getting CPU information...")
try:
   import cpuinfo
   cpu_vendor = cpuinfo.get_cpu_info()['vendor_id_raw']
   cpu_model = cpuinfo.get_cpu_info()['brand_raw']
except:
   # If the user does not have py-cpuinfo installed, or if some other error occurs, the script will die, throwing the following error message.
   print("   I was unable to gather CPU information. Do you have py-cpuinfo installed?\n")
   cpydLog("fatal", "User either does not have py-cpuinfo installed, or hit CTRL-C.")
   exit()

# Intel CPU
if (cpu_vendor == "GenuineIntel"):
   cpydLog("info", "User is running on an Intel CPU.")
   cpu_iommu = "intel_iommu=on"
# AMD CPU
elif (cpu_vendor == "AuthenticAMD"):
   cpydLog("info", "User is running on an AMD CPU.")
   cpu_iommu = "amd_iommu=on"
# Unsupported CPU
else:
   cpydLog("fatal", "User is running on an unsupported CPU.")
   print("   Your CPU is unsupported, sorry. :(")
   pause()
   exit()

# VFIO IDs
def vfio():
   clear()
   global vfio_stub   
   global vfio_stub_str
   os.system("./scripts/vfio-ids.py")
   print("\n   If you wish to stub any PCI devices, input them one at a time here.")
   print("   If you are done, or wish to skip this process entirely, type \"done\".\n")
   print("   Current VFIO Configuration Selected: " + vfio_stub_str + "\n")
   cpydLog("wait", "Awaiting user input on VFIO IDs...")
   user_input = input("xxxx:xxxx> ")
   if (user_input == "done"):
      cpydLog("info", "User has concluded VFIO ID selection.")
      if (len(vfio_stub) == 0):
         vfio_stub = ""
      else:
         vfio_stub = vfio_stub_str
      menu()
      return
   else:
      stub_matches = re.findall("[0-9A-Fa-f]{4}:[0-9A-Fa-f]{4}", user_input)
      if (len(stub_matches) <= 0 or len(stub_matches) > 1):
         cpydLog("error", "User put in an invalid VFIO ID.")
         vfio()
         return
      vfio_stub.append(str(user_input))
      cpydLog("info", "User has added " + user_input + " to their VFIO stubs.")
      vfio_stub_str = "vfio-pci.ids=" + (",".join(vfio_stub))
      cpydLog("info", "The overall argument is currently " + vfio_stub_str)
      vfio()
      return
   

# Main Menu
def menu():
   global detectchoice
   global vfio_stub
   os.system("grep GRUB_CMDLINE_LINUX_DEFAULT /etc/default/grub")
   grubargs = os.popen('grep GRUB_CMDLINE_LINUX_DEFAULT /etc/default/grub').read()
   grubargs = grubargs[28:(len(grubargs) - 2)]
   clear()
   print("   Welcome to \033[95mGrub Editor\033[0m")
   print("   Created by \033[1mHyperchromatic\033[0m\n")
   print("   CPU Model: \033[37m" + cpu_model + "\033[0m")
   print("\n   Optimal Boot Flags Based on Your System:")
   print("   \033[37m" + cpu_iommu + " " + iommu + " " + video_efifb + " " + vfio_stub + "\033[0m\n")
   print("   Current Boot Arguments:")
   
   print("   \033[37m" + grubargs + "\033[0m\n")
   print("   ⚠  \033[93mRequires superuser privileges.\033[0m\n")
   print("   Select an option to continue.\n")
   print("      1. Add All Relevant Parameters ⚠\n")
   print("      2. Enable IOMMU ⚠\n")
   print("      3. PCIE ACS Patch (kernel support required) ⚠\n")
   print("      4. Video EFIFB Off ⚠\n")
   
   if (vfio_stub != ""):
      print("      5. PCI Stubs ⚠\n")

   print("      B. Back")
   print("      M. Main Menu")
   print("      Q. Quit\n")
   
   cpydLog("wait", "Awaiting user input on main menu...")

   detectchoice = input("\033[1mSelect> \033[0m")
   if (detectchoice == "1"):
      os.system('sudo sed -i \'s/^GRUB_CMDLINE_LINUX_DEFAULT="/&' + cpu_iommu + " " + iommu + " " + video_efifb + ' /\' /etc/default/grub')
      if (vfio_stub != ""):
         os.system('sudo sed -i \'s/^GRUB_CMDLINE_LINUX_DEFAULT="/&' + vfio_stub + ' /\' /etc/default/grub')
      os.system("sudo grub-mkconfig -o /boot/grub/grub.cfg")
      os.system("sudo grub-mkconfig -o /boot/grub/grub.cfg")
      cpydLog("info", "User has added all recommended boot arguments.")
   if (detectchoice == "2"):
      os.system('sudo sed -i \'s/^GRUB_CMDLINE_LINUX_DEFAULT="/&' + cpu_iommu + " " + iommu + ' /\' /etc/default/grub')
      os.system("sudo grub-mkconfig -o /boot/grub/grub.cfg")
      os.system("sudo grub-mkconfig -o /boot/grub/grub.cfg")
      cpydLog("info", "User has added base IOMMU boot arguments.")
   if (detectchoice == "3"):
      os.system('sudo sed -i \'s/^GRUB_CMDLINE_LINUX_DEFAULT="/&' + pcie_acs + ' /\' /etc/default/grub')
      os.system("sudo grub-mkconfig -o /boot/grub/grub.cfg")
      os.system("sudo grub-mkconfig -o /boot/grub/grub.cfg")
      cpydLog("info", "User has added the PCIE ACS patch boot argument.")
   if (detectchoice == "4"):
      os.system('sudo sed -i \'s/^GRUB_CMDLINE_LINUX_DEFAULT="/&' + video_efifb + ' /\' /etc/default/grub')
      os.system("sudo grub-mkconfig -o /boot/grub/grub.cfg")
      os.system("sudo grub-mkconfig -o /boot/grub/grub.cfg")
      cpydLog("info", "User has added the Video EFIFB Off boot argument.")
   if (detectchoice == "5" and vfio_stub != ""):
      os.system('sudo sed -i \'s/^GRUB_CMDLINE_LINUX_DEFAULT="/&' + vfio_stub + ' /\' /etc/default/grub')
      os.system("sudo grub-mkconfig -o /boot/grub/grub.cfg")
      os.system("sudo grub-mkconfig -o /boot/grub/grub.cfg")
      cpydLog("info", "User has added VFIO PCI stubbing to the boot arguments.")
   if (detectchoice == "B"):
      clear()
      cpydLog("info", "User has returned to VFIO menu.")
      vfio_stub = []
      vfio()
   if (detectchoice == "Q"):
      clear()
      cpydLog("info", "User has exited the script.")
      exit()
   if (detectchoice == "M"):
      clear()
      cpydLog("info", "User has returned to ULTMOS extras menu.")
      os.system("./scripts/extras.py")
   menu()

vfio()
