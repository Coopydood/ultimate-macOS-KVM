#!/usr/bin/env python3
# pylint: disable=C0301,C0116,C0103,R0903

# AUTOPILOT BY COOPYDOOD

"""
This script was created by Coopydood as part of the ultimate-macOS-KVM project.
It will not work outside of this project.

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

#parser = argparse.ArgumentParser("gpu-check")
#parser.add_argument("-a", "--auto", dest="auto", help="Detect GPU(s) automatically",action="store_true")
#parser.add_argument("-m", "--manual", dest="manual", help="Enter GPU model manually", metavar="<model>", type=str)
#parser.add_argument("-f", "--force", dest="forceModel", metavar="<model>", help="Override auto-detected GPU with a custom model. Pretty useless, mostly for debugging.", type=str)

#args = parser.parse_args()

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
    print("\n\nWelcome to"+color.BOLD+color.PURPLE,"AutoPilot"+color.END,"(BETA)")
    print("Created by",color.BOLD+"Coopydood\n"+color.END)
    print("\nThe purpose of this script is to automatically guide you through \nthe process of",color.BOLD+"creating and running a basic macOS VM",color.END+"using settings \nbased on answers to a number of questions. \n\nMany of the values can be left to default - especially if you are unsure.\nIt won't be perfect, but it's supposed to make it as"+color.BOLD,"easy as possible.\n"+color.END)
    print(color.BOLD+"\n"+"Profile:"+color.END,"https://github.com/Coopydood")
    print(color.BOLD+"   Repo:"+color.END,"https://github.com/Coopydood/ultimate-macOS-KVM")
    print("\nContinue whenever you're ready, or return to the main menu.")
    print(color.BOLD+"\n   1. Start")
    print(color.END+"      Begin creating a new QEMU-based macOS config file \n")
    print(color.END+"   2. Main menu")
    print(color.END+"   3. Exit\n")
    detectChoice = int(input(color.BOLD+"Select> "+color.END))

def clear(): print("\n" * 150)

startup()
clear()

def autopilot():
   global USR_CPU_SOCKS
   global USR_CPU_CORES
   global USR_CPU_THREADS
   global USR_CPU_MODEL
   global USR_CPU_FEATURE_ARGS
   global USR_ALLOCATED_RAM
   global USR_REPO_PATH
   global USR_NETWORK_DEVICE
   global USR_ID
   global USR_NAME
   global USR_CFG

   USR_CPU_SOCKS = 1
   USR_CPU_CORES = 2 
   USR_CPU_THREADS = 1
   USR_CPU_MODEL = "Penryn"
   USR_CPU_FEATURE_ARGS = "+ssse3,+sse4.2,+popcnt,+avx,+aes,+xsave,+xsaveopt,check"
   USR_ALLOCATED_RAM = "4G"
   USR_REPO_PATH = "."
   USR_NETWORK_DEVICE = "e1000-82545em"
   USR_ID = "macOS"
   USR_NAME = "macOS"
   USR_CFG = "boot.sh"


   print("\n"+color.BOLD+""+color.END)
   print("Step 1")
   print("\nThe purpose of this script is to automatically guide you through \nthe process of",color.BOLD+"creating and running a basic macOS VM",color.END+"using settings \nbased on answers to a number of questions. \n\nMany of the values can be left to default - especially if you are unsure.\nIt won't be perfect, but it's supposed to make it as"+color.BOLD,"easy as possible.\n"+color.END)
   print(color.BOLD+"\n"+"Profile:"+color.END,"https://github.com/Coopydood")
   print(color.BOLD+"   Repo:"+color.END,"https://github.com/Coopydood/ultimate-macOS-KVM")
   print("\nContinue whenever you're ready, or return to the main menu.")
   print(color.BOLD+"\n   1. Start")
   print(color.END+"      Begin creating a new QEMU-based macOS config file \n")
   print(color.END+"   2. Main menu")
   print(color.END+"   3. Exit\n")
   detectChoice = int(input(color.BOLD+"Select> "+color.END))



if detectChoice == 1:
   autopilot()
elif detectChoice == 2:
    os.system('./setup.py')

elif detectChoice == 3:
    exit
