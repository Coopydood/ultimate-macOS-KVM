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
import argparse
import platform
import datetime
import hashlib
import sys
sys.path.append('./resources/python')
import distro
import cpuinfo
import psutil
from cpydColours import color
from datetime import datetime

detectChoice = 1
latestOSName = "Sonoma"
latestOSVer = "14"

scriptName = "System Profile Tool"
script = "sysprofiler.py"
scriptID = "SPT"
scriptVendor = "Coopydood"
scriptVer = 1.0
branch = "Unknown"

version = open("./.version")
version = version.read()

versionDash = version.replace(".","-")

def clear(): print("\n" * 150)

cS = 5

clear()

for x in range(1,1):
    print("\nThis script will check your system to ensure it is ready for basic KVM. \nChecks will begin in",cS,"seconds. \nPress CTRL+C to cancel.")
    cS = cS - 1
    # time.sleep(1)
    clear()

clear()

print("\n\n   "+color.BOLD+color.BLUE+"SYSTEM PROFILE TOOL"+color.END,"")
print("   Gathering system information")
print("\n   Please wait while the tool gathers info\n   about your system. No personal data is\n   included in the report.\n\n\n\n\n\n   ")
def progressUpdate(progressVal,*args):
    progress = progressVal
    if progress <= 5:
        progressGUI = (color.BOLD+""+color.GRAY+"━━━━━━━━━━━━━━━━━━━━")
    elif progress > 5 and progress <= 10:
        progressGUI = (color.BOLD+"━"+color.GRAY+"━━━━━━━━━━━━━━━━━━━")
    elif progress > 10 and progress <= 20:
        progressGUI = (color.BOLD+"━━"+color.GRAY+"━━━━━━━━━━━━━━━━━━")
    elif progress > 20 and progress <= 25:
        progressGUI = (color.BOLD+"━━━"+color.GRAY+"━━━━━━━━━━━━━━━━━")
    elif progress > 25 and progress <= 30:
        progressGUI = (color.BOLD+"━━━━"+color.GRAY+"━━━━━━━━━━━━━━━━")
    elif progress > 30 and progress <= 35:
        progressGUI = (color.BOLD+"━━━━━"+color.GRAY+"━━━━━━━━━━━━━━━")
    elif progress > 35 and progress <= 40:
        progressGUI = (color.BOLD+"━━━━━━"+color.GRAY+"━━━━━━━━━━━━━━")
    elif progress > 40 and progress <= 45:
        progressGUI = (color.BOLD+"━━━━━━━"+color.GRAY+"━━━━━━━━━━━━━")
    elif progress > 45 and progress <= 50:
        progressGUI = (color.BOLD+"━━━━━━━━"+color.GRAY+"━━━━━━━━━━━━")
    elif progress > 50 and progress <= 55:
        progressGUI = (color.BOLD+"━━━━━━━━━"+color.GRAY+"━━━━━━━━━━━")
    elif progress > 55 and progress <= 60:
        progressGUI = (color.BOLD+"━━━━━━━━━━"+color.GRAY+"━━━━━━━━━━")
    elif progress > 60 and progress <= 65:
        progressGUI = (color.BOLD+"━━━━━━━━━━━"+color.GRAY+"━━━━━━━━━")
    elif progress > 65 and progress <= 70:
        progressGUI = (color.BOLD+"━━━━━━━━━━━━"+color.GRAY+"━━━━━━━━")
    elif progress > 70 and progress <= 75:
        progressGUI = (color.BOLD+"━━━━━━━━━━━━━"+color.GRAY+"━━━━━━━")
    elif progress > 75 and progress <= 80:
        progressGUI = (color.BOLD+"━━━━━━━━━━━━━━"+color.GRAY+"━━━━━━")
    elif progress > 80 and progress <= 85:
        progressGUI = (color.BOLD+"━━━━━━━━━━━━━━━"+color.GRAY+"━━━━━")
    elif progress > 85 and progress <= 90:
        progressGUI = (color.BOLD+"━━━━━━━━━━━━━━━━"+color.GRAY+"━━━━")
    elif progress > 90 and progress <= 95:
        progressGUI = (color.BOLD+"━━━━━━━━━━━━━━━━━"+color.GRAY+"━━━")
    elif progress > 95 and progress <= 98:
        progressGUI = (color.BOLD+"━━━━━━━━━━━━━━━━━━━"+color.GRAY+"━")
    elif progress > 98 and progress <= 99:
        progressGUI = (color.BOLD+"━━━━━━━━━━━━━━━━━━━━"+color.GRAY+"")
    elif progress >= 100:
        progressGUI = (color.BOLD+color.GREEN+"━━━━━━━━━━━━━━━━━━━━"+color.GRAY+"")
    sys.stdout.write('\033[F\033[F\033[F\033[F\033[2K\033[1G')
    print('   \r    {0}                 '.format((progressGUI+"  "+color.END+color.BOLD+str(progress)+"% "+color.END),('')), end='\n\n\n\n')
    

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", " K", " M", " G", " T", " P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

global logTime
global logFile
global warningCount
logTime = str(datetime.today().strftime('%d-%m-%Y_%H-%M-%S'))

if not os.path.exists("./logs"):
    os.system("mkdir ./logs")

   
os.system("echo ULTMOS SYSTEM REPORT "+str(datetime.today().strftime('%d-%m-%Y %H:%M:%S'))+" > ./logs/SPT_"+logTime+".log")
os.system("echo ───────────────────────────────────────────────────────────────────"+" >> ./logs/SPT_"+logTime+".log")
os.system("echo This report was generated by user request, and includes basic "+" >> ./logs/SPT_"+logTime+".log")
os.system("echo information about your system hardware, as well as your current"+" >> ./logs/SPT_"+logTime+".log")
os.system("echo ULTMOS software environment. "+" >> ./logs/SPT_"+logTime+".log")
os.system("echo "+" >> ./logs/SPT_"+logTime+".log")
os.system("echo This information may help project developers"+" >> ./logs/SPT_"+logTime+".log")
os.system("echo in assisting you in any issues you might have."+" >> ./logs/SPT_"+logTime+".log")

global apFilePath
global apFilePathNoPT
global apFilePathNoUSB

apFile = None
apFilePath = None
apFilePathNoPT = None
apFilePathNoUSB = None

warn = False
warningCount = 0
warnings = []
logFile = open("./logs/SPT_"+logTime+".log", "a")
progressUpdate(2)
def cpydProfile(logMsg,warn=None):
    global warningCount
    if warn == True:
        entryLine = ("⚠ "+str(logMsg)+"\n")
        warningCount = warningCount + 1
    else:
        entryLine = ("   "+str(logMsg)+"\n")
    logFile.write(entryLine)

######################### BRAINS #######################

output_stream = os.popen("git branch --show-current")
branch = output_stream.read()
branch = branch.replace("\n","")

if os.path.exists("./blobs/user/USR_CFG.apb"):
    
    global macOSVer
    global mOSString

    apFilePath = open("./blobs/user/USR_CFG.apb")
    apFilePath = apFilePath.read()
    if os.path.exists("./blobs/user/USR_TARGET_OS_NAME.apb"):
        macOSVer = open("./blobs/user/USR_TARGET_OS_NAME.apb")
        macOSVer = macOSVer.read()

    macOSVer = open("./blobs/user/USR_TARGET_OS.apb")
    macOSVer = macOSVer.read()
    if int(macOSVer) <= 999 and int(macOSVer) > 99:
        macOSVer = str(int(macOSVer) / 100)
        mOSString = "Mac OS X"
    else:
        mOSString = "macOS"
    if os.path.exists("./blobs/user/USR_TARGET_OS_NAME.apb"):
        macOSVer = open("./blobs/user/USR_TARGET_OS_NAME.apb")
        macOSVer = macOSVer.read()
    if os.path.exists("./"+apFilePath):
        global REQUIRES_SUDO
        global VALID_FILE
        global VALID_FILE_NOPT
        global VALID_FILE_NOUSB

        VALID_FILE = 0
        VALID_FILE_NOPT = 0
        VALID_FILE_NOUSB = 0

        apFile = open("./"+apFilePath,"r")

        

        if "REQUIRES_SUDO=1" in apFile.read():
            REQUIRES_SUDO = 1
        else:
            REQUIRES_SUDO = 0

        apFile.close()

        apFile = open("./"+apFilePath,"r")

        apFilePathNoPT = apFilePath.replace(".sh","-noPT.sh")
        apFilePathNoUSB = apFilePath.replace(".sh","-noUSB.sh")
        
        if "APC-RUN" in apFile.read():
            VALID_FILE = 1
    

########################################################

cpydProfile(" ")
cpydProfile(("Name       : "+scriptName))
cpydProfile(("File       : "+script))
cpydProfile(("Identifier : "+scriptID))
cpydProfile(("Version    : "+str(scriptVer)))
cpydProfile(("Vendor     : "+scriptVendor))
cpydProfile(" ")
cpydProfile("Date       : "+str(datetime.today().strftime('%d/%m/%Y')))
cpydProfile("Time       : "+str(datetime.today().strftime('%H:%M:%S')))
cpydProfile(" \n")
progressUpdate(7)
# time.sleep(2)
cpydProfile("ULTMOS")
cpydProfile("────────────────────────────────────────────────────────")
cpydProfile(("Version    : "+version))
if branch != "main":
    cpydProfile(("Branch     : "+branch),True)
    warnings.append(("This version of ULTMOS is from the "+branch+" branch, which"))
    warnings.append("is not considered stable and bugs are likely\n")
else:
    cpydProfile(("Branch     : "+branch))
cpydProfile((" \n"))
cpydProfile("AUTOPILOT")
cpydProfile("────────────────────────────────────────────────────────")
cpydProfile(("FeatureLvl : "+"7"))

userBlobList = os.listdir("./blobs/user")
if ".user_control" in userBlobList: userBlobList.remove(".user_control")

staleBlobList = os.listdir("./blobs/stale")
if ".stale_control" in staleBlobList: staleBlobList.remove(".stale_control")

liveBlobList = []
for x in os.listdir("./blobs/"):
    if ".apb" in x:
        liveBlobList.append(x)
if ".cdn_control" in liveBlobList: liveBlobList.remove(".cdn_control")

if len(userBlobList) > 0:
    if len(userBlobList) < 17:
        cpydProfile(("UserBlobs  : Yes ("+str(len(userBlobList))+" total)"),True)
        warnings.append("Only "+str(len(userBlobList))+" user blobs are present while more are expected,")
        warnings.append("might be from an old repo version or integrity damage\n")
    else:
        cpydProfile(("UserBlobs  : Yes ("+str(len(userBlobList))+" total)"))
    #cpydProfile("             ⌈ ")
else:
    cpydProfile(("UserBlobs  : No"),True)
    warnings.append("No user blobs were found\n")


for x in userBlobList[0:(len(userBlobList)-1)]:
    cpydProfile("             ├ "+x)
if len(userBlobList) > 0: cpydProfile("             └ "+userBlobList[-1])

if len(userBlobList) > 0: cpydProfile(" ")

if len(staleBlobList) > 0:
    cpydProfile(("StaleBlobs : Yes ("+str(len(staleBlobList))+" total)"))
else:
    cpydProfile(("StaleBlobs : No"))

if len(liveBlobList) > 0:
    cpydProfile(("LiveBlobs  : Yes ("+str(len(liveBlobList))+" total)"),True)
    warnings.append("Live AutoPilot blobs were found, did AutoPilot finish")
    warnings.append("running, or did it suffer a fatality?\n")
    
    for f in liveBlobList[0:(len(liveBlobList)-1)]:
        cpydProfile("             ├ "+f)
    cpydProfile("             └ "+liveBlobList[-1])
else:
    cpydProfile(("LiveBlobs  : No"))
cpydProfile((" "))
if os.path.exists("./boot/OpenCore.qcow2"):
    ocInPlace = "Yes"
    ocHash = hashlib.md5(open('./boot/OpenCore.qcow2','rb').read()).hexdigest()
    
    ocStockHashes = []
    ocStockHashes.append(hashlib.md5(open('./resources/oc_store/compat_new/OpenCore.qcow2','rb').read()).hexdigest())
    ocStockHashes.append(hashlib.md5(open('./resources/oc_store/compat_old/OpenCore.qcow2','rb').read()).hexdigest())
    ocStockHashes.append(hashlib.md5(open('./resources/oc_store/legacy_new/OpenCore.qcow2','rb').read()).hexdigest())
    ocModded = "Unknown"
    if ocHash not in ocStockHashes:
        ocModded = "Yes"
    else:
        ocModded = "No"
    ocSize = get_size(os.path.getsize("./boot/OpenCore.qcow2"))
else:
    ocHash = "N/A"
    ocModded = "N/A"
    ocInPlace = "No"
cpydProfile(("OCInPlace  : "+ocInPlace))
if ocModded == "Yes":
    cpydProfile(("OCModded   : "+ocModded),True)
    warnings.append("OpenCore image is very likely to have been modified")
    warnings.append("by the user, integrity can't be verified\n")

else:
    cpydProfile(("OCModded   : "+ocModded))

if os.path.exists("./boot/OpenCore.qcow2"):
    if os.path.getsize("./boot/OpenCore.qcow2") < 18000000: 
        cpydProfile(("OCSize     : "+ocSize),True)
        warnings.append(("OpenCore image file is only "+ocSize+" in size,"))
        warnings.append("which is much smaller than expected\n")
    else: cpydProfile(("OCSize     : "+ocSize))
    if ocModded == "Yes":
        cpydProfile(("OCHashMD5  : "+ocHash),True)
        warnings.append("OpenCore image MD5 hash does not match any stock")
        warnings.append("OC images supplied with the project\n")

    else:
        cpydProfile(("OCHashMD5  : "+ocHash))
else:
     cpydProfile(("OCSize     : N/A"))   
     cpydProfile(("OCHashMD5  : N/A"))   
cpydProfile((" "))

if apFilePath is not None:
    cpydProfile(("APFileName : "+apFilePath))
    if apFile is not None:
        cpydProfile(("APFilePath : "+str(os.path.realpath(apFile.name))))
    else:
        cpydProfile(("APFilePath : Unknown"),True)
        warnings.append("AutoPilot blobs reference a boot script that does not")
        warnings.append("actually seem to exist - may cause quirky issues\n")
else:
    cpydProfile(("APFileName : N/A"))
    cpydProfile(("APFilePath : N/A"))

cpydProfile((" \n"))

if apFilePath is not None:
    cpydProfile("GENERATED DATA ("+apFilePath.upper()+")")
    cpydProfile("────────────────────────────────────────────────────────")
    cpydProfile(("Name       : "+apFilePath))
    if apFile is not None:
        cpydProfile(("Path       : "+str(os.path.realpath(apFile.name))))
    else:
        cpydProfile(("Path       : Unknown"))
    cpydProfile(" ")
    if os.path.exists("./blobs/user/USR_TARGET_OS_NAME.apb"): 
        targetOSName = open("./blobs/user/USR_TARGET_OS_NAME.apb")
        targetOSName = targetOSName.read()
    else: 
        targetOSName = "Unknown"
    
    if os.path.exists("./blobs/user/USR_TARGET_OS.apb"):
        targetOS = open("./blobs/user/USR_TARGET_OS.apb")
        targetOS = targetOS.read()
    else:
        targetOS = "Unknown"

    if os.path.exists("./blobs/user/USR_HDD_PATH.apb"):
        targetHDDPath = open("./blobs/user/USR_HDD_PATH.apb")
        targetHDDPath = targetHDDPath.read()
        targetHDDPath = targetHDDPath.replace("$REPO_PATH",os.path.realpath(os.path.curdir))
    else:
        targetHDDPath = "Unknown"
    
    if os.path.exists("./blobs/user/USR_HDD_SIZE.apb"):
        targetHDDSize = open("./blobs/user/USR_HDD_SIZE.apb")
        targetHDDSize = targetHDDSize.read()
        targetHDDSize = targetHDDSize.replace("G"," GB")
    else:
        targetHDDSize = "Unknown"

    if os.path.exists("./blobs/user/USR_HDD_TYPE.apb"):
        targetHDDType = open("./blobs/user/USR_HDD_TYPE.apb")
        targetHDDType = targetHDDType.read()
    else:
        targetHDDType = "Unknown"
    
    if os.path.exists("./blobs/user/USR_HDD_ISPHYSICAL.apb"):
        targetHDDPhysical = open("./blobs/user/USR_HDD_ISPHYSICAL.apb")
        targetHDDPhysical = targetHDDPhysical.read()
    else:
        targetHDDPhysical = "Unknown"

    if os.path.exists(targetHDDPath):
        if targetHDDPhysical != "True": targetHDDSizeReal = get_size(os.path.getsize(targetHDDPath))
        else: targetHDDSizeReal = "N/A"
    else:
        targetHDDSizeReal = "Unknown"

    if os.path.exists("./blobs/user/USR_BOOT_FILE.apb"):
        recoveryImagePath = open("./blobs/user/USR_BOOT_FILE.apb")
        recoveryImagePath = recoveryImagePath.read()
    else:
        recoveryImagePath = "Unknown"

    cpydProfile(("OS         : macOS "+str(targetOSName)))
    cpydProfile(("Version    : "+str(targetOS)))
    cpydProfile(" ")
    if os.path.exists(targetHDDPath):
        cpydProfile(("DiskPath   : "+str(targetHDDPath)))
        cpydProfile(("DiskSize   : "+str(targetHDDSizeReal)))
    else:
        cpydProfile(("DiskPath   : "+str(targetHDDPath)),True)
        cpydProfile(("DiskSize   : "+str(targetHDDSizeReal)),True)
        warnings.append("AutoPilot blobs reference a disk file that does not")
        warnings.append("actually seem to exist - boot will likely fail\n")

        warnings.append("Current virtual hard disk size cannot be determined")
        warnings.append("because the file does not appear to exist\n")
    
    
    cpydProfile(("DiskMax    : "+str(targetHDDSize)))
    cpydProfile(("DiskType   : "+str(targetHDDType)))
    if targetHDDPhysical == "True":
        cpydProfile(("DiskIsReal : "+"Yes"))
    else:
        cpydProfile(("DiskIsReal : "+"No"))
    
    cpydProfile(" ")

    if recoveryImagePath != "-1" and recoveryImagePath != "-2":
        cpydProfile(("RecImgPath : "+str(recoveryImagePath)))
        if os.path.exists(recoveryImagePath): 
            recoveryImageSize = get_size(os.path.getsize(recoveryImagePath))
            recoveryImageHash = hashlib.md5(open(recoveryImagePath,'rb').read()).hexdigest()
            if os.path.getsize(recoveryImagePath) < 2004255385:
                cpydProfile(("RecImgSize : "+str(recoveryImageSize)),True)
                warnings.append(("macOS Recovery image file is only "+str(recoveryImageSize)+" in size,"))
                warnings.append("which is much smaller than expected (did conversion fail?)\n")
            else:
                cpydProfile(("RecImgSize : "+str(recoveryImageSize)))
            cpydProfile(("RecImgHash : "+str(recoveryImageHash)))
        else: recoveryImageSize = "Unknown"
        cpydProfile(("RecImgFrom : Local file"))
        
    else:
        if os.path.exists("./BaseSystem.img"):
            recoveryImagePath = os.path.realpath("./BaseSystem.img")
            if os.path.exists(recoveryImagePath): recoveryImageSize = get_size(os.path.getsize(recoveryImagePath))
            else: recoveryImageSize = "Unknown"
            recoveryImageHash = hashlib.md5(open(recoveryImagePath,'rb').read()).hexdigest()
            
            cpydProfile(("RecImgPath : "+str(recoveryImagePath)))
            if os.path.getsize(recoveryImagePath) < 2004255385:
                cpydProfile(("RecImgSize : "+str(recoveryImageSize)),True)
                warnings.append(("macOS Recovery image file is only "+str(recoveryImageSize)+" in size,"))
                warnings.append("which is much smaller than expected (did conversion fail?)\n")
            else:
                cpydProfile(("RecImgSize : "+str(recoveryImageSize)))
            cpydProfile(("RecImgHash : "+str(recoveryImageHash)))
            cpydProfile(("RecImgFrom : Downloaded with APC"))
        else:
            cpydProfile(("RecImgPath : Unknown"))
            cpydProfile(("RecImgSize : Unknown"))
            cpydProfile(("RecImgHash : Unknown"))
            cpydProfile(("RecImgFrom : Unknown"))

    cpydProfile((" \n"))

cpydProfile("OPERATING SYSTEM")
cpydProfile("────────────────────────────────────────────────────────")

progressUpdate(16)
# time.sleep(1)
if platform.system() != "Linux":
    cpydProfile("OS         : "+platform.system(),True)
    warnings.append("The system is running "+str(platform.system())+" which is an unsupported")
    warnings.append("operating system. Use with caution. Linux is required\n")
else:
    cpydProfile("OS         : "+platform.system())
progressUpdate(18)
cpydProfile("Distro     : "+distro.name())
progressUpdate(24)
cpydProfile("Release    : "+distro.version())
progressUpdate(27)
cpydProfile("Kernel     : "+platform.release())
progressUpdate(29)
cpydProfile(" \n")
# time.sleep(1)
progressUpdate(33)
cpydProfile("PROCESSOR")
cpydProfile("────────────────────────────────────────────────────────")
cpydProfile("Model      : "+f"{cpuinfo.get_cpu_info()['brand_raw']}")
progressUpdate(35)
cpydProfile("Physical   : "+str(psutil.cpu_count(logical=False)))
progressUpdate(38)
logCPUCores = psutil.cpu_count(logical=True)
if logCPUCores <= 2:
    cpydProfile(("Logical    : "+str(logCPUCores)),True)
    warnings.append("System processor appears as having only "+str(logCPUCores)+" logical cores")
    warnings.append("which is at or below the project's minimum requirements\n")
else:
    cpydProfile("Logical    : "+str(logCPUCores))
progressUpdate(41)
if platform.machine() != "x86_64":
    cpydProfile("Arch       : "+platform.machine(),True)
    warnings.append("System processor architecture detected as "+str(platform.machine())+", which")
    warnings.append("is unsupported. An x86_64 processor is required\n")
else:
    cpydProfile("Arch       : "+platform.machine())
progressUpdate(46)
cpydProfile(" \n")
# time.sleep(1)
cpydProfile("MEMORY")
cpydProfile("────────────────────────────────────────────────────────")
svmem = psutil.virtual_memory()
progressUpdate(48)
if svmem.total >= 4004255385:
    cpydProfile("Total      : "+f"{get_size(svmem.total)}")
else:
    cpydProfile("Total      : "+f"{get_size(svmem.total)}",True)
    warnings.append("The system only has a total of "+str(get_size(svmem.total))+" of RAM, which is")
    warnings.append("at or below the project's minimum requirements\n")

progressUpdate(49)
cpydProfile("Used       : "+f"{get_size(svmem.used)}")
progressUpdate(51)
if svmem.free >= 4004255385:
    cpydProfile("Free       : "+f"{get_size(svmem.free)}")
else:
    cpydProfile("Free       : "+f"{get_size(svmem.free)}",True)
    warnings.append("The system only has "+str(get_size(svmem.free))+" of RAM free, which may")
    warnings.append("severely degrade performance of virtual machines\n")
progressUpdate(53)
# time.sleep(1)
progressUpdate(97)
cpydProfile(" \n")
# time.sleep(1)
if warningCount > 0:
    cpydProfile("WARNINGS ("+str(warningCount)+")")
    cpydProfile("────────────────────────────────────────────────────────")
    for x in warnings:
        cpydProfile(x)
logFile.close()
progressUpdate(100)
os.system("xdg-open ./logs/SPT_"+logTime+".log")