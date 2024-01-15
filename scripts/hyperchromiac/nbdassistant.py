#!/usr/bin/env python3
# pylint: disable=C0301,C0116,C0103,R0903

# Vendor         : Hyperchromiac
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
   os.system("echo ULTMOS OCMA LOG "+str(datetime.today().strftime('%d-%m-%Y %H:%M:%S'))+" > ./logs/OCMA_RUN_"+logTime+".log")
   os.system("echo ──────────────────────────────────────────────────────────────"+" >> ./logs/OCMA_RUN_"+logTime+".log")

   def cpydLog(logStatus,logMsg,*args):
      logFile = open("./logs/OCMA_RUN_"+logTime+".log","a")
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

script = "nbdassistant.py"
scriptName = "OpenCore Configuration Assistant"
scriptID = "OCMA"
scriptVendor = "Hyperchromiac"


cpydLog("info",("ULTMOS v"+version))
cpydLog("info",(" "))
cpydLog("info",("Name       : "+scriptName))
cpydLog("info",("File       : "+script))
cpydLog("info",("Identifier : "+scriptID))
cpydLog("info",("Vendor     : "+scriptVendor))
cpydLog("info",(" "))
cpydLog("info",("Logging to ./logs/OCMA_RUN_"+logTime+".log"))

detectchoice = 0

def menu():
    global detectchoice
    # Get Terminal Size
    if args.quiet != True:
        os.system("clear")
    spaces = ""
    i = 0
    terminal_size = os.get_terminal_size()
    while i < terminal_size.lines:
        spaces = spaces + "\n"
        i += 1
    # Menu
    if args.mount != True and args.unmount != True:
        print(spaces + "   \033[1m\033[94mOPENCORE ASSISTANT\033[0m")
        print("   by \033[1mHyperchromiac\033[0m\n")
        print("   This script was created with the sole purpose of simplifying\n   the process of mounting and unmounting your OpenCore.qcow2\n   so you can make any modifications necessary. \033[37m(e.g. config.plist)\n\n\033[93m   It is highly recommended that you \033[91m\033[1mBACKUP\033[0m\033[93m your OpenCore.qcow2\n   in case you mess something up.\033[0m\n")
        #print("   \033[93mAlso, please note that it is \033[91m\033[1mREQUIRED\033[0m\033[93m to have NBD installed on\n   your system.\033[0m\n")
        print("   Select an option to continue.\n")
        print("      1. Mount OpenCore ⚠\n         This will mount your OpenCore.qcow2 with read-write permissions.\n         \033[93mWill prompt you for superuser permissions, which are required.\033[0m\n")
        print("      2. Unmount OpenCore ⚠\n         This will unmount your OpenCore.qcow2 so you can boot with your modifications.\n         \033[93mWill prompt you for superuser permissions, which are required.\033[0m\n")
        print("      B. Back...")
        print("      Q. Exit\n")
        cpydLog("info",("Awaiting user input."))
        detectchoice = input("\033[1mSelect> \033[0m")
    elif args.mount == True:
        detectchoice = 1
    elif args.unmount == True:
        detectchoice = 2
    else:
        cpydLog("fatal","Invalid argument passthrough")
        exit

    if detectchoice == 1 or detectchoice == "1":
        os.system("sudo modprobe nbd")
        os.system("sudo qemu-nbd --connect=/dev/nbd0 boot/OpenCore.qcow2")
        os.system("mkdir -p boot/mnt")
        os.system("sudo mount /dev/nbd0p1 boot/mnt -o uid=$UID,gid=$(id -g)")
        if args.quiet != True:
            print(spaces)
            print("\n   \033[92mOperation completed. \033[32m(mounted at ./boot/mnt/)\033[0m")
            input("\n\033[1m   Press [ENTER] to continue...\033[0m\n")
        cpydLog("ok",("User has mounted OpenCore image."))
        if args.mount != True and args.unmount != True:
            detectchoice = 0
            menu()

    elif detectchoice == 2 or detectchoice == "2":
        
        os.system("sudo umount -R boot/mnt")
        os.system("sudo qemu-nbd --disconnect /dev/nbd0 2>&1 >/dev/null")
        os.system("sudo rmmod nbd")
        if args.quiet != True:
            print(spaces)
            print("\n   \033[92mOperation completed. \033[32m(unmounted from ./boot/mnt/)\033[0m")
            input("\n\033[1m   Press [ENTER] to continue...\033[0m\n")
        cpydLog("ok",("User has unmounted OpenCore image."))
        if args.mount != True and args.unmount != True:
            detectchoice = 0
            menu()
    elif detectchoice == "B" or detectchoice == "b":
        print(spaces)
        os.system('./scripts/extras.py')
    elif detectchoice == "Q" or detectchoice == "q":
        exit()
    else:
        if len(detectchoice) > 3:
            print(spaces)
            print("   So... we wanna be a smartass. Well,\n   in the least respectful way possible...\n")
            print("                        /´¯¯`/)")
            print("                       /¯.../")
            print("                      /..../")
            print("                  /´¯/'..'/´¯¯`·¸")
            print("              /'/.../..../....../¨¯\\")
            print("             ('(....´...´... ¯~/'..')")
            print("              \\..............'...../")
            print("               \\....\\.........._.·´")
            print("                \\..............(")
            print("                 \\..............\\\n")
            cpydLog("fatal",("User is being belligerent."))
            input("\n\033[1m   Press [ENTER] to continue...\033[0m")
        else:
            cpydLog("ok",("User has fat fingered a mere script. Yeah, that extra character didn't work."))
        detectchoice = 0
        menu()

menu()
