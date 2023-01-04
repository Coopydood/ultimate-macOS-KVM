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

def clear(): print("\n" * 150)


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

output_stream = os.popen('lspci |  grep "VMWare"')
vmc1 = output_stream.read().splitlines()

output_stream1 = os.popen('lspci |  grep "VirtualBox\|Oracle"')
vmc2 = output_stream1.read().splitlines()

output_stream2 = os.popen('lspci |  grep "Redhat\|RedHat"')
vmc3 = output_stream2.read().splitlines()

detected = 0

for x in vmc1:
    if "VMware" in vmc1:
      detected = 1

for x in vmc2:
   if "VirtualBox" in vmc2 or "Oracle" in vmc2:
      detected = 1

for x in vmc3:
   if "Redhat" in vmc3 or "RedHat" in vmc3:
      detected = 1


clear()

if detected == 1:
   print("\n   "+color.BOLD+color.YELLOW+"⚠ VIRTUAL MACHINE DETECTED"+color.END)
   print("   Virtualised devices detected")
   print("\n   I've determined that it's more than likely that \n   you're using a virtual machine to run this. I won't\n   stop you, but there really isn't much point in continuing."+color.END)
   
   print("\n   "+color.BOLD+color.YELLOW+"PROBLEM:",color.END+"Virtual hardware detected"+color.END)
   print(color.BOLD+"\n      1. Exit")
   print(color.END+"      2. Continue anyway")
   stageSelect = str(input(color.BOLD+"Select> "+color.END))
   
   if stageSelect == "1":
      exit
      exit
      exit

   elif stageSelect == "2":
      exit