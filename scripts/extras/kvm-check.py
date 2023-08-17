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
vfcQemu = 0
vfcLibvirt = 0
vfcQemuChk = "TEST"


output_stream = os.popen('lspci')
vmc1 = output_stream.read()

detected = 0

global isVM

isVM = False

if "VMware" in vmc1:
   detected = 1

if "VirtualBox" in vmc1 or "Oracle" in vmc1:
   detected = 1

if "Redhat" in vmc1 or "RedHat" in vmc1 or "QEMU" in vmc1:
   detected = 1

if "Bochs" in vmc1 or "Sea BIOS" in vmc1 or "SeaBIOS" in vmc1:
   detected = 1


clear()
print("Checking your system... (1/9)")

output_stream = os.popen("uname -r")
vfcKernelChk = output_stream.read().replace(".","")
vfcKernelChk = vfcKernelChk[0:3]
vfcKernelChk = int(vfcKernelChk)

if vfcKernelChk < 500:
    vfcKernel = -1
    vfcScore = vfcScore - 10
else:
    vfcKernel = 1
    vfcScore = vfcScore + 1
clear()
print("Checking your system... (2/9)")



# vfcLibvirtd
output_stream = os.popen("systemctl status libvirtd")
checkStream = output_stream.read()
if "active (running)" in checkStream:
    vfcLibvirtd = 1
    vfcScore = vfcScore + 1
elif "enabled" in checkStream:
    vfcLibvirtd = 2
    vfcScore = vfcScore + 2
else:
    vfcLibvirtd = -1
    vfcScore = vfcScore - 1
clear()
print("Checking your system... (3/9)")


# vfcLibvirt
output_stream = os.popen("whereis libvirt")
vfcLibvirtChk = output_stream.read()
#output_stream = os.popen("whereis virsh")
#vfcLibvirtChk1 = output_stream.read()

if "libvirt:\n" == vfcLibvirtChk: # or "virsh:\n" == vfcLibvirtChk1
    vfcLibvirt = -1
else:
    vfcLibvirt = 1
    vfcScore = vfcScore + 3
clear()
print("Checking your system... (4/9)")

# vfcQemu
output_stream = os.popen("whereis qemu-system-x86_64")
vfcQemuChk = output_stream.read()

output_stream = os.popen("whereis qemu-x86_64")
vfcQemuChk1 = output_stream.read()

output_stream = os.popen("whereis qemu-img")
vfcQemuChk2 = output_stream.read()

output_stream = os.popen("whereis qemu-img")
vfcQemuChk2 = output_stream.read()

if "qemu-system-x86_64:\n" == vfcQemuChk or "qemu-x64:\n" == vfcQemuChk1 or "qemu-img:\n" == vfcQemuChk2:
    vfcQemu = -1
    vfcScore = vfcScore - 2
else:
    vfcQemu = 1
    vfcScore = vfcScore + 2
clear()
print("Checking your system... (5/9)")

# vfcIntegrity
if os.path.exists("./scripts/autopilot.py") and os.path.exists("./scripts/vfio-ids.py") and os.path.exists("./scripts/vfio-pci.py") and os.path.exists("./resources/baseConfig") and os.path.exists("./resources/ovmf/OVMF_CODE.fd") and os.path.exists("./resources/oc_store/compat_new/OpenCore.qcow2"):
    vfcIntegrity = 1
    vfcScore = vfcScore + 1
else:
    vfcIntegrity = -1
    vfcScore = vfcScore - 2
clear()
print("Checking your system... (6/9)")


output_stream = os.popen("whereis virt-manager")
vfcVirtmanChk = output_stream.read()
if "virt-manager:\n" == vfcVirtmanChk:
    vfcVirtman = -1
else:
    vfcVirtman = 1
    #vfcScore = vfcScore + 1        # This does not effect rediness score

clear()
print("Checking your system... (7/9)")


usrName = os.popen("echo $USER")
usrName = usrName.read().replace("\n","")

#usrName = "eversiege" # uncomment to debug fake user

output_stream = os.popen("groups "+usrName)
vfcUsrChk = output_stream.read()
if "libvirt" not in vfcUsrChk and "kvm" not in vfcUsrChk:
    vfcUsr = -1
else:
    vfcUsr = 1
    vfcScore = vfcScore + 2

clear()
print("Checking your system... (8/9)")


# vfcConfig 
if os.path.exists("./blobs/user/USR_CFG.apb"):
            apFilePath = open("./blobs/user/USR_CFG.apb")
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



clear()
print("Checking your system... (9/9)")

if detected == 1:
    vfcScore = 0


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
if detected == 1:
    print("   "+"\n   "+color.BOLD+"──────────────────────────────────────────────────────────────",color.END)
    print("   "+color.BOLD+color.YELLOW+"\n   ⚠ "+color.END+color.BOLD+" VIRTUAL MACHINE DETECTED"+color.END)
    print("   "+color.END+"   This is a virtual machine, therefore your system cannot be\n      accurately tested. Please see the documentation on running\n      this project in a virtual machine."+color.END)
print("   "+"\n   "+color.BOLD+"──────────────────────────────────────────────────────────────",color.END)

if vfcKernel == 1:
    print("   "+color.GREEN+"   ✔ "+color.END+" Kernel version supported")
elif vfcKernel == 0:
    print("   "+color.YELLOW+"   ⚠ "+color.END+" Unable to get kernel version")
else:
    print("   "+color.RED+"   ✘ "+color.END+" Kernel version unsupported")


if vfcLibvirt == 1:
    print("   "+color.GREEN+"   ✔ "+color.END+" Libvirt packages are installed")
elif vfcLibvirt == 0:
    print("   "+color.YELLOW+"   ⚠ "+color.END+" Unable to determine Libvirt installation status")
else:
    print("   "+color.RED+"   ✘ "+color.END+" Required Libvirt packages are missing")

if vfcQemu == 1:
    print("   "+color.GREEN+"   ✔ "+color.END+" QEMU packages are installed")
elif vfcQemu == 0:
    print("   "+color.YELLOW+"   ⚠ "+color.END+" Unable to determine QEMU installation status")
else:
    print("   "+color.RED+"   ✘ "+color.END+" Required QEMU packages are missing")

if vfcVirtman == 1:
    print("   "+color.GREEN+"   ✔ "+color.END+" Virt-manager is installed")
else:
    print("   "+color.YELLOW+"   ⚠ "+color.END+" Virt-manager is not installed, QEMU by command line only")

if vfcUsr == 1:
    print("   "+color.GREEN+"   ✔ "+color.END+" User \""+usrName+"\" member of correct groups")
else:
    print("   "+color.YELLOW+"   ⚠ "+color.END+" User \""+usrName+"\" not a member of the libvirt and kvm groups")


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

#if vfcConfig == 1:
#    print("   "+color.GREEN+"   ✔ "+color.END+" Compatible boot config script found")
#elif vfcConfig <= 0:
#    print("   "+color.YELLOW+"   ⚠ "+color.END+" Couldn't find compatible boot config script")

#print("   "+"   Lorem ipsum et delor ")
print("   "+color.BOLD+"──────────────────────────────────────────────────────────────",color.END)
if detected == 0:
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
else:
    print("   "+color.BOLD+"   UNSUPPORTED   "+color.GRAY+"❚❚❚❚❚❚❚❚❚❚"+color.GRAY+""+color.END+" N/A")


print("   "+color.BOLD+"──────────────────────────────────────────────────────────────\n",color.END)
