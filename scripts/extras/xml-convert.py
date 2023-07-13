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



def choiceMenu():

    print("\n   This script can assist you in converting (or creating) an AutoPilot config\n   into an XML file for use with virsh. This script can then optionally\n   define and import the XML file into virt-manager for you."+color.END)
    #print(color.BOLD+"\n"+"Profile:"+color.END,"https://github.com/Coopydood")
    #print(color.BOLD+"   Repo:"+color.END,"https://github.com/Coopydood/ultimate-macOS-KVM")
    print("\n   Select what you'd like to do when you're ready.")
    print(color.BOLD+"\n      1. Next...")
    print(color.END+"         Continue to the choice selection screen \n")
    print(color.END+"      2. Help...")
    print(color.END+"      3. Main menu")
    print(color.END+"      4. Exit\n")
    detectChoice = int(input(color.BOLD+"Select> "+color.END))


def startup():
    global detectChoice
    print("   "+"\n   "+color.BOLD+"XML creation type"+color.END)
    print("   "+"Choose a method to use")
    print("   "+"\n   This tool can use both an existing AutoPilot file, or even\n   assist you in creating a new one. Please read and choose\n   from the options below."+color.END)#print(color.BOLD+"\n"+"Profile:"+color.END,"https://github.com/Coopydood")
    #print(color.BOLD+"   Repo:"+color.END,"https://github.com/Coopydood/ultimate-macOS-KVM")
    print(color.BOLD+"\n      1. Convert AutoPilot config to XML")
    print(color.END+"         This option allows you to convert a previously-created AutoPilot\n         config file into an XML file for use with virsh. Your AutoPilot\n         settings, data, and ROMs will be preserved and will be used with\n         virsh / virt-manager, including any VFIO-PCI passthrough settings.")
    print(color.BOLD+"\n      2. Create a new XML file using AutoPilot")
    print(color.END+"         Use this option if you do not have an AutoPilot config file.\n         This script will take you through the AutoPilot steps before\n         generating an XML file based on your answers. No existing\n         data, such as vHDDs, can be used with this method.\n")
    
    print(color.END+"      ?. Help...")
    print(color.END+"      M. Main menu")
    print(color.END+"      Q. Exit\n")
    detectChoice = int(input(color.BOLD+"Select> "+color.END))

       


def clear(): print("\n" * 150)

startup()

if detectChoice == "1":
    clear()
    choiceMenu()
elif detectChoice == "2":
    os.system('./scripts/dlosx.py')