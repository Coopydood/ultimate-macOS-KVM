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


def clear(): print("\n" * 150)


print("This script will check your system to ensure it is ready for passthrough. Checks will begin in 5 seconds, press CTRL+C to cancel.")
time.sleep(6)
clear()

vfcKernel = 0
vfcUefi = 0
vfcIommu = 0
vfcStubbing = 0
vfcLibvirtd = 0
vfcIntegrity = 0
vfcConfig = 0

# vfcKernel
output_stream = os.popen("lsmod | grep \"vfio_pci\"")
checkStream = output_stream.read()
if "vfio_pci" in checkStream and "vfio_pci_core" in checkStream and "vfio_iommu_type1" in checkStream:
    vfcKernel = 1
else:
    vfcKernel = -1

# vfcUefi
if os.path.exists("/sys/firmware/efi"):
    vfcUefi = 1
else:
    vfcUefi = -1

# vfcIommu



# force for debug
#vfcKernel = -1
#vfcUefi = 0

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
#print("   "+"   Lorem ipsum et delor ")
print("   "+color.BOLD+"──────────────────────────────────────────────────────────────\n\n\n",color.END)
