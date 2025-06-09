#!/usr/bin/env python3
# pylint: disable=C0301,C0116,C0103,R0903

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
sys.path.append('./resources/python')
try:
    from pypresence import Presence
except:
     None
osVer = "Unknown"
ptCount = 0
show = "default"
smolImage = "ultmoslite"

parser = argparse.ArgumentParser("main")
parser.add_argument("--os", dest="osVer",action="store")
parser.add_argument("--pt", dest="pt",action="store")
parser.add_argument("--wd", dest="wd",action="store")
parser.add_argument("--show", dest="show",action="store")

args = parser.parse_args()

#args.pt = "0"

if args.wd is None:
    version = open("./.version")
else:    
    version = open(args.wd+"/.version") # PORTABLE SCRIPT SUPPORT
    #print("DEBUG: Captured workdir ver as",args.wd)

version = version.read()
versionDash = version.replace(".","-")


osVer = args.osVer
try:
    ptCount = int(args.pt)
except:
    None

if args.show != None:
    show = args.show
else:
    show = "default"


client_id = "1149434759152422922"

try:
    RPC = Presence(client_id)
except:
    None

projectVer = "Powered by ULTMOS v"+version

if osVer is not None:
    if "Beta" in osVer: osVer = osVer.replace(" Beta","")

if osVer is not None and osVer == "Sierra" or osVer == "High Sierra" or osVer == "Mojave" or osVer == "Catalina" or osVer == "Big Sur" or osVer == "Monterey" or osVer == "Ventura" or osVer == "Sonoma" or osVer == "Sequoia" or osVer == "Tahoe":
    osName = "macOS "+osVer
elif osVer is not None:
    osName = "Mac OS X "+osVer

if osVer is None:
        osVer = "unknown"
        osName = "macOS"
os = "macos"

startTime = int(time.time())
osVer = osVer.replace(" ","")
osOpt = os+"-"+osVer.lower()

#print(osOpt)

if osOpt != "macos-highsierra" and osOpt != "macos-mojave" and osOpt != "macos-catalina" and osOpt != "macos-bigsur" and osOpt != "macos-monterey" and osOpt != "macos-ventura" and osOpt != "macos-sonoma" and osOpt != "macos-sequoia" and osOpt != "macos-tahoe" and osOpt != "macos-sierra" and osOpt != "macos-elcapitan" and osOpt != "macos-yosemite" and osOpt != "macos-mavericks" and osOpt != "macos-mountainlion" and osOpt != "macos-lion" and osOpt != "macos-snowleopard" and osOpt != "macos-leopard":
     osOpt = "macos-unknown" # arm large image to use the unknown asset if valid macOS version can't be detected

if osName == "macOS Sequoia": osName = "macOS Sequoia"
if osName == "macOS Tahoe": osName = "macOS Tahoe"

osName1 = osName




if show != "default":
    smolImage = osOpt
    osOpt = show
    hold = osName
    osName1 = projectVer
    projectVer = osName
    osName = hold
    


# print("DEBUG:",osVer,osName,osOpt)    #  mmmmm it works, sexy

try:
    RPC.connect()
    RPC.update(large_image="ultmos",large_text=projectVer,details="Loading...",buttons=([{"label": "View on GitHub", "url": "https://github.com/Coopydood/ultimate-macOS-KVM"}])) 
except:
    exit
time.sleep(2)

if ptCount == 1:
    try:
        RPC.update(small_image=smolImage,large_image=osOpt,large_text=osName1,small_text=projectVer,details=osName,state="Passthrough with "+str(ptCount)+" device",start=startTime,buttons=([{"label": "View on GitHub", "url": "https://github.com/Coopydood/ultimate-macOS-KVM"}])) 
        while True:  
            time.sleep(15) 
    except:
        exit
elif ptCount > 1:
    try:
        RPC.update(small_image=smolImage,large_image=osOpt,large_text=osName1,small_text=projectVer,details=osName,state="Passthrough with "+str(ptCount)+" devices",start=startTime,buttons=([{"label": "View on GitHub", "url": "https://github.com/Coopydood/ultimate-macOS-KVM"}])) 
        #RPC.update(small_image=osOpt,large_image="ultmos",large_text=osName,small_text=projectVer,details=osName,start=startTime,buttons=([{"label": "View on GitHub", "url": "https://github.com/Coopydood/ultimate-macOS-KVM"}]))
        while True:  
            time.sleep(15) 
    except:
        exit
else:
    try:
        RPC.update(small_image=smolImage,large_image=osOpt,large_text=osName1,small_text=projectVer,details=osName,start=startTime,buttons=([{"label": "View on GitHub", "url": "https://github.com/Coopydood/ultimate-macOS-KVM"}])) 
        while True:  
            time.sleep(15) 
    except:
        exit