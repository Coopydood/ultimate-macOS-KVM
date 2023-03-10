#!/usr/bin/env python3
# pylint: disable=C0301,C0116,C0103,R0903

# KVM READINESS CHECKER
# (c) Copyright Coopydood 2022-2023

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
from datetime import datetime
import timeit

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
   GRAY = '\u001b[38;5;245m'
   ORANGE = '\u001b[38;5;202m'
   GREENLIGHT = '\u001b[38;5;46m'


def clear(): print("\n" * 150)

cS = 5

clear()

for x in range(1,6):
    print("\nThis script will check your system to ensure it is ready for basic KVM. \nChecks will begin in",cS,"seconds. \nPress CTRL+C to cancel.")
    cS = cS - 1
    time.sleep(1)
    clear()

clear()

os.system("chmod +x ./scripts/*.py")
os.system("chmod +x ./scripts/*.sh")

vfcLibvirtd = 0
vfcIntegrity = 0
vfcConfig = 0
vfcScore = 0


clear()
print("Checking your system... (1/3)")

# vfcLibvirtd
output_stream = os.popen("systemctl status libvirtd")
checkStream = output_stream.read()
if "active (running)" in checkStream:
    vfcLibvirtd = 1
    vfcScore = vfcScore + 1
elif "enabled" in checkStream:
    vfcLibvirtd = 2
    vfcScore = vfcScore + 1
else:
    vfcLibvirtd = -1
    vfcScore = vfcScore - 1
clear()
print("Checking your system... (2/3)")

# vfcIntegrity
if os.path.exists("./scripts/autopilot.py") and os.path.exists("./scripts/vfio-ids.py") and os.path.exists("./scripts/vfio-pci.py") and os.path.exists("./resources/baseConfig") and os.path.exists("./ovmf/OVMF_CODE.fd") and os.path.exists("./resources/oc_store/compat_new/OpenCore.qcow2"):
    vfcIntegrity = 1
    vfcScore = vfcScore + 1
else:
    vfcIntegrity = -1
clear()
print("Checking your system... (3/3)")

# vfcConfig 
if os.path.exists("./blobs/USR_CFG.apb"):
            apFilePath = open("./blobs/USR_CFG.apb")
            apFilePath = apFilePath.read()
            if os.path.exists("./"+apFilePath):
                apFile = open("./"+apFilePath,"r")
            
                if "APC-RUN" in apFile.read():
                    vfcConfig = 1
                    vfcScore = vfcScore + 1
                else:
                    vfcConfig = -1

            else:
                vfcConfig = -1


else:
    vfcConfig = -1

# force for debug
#vfcKernel = -1
#vfcUefi = -1
#vfcIommu = -1

#vfcScore = 9

time.sleep(1)

# TUI frontend to user
clear()
print("   "+"\n   "+color.BOLD+"Results"+color.END)
print("   "+"All checks have been completed")
print("   "+"\n   Your system has been reviewed. The results for each check\n   are listed below. You can re-run this test at any time\n   for new results."+color.END)
print("   "+"\n   "+color.BOLD+"──────────────────────────────────────────────────────────────",color.END)
if vfcLibvirtd == 1:
    print("   "+color.GREEN+"   ✔ "+color.END+" Libvirt daemon is enabled and running")
elif vfcLibvirtd == 2:
    print("   "+color.GREEN+"   ✔ "+color.END+" Libvirt daemon is enabled")
elif vfcLibvirtd == 0:
    print("   "+color.YELLOW+"   ⚠ "+color.END+" Unable to determine status of libvirtd")
else:
    print("   "+color.RED+"   ✘ "+color.END+" Libvirt daemon is disabled or not working")

if vfcIntegrity == 1:
    print("   "+color.GREEN+"   ✔ "+color.END+" Repository file integrity passed")
elif vfcIntegrity == 0:
    print("   "+color.YELLOW+"   ⚠ "+color.END+" Couldn't check repository integrity")
else:
    print("   "+color.RED+"   ✘ "+color.END+" Repository file integrity damaged")

if vfcConfig == 1:
    print("   "+color.GREEN+"   ✔ "+color.END+" Compatible boot config script found")
elif vfcConfig <= 0:
    print("   "+color.YELLOW+"   ⚠ "+color.END+" Couldn't find compatible boot config script")

#print("   "+"   Lorem ipsum et delor ")
print("   "+color.BOLD+"──────────────────────────────────────────────────────────────",color.END)

if vfcScore <= 0:
    print("   "+color.BOLD+"   NOT READY   "+color.RED+"❚"+color.GRAY+"❚❚❚❚❚❚❚❚❚"+color.END+" 0%")
elif vfcScore == 1:
    print("   "+color.BOLD+"   NOT READY   "+color.RED+"❚"+color.GRAY+"❚❚❚❚❚❚❚❚❚"+color.END+" 10%")
elif vfcScore == 2:
    print("   "+color.BOLD+"   NOT READY   "+color.RED+"❚❚"+color.GRAY+"❚❚❚❚❚❚❚❚"+color.END+" 20%")
elif vfcScore == 3:
    print("   "+color.BOLD+"   NOT READY   "+color.RED+"❚❚❚"+color.GRAY+"❚❚❚❚❚❚❚"+color.END+" 30%")
elif vfcScore == 4:
    print("   "+color.BOLD+"   NOT READY   "+color.ORANGE+"❚❚❚❚"+color.GRAY+"❚❚❚❚❚❚"+color.END+" 40%")
elif vfcScore == 5:
    print("   "+color.BOLD+"   NOT READY   "+color.ORANGE+"❚❚❚❚❚"+color.GRAY+"❚❚❚❚❚"+color.END+" 50%")
elif vfcScore == 6:
    print("   "+color.BOLD+"   NOT READY   "+color.YELLOW+"❚❚❚❚❚❚"+color.GRAY+"❚❚❚❚"+color.END+" 60%")
elif vfcScore == 7:
    print("   "+color.BOLD+"   PARTLY READY   "+color.YELLOW+"❚❚❚❚❚❚❚"+color.GRAY+"❚❚❚"+color.END+" 70%")
elif vfcScore == 8:
    print("   "+color.BOLD+"   PARTLY READY   "+color.YELLOW+"❚❚❚❚❚❚❚❚"+color.GRAY+"❚❚"+color.END+" 80%")
elif vfcScore == 9:
    print("   "+color.BOLD+"   READY   "+color.GREEN+"❚❚❚❚❚❚❚❚❚"+color.GRAY+"❚"+color.END+" 90%")
elif vfcScore >= 10:
    print("   "+color.BOLD+"   READY   "+color.GREEN+"❚❚❚❚❚❚❚❚❚❚"+color.GRAY+""+color.END+" 100%")


print("   "+color.BOLD+"──────────────────────────────────────────────────────────────\n",color.END)
