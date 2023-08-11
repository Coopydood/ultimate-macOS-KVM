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
    print("\n\n   Welcome to"+color.BOLD+color.GREEN,"Backup and Restore Assistant"+color.END,"")
    print("   Created by",color.BOLD+"Coopydood\n"+color.END)
    print("   This script can assist you in creating backups of your customised\n   files, including config and boot scripts.\n\n   It can also help you restore them in case you need to."+color.END)
    #print(color.BOLD+"\n"+"Profile:"+color.END,"https://github.com/Coopydood")
    #print(color.BOLD+"   Repo:"+color.END,"https://github.com/Coopydood/ultimate-macOS-KVM")
    print("\n   Please choose what you'd like to do below.")
    print(color.BOLD+"\n      1. Backup...")
    print(color.END+"         This option allows you to back up varying selections of\n         files, such as configs, boot files, or everything.\n")
    print(color.BOLD+"      2. Restore...")
    print(color.END+"         This option allows you to restore your data\n         from a previously created compressed file.\n")
    print(color.END+"      3. Main menu")
    print(color.END+"      ?. Help")
    print(color.END+"      Q. Exit\n")
    detectChoice = str(input(color.BOLD+"Select> "+color.END))

       


def clear(): print("\n" * 150)

startup()

if detectChoice == "1":
    clear()
    print("\n\n  "+color.BOLD+color.GREEN,"SELECT BACKUP OPTION"+color.END,"")
    print("   Select what to back up\n"+color.END)
    print("   You can choose what things you want to back up\n   using the selection groups listed below."+color.END)
    print(color.BOLD+"\n      1. Config files only")
    print(color.END+"         AutoPilot config files and boot scripts only\n")
    print(color.BOLD+"      2. Config and boot data")
    print(color.END+"         AutoPilot config files, boot scripts, and OpenCore image\n")
    print(color.BOLD+"      3. All user data")
    print(color.END+"         All config and boot data, as well as all virtual disk files\n")
    print(color.BOLD+"      4. Everything")
    print(color.END+"         All user data and a full repository backup\n")
    print(color.END+"      5. Main menu")
    print(color.END+"      ?. Help")
    print(color.END+"      Q. Exit\n")
    detectChoice = str(input(color.BOLD+"Select> "+color.END))