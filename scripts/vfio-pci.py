#!/usr/bin/env python3
# pylint: disable=C0301,C0116,C0103,R0903

"""
This script was created by Coopydood as part of the ultimate-macOS-KVM project.
You are free to distribute this script however you see fit as long as credit is given.
Enjoy!

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

output_stream = os.popen('lspci -k | grep -B 2 "vfio-pci"')
vgaGrep = output_stream.read()

vfioCount = vgaGrep.count("vfio-pci")

print("\n")
if vfioCount >= 2:
    print("I"+color.BOLD+color.GREEN,"successfully"+color.END,"detected"+color.BOLD,vfioCount,"devices correctly bound to vfio-pci"+color.END,"in your system.\n")
elif vfioCount == 1:
    print("I"+color.BOLD+color.GREEN,"successfully"+color.END,"detected"+color.BOLD,vfioCount,"device correctly bound to vfio-pci"+color.END,"in your system.\n")
else:
    print("I"+color.BOLD+color.RED,"failed"+color.END,"to detect any devices correctly bound to vfio-pci in your system.\nYou must make sure your"+color.BOLD,"vfio-ids"+color.END,"are entered in your host boot-args.\n")
print("\n",vgaGrep)

print(color.BOLD+color.CYAN+"HOW TO:"+color.END,"For each device you intend on passing through, you must \"stub\" it\n        to the"+color.BOLD+" vfio-pci kernel driver."+color.END+" This is done by modifying your "+color.BOLD+"\n        mkinitcpio.conf and boot-args. "+color.END+"See GitHub for instructions!")
print("\n"+color.BOLD+"         Example:"+color.END,"...loglevel=3 intel_iommu=1..."+color.BOLD+color.YELLOW+color.UNDERLINE+"vfio-pci.ids=1002:67ff,1002:aae0"+color.END+"\n")