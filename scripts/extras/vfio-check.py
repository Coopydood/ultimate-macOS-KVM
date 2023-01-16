#!/usr/bin/env python3
# pylint: disable=C0301,C0116,C0103,R0903

# VFIO-PCI READINESS CHECKER
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


print("\nThis script will check your system to ensure it is ready for passthrough. \nChecks will begin in 5 seconds. \nPress CTRL+C to cancel.")
#time.sleep(6)
clear()

vfcKernel = 0
vfcUefi = 0
vfcIommu = 0
vfcStubbing = 0
vfcLibvirtd = 0
vfcIntegrity = 0
vfcConfig = 0
vfcScore = 0

# vfcKernel
output_stream = os.popen("lsmod | grep \"vfio_pci\"")
checkStream = output_stream.read()
if "vfio_pci" in checkStream and "vfio_pci_core" in checkStream and "vfio_iommu_type1" in checkStream:
    vfcKernel = 1
    vfcScore = vfcScore + 2
else:
    vfcKernel = -1

# vfcUefi
if os.path.exists("/sys/firmware/efi"):
    vfcUefi = 1
    vfcScore = vfcScore + 2
else:
    vfcUefi = -1

# vfcIommu
output_stream = os.popen("./scripts/iommu.sh")
checkStream = output_stream.read()
if "Group" in checkStream:
    vfcIommu = 1
    vfcScore = vfcScore + 2
else:
    vfcIommu = -1

# vfcStubbing
output_stream = os.popen("lspci -k | grep -B2 \"vfio-pci\"")
checkStream = output_stream.read()
if "Kernel driver in use: vfio-pci" in checkStream:
    vfcStubbing = 1
    vfcScore = vfcScore + 1
else:
    vfcStubbing = -1

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

# vfcIntegrity
if os.path.exists("./scripts/autopilot.py") and os.path.exists("./scripts/vfio-ids.py") and os.path.exists("./scripts/vfio-pci.py") and os.path.exists("./resources/baseConfig") and os.path.exists("./ovmf/OVMF_CODE.fd") and os.path.exists("./resources/oc_store/compat_new/OpenCore.qcow2"):
    vfcIntegrity = 1
    vfcScore = vfcScore + 1
else:
    vfcIntegrity = -1

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

# TUI frontend to user
print("   "+"\n   "+color.BOLD+"Results"+color.END)
print("   "+"All checks have been completed")
print("   "+"\n   Your system has been reviewed. The results for each check\n   are listed below. You can re-run this test at any time\n   for new results."+color.END)
print("   "+"\n   "+color.BOLD+"──────────────────────────────────────────────────────────────",color.END)
if vfcKernel == 1:
    print("   "+color.GREEN+"   ✔ "+color.END+" Kernel set up correctly")
elif vfcKernel == 0:
    print("   "+color.YELLOW+"   ⚠ "+color.END+" Kernel set up could not be evaluated")
else:
    print("   "+color.RED+"   ✘ "+color.END+" Kernel is not set up correctly")

if vfcUefi == 1:
    print("   "+color.GREEN+"   ✔ "+color.END+" Booted in UEFI mode")
elif vfcUefi == 0:
    print("   "+color.YELLOW+"   ⚠ "+color.END+" Boot mode unknown")
else:
    print("   "+color.RED+"   ✘ "+color.END+" Booted in legacy BIOS mode")

if vfcIommu == 1:
    print("   "+color.GREEN+"   ✔ "+color.END+" IOMMU groups available")
elif vfcIommu == 0:
    print("   "+color.YELLOW+"   ⚠ "+color.END+" IOMMU availability unknown")
else:
    print("   "+color.RED+"   ✘ "+color.END+" IOMMU groups inaccessible/disabled")

if vfcStubbing == 1:
    print("   "+color.GREEN+"   ✔ "+color.END+" VFIO-PCI devices detected")
elif vfcStubbing == 0:
    print("   "+color.YELLOW+"   ⚠ "+color.END+" Couldn't check for VFIO-PCI devices")
else:
    print("   "+color.RED+"   ✘ "+color.END+" No devices bound to VFIO-PCI kernel driver")

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
    print("   "+color.YELLOW+"   ⚠ "+color.END+" Couldn't find boot config script")

#print("   "+"   Lorem ipsum et delor ")
print("   "+color.BOLD+"──────────────────────────────────────────────────────────────",color.END)

if vfcScore == 0:
    print("   "+color.BOLD+"   NOT READY   "+color.GRAY+"❚❚❚❚❚❚❚❚❚❚"+color.END+color.BOLD+"")
elif vfcScore == 1:
    print("   "+color.BOLD+"   NOT READY   "+color.RED+"❚"+color.GRAY+"❚❚❚❚❚❚❚❚❚"+color.END+color.BOLD+"")
elif vfcScore == 2:
    print("   "+color.BOLD+"   NOT READY   "+color.RED+"❚❚"+color.GRAY+"❚❚❚❚❚❚❚❚"+color.END+color.BOLD+"")
elif vfcScore == 3:
    print("   "+color.BOLD+"   NOT READY   "+color.RED+"❚❚❚"+color.GRAY+"❚❚❚❚❚❚❚"+color.END+color.BOLD+"")
elif vfcScore == 4:
    print("   "+color.BOLD+"   NOT READY   "+color.ORANGE+"❚❚❚❚"+color.GRAY+"❚❚❚❚❚❚"+color.END+color.BOLD+"")
elif vfcScore == 5:
    print("   "+color.BOLD+"   NOT READY   "+color.ORANGE+"❚❚❚❚❚"+color.GRAY+"❚❚❚❚❚"+color.END+color.BOLD+"")
elif vfcScore == 6:
    print("   "+color.BOLD+"   NOT READY   "+color.ORANGE+"❚❚❚❚❚❚"+color.GRAY+"❚❚❚❚"+color.END+color.BOLD+"")
elif vfcScore == 7:
    print("   "+color.BOLD+"   ALMOST READY   "+color.YELLOW+"❚❚❚❚❚❚❚"+color.GRAY+"❚❚❚"+color.END+color.BOLD+"")
elif vfcScore == 8:
    print("   "+color.BOLD+"   ALMOST READY   "+color.GREEN+"❚❚❚❚❚❚❚❚"+color.GRAY+"❚❚"+color.END+color.BOLD+"")
elif vfcScore == 9:
    print("   "+color.BOLD+"   READY   "+color.GREEN+"❚❚❚❚❚❚❚❚❚"+color.GRAY+"❚"+color.END+color.BOLD+"")
elif vfcScore == 10:
    print("   "+color.BOLD+"   READY   "+color.GREEN+"❚❚❚❚❚❚❚❚❚❚"+color.GRAY+""+color.END+color.BOLD+"")


print("   "+color.BOLD+"──────────────────────────────────────────────────────────────\n",color.END)
